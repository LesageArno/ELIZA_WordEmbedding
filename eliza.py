import logging
import random
import re
from collections import namedtuple
import os.path as osp
import time
from Initializer.WE_vectorial_comparison_class import VecorialComparison as WEvec
from Initializer.WEdict_creator import Creator
import pickle

# Fix Python2/Python3 incompatibility
try: input = raw_input
except NameError: pass

log = logging.getLogger(__name__)


class Key:
    def __init__(self, word, weight, decomps):
        self.word = word
        self.weight = weight
        self.decomps = decomps

class Decomp:
    def __init__(self, parts, save, reasmbs):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs
        self.next_reasmb_index = 0

class Action:
    no = 0
    def __init__(self, trigger:list, actuator:list, trigfunction:str):
        self.trigger = trigger
        self.actuator = actuator
        self.trigfunction = trigfunction
        Action.no += 1

class Eliza:
    def __init__(self, TARGET = "doctor",SEUIL = 0.7, WEIGHTED = True, LOG = False, 
                 MATCHLOGS = False, SYNON_EXTENT = False, SYNONLOGS = True):
        self.initials = []
        self.finals = []
        self.quits = []
        self.action = {}
        self.pres = {}
        self.posts = {}
        self.synons = {}
        self.keys = {}
        self.memory = []
        self.LOG = LOG
        self.SEUIL = SEUIL
        self.MATCHLOGS = MATCHLOGS
        self.WEIGHTED = WEIGHTED
        self.SYNON_EXTENT = SYNON_EXTENT
        self.SYNONLOGS = SYNONLOGS
        
        if self.SYNONLOGS:
            self.synonlist =  []
        
        if self.SYNON_EXTENT == False:
            self.TARGET = TARGET + ".txt"
        else:
            self.TARGET = "SynonExtended" + TARGET + ".txt"
        
    def initialize(self, WEdict = "glove", entity_form = False, header = False):
        """Fonction d'initialisation de ELIZA

        Args:
            WEdict (str, optional): Word2Vec dict files from ["glove","enwiki"] or specify the path. Defaults to "glove".
        """
        if WEdict == "enwiki":
            entity_form = True
            header = True
        
        #Initialisation WE : 
        if not osp.exists(f"Initializer\\Word2VecPreloaded\\WE{WEdict}_dict.pkl"):
            #On créer le dictionnaire s'il n'existe pas
            log.info("Downloading additional files...")
            print("Downloading additional files...")
            time.sleep(0.5)
            Creator(WEdict, entity_form, header)
            print("###############################################################################\n\n###############################################################################") 
            log.info("Succes")
        log.info("Loading files...") #Dans tous les cas, on charge le dictionnaire
        self.word2vec = WEvec(WEdict) #ET le WEvec
        log.info("Succes")
        print("###############################################################################\n\n###############################################################################") 

        log.info(f"Session du {time.localtime().tm_year}/{time.localtime().tm_mon}/{time.localtime().tm_mon} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}")
        if self.MATCHLOGS:
            with open("Logs\\Matchslog.txt","a",encoding="utf-8") as matchslog:
                sentence = f"∙ Poids {'pondérés' if self.WEIGHTED else 'non pondérés'}, seuil = {round(self.SEUIL,2)}, WE = {WEdict}, source = {self.TARGET}, SynonExtent = {self.SYNON_EXTENT} ∙"
                matchslog.write(f"{'∙'*len(sentence)}\n{sentence}\n{'∙'*len(sentence)}\n")

    def load(self): 
        key = None
        decomp = None
        with open(f"Initializer\\Target\\{self.TARGET}") as file: #Permet d'interpréter le fichier doctor.txt
            for line in file:
                if not line.strip(): #Pour chaque ligne, si ce n'est pas un espace ou un \n, on continue le programme
                    continue
                tag, content = [part.strip() for part in line.split(':')] #Permet de sparer la règle du contenu
                if tag == 'initial':
                    self.initials.append(content) #Règle débute la conversation
                elif tag == 'final':
                    self.finals.append(content) #Règle fin de conversation
                elif tag == 'quit': 
                    self.quits.append(content) #Règle déclancheuse de fin
                elif tag == 'pre':
                    parts = content.split(' ') #Règle de présubstitution
                    self.pres[parts[0]] = parts[1:]
                elif tag == 'post':
                    parts = content.split(' ') #Règle de postsubstitution
                    self.posts[parts[0]] = parts[1:]
                elif tag == 'synon':
                    parts = content.split(' ') #Règle de synonymes (défini les familles de mots)
                    self.synons[parts[0]] = parts

                elif tag == 'key': #Règle mot déclancheur (mot important pour le programme)
                    parts = content.split(' ')
                    word = parts[0]
                    weight = int(parts[1]) if len(parts) > 1 else 1
                    key = Key(word, weight, [])
                    self.keys[word] = key       
                elif tag == 'decomp': #Règle de décomposition (patrons)
                    parts = content.split(' ')
                    save = False
                    if parts[0] == '$': #S'il y a un $, nous pouvons le stocker en mémoire 
                        save = True
                        parts = parts[1:]
                    decomp = Decomp(parts, save, [])
                    key.decomps.append(decomp)
                elif tag == 'reasmb':
                    parts = content.split(' ') #Règle d'assemblage de la phrase de réponse à partir du patron
                    decomp.reasmbs.append(parts)

                elif tag == 'action':
                    action = Action([],[],"") #Règle de création d'un trigger
                    self.action["A"+str(Action.no)] = action
                elif tag == 'trigger':
                    parts = content.strip() #Règle du mot déclancheur
                    action.trigfunction = parts if parts == 'final' else None #Si le mot déclancheur est dirigé par la fonction final, on l'indique
                    trig_seq = True
                elif tag == 'actuator': #Règle de l'actionneur
                    trig_seq = False
                elif tag == 'seq': #Règle de renvoie de l'actionneur
                    if trig_seq:
                        action.trigger.append(content.lower())
                    else:
                        action.actuator.append(content)

    def _match_decomp_r(self, parts, words, results):
        if self.LOG: log.debug("parts : %s | words : %s | results : %s",parts,words,results)
        if not parts and not words: # Si il n'y a pas de patrons ni de mots, on renvoie True
            return True
        if not parts or (not words and parts != ['*']): #Si il y a un patron et des mots ou que le premier est [*] alors on renvoie False
            return False
        if parts[0] == '*': #Si le premier élement du patron est un joker
            for index in range(len(words), -1, -1): #Pour chaque mot dans la liste de mots
                if self.LOG: log.debug("%s",index)
                results.append(words[:index]) #On ajoute à results tous les mots de la liste de mot (jusqu'à l'index)
                if self._match_decomp_r(parts[1:], words[index:], results): #Nous faisons une récursion pour savoir si le paterne suivant (avec tout le paterne sans le premier élement) match
                    return True #Si c'est le cas, on renvoie True
                results.pop() #Si ca ne match pas, on retire le dernier mot de la liste results
            return False #Si pour chaque mot, ca ne marche pas, on retourne faux
        elif parts[0].startswith('@'): #Si le mot est un synonyme
            root = parts[0][1:] #On prend la famille de mot @family -> family
            if not root in self.synons: #Si la famille de mot est inconnu, on renvoie une erreur si'lon est pas sur un paramètre étendu
                if self.SYNON_EXTENT == False:
                    raise ValueError("Unknown synonym root {}".format(root))
                elif (self.word2vec.cosineSimilarity(root.lower(), words[0]) if self.word2vec.cosineSimilarity(root.lower(), words[0]) is not None else 0) >= self.SEUIL:
                    if self.SYNONLOGS:
                        self.synonlist.append((root, words[0], round(self.word2vec.cosineSimilarity(root.lower(), words[0]),3)))
                else:
                    return False
            else:
                if not words[0].lower() in self.synons[root]: #Si le premier mot n'est pas dans la liste de synonyme, on renvoie False
                    return False
            results.append([words[0]])
            return self._match_decomp_r(parts[1:], words[1:], results) #Renvoie à match_decomp
        
        ### LA SUITE DE LA FONCTION EST ACTIVÉE UNIQUEMENT S'IL EXISTE DES PATRONS AVEC DES MOTS SANS PRISE EN 
        # CHARGE DE SYNONYMES (GÉNÉRALEMENT QUAND SYNON_EXTENT = False) ###
        elif parts[0].lower() != words[0].lower(): #Le paterne et le mot ne matchs pas donc on retourne FAUX ex : Am i * ≠ You are *
            return False
        else:
            return self._match_decomp_r(parts[1:], words[1:], results) #Renvoie à match_decomp

    def _match_decomp(self, parts, words): #Vérificatteur de matchs
        results = []
        if self._match_decomp_r(parts, words, results):
            return results #On renvoie le résultat si un patron match
        return None #Sinon on recommence

    def _next_reasmb(self, decomp): #Dis la loi de réassamblage à appliquer
        index = decomp.next_reasmb_index 
        result = decomp.reasmbs[index % len(decomp.reasmbs)] #Prend la loi d'assamblage associé au patron de tel manière à ce que la phrase ne soit pas répété en dehors d'une période de len(decomp.reasmb)
        decomp.next_reasmb_index = index + 1 
        if self.LOG: log.debug("index : %s | result : %s | index %% len(decomp.reasmbs) : %s", index,decomp.reasmbs[index % len(decomp.reasmbs)],index % len(decomp.reasmbs))
        return result

    def _reassemble(self, reasmb, results): #Fonction de réassamblage
        if self.LOG: log.debug("%s | %s",reasmb,results)
        output = []
        for reword in reasmb: #Pour chaque mot dans la clé d'assemblage
            if not reword: #Si elle est vide, on passe au mot suivant dans la clé d'assembalge
                continue
            if reword[0] == '(' and reword[-1] == ')': #Si c'est la position d'insertion d'un mot (patron)
                index = int(reword[1:-1])
                if index < 1 or index > len(results): #Si le nombre référant l'isnsertion est inférieur à 0 ou supérieur à la longueur de la liste result
                    raise ValueError("Invalid result index {}".format(index)) #On pose une erreur
                insert = results[index - 1]
                for punct in [',', '.', ';']:
                    if punct in insert:
                        insert = insert[:insert.index(punct)] #Supprime les ponctuations
                output.extend(insert) #Ajoute l'insertion à la liste
            else:
                output.append(reword) #Si ce n'est pas une position d'insertion, on ajoute juste le mot
        return output

    def _sub(self, words, sub): #Fonction de substitution
        output = []
        for word in words:
            word_lower = word.lower() #On transforme chaque mot de telle sortes qu'ils soient tous en minuscules
            if word_lower in sub:
                output.extend(sub[word_lower]) #On applique la substituion s'il y en a une
            else:
                output.append(word) #Sinon on remet le mot de départ dans la liste renvoyé
        return output

    def _match_key(self, words, key):
        for decomp in key.decomps: #Pour chaques patrons
            results = self._match_decomp(decomp.parts, words) #On verifie s'il y en a un qui marche (match)
            if results is None: #Si il n'y a pas de matchs, alors on relance pour vérifier avec un autre paterne
                if self.LOG: log.debug('Decomp did not match: %s', decomp.parts)
                continue
            if self.LOG: 
                log.debug('Decomp matched: %s', decomp.parts)
                log.debug('Decomp results: %s', results)
            results = [self._sub(words, self.posts) for words in results] #Une fois qu'on a match, on fait la post substitution
            if self.LOG: 
                log.debug('Decomp results after posts: %s', results)
            reasmb = self._next_reasmb(decomp) #On cherche la loi de réassamblage
            if self.LOG: 
                log.debug('Using reassembly: %s', reasmb)
            if reasmb[0] == 'goto': #Si la loi de réassamblage nous dis de nous référé à une autre clé
                goto_key = reasmb[1] #Nous nous référrons à l'autre clé
                if not goto_key in self.keys:
                    raise ValueError("Invalid goto key {}".format(goto_key)) #Si la clé donné n'existe pas, nous lancons une erreur
                if self.LOG: log.debug('Goto key: %s', goto_key)
                return self._match_key(words, self.keys[goto_key]) #Nous relançons la recherche de match avec la nouvelle clé 
            output = self._reassemble(reasmb, results) #On applique le réassemblage
            if decomp.save: 
                self.memory.append(output) #Si le patern nous dis de garder en mémoire, nous gardons en mémoire le réassemblage
                log.info('Saved to memory: %s', output)
                continue
            
            log.info('Decomp matched: %s', decomp.parts)
            log.info("Reasmb match : %s",reasmb)
            return output #Si on a réassemblé, on renvoie la réponse
        return None #Sinon on renvoie None

    def respond(self, text: str):
        if text.lower() in self.quits: #Si le mot est dans quits on retourne None
            return None

        for key in self.action.keys(): #Pour chaque actions
            if text.lower() in self.action.get(key).trigger: #Si la phrase est dans un trigger
                if self.action.get(key).trigfunction == 'final':
                    return "quit:"+random.choice(self.action.get(key).actuator) #Si la phrase est de param final, on quitte le code en renvoyant l'actionneur
                else: return random.choice(self.action.get(key).actuator) #On renvoie l'actionneur

        text = re.sub(r'\s*\.+\s*', ' . ', text) #Transforme les ",,;;;...." en " ,  ;  . "
        text = re.sub(r'\s*,+\s*', ' , ', text)
        text = re.sub(r'\s*;+\s*', ' ; ', text)
        if self.LOG: log.debug('After punctuation cleanup: %s', text)

        words = [w for w in text.split(' ') if w] #Créé une liste de string <=> text.split(' ') dans la plupart des cas
        if self.LOG: log.debug('Input: %s', words)

        words = self._sub(words, self.pres) #On exécute la pré-substitution
        if self.LOG: log.debug('After pre-substitution: %s', words)

        #Nouvelle : 
        keys = {}
        if self.MATCHLOGS:
            with open("Logs\\Matchslog.txt","a",encoding="utf-8") as matchslog:
                matchslog.write(f"{'-'*len(' '.join(words))}\n{' '.join(words)}\n{'-'*len(' '.join(words))}\n")
       
        subject_string = ""
        subject = False
        for w in words:
            if w.startswith("~"): #Si c'est un sujet, alors on enregistre le sujet et on évalue le sujet plutôt que mots par mots
                subject_string += w[1:]
                subject = True
                continue
            elif w.endswith("~"):
                subject_string += " " + w[:len(w)-1]
                w = subject_string.rstrip()
                subject = False
            if subject:
                subject_string += " " + w 
                continue

            cosin = self.word2vec.maxCosineSimilarity(list(self.keys.keys()), w.lower()) #Pour chaque mot, on calcule le maxCosSim
            if not cosin is None and cosin[1] >= self.SEUIL: 
                if self.MATCHLOGS:
                    with open("Logs\\Matchslog.txt","a",encoding="utf-8") as matchslog: #On indique dans les logs que le matchs est validé
                        matchslog.write(f"[o]")
                
                #Si None n'est pas renvoyé, c'est que le mot est bien dans le dictionnaire et que le seuil est vérifié
                if self.WEIGHTED:
                    keys[cosin[0]] = round(cosin[1]*self.keys[cosin[0]].weight,3) #Dans ce cas on enregistre le mot, le poids adapté, si l'option est enclenché
                else:
                    keys[cosin[0]] = round(cosin[1],3) # Si ce n'est pas pondéré alors, nous arrondissons juste le résultat  
            if self.MATCHLOGS:    
                with open("Logs\\Matchslog.txt","a",encoding="utf-8") as matchslog: #On enregistre dans les logs le matchs
                    matchslog.write(f"{w} {cosin[0] if not cosin is None else ''} ({round(cosin[1],3) if not cosin is None else ''}) [{round(keys[cosin[0]],3) if not cosin is None and cosin[1] >= self.SEUIL else ''}]\n")
                
        keys = list(map(tuple,sorted(keys.items(), key=lambda x: x[1], reverse=True))) #Finalement on met en ordre
        log.info("%s",keys)
        keys = [self.keys[key[0]] for key in keys] #On associe la clé à sa clé de classe Key
        if self.LOG: log.debug("%s",keys)
        
        
        """#Ancienne version
        keys = [self.keys[w.lower()] for w in words if w.lower() in self.keys] #Pour chaque mot, on regarde s'ils sont clés, si c'est le cas, on l'enregistre, A MODIFIER POUR LE WIKI2VEC
        keys = sorted(keys, key=lambda k: -k.weight) #Liste dans l'ordres des clés par poids
        if self.LOG: log.debug('Sorted keys: %s', [(k.word, k.weight) for k in keys])
        """
        output = None

        for key in keys: #Pour chaques clés dans la liste
            output = self._match_key(words, key) #On cherche une réponse
            if output: #S'il y a une réponse on sort de la boucle
                if self.LOG: log.debug('Output from key: %s', output)
                break
        if not output: #S'il n'y a pas de réponses
            if self.memory: #On prend une réponse aléatoire en mémoire, s'il y en a
                index = random.randrange(len(self.memory))
                output = self.memory.pop(index)
                log.info('Output from memory: %s', output)
            else:
                output = self._next_reasmb(self.keys['xnone'].decomps[0]) #S'il n'y en a pas, nous renvoyons une réponses par défaut
                log.info('Output from xnone: %s', output)

        return " ".join(output) #On retourne une réponse

    def initial(self): #Fonction du début de la conversation
        return random.choice(self.initials)

    def final(self): #Fonction de la fin de la conversation
        return random.choice(self.finals)

    def run(self): #Fonction qui lance le code Eliza
        print('\x1b[35m'+self.initial()+'\x1b[0m') #Introduction

        while True:
            sent = input('\x1b[33m'+'> ')
            output = self.respond(sent) #Analyse de la réponse de l'utilisateur et réponse approprié
            if output is None: #Si l'utilisateur met un mot de quits alors on quitte la séance
                break
            if output.startswith('quit:'): #S'il s'agit d'un trigger final, on quitte sans plus attendre 
                print('\x1b[35m'+output[5:]+'\x1b[0m')
                break
            print('\x1b[35m'+output) #On renvoie la réponse à l'utilisateur

        if output is None:
            print('\x1b[35m'+self.final()+'\x1b[0m')
        
        if self.SYNONLOGS:
            print()
            with open("Logs\\synonlog.txt","a") as f:
                f.write(str(self.synonlist)+"\n")
        
def main(WEdict = "glove", TARGET = "doctor", SEUIL = 0.7, WEIGHTED = True, LOG = False, 
         MATCHLOGS = False, SYNON_EXTENT = True, SYNONLOGS = False): #Lancement d'Eliza
    logging.basicConfig(filename="Logs\\Elizalog.log",level=logging.DEBUG,encoding='utf-8') #On génère un log d'eliza
    eliza = Eliza(TARGET = TARGET, SEUIL = SEUIL, WEIGHTED = WEIGHTED, LOG = LOG, 
                  MATCHLOGS = MATCHLOGS, SYNON_EXTENT = SYNON_EXTENT, SYNONLOGS = SYNONLOGS) #LOG = True pour avoir les log (il y en a beaucoups)
    eliza.load()
    eliza.initialize(WEdict)
    eliza.run()

if __name__ == '__main__':
    main()
