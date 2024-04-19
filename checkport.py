import socket
import sys
import platform
import subprocess

def main():
    print("Welcome to the Port Checker!")
    
    # Ask the user what protocol they want to check (TCP, UDP, or both)
    protocol = ''
    while protocol.lower() not in ['tcp', 'udp', 'both']:
        protocol = input("Which protocol do you want to check? (TCP, UDP, or both): ")
    
    # Ask the user for the port number
    while True:
        try:
            port = int(input("Please enter the port number you want to check: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid port number.")
    
    # Check if the port is open or closed
    if protocol.lower() == 'both':
        tcp_check(port)
        udp_check(port)
    elif protocol.lower() == 'tcp':
        tcp_check(port)
    else:
        udp_check(port)

    # Ask if the user wants to open the port in the firewall
    open_port = input("Do you want to open the port in the firewall? (yes / no): ")

    if open_port.lower() == 'yes':
        if protocol.lower() == 'both':
            open_firewall_port(port, 'TCP')
            open_firewall_port(port, 'UDP')
        elif protocol.lower() == 'tcp':
            open_firewall_port(port, 'TCP')
        else:
            open_firewall_port(port, 'UDP')
    else:
        print("OK. The port will remain unchanged.")

def tcp_check(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', port))
        if result == 0:
            print(f"TCP port {port} is open.")
        else:
            print(f"TCP port {port} is closed.")

def udp_check(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            print(f"UDP port {port} is open.")
        except OSError:
            print(f"UDP port {port} is closed.")

def open_firewall_port(port, protocol):
    if platform.system() == "Windows":
        cmd = f"netsh advfirewall firewall add rule name=\"Open {protocol} Port {port}\" dir=in action=allow protocol={protocol} localport={port}"
        try:
            subprocess.run(cmd, shell=True)
            print(f"{protocol} port {port} has been successfully opened in the firewall.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"{platform.system()} is not supported for automatically opening ports. Please open {protocol} port {port} manually.")

if __name__ == "__main__":
    main()
