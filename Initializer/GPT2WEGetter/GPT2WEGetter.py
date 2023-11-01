#https://github.com/huggingface/transformers/issues/1458
#https://huggingface.co/transformers/v3.0.2/model_doc/gpt2.html
#https://medium.com/@TaaniyaArora/visualizing-gpt2-word-embeddings-on-tensorboard-ea5c8fef9efa#:~:text=Load%20model%20from%20transformers%20import%20GPT2TokenizerFast%2C%20GPT2LMHeadModel%20import,embeddings%20word_embeddings%20%3D%20model.transformer.wte.weight%20%23%20Word%20Token%20Embeddings
#https://github.com/Taaniya/exploring-gpt2-language-model/blob/main/Visualizing_gpt2_token_embeddings.ipynb

from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')

print(tokenizer.pretrained_vocab_files_map)
"""
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