#https://stacktuts.com/how-to-load-a-pre-trained-word2vec-model-file-and-reuse-it-in-python
#https://stackoverflow.com/questions/45310409/using-a-word2vec-model-pre-trained-on-wikipedia
#https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file

import time
import pickle

begin = time.time()

countline = 0
dictionary = dict()

class Creator():
    def __init__(self, Word2Vec = "glove", entity_form = False, header = False) -> None:
        """_summary_
        Args:
            Word2Vec (str, optional): Word2Vec files from ["glove","enwiki"] or specify the path. Defaults to "glove".
            entity_form (bool): is your file containing line begining with ENTITY/ like in entwiki. Defaults to False.
            header (bool): is your Word2Vec first line isn't data. Default to False
        """
        if Word2Vec == "glove":
            file_path = __file__.removesuffix("WEdict_creator.py")+"Word2Vec\\glove.6B.100d.txt" #__file__+... permet de récupérer le fichier depuis Initializer et non ELIZA_APP
        elif Word2Vec == "enwiki":
            file_path = __file__.removesuffix("WEdict_creator.py")+"Word2Vec\\enwiki_20180420_100d.txt"
        else:
            file_path = __file__.removesuffix("WEdict_creator.py")+"Word2Vec\\"+Word2Vec
        
        with open(file = file_path, mode = "r", encoding = "utf-8") as file: #On lit le fichier de word_embeding 
            if header == True:
                file.readline() #On retire la première ligne
            countline = 0
            while True:
                line = file.readline()
                form = line.rstrip().split(" ",1) #On sépare la liste en deux partie : [key, vector] 
        
                if line == "":
                    break
                elif form[0] in """~"#'{[]'()-|`\_^@°}+=*µ¤^¨§!:/;.,? """:
                    continue
                else:
                    countline += 1
                if (countline%10000 == 0):
                    print(countline,time.time()-begin) #On compte les lignes et on fait un retout utilisateur

                
                if entity_form == True and form[0].startswith("ENTITY/"):
                    dictionary[form[0].removeprefix("ENTITY/").replace("_"," ").lower()] = form[1] #Entity/United_States -> united states
                    continue
                dictionary[form[0]] = form[1]

        with open(f"{__file__.removesuffix('WEdict_creator.py')}Word2VecPreloaded\\WE{Word2Vec}_dict.pkl","wb") as f: #On enregistre le dictionnaire avec pickle
            pickle.dump(dictionary, f)

        print("Downloaded", countline,"lines in", round(time.time()-begin,3), "seconds") #A peu près 10 secondes pour créer le dictionnaire
        #format : {mot <str>:vecteur <str>}

if __name__ == "__main__":
    Creator("glove",False,False)
    Creator("enwiki",True,True)