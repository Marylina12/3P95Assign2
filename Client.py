import os
import socket
import random

def generate_file(filename, file_size):
    #open a file in binary write mode
    with open(filename, "wb") as f:
        #generate random binary data of size filesize*1024
        bytes_data = bytearray(random.getrandbits(8) for _ in range(file_size * 1024))

        #write the generate binary data to file
        f.write(bytes_data)
        #print a  of succesful creation
        print(f"File: {filename} has been created.")

def main():
    #generate and send 20 files to the server
    for i in range(20):
        #create a filename for the current iteration
        filename = f"file{i+1}.txt"
        #calculate the file sized based on the iteration
        file_size = (i+1) * 5
        #generate a file with the specified filename and size
        generate_file(filename, file_size)

        #iteration through the 20 files and send to server

    for i in range(20):
        try:
            #create a socket using 1pv4 and tcp
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                #connect to the server at localhost and port 5001
                s.connect(("localhost", 5001))

                #Specify the filename of the current file to be sent
                file = f"file{i+1}.txt"
            #open the file in binary read mode('rb')
                with open(file, 'rb') as f:
                    #send the contents of file through sockt using sendfile
                    s.sendfile(f)

                    #print a message indicating that the file has been sent successfuly
                print(f"File {file} sent to the server.")
        except Exception as e:
            #Handle any exception that may occur during file sending or socket operations
            print(f"Error: {e}")

if __name__ == "__main__":
    #Execute the main function i
    main()
