base=/home/coast/project/QbE/BUT/PhnRec/PHN_CZ_SPDAT_LCRC_N1500/SWS2013
query_dir=${base}/posteriorgram/query_dev
utt_dir=${base}/posteriorgram/utt_tmp
ret_dir=${base}/ret/dev

st=`date '+%Y-%m-%d %H:%M:%S'`
echo 'start at '$st

python dtw_mul_1.py $query_dir $utt_dir $ret_dir
et=`date '+%Y-%m-%d %H:%M:%S'`
echo 'end at '$et
