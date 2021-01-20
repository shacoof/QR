from __future__ import print_function
import sys, traceback
from datetime import date
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from shacoof.misc_utils import createCSV
from shacoof.SQLiteUtil import create_connection,create_table
from sqlite3 import Error
from QRUtils import dbInsert, initAPI

def readGmail(creds,user_id='me',runName="temp", batchSize=10):

    service = build('gmail', 'v1', credentials=creds)
    page_token = None
    i=0

    while True:  #page token
        res=[]
        threadList = service.users().threads().list(userId=user_id,maxResults=batchSize,pageToken=page_token).execute()
        for thread in threadList.get('threads'): #loop through all threads
            i+=1
            print("email ",i) 
            tdata = service.users().threads().get(userId=user_id, id=thread['id'], format="metadata").execute()
            for msg in tdata['messages']:
                _d      = ''
                _from   = ''
                _to     = ''
                for header in  msg['payload']['headers']: #extracting the fields we are interested in 
                    if header['name'] == 'Date':
                        _d = header['value']
                    elif header['name'] == 'From':
                        _from = header['value']
                    elif header['name'] == 'To':
                        _to = header['value']
                res += [[runName,_d,_from,_to]]
        dbInsert("QR_GMAIL",res)
        page_token = threadList.get('nextPageToken') # if not empty will be used to bring the next round
        if not page_token:
            break




