"""
    Import this onto your pi and run it. 
    It will listen for commands on the serial port and execute them as shell commands.
"""
import serial
import subprocess

def execute_command(command):
    """
    Execute a shell command and return the output.
    """
    try:
        # Execute the command, capture the output and error (if any)
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def listen_and_execute(port='/dev/ttyUSB0', baudrate=57600, terminator='[END_OF_RESPONSE]'):
    """
    Listen for commands on the specified serial port and execute them as shell commands.
    """
    with serial.Serial(port, baudrate=baudrate, timeout=1) as ser:
        print(f"Listening for commands on {port} at {baudrate} baud...")
        while True:
            # Read a line from the serial port
            line = ser.readline().decode().strip()
            if line:  # If a line is received, execute it as a command
                print(f"Received command: {line}")
                response = execute_command(line)
		# Append the termination string to the response
                response += terminator
                print(f"Command output: {response}")
                # Optional: Send the response back over the serial connection
                ser.write(response.encode())

# main function
if __name__ == "__main__":
    listen_and_execute()
