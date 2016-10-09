import os
import sys
import re
import numpy as np
import time

def usage():
	print "usage:python dtw.py featFile_query featFile_utt";
	print "--featFile_query:file containing the feature(eg. posteriorgram) of query";
	print "--featFile_query:file containing the feature(eg. posteriorgram) of utterance";
	exit();

def readFeat(filePath):
	con=open(filePath).readlines();
	feat=[map(float,one.strip().split()) for one in con];
	return np.array(feat);

def smooth_feat(feat,smooth_param):
	dim=len(feat[0]);
	u=np.ones([len(feat),dim])*(1.0/dim); ###the uniform probability distribution matrix
	smoothed_feat=(1-smooth_param)*feat+smooth_param*u;
	return smoothed_feat;
	
def comput_distance(vec1,vec2):
	distance=-np.log10(np.dot(vec1,vec2));
	return distance;

def compute_simi_matrix(feat_utt,feat_query):
	simi_matrix=-np.log10(np.dot(feat_query,np.transpose(feat_utt)));
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
		distance_acc[j][0]=np.sum(similarity_matrix[0:j+1,0])  ###/path_len[j][0];	###compute_distance(smoothed_feat_query[j],smoothed_feat_utt[0]); 
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
	distance_path=[];
	f4=open("distance_matrix","w");

	for i in range(len(distance_acc)):
		tmp=[];
		for j in range(len(distance_acc[i])):
			tmp.append(str(j)+":"+str(distance_acc[i][j])+"/"+str(path_len[i][j])+"="+str(distance_acc[i][j]/path_len[i][j]));
		distance_path.append(tmp);
		
	f4.writelines('\n'.join(['\t'.join(one) for one in distance_path]));		
	f4.close();

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


	###search for the best full matching path and its distance
	last_row=[(index,distance/length,distance,length) for index,distance,length in zip(range(num_feat_utt),distance_acc[num_feat_query-1],path_len[num_feat_query-1])];	
	last_row_sorted=sorted(last_row,key=lambda x:x[1]);
	minDistance=last_row_sorted[0][1];
	best_ones=[one for one in last_row_sorted if one[1]==minDistance];
	bestPaths=dict(zip(range(len(best_ones)),[[(num_feat_query-1,one[0])] for one in best_ones]));	

	return minDistance,paths,bestPaths;

def dtw(feat_query,feat_utt,smooth_param,fai):
	num_feat_query=len(feat_query);
	num_feat_utt=len(feat_utt);
	
	###smooth the feats
	smoothed_feat_query=smooth_feat(feat_query,smooth_param);
	smoothed_feat_utt=smooth_feat(feat_utt,smooth_param);	
	print smoothed_feat_query;
	print smoothed_feat_utt;		
	similarity_matrix=compute_simi_matrix(smoothed_feat_utt,smoothed_feat_query);


	###output the mediate results
	f1=open("smoothed_query","w");
	f1.writelines('\n'.join([' '.join(map(str,one)) for one in smoothed_feat_query]));
	f2=open("smoothed_utt","w");
	f2.writelines('\n'.join([' '.join(map(str,one)) for one in smoothed_feat_utt]));
	f3=open("similarity","w");
	f3.writelines('\n'.join([' '.join(map(str,one)) for one in similarity_matrix]));
	f3.close();

	path_len=np.ones([num_feat_query,num_feat_utt])*float('inf'); ###save the length of path
	distance_acc=np.ones([num_feat_query,num_feat_utt])*float('inf'); ###initiate the whole minimal accumulating distance matrix as INF	 
		
	minDistance,paths,bestPaths=dystep_ISA(num_feat_query,num_feat_utt,path_len,distance_acc,similarity_matrix);

	for key in bestPaths:	
		while(True):
			cur_point=bestPaths[key][-1];
			if(not paths.has_key(cur_point)):
				break;
			pre_point=paths[cur_point];
			bestPaths[key].append(pre_point);
		bestPaths[key].reverse();
	print bestPaths[0];
	frameLength=25;
	shift=10;
	begin=getTime(bestPaths[0][0][1],shift);
	end=getTime(bestPaths[0][-1][1],shift);
	return minDistance,begin,end;

def getTime(frameNo,shift):
	if(frameNo==0):
		return 0.0;
	return float(frameNo*shift)/1000; #float(frameLength+(frameNo-1)*shift)/1000;

def main():
	argc=len(sys.argv);
	if(argc != 3):
		usage();

	featFile_query=sys.argv[1];
	featFile_utt=sys.argv[2];
	feat_query=readFeat(featFile_query); ###feature matrix of query
	feat_utt=readFeat(featFile_utt);     ###feature matrix of utterance
	smooth_param=0.00001;		###parameter value for smoothing
	fai=1;
	[minDistance,begin,end]=dtw(feat_query,feat_utt,smooth_param,fai);
	
	print "---"+os.path.basename(featFile_utt).split(".")[0]+": begin="+str(begin)+" end="+str(end)+" socre="+str(minDistance)+"\n";

main();

