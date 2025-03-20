import threading
import queue
import time
import json
import psutil
import socket
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from camera import open_camera
from s3_upload import upload_photo_s3_async
from put_watermark import set_watermark
from config import *

# Global Variables
task_queue = queue.Queue()
last_capture_time = 0

def is_wifi_connected():
    for iface, addrs in psutil.net_if_addrs().items():
        if "wlan" in iface.lower() or "wi-fi" in iface.lower():
            for addr in addrs:
                if addr.family == socket.AF_INET:  # ตรวจสอบว่าได้ IP Address หรือไม่
                    return True
    return False

def mqtt_reconnect():
    while True:
        try:
            mqtt_client.connect()
            print("Reconnected to AWS IoT!")
            return
        except Exception as e:
            print(f"Reconnect failed: {e}, retrying in 5s...")
            time.sleep(5)

def process_task():
    while True:
        task = task_queue.get()
        if task is None:
            break
        action, params = task
        if action == "capture_image" or "stream":
            global last_capture_time
            current_time = time.time()
            if current_time - last_capture_time < CAPTURE_INTERVAL:
                print("Skipping capture: Too frequent")
                continue
            last_capture_time = current_time
            image_name = params.get("image_name", "image.jpg")
            format_name = params.get("format", "jpg")
            user_id = params.get("user_id", "1")
            camera_id = params.get("camera_id", "0")
            watermark_name = params.get("watermark", "none")
            image_file = image_name+'.'+format_name
            if watermark_name != 'none':
                if open_camera(image_file):
                    set_watermark(image_name,watermark_name)
                    upload_photo_s3_async(image_file,user_id,camera_id)
            elif watermark_name == 'none':
                if open_camera(image_file):
                    upload_photo_s3_async(image_file,user_id,camera_id)
        task_queue.task_done()

def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        action = payload.get("state", {}).get("camera", {}).get("action")
        params = payload.get("state", {}).get("camera", {}).get("params", {})
        print(payload)
        if action:
            task_queue.put((action, params))
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")

# Start Worker Thread
worker_thread = threading.Thread(target=process_task, daemon=True)
worker_thread.start()

while True:
    try:
        is_wifi_connected()
        break 
    except Exception as e:
        print(f"Failed to connect wifi: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
        
mqtt_client = AWSIoTMQTTClient(CLIENT_ID)
mqtt_client.configureEndpoint(ENDPOINT, 8883)
mqtt_client.configureCredentials(CA_FILE, KEY_FILE, CERT_FILE)
mqtt_client.configureOfflinePublishQueueing(10)
mqtt_client.configureDrainingFrequency(1)
mqtt_client.configureConnectDisconnectTimeout(5)
mqtt_client.configureMQTTOperationTimeout(3)

print("Connecting to AWS IoT Core...")
while True:
    try:
        print("Attempting to connect to AWS IoT Core...")
        mqtt_client.connect()
        print("Connected!")
        break 
    except Exception as e:
        print(f"Failed to connect to AWS IoT Core: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)

try:
    mqtt_client.subscribe(SHADOW_TOPIC, 1, on_message)
    print("Subscribed to topic")
except Exception as e:
    print(f"Subscription error: {e}")


print(f"Listening for messages on: {SHADOW_TOPIC}")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
    mqtt_client.disconnect()
    task_queue.put(None)  # Stop worker
    worker_thread.join()
    print("Disconnected!")