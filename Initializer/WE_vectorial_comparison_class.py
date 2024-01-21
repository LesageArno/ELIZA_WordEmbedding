#https://www.geeksforgeeks.org/numpy-vector-multiplication/
import numpy as np
import scipy.spatial.distance as distance 
import time
import pickle

class VecorialComparison:
    def __init__(self, WEdict:str = "glove") -> None:
        """Class to compare word and vector distance

        Args:
            WEdict (str, optional): Word2Vec dict files from ["glove","enwiki"] or specify the path. Defaults to "glove".
        """
        if WEdict == "glove":
            dict_path = __file__.removesuffix("WE_vectorial_comparison_class.py")+"Word2VecPreloaded\\WEglove_dict.pkl"  #__file__+... permet de récupérer le fichier depuis Initializer et non ELIZA_APP
        elif WEdict == "enwiki":
            dict_path = __file__.removesuffix("WE_vectorial_comparison_class.py")+"Word2VecPreloaded\\WEenwiki_dict.pkl"
        else:
            dict_path = __file__.removesuffix("WE_vectorial_comparison_class.py")+"Word2VecPreloaded\\"+"WE"+WEdict+"_dict.pkl"
        
        self.model = WEdict #Stockage de l'attribut WEdict
        
        print("Loading files...")
        time.sleep(0.5)
        begin = time.time()

        with open(dict_path,"rb") as f:
            self.dicVec = pickle.load(f)
        print("Loaded in",round(time.time()-begin,3),"seconds") #5 secondes pour charger les données
    
    def computeDistance(self, word1:str, word2:str, method:str = "cosine", correction:str = None) -> float:
        """Compute distance between two word using the loaded word-embedding 

        Args:
            `word1` (str): String for the first word.\n
            `word2` (str): String for the second word.\n
            `method` (str, optional): Mehod between `cosine, manhattan, euclidean, jaccard` . Defaults to `cosine`.\n
            `correction` (str, optional): String interpreted as a formula of correction. Defaults to `None`.\n

        Returns:
            float: Distance with the selected method and correction
        """
        computedDistance = None
        if word1 not in self.dicVec.keys() or word2 not in self.dicVec.keys(): #Si le mot n'est pas dans le dictionnaire alors on retourne None
            return None
        vec1, vec2 = self.initDistance(word1, word2)
        
        if method == "cosine": #Calcul de la distance
            computedDistance = self.cosineDistance(vec1, vec2)
        elif method == "manhattan":
            computedDistance = self.manhattanDistance(vec1, vec2)
        elif method == "euclidean":
            computedDistance = self.euclideanDistance(vec1, vec2)
        elif method == "jaccard":
            computedDistance = self.jaccardDistance(vec1, vec2)
        elif method == "tanimoto":
            computedDistance = self.tanimotoDistance(vec1, vec2)
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
            
    def initDistance(self, word1, word2): # -> tuple(np.ndarray)
        """Convert string into vector using the loaded word_embedding.

        Args:
            `word1` (str): Word1 to compute.\n
            `word2` (str): Word2 to compute. \n

        Returns:
            tuple(numpy.ndarray): The first vector is the vector of word1, the second is for word2.
        """
        vec1 = np.array(list(map(float,self.dicVec[word1].split(" "))))
        vec2 = np.array(list(map(float,self.dicVec[word2].split(" "))))
        return (vec1, vec2)
    
    def manhattanDistance(self, word1:np.ndarray, word2:np.ndarray) -> float:
        """Compute the Manhattant distance between two word/vector.

        Args:
            `word1` (str|numpy.ndarray): First word or vector.
            `word2` (str|numpy.ndarray): Second word or vector.
        Returns:
            float: Computed Manhattan distance.
        """
        return distance.cityblock(word1, word2)
    
    def euclideanDistance(self, word1:np.ndarray, word2:np.ndarray) -> float:
        """Compute the Euclidean distance between two word/vector.

        Args:
            `word1` (str|numpy.ndarray): First word or vector.\n
            `word2` (str|numpy.ndarray): Second word or vector.\n
            
        Returns:
            float: Computed Euclidean distance.
        """
        return distance.euclidean(word1, word2)
    
    def jaccardDistance(self, word1:np.ndarray, word2:np.ndarray) -> float:
        """Compute the Jaccard distance between two word/vector.

        Args:
            `word1` (str|numpy.ndarray): First word or vector.\n
            `word2` (str|numpy.ndarray): Second word or vector.\n
            
        Returns:
            float: Computed Jaccard distance.
        """
        return distance.jaccard(word1, word2)
    
    def tanimotoDistance(self, word1:np.ndarray, word2:np.ndarray) -> float:
        """Compute the Tanimoto distance between two word/vector. 

        Args:
            `word1` (str|numpy.ndarray): First word or vector.
            `word2` (str|numpy.ndarray): Second word or vector.
        Returns:
            float: Computed Manhattan distance.
        """
        returnedDistance = np.dot(word1, word2) / (np.linalg.norm(word1)**2 + np.linalg.norm(word2)**2 - np.dot(word1, word2))
        return returnedDistance
          
    def cosineDistance(self, word1:np.ndarray, word2:np.ndarray) -> float:
        """Compute the Cosine similarity between two word/vector.

        Args:
            `word1` (str|numpy.ndarray): First word or vector.\n
            `word2` (str|numpy.ndarray): Second word or vector.\n
            
        Returns:
            float: Computed Cosine similarity.
        """
        return 1 - distance.cosine(word1, word2) #La commande fait comme calcul 1 - cos(θ) donc on corrige
    
    def nearestDistance(self, keys_list:list[str], word:str, method:str = "cosine", correction:str = None, ignore:list[str] = ["xnone","xforeign"]):
        """Compute the nearest distance between each element of a list and a word.

        Args:
            `keys_list` (list(str)): List of words to compare.\n
            `word` (str): The word compared to each element of the list.\n
            `method` (str, optional): Distance Method between `cosine, manhattan, euclidean, jaccard`. Defaults to `"cosine"`.\n
            `correction` (str, optional): String interpreted as a formula of correction. Defaults to `None`.\n
            `ignore` (list[str], optional): Ignore key in the list but present in keys_list. Defaults to `["xnone","xforeign"]`.\n

        Returns:
            list(str,float): First element the bestKey of the list having the lowest distance with the word to compare. 
        """
        nearestDistance = None
        bestKey = ""
        countNone = 0
        
        for pop_elem in ignore:
            keys_list.pop(keys_list.index(pop_elem)) #Retire les élement non-intéressant dans la liste
        
        for key in keys_list:
            keyDistance = self.computeDistance(word1 = key.rstrip(), word2 = word, method = method, correction = correction) #Calcul la distance entre le mot de la liste et le mot de comparaison
            
            if keyDistance is None: #Si le mot n'est pas dans le word embeding, on passe au suivant
                countNone += 1
                continue
                
            if nearestDistance is None:
                nearestDistance = keyDistance #Si c'est le premier résultat, il s'agit du plus proche par défaut
            if method in ["manhattan","euclidean"]:
                nearestDistance = keyDistance if keyDistance < nearestDistance else nearestDistance #On garde le plus petit nombre pour manhattan et euclidienne
            else:
                nearestDistance = keyDistance if keyDistance > nearestDistance else nearestDistance #On garde la plus grande pour cosinus et tanimoto
            bestKey = key if keyDistance == nearestDistance else bestKey
        
        if countNone == len(keys_list): #Si la liste de tous les mots ne sont pas présents dans le word embedding, alors on retourne None
            return None
        
        return [bestKey, nearestDistance] #On retourne la meilleure clée accompagnée de sa distance

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

    def getVector(self, word:str) -> np.ndarray:
        return np.array(list(map(float,self.dicVec.get(word).split(" ")))) if self.dicVec.get(word) is not None else None

