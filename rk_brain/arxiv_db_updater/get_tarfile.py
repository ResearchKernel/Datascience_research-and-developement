import boto3 
s3 = boto3.client('s3')
BUCKET = 'arxivoverload-developement'
s3.download_file(BUCKET, i, 'data/tar/data.tar')