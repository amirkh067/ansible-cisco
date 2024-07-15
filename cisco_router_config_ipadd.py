import os
import json
import telnetlib

def read_configuration():
    try:
        print("Reading configuration from environment variables...")
        hostvars = json.loads(os.getenv('HOSTVARS'))
        commands_file = os.getenv('COMMANDS_FILE')

        if not commands_file:
            raise Exception("Commands file not specified in environment variables.")

        # Read commands from commands.txt file
        with open(commands_file, 'r') as file:
            commands = file.readlines()

        # Remove any trailing newline characters from each command
        commands = [command.strip() for command in commands]

        for host, vars in hostvars.items():
            if 'ansible_host' in vars and 'ansible_user' in vars and 'ansible_password' in vars:
                host_ip = vars['ansible_host']
                username = vars['ansible_user']
                password = vars['ansible_password']

                print(f"Configuration read. Host: {host_ip}, Username: {username}")

                telnet_configure_access_list(host_ip, username, password, commands)
                
    except Exception as e:
        print(f"An error occurred: {e}")

def telnet_configure_access_list(host, username, password, commands):
    try:
        # Connect to the device
        tn = telnetlib.Telnet(host)

        # Read username prompt and send username
        tn.read_until(b"Username:")
        tn.write(username.encode('ascii') + b"\n")

        # Read password prompt and send password
        tn.read_until(b"Password:")
        tn.write(password.encode('ascii') + b"\n")

        # Enter enable mode
        tn.write(b"enable\n")
        tn.read_until(b"Password:")
        tn.write(password.encode('ascii') + b"\n")

        # Send each command
        for command in commands:
            print(f"Executing command: {command}")
            tn.write(command.encode('ascii') + b"\n")

        # Read the output of the commands (optional)
        output = tn.read_all().decode('ascii')
        print(output)

        # Close the connection
        tn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    read_configuration()
