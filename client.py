import socket

# Maximum size of data to receive
MAX_PACKET_SIZE = 1024

# List of queries the client can ask
VALID_QUERIES = [
    "What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"
]

def display_queries():
    """Show all the queries the client can choose from."""
    print("\nAvailable queries:")
    for i, query in enumerate(VALID_QUERIES, start=1):
        print(f"{i}. {query}")
    print("Type 'exit' to disconnect.")  # Tell the user how to exit

def start_client():
    """Connect to the server and let the user send questions."""
    # Ask for the server's details
    server_ip = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port number: "))

    # Open a connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))  # Connect to the server
        print(f"Connected to server at {server_ip}:{server_port}")
        display_queries()  # Show the list of queries to the user

        while True:
            # Ask the user for input
            user_input = input("\nEnter your query number (or type 'exit'): ")
            if user_input.lower() == 'exit':  # If they want to exit, close the connection
                print("Closing connection.")
                break

            try:
                # Convert the input into a query number
                query_index = int(user_input) - 1
                if 0 <= query_index < len(VALID_QUERIES):  # Make sure the number is valid
                    # Send the query to the server
                    client_socket.sendall(VALID_QUERIES[query_index].encode())
                    # Get the server's response
                    server_response = client_socket.recv(MAX_PACKET_SIZE).decode()
                    print(f"Server response: {server_response}")  # Show the server's response
                else:
                    print("Invalid query number. Please try again.")  # Invalid query
            except ValueError:
                print("Invalid input. Please enter a number corresponding to a query.")  # Non-number input

if __name__ == "__main__":
    start_client()  # Start the client
