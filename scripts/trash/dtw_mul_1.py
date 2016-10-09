import os
import sys
import re
import numpy
import time
import pp

def usage():
	print "usage:python dtw.py dir_featFile_query dir_featFile_utt dir_ret";
	print "--dir_featFile_query(without '/' seperator):directory containing the feature(eg. posteriorgram) of queries";
	print "--dir_featFile_query(without '/' seperator):directory containing the feature(eg. posteriorgram) of utterances";	
	print "--dir_ret(without '/' seperator):where to put the result files";
	exit();

def readFeat(filePath):
    
    con=open(filePath).readlines();
    feat=[map(float,one.strip().split()) for one in con];
    return numpy.array(feat);

def smooth_feat(feat,smooth_param):
	dim=len(feat[0]);
	u=numpy.ones([len(feat),dim])*(1.0/dim); ###the uniform probability distribution matrix
	smoothed_feat=(1-smooth_param)*feat+smooth_param*u;
	return smoothed_feat;
	
def comput_distance(vec1,vec2):
	distance=-numpy.log10(numpy.dot(vec1,vec2));
	return distance;

def compute_simi_matrix(feat_utt,feat_query):
	simi_matrix=-numpy.log10(numpy.dot(feat_query,numpy.transpose(feat_utt)));
	return simi_matrix;
	
def compute_acc_distance(similarity_matrix,acc_distance_begin,begin,end,fai):
	begin_x,begin_y=begin;
	end_x,end_y=end;
	distance_sum=0.0;
	gamma=max((end_x-begin_x),(end_y-begin_y));
	if((begin_x+1)==end_x):
		for i in range(begin_y+1,end_y+1):
			distance_sum=distance_sum+similarity_matrix[end_x][i];
		distance_sum=float(gamma**fai)/(end_y-begin_y)*distance_sum;
	elif((begin_y+1)==end_y):	
		for i in range(begin_x+1,end_x+1):
			distance_sum=distance_sum+similarity_matrix[i][end_y];
		distance_sum=float(gamma**fai)*distance_sum;	
	else:
		print "incorrect transition!";
		exit();
	return distance_sum+acc_distance_begin;

def getMin(l):
	l.sort();
	return l[0];

### This version of DY follows the algorithm mentioned in paper 'Intrinsic Spectral Analysis Based on Temporal Context Features for Query-by-Example Spoken Term Detection' 
def dystep_ISA(num_feat_query,num_feat_utt,path_len,distance_acc,similarity_matrix):

	paths={}; ###use a dictionay to save the paths(key=beginning point of a path line; value=ending point of the same path line)

	###initialization
	for i in range(num_feat_utt): 
		path_len[0][i]=1; 
		distance_acc[0][i]=similarity_matrix[0][i];	###compute_distance(smoothed_feat_query[0],smoothed_feat_utt[i]); 		
	
	for j in range(1,num_feat_query):
		path_len[j][0]=j+1; 
		distance_acc[j][0]=numpy.sum(similarity_matrix[0:j+1,0])/path_len[j][0];	###compute_distance(smoothed_feat_query[j],smoothed_feat_utt[0]); 
		paths[(j,0)]=(j-1,0);
			
	
	###DP step
	for i in range(1,num_feat_query):
		for j in range(1,num_feat_utt):
			h_distance_acc=distance_acc[i][j-1]+similarity_matrix[i][j];
			h_path=path_len[i][j-1]+1;
			v_distance_acc=distance_acc[i-1][j]+similarity_matrix[i][j];
			v_path=path_len[i-1][j]+1;
			d_distance_acc=distance_acc[i-1][j-1]+similarity_matrix[i][j];
			d_path=path_len[i-1][j-1]+2;

			candidates=[(h_distance_acc/h_path,h_distance_acc,h_path,(i,j-1)),(v_distance_acc/v_path,v_distance_acc,v_path,(i-1,j)),(d_distance_acc/d_path,d_distance_acc,d_path,(i-1,j-1))];
			candidates_sorted=sorted(candidates,key=lambda x:x[0]);
			path_len[i][j]=candidates_sorted[0][2];
			distance_acc[i][j]=candidates_sorted[0][1];
			paths[(i,j)]=candidates_sorted[0][3];	

	###save the distance_acc
	#f4=open("distance_matrix","w");
	#f4.writelines('\n'.join(['\t'.join(map(str,one)) for one in distance_acc]));		
	#f4.close();

	###search for the best full matching path and its distance
	last_row=[(index,distance/length,distance,length) for index,distance,length in zip(range(num_feat_utt),distance_acc[num_feat_query-1],path_len[num_feat_query-1])];	
	last_row_sorted=sorted(last_row,key=lambda x:x[1]);
	minDistance=last_row_sorted[0][1];
	best_ones=[one for one in last_row_sorted if one[1]==minDistance];
	bestPaths=dict(zip(range(len(best_ones)),[[(num_feat_query-1,one[0])] for one in best_ones]));	

	return minDistance,paths,bestPaths;

