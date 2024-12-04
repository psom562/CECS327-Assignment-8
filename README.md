# CECS327-Assignment-8
End-to-End IoT System with TCP Client-Server and MongoDB Integration

# Overview
This project showcases a fully integrated IoT system that combines:
A TCP client-server model to handle user queries and responses.
A MongoDB database for storing IoT device metadata and sensor data used in our previous lab.

# System Architecture
1. TCP Client
Purpose: Accepts user input, validates queries, and communicates with the TCP server.
Responsibilities:
Sends user-selected queries to the server.
Displays the server's response to the user.
2. TCP Server
Purpose: Handles incoming queries, interacts with MongoDB, and performs calculations.
Responsibilities:
Fetches relevant data from the MongoDB database.
Processes queries using metadata for enhanced context.
Converts units (e.g., moisture to RH%, liters to gallons, and electricity to kWh).
3. MongoDB Database
Components:
Metadata Collection (device_metadata): Stores device-specific details, such as device IDs and names.
Sensor Data Collection (sensor_data): Contains time-stamped IoT sensor readings.
Role: Provides a backend for efficient data retrieval and processing.
4. IoT Devices
Devices Simulated:
SmartFridge: Tracks moisture levels and electricity consumption.
SmartWasher: Tracks water usage and electricity consumption.
SecondFridge: Tracks moisture levels and electricity consumption.

# Usage Instructions
1. Setting Up the Environment
Install Required Libraries:
pip install pymongo
Set Up MongoDB:
Use MongoDB Atlas or a local MongoDB instance.
Create device_metadata and sensor_data collections.
Populate the collections with metadata and sample sensor data.

2. Running the Server
Save the server code as Server.py.
Start the server:

python Server.py

Enter the IP address and port when prompted:

Enter the IP address to bind the server: 
Enter the port number to bind the server: 

3. Running the Client
Save the client code as Client.py.
Start the client:

python Client.py

Enter the server's IP address and port to connect:

Enter the server IP address: 
Enter the server port number: 

4. Sending Queries
Select a Query:
At the client prompt, enter a query such as:
1 (average moisture)
2 (average water consumption)
3 (highest electricity consumption)
View the Response:
Example Output:

Server response: Average moisture from 2024-12-03 22:45:41 PST to 2024-12-04 01:45:41 PST: 55.95 RH%

# Example 
Client Interaction:

Enter the server IP address: 
Enter the server port number: 

Choose a query:
1. Average moisture in the kitchen fridge (past 3 hours).
2. Average water consumption per cycle (smart dishwasher).
3. Device with the highest electricity consumption.

Enter your query: 1
Response from server: Average moisture in the fridge: 47.50 RH%.

Server Output:

Server is active on 127.0.0.1:8000...
Connected to client: ('127.0.0.1', 54321)
Received query: average moisture
DEBUG: Fetching data since 2023-12-01 08:00:00
DEBUG: Average moisture for KitchenFridge: 47.50 RH%.

# Challenges and Solutions
Challenge: Mapping sensor data to device-specific queries.
Solution: Used MongoDB metadata to link sensor readings with unique device IDs.
Challenge: Handling time zones conversions.
Solution: Implemented zone info for UTC-to-PST conversions.
