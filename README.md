Apertium Python Wrapper
======================

Takes an Apertium language pair, a source-language sentence S, and a target-language sentence T, and outputs the set of all possible pairs of subsegments (s,t) such that s is a subsegment of S, t a subsegment of T and t is the Apertium translation of s or vice-versa (a subsegment is a sequence of whole words).

See http://wiki.apertium.org/wiki/User:Pankajksharma/Application#Proposal for more detail.

##GSoC work##

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

##Pre GSoC scripts##

###apertium.py###

usage: pre_soc/apertium.py [-h] [-d D] [-r] [-s] S T P

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

	python pre_soc/apertium.py "bat under rat" "batilo sub rato" "en-eo" [-d installation_directory] [-r] [-s] 

Expected Output:

(bat under, batilo sub)

(bat under rat, batilo sub rato)

(under rat, sub rato)

###fms.py###

usage: pre_soc/fms.py [-h] S S1

Provides FMS of strings S and S1

positional arguments:

  S           First Sentence

  S1          Second Sentence

optional arguments:

  -h, --help  show this help message and exit

Example Usage:

	 python pre_soc/fms.py "The man is in the moon" "The man in the moon"

Expected Output:

	83.33

###pairs.py###
usage: pre_soc/pairs.py [-h] S S1

Provides phrase pairs

positional arguments:

  S           First Sentence

  S1          Second Sentence

optional arguments:

  -h, --help  show this help message and exit

###tmx.py###

usage: pre_soc/tmx.py [-h] [-o O] [-d D] [-r] [-s] TM P

Reads Translation Memory and saves the sub-segments

positional arguments:

  TM          Translation Memory

  P           Language Pair for TM (for example en-eo)

optional arguments:

  -h, --help  show this help message and exit

  -o O        Output file to save new TMX

  -d D        Specify the lanuguage-pair installation directory

  -r          Check for pairs reversibly as well

  -s          Ignore single words

Example Usage:

   python pre_soc/fms.py old.tmx "en-eo" -o new.tmx
