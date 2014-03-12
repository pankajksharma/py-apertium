Apertium Python Wrapper
======================

Takes an Apertium language pair, a source-language sentence S, and a target-language sentence T, and outputs the set of all possible pairs of subsegments (s,t) such that s is a subsegment of S, t a subsegment of T and t is the Apertium translation of s or vice-versa (a subsegment is a sequence of whole words).

apertium.py
-----------
usage: apertium.py [-h] [-d D] [-r] [-s] S T P

Provides pairs of Languages

positional arguments:
  S           Source Language Sentence
  T           Target Language Sentence
  P           Language Pair (for example en-eo)

optional arguments:
  -h, --help  show this help message and exit
  -d D        Specifies the lanuguage pair directory
  -r          Checks for pairs reversibly as well
  -s          Ignore single words

Example Usage:
	python apertium.py "bat under rat" "batilo sub rato" "en-eo" [-d installation_directory] [-r] [-s] 

Expected Output:

(bat under, batilo sub)

(bat under rat, batilo sub rato)

(under rat, sub rato)

fms.py
------
usage: fms.py [-h] S S1

Provides FMS of strings S and S1

positional arguments:
  S           First Sentence
  S1          Second Sentence

optional arguments:
  -h, --help  show this help message and exit

Example Usage:
	 python fms.py "The man is in the moon" "The man in the moon"

Expected Output:
	83.33
