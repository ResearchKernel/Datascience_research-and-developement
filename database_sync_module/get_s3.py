import os
def get_s3_to_local():
    os.system("aws s3 cp s3://s3-to-ebs-data-transfer-example/sample.log pdf/")
