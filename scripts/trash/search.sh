query_dir=/home/coast/project/QbE/BUT/PhnRec/PHN_CZ_SPDAT_LCRC_N1500/SWS2013/posteriorgram/query_val_tmp
utt_dir=/home/coast/project/QbE/BUT/PhnRec/PHN_CZ_SPDAT_LCRC_N1500/SWS2013/posteriorgram/utt_tmp

st=`date '+%Y-%m-%d %H:%M:%S'`
echo 'start at '$st

for query_file in `ls $query_dir`
do
	for utt_file in `ls $utt_dir`
	do
		python dtw_old.py ${query_dir}/${query_file} ${utt_dir}/${utt_file}
	done
done

et=`date '+%Y-%m-%d %H:%M:%S'`
echo 'end at '$et
