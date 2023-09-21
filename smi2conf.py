# using openbabel to convert smi to inchikey
from openbabel import openbabel
import tempfile
import subprocess
import argparse
import shutil
# import boto3
# from botocore.exceptions import ClientError
import os

BUCKET_NAME = "s3://crest-xyz"
FOLDER_NAME = "mari"

#boto3 credentials
#os.environ["AWS_ACCESS_KEY_ID"] = ""
#os.environ["AWS_SECRET_ACCESS_KEY"] = ""

parser = argparse.ArgumentParser()
parser.add_argument('--smi', type=str, default='CC(=O)Oc1ccccc1C(=O)O')
args = parser.parse_args()

# def upload_file(file_name, bucket, object_name=None):
#     """Upload a file to an S3 bucket

#     :param file_name: File to upload
#     :param bucket: Bucket to upload to
#     :param object_name: S3 object name. If not specified then file_name is used
#     :return: True if file was uploaded, else False
#     """

#     # If S3 object_name was not specified, use file_name
#     if object_name is None:
#         object_name = os.path.basename(file_name)

#     # Upload the file
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as e:
#         return False
#     return True

def smi2inchikey(smi):
    """convert smi to inchikey
    
    surprisingly this function is much faster than the openbabel CLI call"""
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("smi", "inchikey")
    mol = openbabel.OBMol()
    obConversion.ReadString(mol, smi)
    inchikey = obConversion.WriteString(mol)
    return inchikey.strip()

def smi2crest_run(smi):
    label = smi2inchikey(smi)
    with tempfile.TemporaryDirectory() as tmpdirname:
        subprocess.run(["obabel", f"-:{smi}", "-O", f"{tmpdirname}/init.xyz", "--gen3d"])
        #subprocess.run(["cat", f"{tmpdirname}/init.xyz"])
        subprocess.run(["crest", f"{tmpdirname}/init.xyz"], cwd=tmpdirname)
        shutil.copyfile(f"{tmpdirname}/crest_conformers.xyz", f"{label}.xyz")
        #upload_file(f"{label}.xyz", BUCKET_NAME, f"{FOLDER_NAME}/{label}.xyz")

def main():
    smi2crest_run(args.smi)

if __name__ == "__main__":
    main()