# Eliza Word Embedding chatbot in Python

Based on Wade Brainerd's version in Python, at https://github.com/wadetb/eliza

In the initial README.md Wade Brainerd said about ELIZA in Python : 

        I feel that it is fairly complete. However there are some holes, as the library was written immediately prior to my discovery of Joseph Weizenbaum's own description of the original program, which is quite detailed, along with the original "doctor" script. Oh well. A copy of that article is provided in the repo as a reference to the correct behavior.  
  
This project has as a goal to adapt Eliza to the modern technique of the Chatbot using Word Embedding, it's not complete, we could note some *grammatical or syntactical error* in the chatbot responses (especially if the setting SYNON_EXTENT is True). This can be explained either by how the word embeddings were calculated (with enwiki and glove, *glove is better* because his definition of "near" is more linked with the natural definition) or the source (doctor.txt, ...).

## Before using ##
Before using, you must either download the __GloVe WordEmbeding__ (recommended), available at *http://web.archive.org/web/20230410222048/https://downloads.cs.stanford.edu/nlp/data/glove.6B.zip*   
or the __ENwiki WordEmbeding__, available at *http://wikipedia2vec.s3.amazonaws.com/models/en/2018-04-20/enwiki_20180420_100d.txt.bz2*.

After unpacking one of these WordEmbeding, put the file (enwiki_20180420_100d.txt|glove.6B.100d.txt) in the ELIZA\Initializer\Word2Vec (you have to keep the name of the file, see ```Architecture```), then just execute __launcher.bat__ or run __main.py__|__eliza.py__

```
Note: The first execution could be long depending on what WE you are using (>20 seconds), but the others execution will be faster.
```
The total ELIZA_APP file's size is varying from __339 MB__ (GloVe only, if we remove the Word2VecPreloaded\WEglove_dict.pkl) to __7407 MB__ (GloVe, ENwiki and preloaded)

## Architecture
```txt
.
│   CHANGELOG.md
│   eliza.py
│   launcher.bat
│   LICENSE
│   main.py
│   README.md
├───Debug
│       I'm tired PWE 070 synon.mp4
│       PWE 070 synonTrue @madness .png
│       _match_decomp_r.png
├───Informations
│       keys_doctor.txt
│       keys_enwiki_20180420_100d.txt
│       keys_glove.txt
│       lien.txt
│       École Polytechnique Bachelor program - Mathematics FR_EN vocabulary sheet.pdf
├───Initializer
│   │   WEdict_creator.py
│   │   WEdict_test.py
│   │   WE_vectorial_comparison_class.py
│   ├───Target
│   │       doctor.txt
│   │       generalist.txt
│   │       SEdoctor.txt
│   ├───Word2Vec
│   │       enwiki_20180420_100d.txt
│   │       glove.6B.100d.txt
│   │       test.txt
│   ├───Word2VecPreloaded
│   │       WEenwiki_dict.pkl
│   │       WEglove_dict.pkl
│   │       WEtest.txt_dict.pkl
│   └───__pycache__
│           WEdict_creator.cpython-310.pyc
│           WE_vectorial_comparison_class.cpython-310.pyc
│           __init__.cpython-310.pyc
├───Logs
│       Elizalog.log
│       Matchslog.txt
│       synonlog.txt
├───Saves
│   ├───03072023_13h25
│   │       eliza.txt
│   │       elizaContexte.txt
│   │       elizaSansPoids.txt
│   ├───05072023_10h54
│   │       elizaArchitecture.txt
│   ├───07072023_11h59
│   │       saveDoctor_before_synonChange.txt
│   │       saveEliza_before_synonChange.txt
│   ├───10072023_14h25
│   │       elizasave.txt
│   ├───12072023_10h50
│   │       eliza.txt
│   ├───14072023_10h50
│   │       doctor_before_removing_arobase.txt
│   ├───26062023_10h45
│   │       WEdict_creator26062023_10h44.txt
│   │       WEdict_test26062023_10h45.txt
│   ├───26062023_13h01
│   │       eliza.txt
│   │       WEdict_creator.txt
│   │       WEdict_test.txt
│   │       WE_vectorial_comparison_class.txt
│   ├───27062023_08h08
│   │       eliza_save.txt
│   ├───27062023_13h50
│   │       saveELIZA.txt
│   ├───27062023_16h33
│   │       saveELIZA_avec_vecteur.txt
│   └───28062023_08h14
│           ElizasaveWithWEWeighted.txt
└───__pycache__
        eliza.cpython-310.pyc
        WE_vectorial_comparison_class.cpython-310.pyc
```

