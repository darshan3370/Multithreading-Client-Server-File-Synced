#PROJECT - 3(CSE-5306-001-DISTRIBUTED SYSTEMS)

#import LIB

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import time
from threading import Thread, Event


class Leader:
    def __init__(self):
        self.participants = [] # store the participants.
        self.participant_add = [] #used to store addresses of the participants.
        self.file = None #store the name of a file or open particular file 
        self.transaction_ID = 0 #used to store a transaction ID of the server1 and 2 in TC.
        self.isRec = 0  #is in recovery mode or not.
        self.flag = False 
        self.jsonres = {}
        self.abortmsgList={} #used to store abort messages.
        self.commitmsgList={} #used to store commit messages.
        
        
    #Method of the Recover of the Server 1 and 2
    def recoveryOf_Server(self):
        self.file = open("tc.log", "r") #read the tc.log file from the folder
        last_line3 = [] 
        for line in (self.file.readlines()[-5:]): #read the line from tc.log
            if not line.isspace():
                last_line3.append(line)    #append the line             

        self.file.close()
        print(last_line3) 
        if len(last_line3)>0:
            a_3=last_line3[2].split(" ") #split the line with array
            if a_3[0]== "Commit":  #commit the statement 
                a_2=last_line3[1].split(" ")
                if a_2[0] == "Commit":   #commit the statement 
                    print(">>> All Done..... ")
                else:
                    a_1=last_line3[1].split(" ") 
                    if a_1[0] == "Prepare": #prepare the statement 
                        transaction_ID=int(a_1[1])
                        actn=a_1[2]
                        k2 = a_1[6]
                        value = int(a_1[9])
                        self.participants[1].commitmsg(k2, str(value), transaction_ID, actn)
                        self.file = open("tc.log", "a+") #open the file

                        self.file.write("\n Commit " + str(transaction_ID) + " transfer to " + k2 + " " + str(value) + " server 2 \n")
                        print("\n Commit " + str(transaction_ID) + " transfer to " + k2 + " " + str(value) + " server 2 ")
                        self.file.close()
                        self.commitmsgList[transaction_ID] = True
                    else:
                        print(">>>No action")

    #time function to start and end time 
    def timeFun(self):
        n = 0
        while n <= 10:
            n += 1
            print(">>>Waiting Sec ... " + str(n)) #waiting till 10 sec if no one get reply
            time.sleep(1)

    #transfer method 
    def transfer(self, transferFrm_acc,transferTo_acc, transfer_amt): #three arguments passed to self.put are transferFrm_acc, transferTo_acc, and transfer_amt
        newTcThread=Thread(target=self.put,args=(transferFrm_acc,transferTo_acc, transfer_amt)) #funds between two accounts transfer 
        newTcThread.start() #thread start
        return True

    #put method 
    def put(self, k1,k2, value): #passing the three argument key1 , key 2 and value
        print(">>>Put all Transaction Inside(TC) ..........")
        self.file = open("tc.log", "a+") #open tc.log file 
        self.transaction_ID = self.transaction_ID + 1
        self.file.write("\n Request " + str(self.transaction_ID) + " transfer from " + k1 + " to " +k2+" of value "+str(value) + "\n") #print the repeart request 

        print("\nRequest " + str(self.transaction_ID) + " transfer from " + k1 + " to " +k2+" of value "+str(value) + "\n")
        count = 0

        self.participants[0].requestmsg("transfer", k1, str(value), self.transaction_ID) #participant with the treansfer key 1
        self.participants[1].requestmsg("transfer", k2, str(value), self.transaction_ID) #participant with the treansfer key 2

        if int(k1) == 3: #if key was 3 
            time.sleep(20) # sleep for 20 sec

        print("\nPrepare " + str(self.transaction_ID) + " transfer from " + k1 + " to " +k2+" of value "+str(value) + "\n")  #prepre
        self.file.write( "\nPrepare " + str(self.transaction_ID) + " transfer from " + k1 + " to " + k2 + " of value " + str(value) + "\n") #prepre 
        self.file.close()
        time1thread=Thread(target=self.participants[0].preparemsg,args=("transfer", k1, str(value), self.transaction_ID,)) #thread 1 start for key 1 
        time1thread.start()
        time2thread=Thread(target=self.participants[1].preparemsg,args=("transfer", k2, str(value), self.transaction_ID,)) #thread 2 start and key 2
        time2thread.start()

        self.timeFun() #call the time method here for server 1 and 2 
        server1 = False
        server2 = False

        key_forServer1 = 'serverone' + str(self.transaction_ID)
        key_forServer2 = 'servertwo' + str(self.transaction_ID)
        if key_forServer1 in self.jsonres: #server 1 in jsonres dic
            server1 = self.jsonres[key_forServer1]
        if key_forServer2 in self.jsonres:  #server 2 in jsonres dic
            server2 = self.jsonres[key_forServer2]

        if server1 and server2:
            print(">>>Start Commit " + str(self.transaction_ID) +"\n") #print the commit 
            self.commitmsg(k1,k2,value,self.transaction_ID,"transfer")
        else:
            self.abortmsg(self.transaction_ID)   # abort scenario if not commit
            self.file = open("tc.log", "a+") #open file tc.log
            self.file.write("\nAbort " + str(self.transaction_ID) + "\n") #write abort in file 
            self.file.close()
            return "Abort"

        return "Function Operation Done.........."
    
    
    #commitmsg method 
    def commitmsg(self,k1,k2,value,transaction_ID,actn): #define k1, k2, value, transaction_ID, and actn as parameters.
        if transaction_ID not in self.commitmsgList: # check transaction ID is not already in the commitmsgList.
            print("Calling all participants to commit")
            self.participants[0].commitmsg(k1,value,transaction_ID,actn)
            self.file = open("tc.log", "a+")
            self.file.write("\nCommit " + str(self.transaction_ID) + " transfer from "+ k1 + " " + str(value) + " server1 \n") #commit with key 1 in server 1
            self.file.close()
            print("\n Commit " + str(self.transaction_ID) + " transfer from " + k1 + " " + str(value) + " server1 ")
            if int(k1)==7: #tc fail when the scenario 3 work
                b=2/0

            self.file = open("tc.log", "a+") #open file 
            self.file.write("\nCommit " + str(self.transaction_ID) + " transfer to "+ k2 + " " + str(value) + " server2 \n") #commit with key 2 in server 2
            print("\nCommit " + str(self.transaction_ID) + " transfer to "+ k2 + " " + str(value) + " server2 ")
            self.file.close()
            self.participants[1].commitmsg(k2, value, transaction_ID, actn)
            self.commitmsgList[transaction_ID]=True #line adds the transaction_ID to the commitmsgList with a value of True.
        return True
    
    
    #abort msg method 
    def abortmsg(self, transaction_ID):

        if transaction_ID not in self.abortmsgList: #Checks the transaction_ID is not already in the abortmsgList.
            print(">>>Calling all participants to abort transactions.....") #calling to all participant for abort
            for item in self.participants: 
                item.abortmsg(transaction_ID)
            self.abortmsgList[transaction_ID]=True
        return True

    #request response method 
    def reqresponse(self, value, transaction_ID):
        print("Response from" + str(value)) #response print
        self.jsonres[transaction_ID] = value  #transaction iD responce in jsoneres dic 
        return True

#main methid
if __name__ == '__main__':
    l1 = Leader() #creates instance of the Leader class.

    participant_add = ["http://localhost:8081", "http://localhost:8082"] #server 1 and server 2 port
    for add in participant_add:
        try:
            client = xmlrpc.client.ServerProxy(add) #creates an XML-RPC client object for each participant server address and 
                                                     #adds it to the participants list of the Leader object.
            print(client)
        except Exception:
            print("Exception!!!!!!...... ")

        l1.participants.append(client)
    l1.recoveryOf_Server() # recover any pending transactions.
    try:
        server = SimpleXMLRPCServer(("localhost", 8083)) #tc run on port 8083
        print("TC listening on 8083")
        server.register_instance(l1)
        server.serve_forever() #starts the TC server and serves incoming XML-RPC requests indefinitely.
    except Exception:
        print("Except!!!!.........")