### This version of DY is a kind of variation of the algorithm mentioned in paper 'Query-By-Example Spoken Term Detection Using Phonetic Posteriorgram Templates' 
def dystep_PPT(num_feat_query,num_feat_utt,path_len,distance_acc,similarity_matrix,fai):

	paths={}; ###use a dictionay to save the paths(key=beginning point of a path line; value=ending point of the same path line)

	###initialization
	for i in range(num_feat_utt): 
		path_len[0][i]=1; 
		distance_acc[0][i]=similarity_matrix[0][i];	###compute_distance(smoothed_feat_query[0],smoothed_feat_utt[i]); 		
	
	for j in range(1,num_feat_query):
		path_len[j][0]=j+1; 
		distance_acc[j][0]=similarity_matrix[j][0];	###compute_distance(smoothed_feat_query[j],smoothed_feat_utt[0]); 
		paths[(j,0)]=(j-1,0);
			
	
	###DP step
	for i in range(1,num_feat_query):
		for j in range(1,num_feat_utt):
			h_distance_acc=distance_acc[i][j-1]+similarity_matrix[i][j];
			h_path=path_len[i][j-1]+1;
			v_distance_acc=distance_acc[i-1][j]+similarity_matrix[i][j];
			v_path=path_len[i-1][j]+1;
			d_distance_acc=distance_acc[i-1][j-1]+similarity_matrix[i][j];
			d_path=path_len[i-1][j-1]+2;

			candidates=[(h_distance_acc/h_path,h_distance_acc,h_path,(i,j-1)),(v_distance_acc/v_path,v_distance_acc,v_path,(i-1,j)),(d_distance_acc/d_path,d_distance_acc,d_path,(i-1,j-1))];
			candidates_sorted=sorted(candidates,key=lambda x:x[0]);
			path_len[i][j]=candidates_sorted[0][2];
			distance_acc[i][j]=candidates_sorted[0][1];
			paths[(i,j)]=candidates_sorted[0][3];	

	###save the distance_acc
	#f4=open("distance_matrix","w");
	#f4.writelines('\n'.join(['\t'.joinfile_query_name(map(str,one)) for one in distance_acc]));		
	#f4.close();

	###search for the best full matching path and its distance
	last_row=[(index,distance/length,distance,length) for index,distance,length in zip(range(num_feat_utt),distance_acc[num_feat_query-1],path_len[num_feat_query-1])];	
	last_row_sorted=sorted(last_row,key=lambda x:x[1]);
	minDistance=last_row_sorted[0][1];
	best_ones=[one for one in last_row_sorted if one[1]==minDistance];
	bestPaths=dict(zip(range(len(best_ones)),[[(num_feat_query-1,one[0])] for one in best_ones]));	

	return minDistance,paths,bestPaths;

