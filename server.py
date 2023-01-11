# echo-server.py
import socket
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import time
import logging

def get_filename_incre(ext):
    list_files = os.listdir(log_folder)
    filename = 'log'
    i = 0
    while True:
        tmp = f"{filename}_{i}{ext}"
        if tmp not in list_files and tmp[-4:] == ext:
            return os.path.join(log_folder, tmp)
        i = i+1

log_folder = 'log_folder'
os.makedirs(log_folder, exist_ok = True)

logfilename = get_filename_incre('.txt')
logging.basicConfig(filename=logfilename, level=logging.DEBUG,
                    format="%(asctime)s %(message)s")
log_ds_filename = get_filename_incre('.csv')

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (HOST, PORT)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
plt.ion()
figure =plt.figure()
threads = []
idx = 0
# fig = plt.figure()

def get_df_based_on_code(df, code):
    return df[df['code']==code]

def show_image(df):
    image_path = df.iloc[0,8].strip() if type(df.iloc[0,8]) == str else './images/001.jpg'
    print(image_path)
    if not os.path.exists(image_path):
        print("Khong co hinh cua cuu")
        return
    img = mpimg.imread(image_path)
    plt.imshow(img)
    figure.canvas.draw()

    figure.canvas.flush_events()


df = pd.read_csv('./ds_alumni_full.csv')
    
def get_current_time_str():
    localtime = time.localtime(time.time())
    hours = localtime.tm_hour
    minutes = localtime.tm_min
    seconds = localtime.tm_sec
    return "{}:{}:{}".format(hours, minutes, seconds)

def process(df, code):
    tmp_df = get_df_based_on_code(df, code) 
    show_image(tmp_df)
    for index, row in df.iterrows():
        if row['code'] == code:
            status = "I" if pd.isnull(row['checkin']) else "O"
            if status == "I":
                df.at[index,'checkin'] = get_current_time_str()
            elif status == "O":
                df.at[index,'checkout'] = get_current_time_str()
    return df


save_df = df
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            code = int(message)
            if not data or code == 0:
                break
            connection.sendall(data)
            save_df = process(df, code)
            logging.info(f"alumni id: {message}")
    except:
        print(f"error with message: {message}")
    finally:
        # Clean up the connection
        connection.close()
    save_df.to_csv(log_ds_filename, index=False)