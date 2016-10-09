import re
import os
import sys

def processDir(dire):
	if(not dire.endswith("/")):
		dire=dire+"/";
	return dire;

def getAudioDur(wavPath):
	if(not os.path.exists(wavPath)):
		print 'Error: file '+wavPath+' not exists'
		exit();
	dur=os.popen('mediainfo "--Inform=Audio;%Duration%" ' + wavPath).read().strip(); #get audio duration in ms
	#print wavPath;
	#print dur;
	return float(dur);

