import argparse
import subprocess
import os.path, sys
from lib.fms import FMS
from lib.utilities import preprocess, assertion

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='Preprocess the corpus for generating input for reg_test')
parser.add_argument('SLF', help='Source Language file for training')
parser.add_argument('TLF', help='Target Language file for training')
parser.add_argument('SLFT', help='Source Language file for testing')
parser.add_argument('TLFT', help='Target Language file for testing')
parser.add_argument('OUT', help='Output file for saving pairs', default='out.txt')

parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
parser.add_argument('--max-len', help='Maximum length of sentences allowed.', default='25')
args = parser.parse_args()

#Make sure all files exist
assertion(os.path.isfile(args.SLF), "Source Language file for training could not be found.")
assertion(os.path.isfile(args.TLF), "Target Language file for training could not be found.")
assertion(os.path.isfile(args.SLFT), "Source Language file for testing could not be found.")
assertion(os.path.isfile(args.TLFT), "Target Language file for testing could not be found.")

#TODO:Check lines are equal in SLFs and TLFs.

#Command line params
min_fms = float(args.min_fms)
max_len = int(args.max_len) 

#Training file pointers
file1 = open(args.SLF)
file2 = open(args.TLF)


src_sentences, tgt_sentences = [], []

while True:
	line = preprocess(file1.readline())
	line1 = preprocess(file2.readline())
	if not line or not line1:
		break
	if len(line.split()) > max_len:
		continue
	src_sentences.append(line)
	tgt_sentences.append(line1)

#Close files
file1.close()
file2.close()

#Testing file pointers
file3 = open(args.SLFT)
file4 = open(args.TLFT)

#Create new files where we could write our Pairs
file5 = open(args.OUT, 'w')

while True:
	line = preprocess(file3.readline())
	line1 = preprocess(file4.readline())
	if not line or not line1:
		break
	if len(line.split()) > max_len:
		continue
	for s,t in zip(src_sentences, tgt_sentences):
		fms = FMS(s, line)
		max_fms = fms.get_max_fms()			#Get max possible FMS for the pair
		if max_fms >= min_fms:
			fms = fms.calculate_using_wanger_fischer()	#Get actual FMS
			if fms >= min_fms and fms < 1.0:
				file5.write(s+"\n")
				file5.write(t+"\n")
				file5.write(line+"\n")
				file5.write(line1+"\n")
#Close remaining files
file3.close()
file4.close()
file5.close()
