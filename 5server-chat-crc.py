#Joseph 103 CRC

import time, socket, sys

# Returns XOR of 'a' and 'b' 
# (both of same length) 


def xor(a, b): 

	# initialize result 
	result = [] 

	# Traverse all bits, if bits are 
	# same, then XOR is 0, else 1 
	for i in range(1, len(b)): 
		if a[i] == b[i]: 
			result.append('0') 
		else: 
			result.append('1') 

	return ''.join(result) 


# Performs Modulo-2 division 
def mod2div(dividend, divisor): 

	# Number of bits to be XORed at a time. 
	pick = len(divisor) 

	# Slicing the dividend to appropriate 
	# length for particular step 
	tmp = dividend[0: pick] 

	while pick < len(dividend): 

		if tmp[0] == '1': 

			# replace the dividend by the result 
			# of XOR and pull 1 bit down 
			tmp = xor(divisor, tmp) + dividend[pick] 

		else: # If leftmost bit is '0' 
			# If the leftmost bit of the dividend (or the 
			# part used in each step) is 0, the step cannot 
			# use the regular divisor; we need to use an 
			# all-0s divisor. 
			tmp = xor('0'*pick, tmp) + dividend[pick] 

		# increment pick to move further 
		pick += 1

	# For the last n bits, we have to carry it out 
	# normally as increased value of pick will cause 
	# Index Out of Bounds. 
	if tmp[0] == '1': 
		tmp = xor(divisor, tmp) 
	else: 
		tmp = xor('0'*pick, tmp) 

	checkword = tmp 
	return checkword 

# Function used at the sender side to encode 
# data by appending remainder of modular division 
# at the end of data. 


def decodeData(data, key): 

	l_key = len(key) 

	# Appends n-1 zeroes at end of data 
	appended_data = data + '0'*(l_key-1) 
	remainder = mod2div(appended_data, key) 

	# Append remainder in the original data 
	codeword = data + remainder 
	print("Remainder : ", remainder)
	return remainder




print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket()
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 1234
s.bind((host, port))
print(host, "(", ip, ")\n")
name = input(str("Enter your name: "))
           
s.listen(1)
print("\nWaiting for incoming connections...\n")
conn, addr = s.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")

s_name = conn.recv(1024)
s_name = s_name.decode()
print(s_name, "has connected to the chat room\nEnter [e] to exit chat room\n")
conn.send(name.encode())

while True:
    message = input(str("Me : "))
    if message == "[e]":
        message = "Left chat room!"
        conn.send(message.encode())
        print("\n")
        conn.close()
        break
    conn.send(message.encode())
    message = conn.recv(1024)
    message = message.decode()
    print(s_name, ":", message)
    test=decodeData(message,"1011")
    if (test=="000"):
    	print("No error")
    else:
    	print("error in message")







OUTPUT :

CASE 1 : WITHOUT ERROR

Client:
Welcome to Chat Room

Initialising....

csadmin-OptiPlex-3020 ( 127.0.1.1 )

Enter server address: 127.0.1.1

Enter your name: Client

Trying to connect to  127.0.1.1 ( 1234 )

Connected...

Server has joined the chat room
Enter [e] to exit chat room

Server : hi
Me : hello
Server : Left chat room!
Me : [e]


Server side:
Welcome to Chat Room

Initialising....

csadmin-OptiPlex-3020 ( 127.0.1.1 )

Enter your name: Server

Waiting for incoming connections...

Received connection from  127.0.0.1 ( 50694 )

Client has connected to the chat room
Enter [e] to exit chat room

Me : hi
Client : 0110100001100101011011000110110001101111011
Remainder :  000
No error
Me : [e]


CASE 2 : WITH ERROR

Client:
Welcome to Chat Room

Initialising....

csadmin-OptiPlex-3020 ( 127.0.1.1 )

Enter server address: 127.0.1.1

Enter your name: Client

Trying to connect to  127.0.1.1 ( 1234 )

Connected...

Server has joined the chat room
Enter [e] to exit chat room

Server : hi
Me : hello
Server : Left chat room!
Me : [e]


Server side:
Welcome to Chat Room

Initialising....

csadmin-OptiPlex-3020 ( 127.0.1.1 )

Enter your name: Server

Waiting for incoming connections...

Received connection from  127.0.0.1 ( 50694 )

Client has connected to the chat room
Enter [e] to exit chat room

Me : hi
Client : 0110100001100101011011000110110001101111011
Remainder :  010
Error in message
Me : [e]
