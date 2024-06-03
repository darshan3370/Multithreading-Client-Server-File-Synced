#PROJECT - 3(CSE-5306-001-DISTRIBUTED SYSTEMS)

#import LIB

import xmlrpc.client

 
def main():
    print(">>>>>>Request Sent to TC and Server's....... ")
    client = xmlrpc.client.ServerProxy("http://localhost:8083")

    #Scenario 1.....................................
    # TC goes down before prepare message (TC fail) 
    #result_tc = client.transfer("3","1",10)
    #print(str(result_tc) + "\n")

    #Scenario 2.....................................
    #if TC does not receive yes from a node, it should abort transaction (Node Fail)
    #result_tc = client.transfer("1","3",10)
    #print(str(result_tc) + "\n")
    
    #Scenario 3..................................... (TC Fail)
    #result_tc = client.transfer("7","8",10)
    #print(str(result_tc) + "\n")

    #Scenario 4.....................................
    #Both say Yes but Server2 fails after Sending Yes to TC  (Node Fail)
    #result_tc = client.transfer("9","10",10)
    #print(str(result_tc) + "\n")


    # both say no .. tends to abort
    #result_tc = client.transfer("4","2",10)
   
    #both say Yes .. tends to commit
    #result_tc = client.transfer("5","6",10)
    
    #one of the server says no to change 2
    #result_tc = client.transfer("2","4",10)

   
if __name__ == '__main__':
    main()
