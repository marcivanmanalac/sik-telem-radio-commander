# This will need to be ran on the computer that is connected to the SiK radio. This will allow you to send commands to the Raspberry Pi via the SiK radio.
import serial
import time

def comms(serial_port='/dev/ttyUSB0', baud_rate=57600, message='ls', terminator='[END_OF_RESPONSE]'):
    """
    Send a specified message to the Raspberry Pi via a SiK radio, wait for the complete response
    including multiple lines, and then return the response.

    Args:
    serial_port (str): The serial port the SiK radio is connected to.
    baud_rate (int): The baud rate for the serial communication (defaults to 57600).
    message (str): The message/command to be sent.
    terminator (str): The special string to indicate the end of the response.
    """
    try:
        # Initialize serial connection
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            print(f"Sending '{message}' to {serial_port} at {baud_rate} baud rate...")
            ser.write(f"{message}\n".encode('utf-8'))  # Encode the message to bytes and send
            
            response = ""  # Initialize an empty string to hold the response
            while True:
                line = ser.readline().decode('utf-8')  # Read a line from the serial port
                if terminator in line:  # If the terminator is found, stop reading
                    break
                response += line  # Add the line to the response

            # Optional: remove the trailing newline from the response
            response = response.strip()

            if response:  # If a response is received, print it
                print(f"Received response:\n{response}")
    except serial.SerialException as e:
        print(f"Failed to open serial port {serial_port}: {e}")

while True:
    # Prompt the user for a command to send
    user_input = input("Enter the command to send (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':  # Check if the user wants to exit the program
        break
    comms(message=user_input)  # Pass the user input as the message argument
    time.sleep(2)  # Wait for a specified interval between sending commands


