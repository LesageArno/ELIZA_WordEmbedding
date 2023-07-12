#https://www.geeksforgeeks.org/numpy-vector-multiplication/
import pickle
import time
import numpy as np

begin = time.time()

with open("Initializer\\Word2VecPreloaded\\WEglove_dict.pkl","rb") as f: #|Word2VecPreloaded\\WEglove_dict.pkl
    loaded_dict = pickle.load(f)
    

print(time.time()-begin) #5 secondes pour charger les données

def cosineSimilarity(source = {str:str}, word1 = str, word2 = str) -> float:
    """_summary_

    Args:
        source (dict): _description_. Put the file loaded with pickle (word_embeded_dict.pkl).
        word1 (_str_): _description_ word n°1.
        word2 (_str_): _description_ word n°2.

    Returns:
        float: _description_ Compute cosine similarity with the formula A∙B/(||A||∙||B||)
    """
    
    vec1 = np.array(list(map(float,source[word1].split(" ")))) #On convertie les mots en matrice de 100 ligne et 1 colonne (vecteur colonne)
    vec2 = np.array(list(map(float,source[word2].split(" "))))
    
    dot_prod = np.dot(vec1,vec2) #euclidian dot product A∙B = Σa₁b₁
    vecnorm1 = np.linalg.norm(vec1)
    vecnorm2 = np.linalg.norm(vec2) #magnitude // norme du vecteur
    
    cosine_similarity = dot_prod/(vecnorm1*vecnorm2) #https://en.wikipedia.org/wiki/Cosine_similarityimport 
    
    return(cosine_similarity)

def maxCosineSimilarity(keys_path = str, source = {str:str}, word = str):
    with open(keys_path,"r") as f:
        key_list = []
        while True:
            line = f.readline()
            if line == "":
                break
            key_list.append(line)
    maxCosine = 0
    bestKey = ""
    for key in key_list:
        if key.rstrip() in ["xnone","xforeign"]:
            continue
        else:
            cosine = cosineSimilarity(source,key.rstrip(),word)
            maxCosine = cosine if cosine > maxCosine else maxCosine #On remplace si le cos est plus grand
            if cosineSimilarity(source,key.rstrip(),word) == maxCosine:
                bestKey = key.rstrip()
    
    return {bestKey : maxCosine}

begin = time.time()

"""#Generate doctor_keys.txt
with open("doctor.txt","r") as f:
    open("doctor_keys.txt","w").close()
    g = open("doctor_keys.txt","a")
    
    while True:
        line = f.readline()
        if line == "":
            break
        
        if line.startswith("key: "):
            if line.split("key: ")[1].find(" ") == -1: #S'il n'y a pas d'espaces, one enregistre directement le mot
                g.write(line.split("key: ")[1])
            else:
                g.write(line.split("key: ")[1].split(" ")[0]+"\n") #On ne récupère que la liste de clé
    g.close()
"""

""" #Generate keys.txt
with open("keys.txt","w",encoding="utf-8") as f:
    f.close()

with open("keys.txt","a",encoding="utf-8") as f:
    count = 0
    for i in loaded_dict.keys():
        count+=1
        #if count%10000 == 0:
        #    print(i,time.time()-begin)
        f.write(i+"\n")
"""
#Generate glove.txt
with open("keys.txt","w",encoding="utf-8") as f:
    f.close()

with open("keys.txt","a",encoding="utf-8") as f:
    count = 0
    for i in loaded_dict.keys():
        count+=1
        #if count%10000 == 0:
        #    print(i,time.time()-begin)
        f.write(i+"\n")

print("###############################################################################\n\n###############################################################################") 

""" #Test de la fonction cosineSimilarity
while True: 
    if (input("Continuer ? (y/n) : ") == "y"):
        print(cosineSimilarity(source=loaded_dict,word1=input("Word 1 : "),word2=input("Word 2 : ")))
    else:
        break
"""

'''
#Test de la fonction maxCosineSimilarity
while True: 
    if (input("Continuer ? (y/n) : ") == "y"):
        print(maxCosineSimilarity("doctor_keys.txt",loaded_dict,input("Word : ")))
    else:
        break
'''