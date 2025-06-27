import cv2            
import imutils        
import socket         
import numpy as np   
import time           
import base64         

BUFF_SIZE = 65536

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the socket's receive buffer size (optional but helps for large video frames)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

# Get your computer's hostname (not used in this example)
host_name = socket.gethostname()

# Define the IP address of the server (where the video is being streamed from)
host_ip = '192.168.0.4'  # Change to the actual server IP if different
print(host_ip)

# Define the port number where the server is listening
port = 9993

# Send a dummy message to the server to "trigger" the stream
message = b'Hello'
client_socket.sendto(message, (host_ip, port))  

# Start receiving and displaying frames in a loop
while True:
    # Receive a UDP packet from the server
    packet, _ = client_socket.recvfrom(BUFF_SIZE)

    # Decode the Base64-encoded data to get the original image bytes
    data = base64.b64decode(packet, ' /') 

    # Convert the byte data into a NumPy array
    npdata = np.frombuffer(data, dtype=np.uint8)

    # Decode the NumPy array back into an image (OpenCV format)
    frame = cv2.imdecode(npdata, 1) 

    # Show the image frame in a window
    cv2.imshow('', frame) 
    
    # Wait for 1 ms for a key press
    key = cv2.waitKey(1)

    # If 'q' is pressed, exit the loop
    if key == ord('q'):
        client_socket.close()  
        break  