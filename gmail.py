from __future__ import print_function
import sys, traceback
from datetime import date
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from shacoof.misc_utils import createCSV
from  shacoof.SQLiteUtil import create_connection,create_table
from sqlite3 import Error

from six import MAXSIZE

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    readEmails(service)



def readEmails(service, user_id='me'):
    print ("start readEmails")
    page_token = None
    res=[]
    i=0
    while True:  #page token == 
        threadList = service.users().threads().list(userId=user_id,maxResults=500,pageToken=page_token).execute()
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
                res += [[_d,_from,_to]]
        page_token = threadList.get('nextPageToken') # if not empty will be used to bring the next round
        if not page_token:
            break

    full_db_name = os.path.join(os.getcwd(), 'QR-DB.db')
    conn = create_connection(full_db_name)
    if conn is None:
        print("Error! cannot create the database connection.")
    email_table_name = "QR_GMAIL "
    sql_create_tbl = "CREATE TABLE IF NOT EXISTS "+ email_table_name +"(EMAIL_DATE TEXT, SENDER TEXT, RECIEVER TEXT);"
    print (sql_create_tbl)
    create_table(conn,sql_create_tbl)
    print("table created")
    try:
        c = conn.cursor()
        cmd = 'INSERT INTO '+email_table_name+' VALUES (?,?,?)'
        print(cmd)
        c.executemany (cmd,res)
        conn.commit()
        conn.close()
    except Error as e:        
        print(traceback.format_exc())

    print('done')

if __name__ == '__main__':
    main()

