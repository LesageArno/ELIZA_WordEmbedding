# Eliza chatbot in Python

Based on Wade Brainerd's version in Python, at https://github.com/wadetb/eliza

In the initial README.md Wade Brainerd said : 
```
I feel that it is fairly complete. However there are some holes, as the library was written immediately prior to my discovery of Joseph Weizenbaum's own description of the original program, which is quite detailed, along with the original "doctor" script. Oh well. A copy of that article is provided in the repo as a reference to the correct behavior.
```
## Before using ##
Before using, you muss either download the __GloVe WordEmbeding__ (recommended), available at *http://web.archive.org/web/20230410222048/https://downloads.cs.stanford.edu/nlp/data/glove.6B.zip* or the __ENwiki WordEmbeding__, available at *http://wikipedia2vec.s3.amazonaws.com/models/en/2018-04-20/enwiki_20180420_100d.txt.bz2*.

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
├───.vscode
│       settings.json
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
│   ├───Word2VecPreloaded
│   │       WEenwiki_dict.pkl
│   │       WEglove_dict.pkl
│   └───__pycache__
│           WEdict_creator.cpython-310.pyc
│           WE_vectorial_comparison_class.cpython-310.pyc
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

Can be run interactively, with these parameters:
TARGET = "doctor.txt"

```
$ python eliza.py
How do you do.  Please tell me your problem.
> I would like to have a chat bot.
You say you would like to have a chat bot ?
> bye
Goodbye.  Thank you for talking to me.
```

...or imported and used as a library:

```python
import eliza

eliza = eliza.main(WEdict = "glove", TARGET = "doctor.txt", SEUIL = 0.7, WEIGHTED = True, SYNON_EXTENT = False
                   LOG = False, MATCHLOGS = False, SYNONLOGS = False)
```