def generateDumpComparisonCsv(path:str = __file__.removesuffix("WE_vectorial_comparison_class.py")+"ModelTester\\generatedDump.csv", 
                              listOfModel:list[str] = ["enwiki","glove","gpt-2"], listOfWord1:list[str] = None, listOfWord2:list[str] = None):
    """Create a csv file to compare each model and distance. 
    The distance is computed pairwise between listOfWord1[i] and listOfWord2[i], this imply that the size of both
    list MUST be the same.

    Args:
        path (str, optional): Path to csv. Defaults to `__file__.removesuffix("WE_vectorial_comparison_class.py")+"ModelTester\generatedDump.csv"`.\n
        listOfModel (list, optional): List of model to compare. Defaults to `["enwiki","glove","gpt-2"]`.\n
        listOfWord1 (list[str], optional): List of word to compare. Defaults to `None`.\n
        listOfWord2 (list[str], optional): _description_. Defaults to `None`.\n
    """
    
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
    comparisonGPT2 = VecorialComparison("gpt-2")
    comparisonGlove = VecorialComparison("glove")
    
    #generateDumpComparisonCsv()
    
    while True:
        text = input("Expression 1 : ")
        if text == "--0--":
            break
        else:
            text2 = input("Expression 2 : ")
            cosGPT2 = comparisonGPT2.computeDistance(text, text2, "cosine")
            euclideanGPT2 = comparisonGPT2.computeDistance(text, text2, "euclidean")
            manhattanGPT2 = comparisonGPT2.computeDistance(text, text2, "manhattan")
            jaccardGPT2 = comparisonGPT2.computeDistance(text, text2, "jaccard")
            tanimotoGPT2 = comparisonGPT2.computeDistance(text, text2, "tanimoto")
            
            cosGlove = comparisonGlove.computeDistance(text, text2, "cosine")
            euclideanGlove = comparisonGlove.computeDistance(text, text2, "euclidean")
            manhattanGlove = comparisonGlove.computeDistance(text, text2, "manhattan")
            jaccardGlove = comparisonGlove.computeDistance(text, text2, "jaccard")
            tanimotoGlove = comparisonGlove.computeDistance(text, text2, "tanimoto")
            
            print(f"Link between {text} and {text2} : \n- Cosinus de similarité : {cosGPT2} [{comparisonGPT2.model}] {cosGlove} [{comparisonGlove.model}]\n- Distance euclidienne : {euclideanGPT2} [{comparisonGPT2.model}] {euclideanGlove} [{comparisonGlove.model}]\n- Distance de Manhattan : {manhattanGPT2} [{comparisonGPT2.model}] {manhattanGlove} [{comparisonGlove.model}]\n- Distance de Jaccard : {jaccardGPT2} [{comparisonGPT2.model}] {jaccardGlove} [{comparisonGlove.model}]\n- Distance de Tanimoto : {tanimotoGPT2} [{comparisonGPT2.model}] {tanimotoGlove} [{comparisonGlove.model}]")
    
if __name__ == "__main__":
    main()