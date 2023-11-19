#https://www.geeksforgeeks.org/numpy-vector-multiplication/
import numpy as np
import scipy.spatial.distance as distance 
import time
import pickle

class VecorialComparison:
    def __init__(self, WEdict = "glove") -> None:
        """_summary_

        Args:
            WEdict (str, optional): Word2Vec dict files from ["glove","enwiki"] or specify the path. Defaults to "glove".
        """
        if WEdict == "glove":
            dict_path = __file__.removesuffix("WE_vectorial_comparison_class.py")+"Word2VecPreloaded\\WEglove_dict.pkl"  #__file__+... permet de récupérer le fichier depuis Initializer et non ELIZA_APP
        elif WEdict == "enwiki":
            dict_path = __file__.removesuffix("WE_vectorial_comparison_class.py")+"Word2VecPreloaded\\WEenwiki_dict.pkl"
        else:
            dict_path = __file__.removesuffix("WE_vectorial_comparison_class.py")+"Word2VecPreloaded\\"+"WE"+WEdict+"_dict.pkl"
        
        print("Loading files...")
        time.sleep(0.5)
        begin = time.time()

        with open(dict_path,"rb") as f:
            self.dicVec = pickle.load(f)
        print("Loaded in",round(time.time()-begin,3),"seconds") #5 secondes pour charger les données
        
    def computeDistance(self, word1 = str, word2 = str, method = "cosine", correction = None) -> float:
        computedDistance = None
        if word1 not in self.dicVec.keys() or word2 not in self.dicVec.keys(): #Si le mot n'est pas dans le dictionnaire alors on retourne None
            return None
        
        vec1, vec2 = self.initDistance(word1, word2)
        
        if method == "cosine":
            computedDistance = self.cosineDistance(vec1, vec2)
        elif method == "manhattan":
            computedDistance = self.manhattanDistance(vec1, vec2)
        elif method == "euclidean":
            computedDistance = self.euclideanDistance(vec1, vec2)
        elif method == "jaccard":
            computedDistance = self.jaccardDistance(vec1, vec2)
        else: return None
        
        if correction is None:
            return computedDistance
        else:
            autorized_character = ['X','Y','I','E','A','O','*','/','+','-','=','(',')',' ','.','>','<','!'] 
            autorized_character.extend([str(i) for i in range(0,10)]) #Pour des raisons de sécurité, seul ces caractères sont autorisés
            if [i in autorized_character for i in correction].count(False) >= 1: #Si un caractère n'est pas autorisé, on renvoie le cosinus sans corrections
                return computedDistance
            else:
                _locals = locals() #dictionnaire des variables locales
                correction = correction.replace("Y","computedDistance_corrected") 
                correction = correction.replace("X","computedDistance")
                correction = correction.replace("I","if")
                correction = correction.replace("E","else") 
                correction = correction.replace("A","and")
                correction = correction.replace("O","or")
                
                exec(correction, globals(), _locals) #On fait la correction et on met le résultat dans cos corrected du dictionnaire _locals
                computedDistance = _locals.pop("computedDistance_corrected")
                
                return computedDistance #On renvoie le résultat corrigé
            
    def initDistance(self, word1 = str, word2 = str): # -> tuple(np.ndarray)
        vec1 = np.array(list(map(float,self.dicVec[word1].split(" "))))
        vec2 = np.array(list(map(float,self.dicVec[word2].split(" "))))
        return (vec1, vec2)
    
    def manhattanDistance(self, word1 = str|np.ndarray, word2 = str|np.ndarray) -> float:
        if isinstance(word1, str) and isinstance(word2, str):  
            vec1, vec2 = self.initDistance(word1, word2)
        elif isinstance(word1, np.ndarray) and isinstance(word2, np.ndarray):
            vec1, vec2 = word1, word2
        else: 
            return None
        return distance.cityblock(vec1, vec2)
    
    def euclideanDistance(self, word1 = str|np.ndarray, word2 = str|np.ndarray) -> float:
        if isinstance(word1, str) and isinstance(word2, str):  
            vec1, vec2 = self.initDistance(word1, word2)
        elif isinstance(word1, np.ndarray) and isinstance(word2, np.ndarray):
            vec1, vec2 = word1, word2
        else: 
            return None
        return distance.euclidean(vec1, vec2)
    
    def jaccardDistance(self, word1 = str|np.ndarray, word2 = str|np.ndarray) -> float:
        if isinstance(word1, str) and isinstance(word2, str):  
            vec1, vec2 = self.initDistance(word1, word2)
        elif isinstance(word1, np.ndarray) and isinstance(word2, np.ndarray):
            vec1, vec2 = word1, word2
        else: 
            return None
        return distance.jaccard(vec1, vec2)
    
    def cosineDistance(self, word1 = str|np.ndarray, word2 = str|np.ndarray) -> float:
        if isinstance(word1, str) and isinstance(word2, str):  
            vec1, vec2 = self.initDistance(word1, word2)
        elif isinstance(word1, np.ndarray) and isinstance(word2, np.ndarray):
            vec1, vec2 = word1, word2
        else: 
            return None
        return 1 - distance.cosine(vec1, vec2) #La commande fait comme calcul 1 - cos(θ) donc on corrige

    def maxCosineSimilarity(self, keys_list, word, correction):
        maxCosine = 0
        bestKey = ""
        
        for pop_elem in ["xnone","xforeign"]: #On retire les élements problématiques
            keys_list.pop(keys_list.index(pop_elem))
        
        for key in keys_list:
            cosine = self.computeDistance(word1 = key.rstrip(), word2 = word, method = "cosine", correction = correction)
            if cosine is None: #Si le mot n'existe pas on ne le prend pas
                return None
            maxCosine = cosine if cosine > maxCosine else maxCosine #On remplace si le cos est plus grand
            if self.computeDistance(word1 = key.rstrip(), word2 = word, method = "cosine", correction = correction) == maxCosine:
                bestKey = key.rstrip()
        
        return [bestKey, maxCosine]

    def getVector(self,word):
        return np.array(list(map(float,self.dicVec.get(word).split(" ")))) if self.dicVec.get(word) is not None else None


