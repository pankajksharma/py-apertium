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
