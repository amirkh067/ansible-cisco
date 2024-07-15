import telnetlib
import json
import os

def telnet_configure_access_list(host, username, password, commands):
    try:
        print(f"Connecting to {host}...")
        tn = telnetlib.Telnet(host)

        tn.read_until(b"Username: ")
        tn.write(username.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")

        tn.write(b"term len 0\n")  # Adjust terminal length for easier parsing
        tn.write(b"conf t\n")
        for cmd in commands:
            tn.write(cmd.encode('ascii') + b"\n")
            tn.write(b"show running-config | include " + cmd.split()[0].encode('ascii') + b"\n")
        tn.write(b"end\n")
        tn.write(b"wr\n")  # Save configuration
        tn.write(b"exit\n")

        print(f"Configuration applied on {host}:")
        output = tn.read_all().decode('ascii')
        print(output)

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

            telnet_configure_access_list(
                vars["ansible_host"],
                vars["ansible_user"],
                vars["ansible_password"],
                commands
            )
