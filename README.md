# Description
Implemented a fault-tolerant 2-phase distributed commit(2PC) protocol and use controlled and randomly injected failures to study how the 2PC protocol handles node crashes. We have Assumed one transaction coordinator (TC) and at least two participants in the 2PC protocol. Similar to the previous projects, we use multiple processes to emulate multiple nodes. Each node (both the TC and the participants) devises a time-out mechanism when no response is received and transits to either the abort or commit state

## Before executing the command, please read the ReadMe file thoroughly.

## Execution Steps 

Open Four Separate terminal and execute below command. (Make sure in cd directory is same to execute command) 
>>>First run TC then after Server 1 , Server 2 and Client.

## Transaction Controller
Run Below command for TC in 1st terminal.
>>>> python TransactionController.py
    
The Transaction controller controls all the transaction that happen throughout the system. 
The logging is set up to log the messages to the tc.log file.

## Server 1
Run Below command for server 1 in 2nd terminal.
>>>python Server1.py 
These server 1 is main server in which client request will be processed.

## Server 2
Run Below command for server 2 in 3rd terminal.
>>>python Server2.py 
These server 2 is main server in which client request will be processed.

## Client
Run Below command for client in 4th terminal.
>>>python client.py
    
The client file is mainly used to send request to main server (Here request will go to Transaction Controller).
There are four different scenarios in the client code, and in order to run each one, you need to remove the comment symbol from the corresponding section in the client.py file before running the code.

### Scenario 1: TC fail before Prepare request.(All Abort)
For this particular scenario, you need to remove a specific comment from the client code and then run it. After running the code, please check the terminal output as well as the log files for all three TC , Server 1 and Server 2.

### Scenario 2: Node fail: TC does not receive “Yes” from a node. (All Abort)
For this particular scenario, you need to remove a specific comment from the client code and then run it. After running the code, please check the terminal output as well as the log files for all three TC , Server 1 and Server 2.

### Scenario 3: TC fail: TC fails after sending commit to one server.(All Commit)
In this scenario, you need to remove a particular comment from the client code and run it. After running the code, you should check the Transaction Controller (TC) terminal because the TC fails once it sends the Commit request to one of the nodes. Therefore, you need to restart the TC by opening a new terminal and running it again. After that, you should check the output in both Server 1 and Server 2 terminals, as well as the log files for all three: the TC, Server 1, and Server 2.

### Scenario 4: Node Fail: Server 2 fails after sending “Yes” to TC. (All Commit)

In this scenario, you need to remove a particular comment from the client code and run it. After running the code, you should check the Server 2 terminal because the its fails after sending “Yes” to TC. Therefore, you need to restart the Server 2 by opening a new terminal and running it again. After that, you should check the output in both Server 1 and Server 2 terminals, as well as the log files for all three: the TC, Server 1, and Server 2.
