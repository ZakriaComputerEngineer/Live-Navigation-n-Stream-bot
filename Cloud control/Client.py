import socket
import threading
import json
import random
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

# for python to communicate with raspberryPi
REMOTEIT_URL = 'tcp://proxy61.rt3.io:33279'

# Making a Flask server to communicate with JS
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
Current = ""
Directions = ""


@app.route('/data', methods=['POST'])
def receive_data_from_JS():
    global Directions
    direction_val = request.json  # Receive data sent from JavaScript
    if direction_val != "":
        Directions = direction_val
    print("Data received:", Directions)
    # Process the data as needed

    # Send a response back to JavaScript
    response_data = {"message": Directions}
    return jsonify(response_data)


@app.route('/sendDataToJS', methods=['GET'])
def send_data_to_JS():
    data = ""
    if Current == None:
        data = "meow!!!"
    else:
        data = "data from python: " + Current
    # Data to send from Python to JavaScript
    return jsonify(data)


def send_data_to_PI(client_socket):
    global Directions
    old_directions = ""
    try:
        while True:
            try:
                # Read the value from the file "direction.txt"
                # D = "Random" + random()%100
                if old_directions == Directions:
                    continue
                time.sleep(10)
                old_directions = Directions
                client_socket.sendall(json.dumps(Directions).encode())
            except ValueError:
                print("Invalid input")
    except KeyboardInterrupt:
        print("Client interrupted by user")
    finally:
        client_socket.close()


def receive_data_from_GPS(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            global Current
            Current = data.decode()
            print(f"Current: {Current}")
            # send_data_to_JS()
    except KeyboardInterrupt:
        print("Client interrupted by user")
    finally:
        client_socket.close()


def main():
    # Running Flask Server
    app.run(debug=True, port=4050)

    parts = REMOTEIT_URL.split(':')
    host = parts[1][2:]
    port = int(parts[2])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_thread1 = threading.Thread(
        target=send_data_to_PI, args=(client_socket,))
    client_thread2 = threading.Thread(
        target=receive_data_from_GPS, args=(client_socket,))
    client_thread1.start()
    client_thread2.start()
    client_thread1.join()
    client_thread2.join()


if __name__ == "__main__":
    main()
