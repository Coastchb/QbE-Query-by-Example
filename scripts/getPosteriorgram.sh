if [ $# != 3 ]; then
	echo '. getPosteriorgram.sh database system audioListFileName
		eg: getPosteriorgram.sh SWS2013 PH_EN_TIMIT_LCRC_N500 query_dev.scp'
else
	phnRecDir='../BUT/PhnRec/'
	HListPath='../BUT/phnrec_tscripts/htk/bin.cpu/HList'
	database=$1
	path_to_system=${phnRecDir}$2
	audioListFileName=$3

	python getPosteriorgram.py $phnRecDir $HListPath $database $path_to_system $audioListFileName
fi
