"""
Cloud Storage Infrastructure

using MinIO (S3-compatible open source storage)
"""

import json

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create MinIO client and resource (S3-compatible)
s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    region_name='us-east-1'  # MinIO requires a region
)
s3_resource = boto3.resource(
    's3',
    endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    region_name='us-east-1'
)
AspiringStorageBucket = os.getenv("MINIO_BUCKET_NAME")

print("Starting cloud import");

#
# The following are the base ITEM key, value APIs
#    Using this key,value storage is built a
#    user storage metaphor
#


# store a user item
# returns True/False
def putItem(path, filedata, bucket_name=None):
    if bucket_name is None:
        bucket_name = AspiringStorageBucket
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=path,
            Body=filedata
        )
        return True
    except ClientError as e:
        print(f"Error putting item: {e}")
        return False

# get a user item
# returns data/None
def getItem(path, bucket_name=None):
    if bucket_name is None:
        bucket_name = AspiringStorageBucket
    try:
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=path
        )
        return response['Body'].read().decode('utf-8')
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return None
        print(f"Error getting item: {e}")
        return None

# does item exist
# returns boolean
def existsItem(path, bucket_name=None):
    if bucket_name is None:
        bucket_name = AspiringStorageBucket
    try:
        s3_client.head_object(
            Bucket=bucket_name,
            Key=path
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey' or e.response['Error']['Code'] == '404':
            return False
        print(f"Error checking item existence: {e}")
        return False


# delete a user item
# returns True/False
def deleteItem(path, bucket_name=None):
    if bucket_name is None:
        bucket_name = AspiringStorageBucket
    try:
        s3_client.delete_object(
            Bucket=bucket_name,
            Key=path
        )
        return True
    except ClientError as e:
        print(f"Error deleting item: {e}")
        return False

#  The following are helpers to implement the API

def createBucket(bucketname):
    try:
        s3_client.create_bucket(Bucket=bucketname)
        return s3_resource.Bucket(bucketname)
    except ClientError as e:
        print(f"Error creating bucket: {e}")
        return None

def getBucket(bucketname):
    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucketname)
        return s3_resource.Bucket(bucketname)
    except ClientError as e:
        print(f"Error getting bucket: {e}")
        return None

#
#
#  The following are user file abstraction
#    built using a key-value storage
#
#  The abstraction is simple
#  The path to the file is the key
#  The metadata on the key indicates if it is a file or directory
#  If it is a directory, then, it contains the list of files as the value
#  which gets updated when files get added or deleted 
#
#  Note that the user is embedded into the filesystem path
#
#  path itself is a stringified json list
#
#

# path manipulation apis

# first define dir, and file classes

class File:
    def __init__(self,name,data):
        self.fname = name
        self.data = data

class Directory:
    def __init__(self,name,filelist):
        self.fname = name
        self.files = [File(i,"") for i in filelist]


def pathToString(path):
    return json.dumps(path)

# path is a list
# returns True/False
def createDir(path):
    # check if dir exists, if so fail
    spath = pathToString(path)
    data = getItem(spath)
    if (data != None):
        print("dir exists");
        return False
    # create the dir file
    dirdata = {}
    dirdata["data"] = json.dumps([])
    dirdata["path"] = path
    dirdata["type"] = "dir"
    if not (putItem(spath, json.dumps(dirdata))):
        print("putitem failed");
        return False
    #print("createDir passed"    );
    return True
    
    
def deleteDir(path):
    # not implemented yet
    pass


# path is list, return python file object
def getFileRaw(path):
    pathstr = pathToString(path)
    try:
        response = s3_client.get_object(
            Bucket=AspiringStorageBucket,
            Key=pathstr
        )
        return response['Body'].read()
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return None
        print(f"Error reading file: {e}")
        return None

# path is list, returns directory object or file object as the case
# may be
def getFile(path):
    data = getFileRaw(path)
    print("getfile",data);
    if data == None:
        return None

    data_json = json.loads(data.decode('utf-8'))

    if data_json["type"] == "dir":
        fileslist = json.loads(data_json["data"])
        fname = path[len(path)-1]
        fileobj = Directory(fname, fileslist)
        return fileobj
    elif data_json["type"] == "file":
        fname = path[len(path)-1]
        fileobj = File(fname, data_json["data"])
        return fileobj
    else:
        return None

