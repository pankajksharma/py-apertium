Apertium Python Wrapper
======================

Takes an Apertium language pair, a source-language sentence S, and a target-language sentence T, and outputs the set of all possible pairs of subsegments (s,t) such that s is a subsegment of S, t a subsegment of T and t is the Apertium translation of s or vice-versa (a subsegment is a sequence of whole words).

See http://wiki.apertium.org/wiki/User:Pankajksharma/Application#Proposal for more detail.

##GSoC work##

###On the fly patching###

usage: repair.py [-h] [-d D] [--min-fms MIN_FMS] [--min-len MIN_LEN]
                 [--max-len MAX_LEN]
                 S T S1 LP

On the fly repairing of sentence.

positional arguments:

  S                  Second Sentence

  T                  First Sentence Translation

  S1                 Second Sentence

  LP                 Language Pair

optional arguments:

  -h, --help         show this help message and exit

  -d D               Specify the lanuguage-pair installation directory

  --min-fms MIN_FMS  Minimum value of fuzzy match score of S and S1.

  --min-len MIN_LEN  Minimum length of sub-segment allowed.

  --max-len MAX_LEN  Maximum length of sub-segment allowed.

###fms.py

usage: fms.py [-h] S S1

Provides FMS of strings S and S1 using Wagner-Fischer algorithm.

positional arguments:

  S           First Sentence

  S1          Second Sentence

optional arguments:

  -h, --help  show this help message and exit


###file_stats.py

usage: file_stats.py [-h] [--min-fms MIN_FMS] F

Calculates and show a histogram of the distribution of FMS between pair of sentences present in corpus F.

positional arguments:

  F                  Corpus path.

optional arguments:

  -h, --help         show this help message and exit

  --min-fms MIN_FMS  Minimum value of fuzzy match score of S and S1.

###stats.py

usage: stats.py [-h] [-d D] [--min-fms MIN_FMS] [--min-len MIN_LEN]
                [--max-len MAX_LEN]
                D

Calulates FMS distribtution for all corpuses pressent in directory D.

positional arguments:

  D                  Corpus directory.

optional arguments:

  -h, --help         show this help message and exit

  -d D               Specify the lanuguage-pair installation directory

  --min-fms MIN_FMS  Minimum value of fuzzy match score of S and S1.

  --min-len MIN_LEN  Minimum length of sub-string allowed.

  --max-len MAX_LEN  Maximum length of sub-string allowed.

###Set A generator###

usage: A_generator.py [-h] [--min-fms MIN_FMS] [--min-len MIN_LEN]
                      [--max-len MAX_LEN]
                      S S1

Generates set A.

positional arguments:
  S                  First Sentence

  S1                 Second Sentence

optional arguments:

  -h, --help         show this help message and exit

  --min-fms MIN_FMS  Minimum value of fuzzy match score of S and S1.

  --min-len MIN_LEN  Minimum length of sub-string allowed.

  --max-len MAX_LEN  Maximum length of sub-string allowed.


Example:  python A_generator.py "some string" "some another string" --min-fms=0.6 --min-len=1 --max-len=3

Expected Output:

("some string", "some another string")

("string", "another string") 


###Set D generator###

Usage: python D_generator.py --helpusage: D_generator.py [-h] [-d D] [--min-fms MIN_FMS] [--min-len MIN_LEN] [--max-len MAX_LEN]
                      S T S1 LP

Generates set D.

positional arguments:

  S                  Second Sentence

  T                  First Sentence Translation

  S1                 Second Sentence

  LP                 Language Pair

optional arguments:

  -h, --help         show this help message and exit

  -d D               Specify the lanuguage-pair installation directory

  --min-fms MIN_FMS  Minimum value of fuzzy match score of S and S1.

  --min-len MIN_LEN  Minimum length of sub-string allowed.

  --max-len MAX_LEN  Maximum length of sub-string allowed.

Example: python D_generator.py "he changed his number recently" "Va canviar el seu número recentment" "he changed his address recently" en-ca

("Va canviar el seu", "Va canviar la seva adreça")

("Va canviar el seu número", "Va canviar el seu")

("Va canviar el seu número", "Va canviar la seva adreça")

("Va canviar el seu número recentment", "Va canviar la seva adreça recentment")

("El seu número", "El seu")

("El seu número", "La seva adreça")

("El seu número recentment", "La seva adreça recentment")

("Número recentment", "Recentment")

("Número recentment", "Adreça recentment")

####For pre-SoC wok see [pre-soc/](https://github.com/pankajksharma/py-apertium/tree/master/pre_soc)