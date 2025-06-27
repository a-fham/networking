import cv2          
import imutils      
import socket      
import numpy as np  
import time         
import base64       


BUFF_SIZE = 65536  # Maximum size of a UDP packet buffer

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the receive buffer size option on the socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

# Set the server's IP address (use your own IP here)
host_ip = '192.168.0.4'  # Replace with your actual IP if needed
print(host_ip)

# Set the port number to listen on
port = 9993

# Combine IP and port into a single address tuple
socket_address = (host_ip, port)

# Bind the server socket to the IP and port
server_socket.bind(socket_address)
print('Listening at:', socket_address)

# Open the default webcam (device index 0)
vid = cv2.VideoCapture(0)

# Wait for client to send any message to begin video stream
while True:
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)  # Wait for client connection
    print('GOT connection from ', client_addr)  # Print client's IP and port

    WIDTH = 400  # Set the desired width of the video frame

    # Start capturing and sending video frames
    while vid.isOpened():
        _, frame = vid.read()  # Capture a frame from the webcam
        frame = imutils.resize(frame, width=WIDTH)  # Resize the frame for lower bandwidth

        # Encode the frame as JPEG (compress it)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

        # Convert the encoded frame into base64 so it can be sent over UDP as text
        message = base64.b64encode(buffer)

        # Send the base64-encoded frame to the client
        server_socket.sendto(message, client_addr)

        # Check for the 'q' key to stop the stream
        key = cv2.waitKey(1)
        if key == ord('q'):
            server_socket.close()
            break  
