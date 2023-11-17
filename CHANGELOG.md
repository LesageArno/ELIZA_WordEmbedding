#### 26/06/2023 ####
```
[1.] Ajout dans Eliza:
```
```python
import os.path as osp
import time
from WE_vectorial_comparison_class import VecorialComparison as WEvec

#Initialisation WE : 
def initialize(self):
    #Initialisation WE : 
    if not osp.exists("word_embeded_dict.pkl"):
        with open("WEdict_creator.py","r") as creator: #On créer le dictionnaire s'il n'existe pas
            logging.info("Downloading additional files...")
            print("Downloading additional files...")
            time.sleep(1.5)
            exec(creator.read())
            print ("###############################################################################\n\n###############################################################################") 
            logging.info("Succes")
    logging.info("Loading files...") #Dans tous les cas, on charge le dictionnaire
    self.word2vec = WEvec("word_embeded_dict.pkl") 
    logging.info("Succes")
    print("###############################################################################\n\n###############################################################################") 

    logging.info(f"Session du {time.localtime()}")

eliza.initialize()
```
- Initialisation de Eliza avec le nouveau programme Word2Vec (téléchargement et chargement du jeu de données)
```
[2.] Création de creator.py
```
- Fichier de chargement des données (transformation du Wiki2Vec en dictionnaire) puis téléchargement du dictionnaire (pour éviter  la latence)
```
[3.] Création de WEdict_comparison_class.py
```
- Classe pour faire les calculs du cosinusSimilarity et du maxCosinus, charge aussi le dictionnaire précedement créé.
```
[4.] Création de Elizalog.log
```
- Permet de savoir comment le code agis réélement et cela en direct (debug++)
```
[5.] Identification des zones à modifier pour adapter le code
```
- Dans respond : 
```python
keys = [self.keys[w.lower()] for w in words if w.lower() in self.keys]
keys = sorted(keys, key=lambda k: -k.weight)
```
#### 27/06/2023 ####
```
[1.] Commentaire, amélioration du système de log, compréhension du code en détail
```
- Ajout du paramètre LOG dans le __init__ de ELIZA
- Commentaire détaillé dans tout ELIZA
```
[2.] Implémentation du WE dans ELIZA
```
- Dans respond : 
```python
keys = {}
        for w in words:
            cosin = self.word2vec.maxCosineSimilarity(list(self.keys.keys()),w.lower()) #Pour chaque mot, on calcule le maxCosSim
            if not cosin is None and cosin[1] >= self.SEUIL*self.keys[cosin[0]].weight: 
                #Si None n'est pas renvoyé, c'est que le mot est bien dans le dictionnaire et que le seuil adaptatif est vérifié
                keys[cosin[0]] = cosin[1]*self.keys[cosin[0]].weight #Dans ce cas on enregistre le mot, le poids adapté
        keys = list(map(list,sorted(keys.items(), key=lambda x: x[1], reverse=True))) #Finalement on met en ordre
        log.info("%s",keys)
        keys = [self.keys[key[0]] for key in keys] #On associe la clé à sa clé de classe Key
        if self.LOG: log.debug("%s",keys)
```
#### 28/06/2023 ####
```
[1.] Créations de conversation avec les différents modèles de ELIZA (@sad, @delighted, @madness)
[2.] Comparaison des modèles (BASE, WE 0, WE 0.7, WE 0.8, PWE 0.7, PWE 0.8)
```
#### 29/06/2023 ####
```
[1.] Ajouts de la conversation (@"nullKey - normale") -- icomplète, abandonée
[2.] Ajouts de modèles supplémentaires (PWE 0.35 et PWE 0.6)
[3.] Ajouts de matching_detail, qui renvoie le mot avec lequel il match
```
#### 30/06/2023 ####
```
[1.] Test augmentations de seuil
[2.] Discussion GPT - ELIZA
[3.] Création de la liste de mot pour détecter les mauvais binding
```
#### 03/07/2023 ####
```
[1.] Discussion GPT - ELIZA
[2.] Augmentation seuil PWE pour GPT
[3.] Ajout de ~x y z~ qui permet d'évaluer un groupe de mot et non uniquement le mot lui même
[4.] Analyse des mots pour détections de stop word via TF-IDF
```
#### 04/07/2023 ####
```
[1.] Ajout de PWE et du WE à 0.9 pour NORMAL
[2.] Fusion des liste de TF-IDF GPT-NORMAL
```
#### 05/07/2023 ####
```
[1.] Changement de la source d'entrée du W2Vec enwiki -> GloVe
[2.] Changement de l'architecture de ELIZA et création d'une interface de paramétrage
```
#### 06/07/2023 ####
```
[1.] Test sur ELIZA GloVe NORMAL WE, PWE (0,035,060,070,080,090) (9 conversation par discussions soit 27)
[2.] Verif sur la loi de Benford (c'est non vérifié donc bon signe -> pas d'aléatoire)
[3.] Test sur ELIZA Glove GPT PWE (035,060,070,080,090) (5 conversation par disucussions soit 15)
```
- Les conversations après tests semblent meilleures, mais ce n'est que léger au niveau du resentie 
```
[4.] Comparaison des mots et des liens depuis Glove NORMAL/GPT PWE (035,060,070,080,090) /!\ EN COURS
```
- Les discussions en PWE étants finites, nous avons un fichier comparatif en sql sur les lien et les cosinus
#### 10/07/2023 ####
```
[1.] Changement pour les nouveaux synonymes entièrement fini
[2.] Détection d'un bug sur la nouvelle version, ligne 163 où le pop n'est pas exécuté.
```
#### 11/07/2023 ####
```
[1.] Tentative de résolution du bug
```
- bug causé par les synonymes mals gérés dans la source (les stopwords tels que why ou les mots lexigraphiquement importants tels que if ou les verbes importants changeant le sens de la phrase tels que do, was et le pronom i ne devrait pas être sous arobase)
#### 14/07/2023 ####
```
[1.] Bug synonymes partiellement patch
[2.] Détection d'un bug dans la gestion des ponctuations (test. ≠ test), le mot n'est pas détecté s'il est collé avec une ponctuation, bug réglé
```
- Résolution du problème par la suppression des ponctuations dans les mots.
```
[3.] Création d'un prototype de source pour la médecine généraliste
```
#### 15/07/2023 ####
```
[1.] Détection des cibles de manières automatiques, doctor.txt n'est plus le seul choix possible, de la même manière, les fichier en SynonymExtend doivent être de préférence précédé de SE et doivent être placé dans le fichier target
[2.] Changement de la gestion des synonymes, le séparateur est ";" au lieu de " ", permet les synonymes en plusieurs mots. On fait la même chose pour la cohérence pour les règles de substitutions
[3.] Suite génération generalist.txt avec GPT
```
#### 16/07/2023 ####
```
[1.] Rédaction du README.md
[2.] Mise en forme du CHANGELOG.md
```
#### 17/07/2023 ####
```
[1.] Ouverture du code pour la prise en charge d'autres sources de WordEmbeding
[2.] Rédaction du README.md
```
#### 18/07/2023 ####
```
[1.] Rédaction du README.md
[2.] Prise en charge complète des synonymes avec plusieurs mots en eux (medical center -> hospital)
[3.] Modification du fonctionnement des vague ~, quand une phrase est ainsi ~mot1 mot2 ...~ alors, nous l'interprétons comme "mot1 mot2 ..." au lieu de ["mot1","mot2",...]
[4.] Si les roots sont utilisé comme clé (allergy par exemple), si un synonyme est détecté (hypersensitivity reaction par exemple), la clé pourra quand même être déclanché (uniquement si le synonyme n'est pas reconnu par le cosinus de similarité)
```
#### 19/07/2023 ####
```
[1.] RESET du protoype de generalist.txt, rédaction de tous les synonymes
```
#### 20/07/2023 ####
```
[1.] Prise en charge des commentaires dans les fichiers sources avec le symbole # placé au début de ligne
[2.] Rédaction de generalistGPTsemi.txt
[3.] Ajout de la partie discussion dans le README.md
```
#### 21/07/2023 ####
```
[1.] main.py commenté
```
#### 02/11/2023 ####
```
[1.] Ajout du Word Embedding de GPT-2 :
```
- Création de GPT2WEGetter.py, qui a pour objectif de récupérer le Word Embedding depuis transformers
- Modification du WEdict_creator pour prendre en charge différents types d'encodages pour le texte.
- Modification de main.py pour rajouter l'accès au Word Embedding de gpt-2
```
[2.] Détection de problème avec le WE de GPT-2 :
```
- Le lien entre des élement proches sont du même ordre de grandeur que ceux qui ne le sont pas
- Potentielle solution par une correction de (cos(θ)-0.99)*100 pour gpt-2

#### 05/11/2023 ####
```
[1.] Word Embedding de GPT-2 quasiment fonctionnel (il faut trouver le bon seuil)
[2.] Ajout d'un mécanisme de correction du cosinus de similarité (qui ne sert pas à grand chose car il existe finalement des cos(θ) < 0.99 pour GPT-2) :
```
- Le mécanisme de correction permet de faire un changement de variable sur le cos(θ), exemple : Y = 3.5*X I X <=0.2 E 0
- Y : résultat, X : cos(θ), I : if, E : else, A : and, O : or 

#### 13/11/2023 ####
```
[1.] Implémentation de la distance de manhattan, euclidienne et jacard
```
#### 17/11/2023 ####
```
[1.] Refonte complète du système de comparaisons de vecteurs, optimisations.
```