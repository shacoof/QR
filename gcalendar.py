from __future__ import print_function
from QRUtils import dbInsert
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import progressbar

def readCalender(creds,runName="temp"):

    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    res=[]
    page_token = None    
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    while True:        
        events = service.events().list(calendarId='primary', 
                                        pageToken=page_token,
                                        maxResults=1000,
                                        singleEvents=True,
                                        timeMax = now).execute()
        #bar = progressbar.ProgressBar(max_value=len(events['items']))   
        #i=0;     
        for event in events['items']:
            #i+=1
            #bar.update(i)
            res+=[[     
                runName,
                event.get('summary',' '), #if meeting is w/o subject summary doesn't exist
                event['start'].get('dateTime'),
                event['end'].get('dateTime'),
                event['organizer'].get('email'),
                len(event.get('attendees',[])) #if no attendees then return empty list
                ]]
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    dbInsert("QR_CALENDAR",res)