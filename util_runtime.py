import re
import os
import csv
import json
import requests

idRegex = re.compile(r'.*file/d/|/view.*|.*id=')

ids = {}
with open('index.csv', 'r') as f:
	reader = csv.reader(f)	
	for row in reader:
		ids[row[0]] = idRegex.sub('', row[1])

def pull(*names):
	for name in names:
		if not os.path.exists(name):
			download_file_from_google_drive(ids[name], name)
	return None

# All codes below are taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
