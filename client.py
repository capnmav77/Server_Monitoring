import socket
import time
import streamlit as st 
import os
import pandas as pd

# define host and port
host = 'localhost'
port = 5000

# create a socket object
sock = socket.socket()

# set timeout for socket operations
sock.settimeout(5)

# repeatedly try to connect to the server
while True:
    try:
        sock.connect((host, port))
        break
    except:
        print("Server is not running. Retrying in 5 seconds...")
        time.sleep(5)

# get input from user
st.title("Server monitoring system")
st.write("Connected to server:", host, ":", port)
option = st.selectbox("Select an option:", ["CPU usage", "Memory usage", "Disk usage","uptime","process","os"])

# send request to server based on user input
if option == "CPU usage":
    sock.send("cpu".encode())
elif option == "Memory usage":
    sock.send("mem".encode())
elif option == "Disk usage":
    sock.send("disk".encode())
elif option == "uptime":
    sock.send("uptime".encode())
elif option == "process":
    sock.send("process".encode())
elif option == "os":
    sock.send("os".encode())

# receive requested data from server
data = sock.recv(1024).decode()
rows = data.split("\n")
df = pd.DataFrame([row.split(",") for row in rows], columns=["Column 1"])

st.write(df)

sock.close()
