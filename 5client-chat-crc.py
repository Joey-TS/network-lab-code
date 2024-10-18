#Joseph 103 crc

import time, socket, sys


def encodeData(data, key): 

	l_key = len(key) 

	# Appends n-1 zeroes at end of data 
	appended_data = data + '0'*(l_key-1) 
	remainder = mod2div(appended_data, key) 

	# Append remainder in the original data 
	codeword = data + remainder 
	return codeword

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







print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print(shost, "(", ip, ")\n")
host = input(str("Enter server address: "))
name = input(str("\nEnter your name: "))
port = 1234
print("\nTrying to connect to ", host, "(", port, ")\n")
time.sleep(1)
s.connect((host, port))
print("Connected...\n")

s.send(name.encode())
s_name = s.recv(1024)
s_name = s_name.decode()
print(s_name, "has joined the chat room\nEnter [e] to exit chat room\n")

while True:
    message = s.recv(1024)
    message = message.decode()
    print(s_name, ":", message)
    message = input(str("Me : "))
    if message == "[e]":
        message = "Left chat room!"
        s.send(message.encode())
        print("\n")
        s.close()
        break
    res = ''.join(format(ord(i), '08b') for i in message)
    message=encodeData(res,"1011")
    s.send(message.encode())
