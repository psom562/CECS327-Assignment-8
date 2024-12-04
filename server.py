import socket
import pytz
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta

# Connect to MongoDB
def connect_to_db():
    """Connect to the database where all IoT data is stored."""
    client = MongoClient("mongodb+srv://jag:winter2024@cecs-327.odbvb.mongodb.net/?retryWrites=true&w=majority&appName=CECS-327")
    return client["test"]  # Use the 'test' database


# Helper Functions
def utc_to_pst(utc_time):
    """Turn UTC time into PST time."""
    pst = pytz.timezone('US/Pacific')
    return utc_time.astimezone(pst)


def get_device_metadata(db, device_name):
    """Find details about a device using its name."""
    metadata_collection = db["DB1_metadata"]
    return metadata_collection.find_one({"customAttributes.name": device_name})


# Queries
def handle_average_moisture(db):
    """Find the average fridge moisture in the past 3 hours."""
    metadata = get_device_metadata(db, "Smart Fridge")  # Get fridge details
    if not metadata:
        return "Can't find fridge details."

    asset_uid = metadata["assetUid"]  # Fridge unique ID
    virtual_collection = db["DB1_virtual"]
    now_pst = utc_to_pst(datetime.now(timezone.utc))  # Current PST time
    three_hours_ago = now_pst - timedelta(hours=3)  # Time 3 hours ago

    # Query to get moisture levels
    pipeline = [
        {"$match": {
            "payload.parent_asset_uid": asset_uid,
            "payload.timestamp": {
                "$gte": str(int(three_hours_ago.timestamp())),
                "$lte": str(int(now_pst.timestamp()))
            }
        }},
        {"$group": {
            "_id": None,
            "avg_moisture": {"$avg": {"$toDouble": "$payload.Moisture Meter - Fridge"}}
        }}
    ]
    result = list(virtual_collection.aggregate(pipeline))  # Run the query
    if result and result[0]["avg_moisture"] is not None:
        avg_moisture = result[0]["avg_moisture"]
        return f"Average fridge moisture: {avg_moisture:.2f} RH%."
    return "No moisture data found for the last 3 hours."


def handle_average_water_consumption(db):
    """Find the average water used by the dishwasher."""
    metadata = get_device_metadata(db, "Smart Dishwasher")  # Get dishwasher details
    if not metadata:
        return "Can't find dishwasher details."

    dishwasher_uid = metadata["assetUid"]  # Dishwasher unique ID
    virtual_collection = db["DB1_virtual"]

    # Query to get water usage
    pipeline = [
        {"$match": {"payload.parent_asset_uid": dishwasher_uid}},
        {"$group": {"_id": None, "avg_water": {"$avg": {"$toDouble": "$payload.Water Consumption"}}}}
    ]
    result = list(virtual_collection.aggregate(pipeline))  # Run the query
    if result and result[0]["avg_water"] is not None:
        avg_water = result[0]["avg_water"]
        return f"Average water use: {avg_water:.2f} gallons."
    return "No water usage data found."


def handle_highest_electricity(db):
    """Find which device used the most electricity."""
    virtual_collection = db["DB1_virtual"]

    # Query to find electricity usage
    pipeline = [
        {"$project": {
            "device": "$payload.board_name",  # Device name
            "electricity": {"$toDouble": "$payload.Ammeter"}  # Convert to double
        }},
        {"$group": {
            "_id": "$device",  # Group by device name
            "total_electricity": {"$sum": "$electricity"}  # Sum electricity per device
        }},
        {"$sort": {"total_electricity": -1}},  # Sort by highest usage
        {"$limit": 1}  # Get the top device
    ]

    result = list(virtual_collection.aggregate(pipeline))

    if result:
        top_device = result[0]["_id"]  # Extract device name
        total_electricity = result[0]["total_electricity"]  # Extract total electricity
        return f"'{top_device}' used the most electricity: {total_electricity:.2f} kWh"
    else:
        return "No electricity usage data available."


# Figure Out What the Client Wants
def process_query(query, db):
    """Pick the right action based on what the client asks."""
    if query == "What is the average moisture inside my kitchen fridge in the past three hours?":
        return handle_average_moisture(db)
    elif query == "What is the average water consumption per cycle in my smart dishwasher?":
        return handle_average_water_consumption(db)
    elif query == "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?":
        return handle_highest_electricity(db)
    return "That query doesn't make sense."


# Main Server
def echo_server():
    """Start the server to handle client questions."""
    server_ip = input("Enter server IP address: ")
    server_port = int(input("Enter server port number: "))

    db = connect_to_db()  # Connect to the database

    # Set up the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))  # Start server on IP/port
        server_socket.listen(5)  # Wait for clients
        print(f"Server is live at {server_ip}:{server_port}...")

        while True:
            client_socket, addr = server_socket.accept()  # Accept client
            print(f"Connected to {addr}")

            with client_socket:
                while True:
                    client_message = client_socket.recv(1024).decode('utf-8')  # Get client message
                    if not client_message:
                        print("Client disconnected.")
                        break

                    print(f"Client asked: {client_message}")
                    response = process_query(client_message, db)  # Get the answer
                    client_socket.send(response.encode('utf-8'))  # Send it back


if __name__ == "__main__":
    echo_server()
