# ds_client.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Ryan Zhang, Yash Pathak
# ryanyz@uci.edu, pathaky@uci.edu
# 20907746, 51317074

import socket
import ds_protocol
import json


def send(server: str, port: int, username: str, password: str, message: str, bio: str = None) -> bool:
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    # TODO: return either True or False depending on results of required operation
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        # Try to connect to the provided server IP and port
        try:
            client.connect((server, port))
        except socket.error:
            print("Could not connect to server. Check your IP and Port.")
            return False

        # Create the abstraction files
        send = client.makefile('w')
        recv = client.makefile('r')

        # Join the server with username and password
        # Encode the data
        try:
            data = ds_protocol.encode_json("join", username, password, '')
        except:
            print("Join data could not be encoded to json.")
            return False

        # Send the data
        try:
            send.write(data)
            send.flush()
        except:
            print("An error occurred while trying to join the server.")
            return False

        # Receive server response and extract token
        srv_msg = recv.readline()
        srv_data = ds_protocol.extract_json(srv_msg)

        # Will evaluate true if extracting encountered a JSONDecodeError
        if not srv_data:
            return False

        token = srv_data.token
        
        # If server responds with an error then print error and return False
        if srv_data.response_type == "error":
            print("Invalid password or username already taken.")
            return False


        # Update bio if bio given
        if bio:
            # Encode the data
            try:
                data = ds_protocol.encode_json("bio", token=token, entry=bio)
            except:
                print("Bio could not be encoded to json.")
                return False

            # Send the data
            try:
                send.write(data)
                send.flush()
            except:
                print("An error occurred while sending the bio to the server.")
                return False

            # Receive server response
            srv_msg = recv.readline()
            srv_data = ds_protocol.extract_json(srv_msg)

            # Will evaluate true if extracting encountered a JSONDecodeError
            if not srv_data:
                return False

            # If server responds with an error then print error and return False
            if srv_data.response_type == "error":
                print("Bio could not be updated.")
                return False

            # Print the server response
            print("\n" + srv_data.response_message)

        # Post message onto the server (the string is a placeholder to allow only editing the bio without making a post)
        if message != "don't print this awawawawawwa":
            # Encode the data
            try:
                data = ds_protocol.encode_json("post", token=token, entry=message)
            except:
                print("Post could not be encoded to json.")
                return False

            # Send the data
            try:
                send.write(data)
                send.flush()
            except:
                print("An error occurred while sending the post to the server.")
                return False

            # Receive server response
            srv_msg = recv.readline()

            srv_data = ds_protocol.extract_json(srv_msg)

            # Will evaluate true if extracting encountered a JSONDecodeError
            if not srv_data:
                return False

            # If server responds with an error then print error and return False
            if srv_data.response_type == "error":
                print("Post could not be added onto the server.")
                return False

            # Print the server response
            print("\n" + srv_data.response_message)
            
        # Only returns true if every operation did not fail
        return True
