import socket
import time
import psutil
import platform

# define host and port
host = 'localhost'
port = 5000

# create a socket object
sock = socket.socket()

# bind the socket to a specific address and port
sock.bind((host, port))

# set the number of queued connections
sock.listen(5)

connected_clients = set()

def get_cpu_usage():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

def get_mem_usage():
    mem_percent = psutil.virtual_memory().percent
    return mem_percent

def get_disk_usage():
    disk_percent = psutil.disk_usage('/').percent
    return disk_percent

# accept incoming connections from clients
while True:
    # establish connection with client
    conn, addr = sock.accept()

    connected_clients.add(conn)
    num_clients = len(connected_clients)
    print("Number of connected clients:", num_clients)

    # receive packet from client
    packet = conn.recv(1024).decode()

    # parse packet to get requested information
    if packet == 'cpu':
        data = f"CPU usage: {get_cpu_usage()}%"
    elif packet == 'mem':
        data = f"Memory usage: {get_mem_usage()}%"
    elif packet == 'disk':
        data = f"Disk usage: {get_disk_usage()}%"
    elif packet == 'uptime':
        uptime = int(time.time() - psutil.boot_time())
        data = f"Uptime: {uptime} seconds"
    elif packet == 'process':
        process = psutil.Process()
        data = f"Process name: {process.name()}\nPID: {process.pid}\nMemory usage: {process.memory_percent()}%"
    elif packet == 'os':
        os_info = f"OS: {platform.system()}\nRelease: {platform.release()}\nVersion: {platform.version()}"
        data = os_info
    elif packet == 'clients':
        data = f"Number of connected clients: {num_clients}"
    else:
        data = "Invalid request"

    # send requested data to client
    conn.send(data.encode())

    # close the connection
    conn.close()