##
## path is list, data is a string
##
# In createFile function
def createFile(path, data):
    if len(path) <= 1:
        print("path too short")
        return False

    ppath = path[:-1]    
    parent_data_raw = getFileRaw(ppath)
    if parent_data_raw == None:
        print("parent dir does not exist")
        return False

    parentdata = json.loads(parent_data_raw.decode('utf-8'))

    spath = pathToString(path)
    if getItem(spath) != None:
        print("file exists")
        return False

    filedata = {}
    filedata["data"] = data
    filedata["path"] = path
    filedata["type"] = "file"
    if (not putItem(spath, json.dumps(filedata))):
        print("putfile failed")
        return False

    fname = path[len(path)-1]
    fileslist = json.loads(parentdata["data"])
    fileslist.append(fname)
    parentdata["data"] = json.dumps(fileslist)    
    if (not putItem(pathToString(ppath), json.dumps(parentdata))):
        print("putdir failed")
        deleteFile(path)
        return False
    return True
    
##
## path is list, data is a string
##    
def updateFile(path, data):
    # file must exist
    filedata = getFileRaw(path)
    if (filedata == None):
        return False
    filedata["data"] = data
    if not putItem(pathToString(path), json.dumps(filedata)):
        return False
    return True

##
## path is list
##
def deleteFile(path):
    filedata = getFileRaw(path)
    if filedata == None or filedata["type"] != "file":
        print("file does not exist");
        return False
    #
    # update the parent directory first
    #
    ppath = path[:-1]    
    parentdata = getFileRaw(ppath)
    if parentdata == None:
        print("parent data failed"        );
        return False
    fileslist = json.loads(parentdata["data"])
    newlist = []
    fname = path[len(path)-1]
    for i in fileslist:
        if fname == i:
            pass
        else:
            newlist.append(i)
    parentdata["data"] = json.dumps(newlist)
    if (not putItem(pathToString(ppath), json.dumps(parentdata))):
        # this is unexpected, unwind !
        print("putdir failed"                        );
        return False
    # then delete the file
    if not deleteItem(pathToString(path)):
        print("delete file failed");
        return False
    return True


#### The following are unit tests

def unitTestItems():
    putItem("foobar1","test1")
    print(getItem("foobar1"))
    putItem("foobar2","test2")    
    print(getItem("foobar2"))
    deleteItem("foobar1")
    deleteItem("foobar2")
    print(getItem("foobar1")    )
    print(getItem("foobar2")    )

def unitTestItemsInBucket():
    bkt_name = "aspiring-pdf-files"
    putItem("foobar1","test1", bkt_name)
    print(existsItem("foobar1", bkt_name))
    print(getItem("foobar1", bkt_name))
    putItem("foobar2","test2", bkt_name)    
    print(existsItem("foobar2", bkt_name))
    print(getItem("foobar2", bkt_name))
    deleteItem("foobar1", bkt_name)
    deleteItem("foobar2", bkt_name)
    print(existsItem("foobar1", bkt_name))
    print(existsItem("foobar1", bkt_name))
    print(getItem("foobar1", bkt_name)    )
    print(getItem("foobar2", bkt_name)    )


def unitTestFiles():
    path = ["home","demo"]
    print("--create dir--");
    createDir(path)
    print(getFileRaw(path))
    fpath = path[:]
    fpath.append("fname")
    print("--del file--"    );
    deleteFile(fpath)
    print("--create file--"        );
    createFile(fpath, "FileData Test1")
    print(getFileRaw(fpath))
    print(getFileRaw(path))
    print(str(getFile(fpath)))
    print("--update file--"        );
    updateFile(fpath, "FileData Test2")
    print(getFileRaw(fpath))
    print(getFileRaw(path))
    print(str(getFile(fpath)))
    print("--create second file--");
    fpath2 = path[:]
    fpath2.append("fname2")    
    createFile(fpath2, "FileData2 Test1")
    print(getFileRaw(fpath2))
    print(getFileRaw(path))
    print(str(getFile(fpath2)))
    print("--update second file--"        );
    updateFile(fpath2, "FileData2 Test2")
    print(getFileRaw(fpath2))
    print(getFileRaw(path))
    print(str(getFile(fpath2)))
    print("--del file--"    );
    deleteFile(fpath)
    print(getFileRaw(path))
    print(str(getFile(fpath)))
    deleteFile(fpath2)
    print(getFileRaw(path))
    print(str(getFile(fpath)))
    
print("Cloud imported");

if __name__ == "__main__":
    # unit tests here
    #unitTestItems()
    #unitTestFiles()
    unitTestItemsInBucket()
