import os
import sys
import re

def usage():
	print "usage: python getPosteriorgram.py path_to_Phnrec path_to_HList database path_to_system audioListFileName ";
	print "--dir_to_Phnrec(with '/' seperator):where the Phnrec tool locates";
	print "--path_to_HListdir:full path to HList tool";
	print "--database:database to do QbE on";
	print "--path_to_system(without '/' seperator):where the trained parameters locate";
	print "--audioListFileName:name of file containing the file names to compute posteriorgram";
	exit();

def getPostMatrix(Dir,fn,List):
	con=''.join(List);
	con=con.replace("\n"," ");
	conList=con.split();	#con.split(" ");
	#conList=[one for one in conList if one !=''];
	content=' '.join(conList)
	
	num_frame=len(content.split(":"))-2;
	prob={}
	for i in range(num_frame-1):
		
		reg=re.compile(".* "+str(i)+":(.*) "+str(i+1)+":.*");
		ret=reg.match(content);	
		if(ret):
			prob[str(i)]=ret.group(1).strip().split(" ");

	reg=re.compile(".*"+str(num_frame-1)+":([0-9\. ]*)");
	ret=reg.match(content);
	if(ret):
		#print 'matched';
		prob[str(num_frame-1)]=ret.group(1).strip().split(" ");
	 
	#print str(len(prob));      
	tarFile=open(Dir+fn+".txt","w");
	for i in range(num_frame):
		tarFile.writelines(' '.join(prob[str(i)])+"\n");	
	tarFile.close();


def getAscii(Dir,f,HListPath):
	fn=f.split(".")[0];
        #asciiFile=open(Dir+fn,"w");
	#console=sys.stdout;
        #sys.stdout=asciiFile;
        output=os.popen(HListPath+" "+Dir+f);
	List=output.read();
        #print List;
	#asciiFile.close();
	#sys.stdout=console;
	getPostMatrix(Dir,fn,List);

        os.system("rm "+Dir+f);	

def main():
	argc=len(sys.argv); 
	if(argc != 6):
		usage();

	toolPath=sys.argv[1];
	HListPath=sys.argv[2];
	database=sys.argv[3];
	sysPath=sys.argv[4];
	audioListFileName=sys.argv[5];
	fl=open(sysPath+"/"+database+"/lists"+"/"+audioListFileName);
	fileList=[one.strip() for one in fl.readlines()];
	fl.close();

	databaseDir=sysPath+"/"+database;
	if(not os.path.exists(databaseDir)):
		os.mkdir(databaseDir);
	postDir=databaseDir+"/posteriorgram"+"/";
	if(not os.path.exists(postDir)):
		os.mkdir(postDir);
	subPostDir=postDir+audioListFileName.split(".")[0]+"/";
	os.mkdir(subPostDir);

	for f in fileList:
		feaFile=os.path.basename(f).split(".")[0]+".fea";
		os.system(toolPath+"phnrec "+"-c "+sysPath+" -i "+f+" -t post -o "+subPostDir+feaFile);
		getAscii(subPostDir,feaFile,HListPath);
		 
main();