## Usage
Can be run __interactively__, with these parameters:  
```WEdict``` = "glove" (WE you are using)  
```TARGET``` = "doctor.txt" (source file with the rules to follow)  
```SEUIL``` = 0.7 (threshold of the keyword, keyword must have a cosine similarity greater than the threshold to be kept)  
```WEIGHTED``` = True (if the weight in the source file have an impact)  
```SYNON_EXTENT``` = False (if unregistred synonyms are accepted)
```LOG``` = False (if we put additionals information to the Elizalog.log file)  
```MATCHLOGS``` = False (if we keep a track of the matching)  
```SYNONLOGS``` = False (if we keep a track of the synonyms matched [don't work, you can use it with SYNON_EXTENT True for better results])  
  
__DO NOT TOUCH THE NEXT SETTINGS UNLESS YOU REALY NEED THEM__ (see ```Extension```)  
```entity_form``` = False (True when you have this kind of form in your WordEmbeding system __ENTITY/...__ VEC,is automatically set to True if the Word Embeding is Enwiki)  
```header``` = False (True when the first line isn't a line of data, is automatically set to True if the Word Embeding is Enwiki)

```
$ python eliza.py
How do you do.  Please tell me your problem.
> I would like to have a chat bot.
You say you would like to have a chat bot ?
> bye
Goodbye.  Thank you for talking to me.
```

...or imported and used as a __library__:

```python
import eliza

eliza = eliza.main(WEdict = "glove", TARGET = "doctor.txt", SEUIL = 0.7, WEIGHTED = True, SYNON_EXTENT = False, LOG = False, MATCHLOGS = False, SYNONLOGS = False, entity_form = False, header = False)
```
...or run with parameter interface with __launcher.bat__|__main.py__ 

## Conversation ##
If you want to talk with Eliza about events, names, etc. You should use __~sentence~__, thus allowing Eliza to interpret the sentence as a word and not a series of words. This is particullarly efficient with enwiki. This synthax allows the use of multi-worded synonyms (such as depression and major depressive disorder)  
  
__Exemple:__
```
# Without ~~ using PWE 0.7 Enwiki, doctor.txt
How do you do.  Please tell me your problem.
> i saw the collapse of the world trade center.
You say you saw the collapse of the world trade center ?

# With ~~ using PWE 0.7 Enwiki, doctor.txt
How do you do.  Please tell me your problem.
> i saw the ~collapse of the world trade center~.
Can you elaborate on that ?

```

## Extension ##
1. if you want to choose *another* Word Embedding system then, you have to use a text file (.txt) in this format :
```
HEADER (optional, information of the document, dimension, no. of line, etc.)
WORD1 VEC1
WORD2 VEC2
...
```
Then, put it in the __ELIZA\Initializer\Word2Vec__ folder, and launch with your specification (__WEdict__ must be the name of the file then if your WE system have either header or entity_form)  

2. if you want to choose *another* source (doctor.txt, SEdoctor.txt, etc.), you have to put your source file (txt format) in the __ELIZA\Initalizer\Target__ folder. This file need to respect this format to work :  
```
#This is a comment (only at the begining of the line)
initial: ... (1st sentence of the Chatbot, multiple possible)

final: ... (Last sentence of the chatbot, multiple possible)

quit: ... (Trigger to the final, multiple possible)

pre: word;result (Presubstitution of the chatbot, the word is substitute with result, multiple possible)

post: word;result (Postsubstitution of the chatbot, the word is substitute with result, multiple possible)

synon: root;word1;... (Synonymes, root is the main word and the others are the synonymes, multiple possible)

key: [xnone, xforeign, <key>] [weight] (Key to detected in the user sentence, xnone if no keys are detected, xforeign for foreign language, weight is the importance of the word, multiple possible)
    decomp: [$] [*] [[@]word1] ... (The decomposition to match for the reassambly $ for store in memory, * for an unknown number of word, @ for the root of a synonym list, multiple possible)
        reasmb: [goto <key>] ... [(int)] ... (Sentence to send, goto to use another key instead of the actual one, int should be replaced by the part of the decomposition you want to integrate (* and @ count for 1), multiple possible)

(optional)
action: (Roughly the same as key, but use direct answer without decomposition, multiple possible)
    trigger: [final] (The trigger that will put on the action, final if the action will generate the last sentence)
        seq: <sentence> (The sentence that will put on the trigger, the user and source file must have the same sentence)
    actuator: (What is return)
        seq: <sentence> (The sentence return, multiple possible)
```
