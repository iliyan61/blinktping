#!/usr/bin/env python
import os
import time
import requests
import signal
import sys
from flask import Flask, render_template
from blinkt import set_brightness, set_pixel, show, clear

# Initialize the Flask application
app = Flask(__name__)

# Clear the LEDs
set_brightness(0.1)
clear()
show()

# Function to clear LEDs on shutdown
def signal_handler(sig, frame):
    print("Shutting down...")
    clear()  # Clear the LEDs
    show()    # Update the display
    time.sleep(0.1)  # Give a moment for the change to take effect
    sys.exit(0)
    
# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Your existing setup code
set_brightness(0.1)
clear()
show()

# Discord Webhook URL
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

# Function to send a message to the Discord channel
def send_discord_notification(message):
    data = {"content": message}
    requests.post(WEBHOOK_URL, json=data)

# Dictionary format: "IP", "description", status where 0 = up and 1 = down
pingdict = {
    0: ["192.168.18.3", "pve1", 1],
    1: ["192.168.18.4", "pve2", 1],
    2: ["192.168.18.5", "pve3", 1],
    3: ["catspyjamas.xyz", "NAS", 1],
    4: ["116.202.155.169", "bkup", 1],
    5: ["192.168.18.1", "router", 1],
    6: ["192.168.18.1", "router", 1],
    7: ["google.com", "google", 1]
}

# Initialize a counter for down statuses
down_counters = [0] * 8
DOWN_THRESHOLD = 3  # Number of cycles a host must be down before notifying

@app.route('/')
def index():
    # Render the status of the hosts
    return render_template('index.html', pingdict=pingdict)

def update_host_status():
    while True:
        for x in range(8):
            # Change color slightly while testing an IP address
            set_pixel(x, 0, 0, 10)  # Dim color to indicate checking
            show()

            # Ping the IP address
            response = os.system(f"ping -c 1 -W 2 {pingdict[x][0]} > /dev/null 2>&1")

            if response == 0:
                set_pixel(x, 255, 20, 147)  # Pink for up
                print(f"{pingdict[x][1]} is up")
                pingdict[x][2] = 0
                down_counters[x] = 0  # Reset counter if the host is up
            else:
                set_pixel(x, 255, 0, 0)  # Red for down
                print(f"{pingdict[x][1]} is down")
                pingdict[x][2] = 1

                # Increment the counter for down statuses
                down_counters[x] += 1

                # Send a notification to Discord only if down for the threshold number of cycles
                if down_counters[x] == DOWN_THRESHOLD:
                    send_discord_notification(f"{pingdict[x][1]} is down!")

            show()

        # Show pink for up statuses for 3 seconds
        for x in range(8):
            if pingdict[x][2] == 0:  # Only keep pink if up
                set_pixel(x, 255, 20, 147)  # Pink for up
            else:
                set_pixel(x, 255, 0, 0)  # Red for down

        show()
        time.sleep(3)  # Keep the status visible for 3 seconds

        # Clear the LEDs for 1 second
        clear()
        show()
        time.sleep(1)  # Wait for 1 second before the next loop

        print("\n" * 3)

if __name__ == "__main__":
    # Start the Flask app in a separate thread or process
    from threading import Thread

    # Start the status checking loop in a separate thread
    status_thread = Thread(target=update_host_status)
    status_thread.daemon = True  # Ensure it exits when the main thread does
    status_thread.start()

    # Start the Flask web server
    app.run(host='0.0.0.0', port=5000)  # Change the port if needed