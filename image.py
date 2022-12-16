import os, json
import requests, io

from dotenv import load_dotenv
load_dotenv()
import boto3
# from botocore.config import Config

regions = ['ams3', 'nyc3', 'sgp1', 'sfo2']
def space_connect():
    session = boto3.session.Session()
    client = session.client('s3',
                        region_name='nyc3',
                        # endpoint_url='https://shein-images.sgp1.digitaloceanspaces.com',
                        endpoint_url='https://sgp1.digitaloceanspaces.com',
                        aws_access_key_id=os.getenv('SPACES_KEY'),
                        aws_secret_access_key=os.getenv('SPACES_SECRET'))
    return client

# def list_spaces():
#     available_spaces = [[], [], [], []]
#     b = -1
#     if b < 5:
#         for i in regions:
#             b += 1
#             # print("checking servers in " + i)
#             response = space_connect(i).list_buckets()
#             buckets = [bucket['Name'] for bucket in response['Buckets']]
#             for space_num in buckets:
#                 # print(space_num)
#                 available_spaces[b].append(str(space_num))

#     return available_spaces

def list_spaces_in(region):
    spaces_region = []
    if region.lower() in regions:
        response = space_connect().list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        for space_num in buckets:
            spaces_region.append(space_num)

        return spaces_region
    else:
        return "Error: Possibly Invalid Region"

def list_files(space_name, dir):
    #take argument for particular directory file listing
    #Put a try:
    r = space_connect().list_objects(Bucket=space_name)
    files = r.get('Contents')
    i = 0
    p = str(files)

    if p == "None":
        print("No Data available")
    else:
        for file in files:
            if len(file) > 0:
                i += 1
            else:
                continue
            file_detect = file['Key']
            if file_detect[-1:] == '/':
                file_type = "Folder"
            else:
                file_type = "File"
            print("Object: ")
            print("     Name: " + file['Key'] + " [" + file_type + "]")
            print("     Size: " + str(file['Size']) + " bytes")
            date, time = str(file['LastModified']).split(" ")
            print("     Last Modified: ")
            print("             Date: " + date)
            timeh, useless = time.split(".")
            print("             Time: " + timeh)

def download_file(space_name, file_name):
    s3 = space_connect()
    local_path = file_name #mistake i made so had to fix here :)
    try:
        s3.download_file(space_name, file_name, local_path)
        print("Data written to ->" + local_path)
    except:
        print("Error: Maybe file does not exist, or check the path you are saving to ")
        print("Usage: download file_to_download_from_the_space file_name_to_save_on_disk")
        print("Ex: download mytest-from-cloud docs.txt")
    #USAGE: download_file('space_name', 'nyc3', 'file_in_space.txt', 'file.txt')


def create_space(name, region):
    region = region.lower()
    if region in regions:
        try:
            client = space_connect()
            client.create_bucket(Bucket=str(name))
            print("Success")
            print("https://" + name + "." + region + ".digitaloceanspaces.com is now available")
        except:
            print("Error: Maybe Inavlid Name")

def upload_file(URL, upload_name):
    s3 = space_connect()
    try:
        # s3.upload_file(local_file, space_name, upload_name)
        response = requests.get(URL)
        image_bytes = io.BytesIO(response.content)
        s3.put_object(Body=image_bytes, Bucket='shein-images', Key=upload_name, ContentType='image/webp')
        message = "Success"
        return message
        # pass
    except Exception as e:
        message = "Error occured. Check Space name, etc"
    return message
