import sys
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import os
import warnings
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased,ALWAYS_ON
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# set the tracer provider
trace.set_tracer_provider(TracerProvider())

# now you can get a tracer instance
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(agent_host_name="localhost",agent_port=5001)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

MAX_HANDLED_CLIENTS = 20
client_count = 0

def handle_client(socket, client_count):
    with tracer.start_as_current_span("handle_client"):
        try:
            # Create a directory named "server_folder" if it doesn't exist
            if not os.path.exists("server_folder"):
                os.makedirs("server_folder")

            #use socket.makefile('rb') to create a file like object reading binary data from the socket
            with socket.makefile('rb') as reader, open(f"server_folder/received_file_{client_count}.txt", 'wb') as writer:
                #iterate through each line of binary data received from the client
                for line in reader:
                    #write the binary data to the file in binary mode(wb')
                    writer.write(line)
                    #print message file recieved
            print("File received")
        except Exception as e:
            #handle exeptions thatmay occur duringffile handling
            print(f"Client exception: {e}")
        finally:
            try:
                socket.close()
            except Exception as e:
                print(f"Failed to close socket: {e}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'probability':
        sampler = TraceIdRatioBased(0.4)
    else:
        sampler = ALWAYS_ON

    #set global tracer provider with a sampler that samples 40% of traces
    trace.set_tracer_provider(TracerProvider(sampler=sampler))
    global client_count
    with ThreadPoolExecutor(max_workers=10) as executor:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            try:
                #bind server socket to port n address
                server_socket.bind(('localhost', 5001))
                print("Server connected")
                #listen for incoming connection
                server_socket.listen()
                # print(f"Server listening on port 5001")
                #accept and handle clients until maxhandleclient is reached
                while client_count < MAX_HANDLED_CLIENTS:
                    #Accept a connection from a client
                    client_socket, _ = server_socket.accept()

                    client_count += 1
                    #submit the handle_client function to the thread pool for concurrent handling
                    executor.submit(handle_client, client_socket, client_count)
            except Exception as e:
                print(f"Error connecting to the server: {e}")

if __name__ == "__main__":
    main()
