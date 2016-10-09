import os
import sys
import re

def usage():
        print "usage: python convertPost.py path_to_HList dir";
        print "--path_to_HListdir:full path to HList tool";
        print "--dir(with '/' seperator):where the posteriorgram file locates";
        exit();

def getPostMatrix(Dir,fn,List):
	con=''.join(List);
	con=con.replace("\n"," ");
	conList=con.split(" ");
	conList=[one for one in conList if one !=''];
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


def getAscii(Dir,f,toolPath):
	fn=f.split(".")[0];
        asciiFile=open(Dir+fn,"w");
	console=sys.stdout;
        sys.stdout=asciiFile;
        output=os.popen(toolPath+" "+Dir+f);
	List=output.read();
        print List;
	asciiFile.close();
	sys.stdout=console;
	getPostMatrix(Dir,fn,List);

        os.system("rm "+Dir+f);	
	
def main():
        argc=len(sys.argv);
        if(argc != 3):
                usage();
        toolPath=sys.argv[1];
        Dir=sys.argv[2];
        files=os.listdir(Dir);
        for f in files:
		getAscii(Dir,f,toolPath);
                

main();

