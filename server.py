import socket
import pymongo
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# MongoDB Connection Details
mongo_client = pymongo.MongoClient("mongodb+srv://CECS327:Password123@cluster0.dqebg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
iot_db = mongo_client["test"]  
metadata_collection = iot_db["device_metadata"]
sensor_data_collection = iot_db["sensor_data"]
