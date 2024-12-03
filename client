import socket
MAX_PACKET_SIZE = 1024

# Predefined Queries
VALID_QUERIES = [
    "What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "Which device consumed more electricity among my three IoT devices?"
]

def display_queries():
    print("\nAvailable queries:")
    for i, query in enumerate(VALID_QUERIES, start=1):
        print(f"{i}. {query}")
    print("Type 'exit' to disconnect.")

def start_client():
    """Prompt for server details and connect to send queries."""
    server_ip = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port number: "))
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")
        display_queries()

        while True:
            user_input = input("\nEnter your query number (or type 'exit'): ")
            if user_input.lower() == 'exit':
                print("Closing connection.")
                break

            try:
                query_index = int(user_input) - 1
                if 0 <= query_index < len(VALID_QUERIES):
                    client_socket.sendall(VALID_QUERIES[query_index].encode())
                    server_response = client_socket.recv(MAX_PACKET_SIZE).decode()
                    print(f"Server response: {server_response}")
                else:
                    print("Invalid query number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number corresponding to a query.")

if __name__ == "__main__":
    start_client()
