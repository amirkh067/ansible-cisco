import telnetlib
import json
import os

def telnet_configure_access_list(host, username, password, commands):
    try:
        print(f"Connecting to {host}...")
        tn = telnetlib.Telnet(host)

        tn.read_until(b"Username: ")
        print(f"Sending username: {username}")
        tn.write(username.encode('ascii') + b"\n")

        if password:
            tn.read_until(b"Password: ")
            print(f"Sending password: {password}")
            tn.write(password.encode('ascii') + b"\n")

        tn.write(b"term len 0\n")  # Adjust terminal length for easier parsing
        print("Setting terminal length to 0")

        tn.write(b"conf t\n")
        print("Entering configuration mode")

        for cmd in commands:
            print(f"Sending command: {cmd.strip()}")
            tn.write(cmd.encode('ascii') + b"\n")

        tn.write(b"end\n")
        print("Exiting configuration mode")

        tn.write(b"wr\n")  # Save configuration
        print("Saving configuration")

        tn.write(b"exit\n")
        print("Exiting telnet session")

        print(f"Configuration applied on {host}")

        # Read and save running-config to a file
        tn.write(b"show running-config\n")
        print("Requesting running-config")

        output = tn.read_until(b"end").decode('ascii')
        print(f"Received running-config:\n{output}")

        # Write running-config output to a file
        file_name = f"{host}_running-config.txt"
        with open(file_name, "w") as file:
            file.write(output)

        print(f"Saved running-config to {file_name}")

        # Grep for added commands in the running-config file
        for cmd in commands:
            grep_command = f"grep '{cmd.strip()}' {file_name}"
            print(f"Running grep command: {grep_command}")
            os.system(grep_command)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Load environment variables
    hostvars = json.loads(os.getenv("HOSTVARS"))
    commands_file = os.getenv("COMMANDS_FILE")

    for host, vars in hostvars.items():
        if vars.get("ansible_host"):
            commands = []
            with open(commands_file, 'r') as file:
                commands = file.readlines()
            commands = [cmd.strip() for cmd in commands]

            print(f"Applying configuration on host: {host}")
            telnet_configure_access_list(
                vars["ansible_host"],
                vars["ansible_user"],
                vars["ansible_password"],
                commands
            )
