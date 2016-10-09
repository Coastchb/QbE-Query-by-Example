import os
import sys

def usage():
	print "usage: python getAudioList.py database srcDir path_to_system tarFileName";
	print "--database:database to do QbE on";
	print "--srcDir(with '/' seperator):where the audio files locate";
	print "--path_to_system(without '/' seperator):where the trained parameters locate";
	print "--tarFileName:name of file contraining the audio file names";
	exit();

def main():
	argc=len(sys.argv);
	if(argc != 5):
		usage();

	database=sys.argv[1];
	srcDir=sys.argv[2];
	sysPath=sys.argv[3];
	tarFileName=sys.argv[4];
	audioFiles=os.listdir(srcDir);
	audioPath=[srcDir+one for one in audioFiles];
	
	databaseDir=sysPath+"/"+database;
	if(not os.path.exists(databaseDir)):
		os.mkdir(databaseDir);
	tarDir=databaseDir+"/lists"+"/";
	if(not os.path.exists(tarDir)):
		os.mkdir(tarDir);
	
	tFile=open(tarDir+tarFileName,'w');
	tFile.writelines('\n'.join(audioPath));
	tFile.close();

main();