def generateDumpComparisonCsv(path = __file__.removesuffix("WE_vectorial_comparison_class.py")+"ModelTester\\generatedDump.csv", 
                              listOfModel = ["enwiki","glove","gpt-2"], listOfWord1 = None, listOfWord2 = None):
    
    if listOfWord1 is None or listOfWord2 is None:
        listOfWord1 = ["brother","nephew","uncle","man","sir","heir","king","earl","emperor","duke",
                       "slow","short","strong","loud","clear","soft","dark"]
        listOfWord2 = ["sister","niece","aunt","woman","madam","heiress","queen","countess","empress","duchess",
                       "slower","shorter","stronger","louder","clearer","softer","darker"]
    
    dictOfModel = {model:VecorialComparison(model) for model in listOfModel}
   
    with open(path,"w") as file:
        file.write("Word1;Word2;Model;Cosine;Manhattan;Euclidean;Jaccard\n")
        for key in dictOfModel:
            for i in range(len(listOfWord1)):
                cos = dictOfModel[key].computeDistance(listOfWord1[i],listOfWord2[i],"cosine")
                manhattan = dictOfModel[key].computeDistance(listOfWord1[i],listOfWord2[i],"manhattan")
                euclidean = dictOfModel[key].computeDistance(listOfWord1[i],listOfWord2[i],"euclidean")
                jaccard = dictOfModel[key].computeDistance(listOfWord1[i],listOfWord2[i],"jaccard")
                file.write(f"{listOfWord1[i]};{listOfWord2[i]};{key};{cos if cos is not None else 'NA'};{manhattan if manhattan is not None else 'NA'};{euclidean if euclidean is not None else 'NA'};{jaccard if jaccard is not None else 'NA'}\n")
    
def main():
    #comparison = VecorialComparison("gpt-2")
    generateDumpComparisonCsv()
    """
    while True:
        text = input("Expression 1 : ")
        if text == "--0--":
            break
        else:
            text2 = input("Expression 2 : ")
            cos = comparison.computeDistance(text, text2, "cosine")
            euclidean = comparison.computeDistance(text, text2, "euclidean")
            manhattan = comparison.computeDistance(text, text2, "manhattan")
            jaccard = comparison.computeDistance(text, text2,"jaccard")
            
            print(f"Link between {text} and {text2} : \n- Cosinus de similarité : {cos}\n- Distance euclidienne : {euclidean}\n- Distance de Manhattan : {manhattan}\n- Distance de Jaccard : {jaccard}")
    """
if __name__ == "__main__":
    main()