######################################
###Trash! Ignore it, please!!!
######################################
def dtw_trash(feat_query,feat_utt,smooth_param,fai):
	num_feat_query=len(feat_query);
	num_feat_utt=len(feat_utt);
	
	###smooth the feats
	smoothed_feat_query=smooth_feat(feat_query,smooth_param);
	smoothed_feat_utt=smooth_feat(feat_utt,smooth_param);	
		
	similarity_matrix=compute_simi_matrix(smoothed_feat_utt,smoothed_feat_query);

	
	h_distance_acc=np.ones([num_feat_query,num_feat_utt])*float('inf'); ###save the horizontal minimal accumulating distance of every point
	v_distance_acc=np.ones([num_feat_query,num_feat_utt])*float('inf'); ###save the vertical minimal accumulating distance of every point
	distance_acc=np.ones([num_feat_query,num_feat_utt])*float('inf'); ###initiate the whole minimal accumulating distance matrix as INF
	 
	paths={}; ###use a dictionay to save the paths(key=beginning point of a path line; value=ending point of the same path line)
	h_paths={}; ###save the horizontal best paths
	v_paths={}; ###save the vertical best paths

	###initialization
	for i in range(num_feat_utt):  
		#v_distance_acc[0][i]=similarity_matrix[0][i];   ###only save the vertical accumulatin distance, ignore the horizontal one (actually both can be ignored)
		distance_acc[0][i]=similarity_matrix[0][i];	###compute_distance(smoothed_feat_query[0],smoothed_feat_utt[i]); 
	
	for j in range(num_feat_query): 
		#h_distance_acc[j][0]=similarity_matrix[j][0];   ###only save the horizontal accumulatin distance, ignore the vertical one (actually both can be ignored) 
		distance_acc[j][0]=similarity_matrix[j][0];	###compute_distance(smoothed_feat_query[j],smoothed_feat_utt[0]); 	
	
	###DP step
	for i in range(1,num_feat_query):
		for j in range(1,num_feat_utt):
			if(i==1 and j==1): ###special case			
				distance_acc[i][j]=distance_acc[i-1][j-1]+similarity_matrix[i][j];
				h_distance_acc[i][j]=distance_acc[i][j];
				v_distance_acc[i][j]=distance_acc[i][j];
				paths[(i,j)]=h_paths[(i,j)]=v_paths[(i,j)]=(i-1,j-1);
			elif(i==1):
				mini=getMin([similarity_matrix[i-1][j-1],h_distance_acc[i][j-1]]);
				distance_acc[i][j]=mini+similarity_matrix[i][j];
				h_distance_acc[i][j]=distance_acc[i][j];
				v_distance_acc[i][j]=similarity_matrix[i-1][j-1]+similarity_matrix[i][j];
				if(mini==similarity_matrix[i-1][j-1]):
					paths[(i,j)]=(i-1,j-1);
				else:
					paths[(i,j)]=h_paths[(i,j-1)];
				h_paths[(i,j)]=paths[(i,j)];
				v_paths[(i,j)]=(i-1,j-1);
		
				#print str(i)+","+str(j);
				#print "acc_dis="+str(distance_acc[i][j]);
				#print "pre point:";
				#print paths[(i,j)];
					
			elif(j==1):	###h_distance_acc[i][j]='inf',indicating that the query must start from the first frame 
				distance_acc[i][j]=v_distance_acc[i-1][j]+similarity_matrix[i][j];
				v_distance_acc[i][j]=distance_acc[i][j];
				paths[(i,j)]=v_paths[(i,j)]=(0,0);				
			else:
				mini=getMin([v_distance_acc[i-1][j],h_distance_acc[i][j-1],distance_acc[i-1][j-1]]);
				distance_acc[i][j]=mini+similarity_matrix[i][j];
				h_mini=getMin([h_distance_acc[i][j-1],distance_acc[i-1][j-1]]);
				h_distance_acc[i][j]=h_mini+similarity_matrix[i][j];
				v_mini=getMin([v_distance_acc[i-1][j],distance_acc[i-1][j-1]]);
				v_distance_acc[i][j]=v_mini+similarity_matrix[i][j];
				if(mini==v_distance_acc[i-1][j]):
					paths[(i,j)]=v_paths[(i,j)]=v_paths[(i-1,j)];
					if(h_mini==h_distance_acc[i][j-1]):
						h_paths[(i,j)]=h_paths[(i,j-1)];
					else:
						h_paths[(i,j)]=(i-1,j-1);
				elif(mini==h_distance_acc[i][j-1]):
					paths[(i,j)]=h_paths[(i,j)]=h_paths[(i,j-1)];
					if(v_mini==v_distance_acc[i-1][j]):
						v_paths[(i,j)]=v_paths[(i-1,j)];
					else:
						v_paths[(i,j)]=(i-1,j-1);
				else:
					paths[(i,j)]=v_paths[(i,j)]=h_paths[(i,j)]=(i-1,j-1);
						


	###search for the best full matching path and its distance
	minDistance=float('inf');
	bestPaths={};	###maybe there exists more than one best paths! key of the dictionay is the best paths' ending point;and the value of the dictionary is the full path
	for i in range(1,num_feat_utt):
		dist=distance_acc[num_feat_query-1][i];
		if(dist<minDistance):
			minDistance=dist;
			#bestPath_end=paths[(num_feat_query-1,i)];
			bestPaths[(num_feat_query-1,i)]=[(num_feat_query-1,i)];
	for key in bestPaths:	
		while(True):
			cur_point=bestPaths[key][-1];
			if(not paths.has_key(cur_point)):
				break;
			pre_point=paths[cur_point];
			bestPaths[key].append(pre_point);
		bestPaths[key].reverse();	
	return minDistance,bestPaths;



