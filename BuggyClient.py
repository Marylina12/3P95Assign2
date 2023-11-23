import os
import socket
import random

# Function to generate a file with a given filename and size
def generate_file(filename, file_size):
    # Open a file in binary write mode
    with open(filename, "wb") as f:
        # Generate random binary data of size filesize*1024
        bytes_data = bytearray(random.getrandbits(8) for _ in range(file_size * 1024))

        # Write the generated binary data to file
        f.write(bytes_data)
        # Print a message of successful creation
        print(f"File: {filename} has been created.")

def main():
    # Create a directory named "buggy_client_folder" if it doesn't exist
    buggy_client_folder = "buggy_client_folder"
    if not os.path.exists(buggy_client_folder):
        os.makedirs(buggy_client_folder)

    # Generate and send 20 files to the server
    for i in range(20):
        # Create a filename for the current iteration in the buggy client folder
        filename = f"{buggy_client_folder}/file{i+1}.txt"
        # Check if the file already exists, if not then generate the file
        if not os.path.isfile(filename):
            # Calculate the file size based on the iteration
            file_size = (i+1) * 5
            # Generate a file with the specified filename and size
            generate_file(filename, file_size)

    # Introduce a bug: Send the first file three times and the rest once
    bug_iteration = 1  # Bug occurs at iteration 1
    repeated_send_count = 3  # Send the file three times
    for i in range(20):
        try:
            # Create a socket using IPv4 and TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Connect to the server at localhost and port 5001
                s.connect(("localhost", 5001))

                # Specify the filename of the current file to be sent from the buggy client folder
                file = f"{buggy_client_folder}/file{bug_iteration}.txt"
                # Open the file in binary read mode('rb')
                with open(file, 'rb') as f:
                    # Send the contents of file through socket using sendfile
                    for _ in range(repeated_send_count):
                        s.sendfile(f)

                # Print a message indicating that the file has been sent successfully
                print(f"File {file} sent to the server {repeated_send_count} times.")
        except Exception as e:
            # Handle any exception that may occur during file sending or socket operations
            print(f"Error: {e}")

if __name__ == "__main__":
    # Execute the main function
    main()
