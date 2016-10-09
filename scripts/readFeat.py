import numpy
import sys
import os

def usage():
	print "usage: readFeat.py dir"
	print "--dir(without '/' seperator):where the feat files locate"
	exit();

def readFeat(dire,fileName):
	fn=fileName.split(".")[0];
	con=open(dire+"/"+fileName).readlines();
	feat=[map(float,one.strip().split()) for one in con];
	return (fn,feat);

def main():
	if(len(sys.argv)!=2):
		usage();

	dire=sys.argv[1];
	featFiles=os.listdir(dire);
	
	feats=[readFeat(dire,featFile) for featFile in featFiles];
	
	print feats;
	#return feats;

main();
