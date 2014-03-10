Apertium Python Wrapper
======================

Takes an Apertium language pair, a source-language sentence S, and a target-language sentence T, and outputs the set of all possible pairs of subsegments (s,t) such that s is a subsegment of S, t a subsegment of T and t is the Apertium translation of s or vice-versa (a subsegment is a sequence of whole words).

usage: apertium.py [-h] [-d D] [-r] [-s] S T P

Provides pairs of Languages

positional arguments:
  S           Source Language Sentence
  T           Target Language Sentence
  P           Language Pair (for example en-eo)

optional arguments:
  -h, --help  show this help message and exit
  -d D        Specify the lanuguage pair directory
  -r          Checks for pairs reversibly
  -s          Translate single words as well.

Example Usage:
	python apertium.py "bat under rat" "batilo sub rato" "en-eo" [-d installation sirectory] [-r] [-s] 

Expected Output:
(bat under, batilo sub)
(bat under rat, batilo sub rato)
(under rat, sub rato)
