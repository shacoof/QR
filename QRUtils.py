from logging import exception
from shacoof.misc_utils import createCSV
from shacoof.SQLiteUtil import create_connection,create_table
from sqlite3 import Error
import sys, traceback
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle


def initAPI():


    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/gmail.readonly"]
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
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            try:
                creds = flow.run_local_server(port=0)
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")
            
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def dbInsert(tblName,tblData):
    full_db_name = os.path.join(os.getcwd(), 'QR-DB.db')
    conn = create_connection(full_db_name)
    if conn is None:
        print("Error! cannot create the database connection.")
    #email_table_name = "QR_GMAIL"
#    sql_create_tbl = "CREATE TABLE IF NOT EXISTS "+ email_table_name +"(RUN TEXT, EMAIL_DATE TEXT, SENDER TEXT, RECIEVER TEXT);"
#    print (sql_create_tbl)
#    create_table(conn,sql_create_tbl)
#    print("table created")
    try:        
        #We deduce the number of fields in the table based on the number of items in each row
        fields=''
        for i in tblData[0]:
            fields+="?,"
        fields=fields[:len(fields)-1] #remove the redundant , (comma)
        c = conn.cursor()
        cmd = 'INSERT INTO '+tblName+' VALUES ('+fields+')'
        print(cmd)
        c.executemany (cmd,tblData)
        conn.commit()
        conn.close()
        print('Inserted',len(tblData)," Rows !")
    except Error as e:        
        print(traceback.format_exc())

    

def getUserInput(name,defaultVal):
    val = defaultVal
    print("Enter "+name+" or exit ["+defaultVal+"]")
    val1 = input()
    if val1:
        val = val1
    if val == "exit":
        sys.exit()

    return val