def dtw(dir_ret,query_name,utt_name,feat_query,feat_utt,smooth_param,fai,shift):
	
	num_feat_query=len(feat_query);
	num_feat_utt=len(feat_utt);
	
	###smooth the feats
	smoothed_feat_query=smooth_feat(feat_query,smooth_param);
	smoothed_feat_utt=smooth_feat(feat_utt,smooth_param);	
	
	del feat_query; #delete the original feat to save memory 
	del feat_utt;	#delete the original feat to save memory
	
	similarity_matrix=compute_simi_matrix(smoothed_feat_utt,smoothed_feat_query);

	###output the mediate results
	#f1=open("smoothed_query","w");
	#f1.writelines('\n'.join([' '.join(map(str,one)) for one in smoothed_feat_query]));
	#f2=open("smoothed_utt","w");
	#f2.writelines('\n'.join([' '.join(map(str,one)) for one in smoothed_feat_utt]));
	#f3=open("similarity","w");
	#f3.writelines('\n'.join(['\t'.join(map(str,one)) for one in similarity_matrix]));

	path_len=numpy.ones([num_feat_query,num_feat_utt])*float('inf'); ###save the length of path
	distance_acc=numpy.ones([num_feat_query,num_feat_utt])*float('inf'); ###initiate the whole minimal accumulating distance matrix as INF	 
		
	minDistance,paths,bestPaths=dystep_ISA(num_feat_query,num_feat_utt,path_len,distance_acc,similarity_matrix);

	for key in bestPaths:	
		while(True):
			cur_point=bestPaths[key][-1];
			if(not paths.has_key(cur_point)):
				break;
			pre_point=paths[cur_point];
			bestPaths[key].append(pre_point);
		bestPaths[key].reverse();

	###save the last_row 
	#f5=open("last_row","w");
	#f5.writelines('\n'.join(['/'.join(map(str,one)) for one in last_row]));		
	#f5.close();
	#print bestPaths

	#frameLength=25;
	#shift=10;
	begin=getTime(bestPaths[0][0][1],shift);
	end=getTime(bestPaths[0][-1][1],shift)

	

	file_query_name=open(dir_ret+"/"+query_name+".ret","aw");


	file_query_name.writelines(utt_name+": begin="+str(begin)+" end="+str(end)+" socre="+str(minDistance)+"\n");
	#return minDistance,begin,end


def getTime(frameNo,shift):
	ret=0.0;
	if(frameNo!=0):
		ret=float(frameNo*shift)/1000; #float(frameLength+(frameNo-1)*shift)/1000;
	return ret;

def main():

	ppservers = ()
	job_server = pp.Server(ppservers=ppservers)
	job_server.set_ncpus(50);

	argc=len(sys.argv);
	if(argc != 4):
		usage();

	dir_featFile_query=sys.argv[1];
	dir_featFile_utt=sys.argv[2];
	
	files_featFile_query=[dir_featFile_query+'/'+one for one in os.listdir(dir_featFile_query)];
	files_featFile_utt=[dir_featFile_utt+'/'+one for one in os.listdir(dir_featFile_utt)];

	feat_queries=[(os.path.basename(one).split(".")[0],readFeat(one)) for one in files_featFile_query]; ###feature matrix of query
	feat_utts=[(os.path.basename(one).split(".")[0],readFeat(one)) for one in files_featFile_utt]; ###feature matrix of utt

	print "Reading the feat files finished!"
	
	smooth_param=0.00001;		###parameter value for smoothing
	fai=1;
	shift=10;
	dir_ret=sys.argv[3];
	
	for feat_query in feat_queries:
	    jobs = [job_server.submit(dtw,(dir_ret,feat_query[0],feat_utt[0],feat_query[1],feat_utt[1],smooth_param,fai,shift), (smooth_feat,compute_simi_matrix,dystep_ISA,getTime), ("numpy",)) for feat_utt in feat_utts]

	    for job in jobs:
		    job();


main();

