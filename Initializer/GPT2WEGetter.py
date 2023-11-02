#https://github.com/huggingface/transformers/issues/1458
#https://huggingface.co/transformers/v3.0.2/model_doc/gpt2.html
#https://medium.com/@TaaniyaArora/visualizing-gpt2-word-embeddings-on-tensorboard-ea5c8fef9efa#:~:text=Load%20model%20from%20transformers%20import%20GPT2TokenizerFast%2C%20GPT2LMHeadModel%20import,embeddings%20word_embeddings%20%3D%20model.transformer.wte.weight%20%23%20Word%20Token%20Embeddings
#https://github.com/Taaniya/exploring-gpt2-language-model/blob/main/Visualizing_gpt2_token_embeddings.ipynb
#https://huggingface.co/transformers/v3.0.2/model_doc/gpt2.html

from transformers import GPT2Tokenizer, GPT2Model
import numpy as np, time

def main():
    begin = time.time()

    tokenizer = GPT2Tokenizer.from_pretrained('gpt2') # On crée les objets nécessaires
    model = GPT2Model.from_pretrained('gpt2')

    print(tokenizer.vocab_size,tokenizer, time.time()-begin) #Nombre de vocabulaire dans GPT-2, paramètre du tokenizer
    #Création du Word embedding en raw_unicode_escape pour éviter les erreurs liées à la sources / caractères inconnus
    open(__file__.removesuffix("GPT2WEGetter.py")+"Word2Vec\\gpt-2.txt","w", encoding="raw_unicode_escape").close()
    with open(__file__.removesuffix("GPT2WEGetter.py")+"Word2Vec\\gpt-2.txt","a", encoding = 'raw_unicode_escape') as file:
        count = 0
        for i in range(tokenizer.vocab_size): 
            inputs = tokenizer(tokenizer.decode(i), return_tensors="pt") #Pour chaque token, on récupère le mot associé
            outputs = model(**inputs) 
            last_hidden_states = outputs[0] #On récupère le vecteur à la fin de sa création
            WEstring = " ".join([str(i) for i in last_hidden_states[0][0].detach().numpy()]) #On transforme le vector tensor flow pour le mettre dans le word embedding
        
            file.write(tokenizer.decode(i).strip().removeprefix('\u0120') +" "+ WEstring +"\n") #\u0120 est un caractère au début de la pluspart des mots donc on le retire : https://github.com/openai/gpt-2/issues/80
            
            if count%100 == 0: #Affichage de la progression
                if count == 0:
                    print(np.size(last_hidden_states[0][0].detach().numpy()))
                print(count,time.time()-begin)
            count += 1

    print("Downloaded", count,"lines in", round(time.time()-begin,3), "seconds") # 22 minutes pour le téléchargement
            
if __name__ == "__main__":
    main()   

#print(tokenizer.decode(9288))
#inputs = tokenizer("test", return_tensors="pt")
#print(inputs)
#outputs = model(**inputs)

#last_hidden_states = outputs[0]  # The last hidden-state is the first element of the output tuple, word embedding
#print(last_hidden_states[0][0].detach().numpy())

#Pour voir les liens mots/tokens
"""
#tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
#print(tokenizer.pretrained_vocab_files_map)
{
    'vocab_file': {
        'gpt2': 'https://huggingface.co/gpt2/resolve/main/vocab.json', 
        'gpt2-medium': 'https://huggingface.co/gpt2-medium/resolve/main/vocab.json', 
        'gpt2-large': 'https://huggingface.co/gpt2-large/resolve/main/vocab.json', 
        'gpt2-xl': 'https://huggingface.co/gpt2-xl/resolve/main/vocab.json', 
        'distilgpt2': 'https://huggingface.co/distilgpt2/resolve/main/vocab.json'
    }, 
    'merges_file': {
        'gpt2': 'https://huggingface.co/gpt2/resolve/main/merges.txt',
        'gpt2-medium': 'https://huggingface.co/gpt2-medium/resolve/main/merges.txt',
        'gpt2-large': 'https://huggingface.co/gpt2-large/resolve/main/merges.txt',
        'gpt2-xl': 'https://huggingface.co/gpt2-xl/resolve/main/merges.txt',
        'distilgpt2': 'https://huggingface.co/distilgpt2/resolve/main/merges.txt'
    },
    'tokenizer_file': {
        'gpt2': 'https://huggingface.co/gpt2/resolve/main/tokenizer.json',
        'gpt2-medium': 'https://huggingface.co/gpt2-medium/resolve/main/tokenizer.json',
        'gpt2-large': 'https://huggingface.co/gpt2-large/resolve/main/tokenizer.json',
        'gpt2-xl': 'https://huggingface.co/gpt2-xl/resolve/main/tokenizer.json',
        'distilgpt2': 'https://huggingface.co/distilgpt2/resolve/main/tokenizer.json'
    }
}
"""

