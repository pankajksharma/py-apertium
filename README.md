Apertium Python Wrapper
======================

Takes an Apertium language pair, a source-language sentence S, and a target-language sentence T, and outputs the set of all possible pairs of subsegments (s,t) such that s is a subsegment of S, t a subsegment of T and t is the Apertium translation of s or vice-versa (a subsegment is a sequence of whole words).

Usage: apertium.py [-h] S T P
-h	Prints Help
S	Source Language Sentence
T	Target Language Sentence
P	Language Pair (for example en-eo)

Example Usage:
python apertium.py "bat under rat" "batilo sub rato" "en-eo" 

Expected Output:
(bat under, batilo sub)
(bat under rat, batilo sub rato)
(under rat, sub rato)
Found 3 pair(s).
