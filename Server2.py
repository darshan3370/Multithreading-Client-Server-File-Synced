#PROJECT - 3(CSE-5306-001-DISTRIBUTED SYSTEMS)

#import LIB

import time
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread, Event
import time
import threading
import sys

StopExitEvent = Event() #define Event class from the threading module

 
class Server2: #called class server 1
    def __init__(self):
        print(">>Inside the Server 2..............") #print while execute server 1
        self.jsonobj = {"6":100,"8":100,"10":100} #define key and ammount number
        self.lock = threading.Lock() #used to synchronize access to the jsonobj dictionary.
        self.file = None #open file 
        self.isRec = None #is in recovery mode or not.
        self.Tc = None #call TC
        self.preparemsgjson = {} #used to store prepare messages.
        self.abortmsgjson = {}  #used to store abort messages.
        self.commitmsgjson={} #used to store commit messages

    #define the recovery of the server 2
    def recoveryOf_Server(self):
        self.file = open("server2.log", "r") #read the server 2 file for the log 
        last_line3 = [] #creates an empty list
        for line in (self.file.readlines()[-3:]):
            if not line.isspace(): # checks if the line is not a blank line.
                last_line3.append(line) #append with that line
        self.file.close()
        print(last_line3)
        if len(last_line3) > 0 and len(last_line3)==3: #check lines in the 'last_line3' list
            a_3 = last_line3[2].split(" ")
            if a_3[0]=="Commit": #commit
                print(">>All Done ")
            elif a_3[0]=="Yes":
                print(a_3[2],a_3[3],int(a_3[4]),a_3[1])
                self.commitmsgFile(a_3[2],a_3[3],int(a_3[4]),a_3[1])
    
    #assign the Key for diffrent Sceinario that all key we use with diffrent 
    def assignKey(self, key):
        if int(key) == 3:
            return True
        elif int(key) == 4:
            return True
        elif int(key) == 1:
            return True
        elif int(key) ==2:
            return False
        elif int(key) == 6:
            return True
        elif int(key) == 8:
            return True
        elif int(key) == 10:
            return True


    #commit msg method 
    def commitmsg(self,key,value,transaction_ID,actn):
        if actn == "transfer" and transaction_ID not in self.commitmsgjson: #check if the action is a transfer and the transaction ID is not in the list.
            if int(key)==10: #if key was 10 then fail TC 
                b=2/0
            self.jsonobj[key] = int(self.jsonobj[key])+int(value) # update the value associated with the key and add value
            print(">>>The Commit Transaction ID "+str(transaction_ID))

            self.commitmsgjson[transaction_ID]=True
            self.file = open("server2.log", "a+") #open server 2 log file
            self.file.write("\n>>Commit Transaction ID......" + str(transaction_ID))
            self.lock.release()
            self.file.flush() #flush the write buffer to make sure the message is written to the file
            self.file.close() # close the log file 
            print(">>>Updated value at " + str(key) + " is " + str(self.jsonobj[key])) #print the upfated value
        return True

    #commit msg in file
    def commitmsgFile(self,key,value,transaction_ID,actn): #check if the action is a transfer and the transaction ID is not in the list.
        if actn == "transfer" and transaction_ID not in self.commitmsgjson:
            self.jsonobj[key] = int(self.jsonobj[key]) + int(value) # update the value associated with the key and add value
            print(">>>The Commit Transaction ID " + str(transaction_ID))
            self.commitmsgjson[transaction_ID] = True
            self.file = open("server2.log", "a+") #open file server2 log
            self.file.write("\n>>>The Commit Transaction ID" + str(transaction_ID))
            #self.lock.release()
            self.file.flush() # flush the write buffer to make sure the message is written to the file
            self.file.close() # close the log files
            print(">>>Updated value at " + str(key) + " is " + str(self.jsonobj[key]))

    #abort the msg 
    def abortmsg(self, transaction_ID):
        self.file = open("server2.log", "a+") #open server 2 log file
        self.file.write("\n>>>Abort.... ") #print abort 
        self.file.flush() # flush the write buffer to make sure the message is written to the file
        self.abortmsgjson[transaction_ID] = 1
        self.lock.release() # release the lock to allow other threads to access the shared resource
        print(">>>Transaction Id Number"+str(transaction_ID)+" is Aborted...........")
        return True
    
    
   #time method 
    def timeFun(self,transaction_ID):
        n = 0
        while n <= 10:
            n += 1
            print("Waiting sec ... " + str(n)) #wait for the 10 sec after perform other task 
            time.sleep(1)
        if transaction_ID not in self.preparemsgjson and transaction_ID not in self.abortmsgjson:
            print(">>>Start Abort......")
            self.abortmsgjson[transaction_ID] = 1
            self.Tc.abortmsg(transaction_ID)

        #request msg method 
    def requestmsg(self, reqName, key, value, transaction_ID):
        print(">>>Inside request.....") # Print a message to indicate that this function has been called
        self.lock.acquire() # Acquire the lock
        self.file = open('server2.log', 'a+') #Append the request details to the server2.log file
        self.file.write("Request " + str(transaction_ID) + " " + reqName + " " + key + " " + value)
        self.file.close()
        acThread = Thread(target=self.timeFun, args=(transaction_ID,)) # Start a new thread to keep track of the transaction time
        acThread.start()
        return True

     #prepare msg method
    def preparemsg(self, reqName, key, value, transaction_ID):
        self.preparemsgjson[transaction_ID] = 1
        self.file = open('server2.log', 'a+') #open file server 2 log
        self.file.write("\nPrepare " + str(transaction_ID))
        print(">>>Prepare " + reqName + " " + key + " " + value) #preaper
        ac = Thread(target=self.giveResponce, args=(reqName, key, value, transaction_ID)) # Start a new thread to keep track of the transaction time
        ac.start()
        return True

      #give responce method 
    def giveResponce(self, reqName, key, value, transaction_ID):
        flag = self.assignKey(key) #calling the assignKey method to flag. 
        self.file = open('server2.log', 'a+') #open server 2
        if flag and transaction_ID not in self.abortmsgjson: #if both flg and tran id in abort dic then go furthur
            self.file.write("\nYes " + reqName + " " + key + " " + value + " " + str(transaction_ID))
            self.file.close()
            print(">>>Request Accepted Responce...")
            self.Tc.reqresponse(True, "servertwo" + str(transaction_ID)) #thread start in servertwo
        else:
            self.file.write("\nNo " + reqName + " " + key + " " + value + " " + str(transaction_ID))
            self.file.close()
            print(">>>Request Not Accepted (Responce not clear) ...")
            self.Tc.reqresponse(False, "servertwo" + str(transaction_ID)) #thread start in servertwo

if __name__ == '__main__':
    try:

        ser2 = Server2()
        ser2.recoveryOf_Server()

        server = SimpleXMLRPCServer(("localhost", 8082))
        print("*********** Server 2 listening on Port 8082 ***********")
        client = xmlrpc.client.ServerProxy("http://localhost:8083") #XML-RPC client that connects to the server running on port 8083 of the localhost.
        ser2.Tc = client
        server.register_instance(ser2)
        server.serve_forever()

    except Exception:
        print("!!!!!!Exception in Main!!!!!")
