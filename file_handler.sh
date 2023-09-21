export BUCKET_NAME=s3://bucket-name
export FOLDER_NAME=folder-name

#conda run -n crest python smi2conf.py -smi $1
python smi2conf.py --smi $1

