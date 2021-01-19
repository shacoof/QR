from gcalendar import readCalender
from QRUtils import *
from gmail import *
from icecream import ic


def main():

    runName = getUserInput("runName","t1")
    batchSize = getUserInput("batchSize","5")
    cmd = getUserInput("Command : [e]mail,[c]alendar,[B]oth","Both")
    creds = initAPI()
    if cmd == "e" or cmd == "B":
        readGmail(creds=creds,runName=runName, batchSize=batchSize)
    elif cmd == "c" or cmd == "B":
        readCalender(creds=creds)
    
    
if __name__ == '__main__':
    main()