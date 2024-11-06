import os
import subprocess
import json
import argparse
import time
import docker
import sys
from dotenv import load_dotenv
import pkg_resources

load_dotenv()
VERSION = os.getenv("VERSION", "0.1.0") 

# def display_ascii_banner():
#     banner_path = os.path.join(os.path.dirname(__file__), "banner.txt")
#     try:
#         with open(banner_path, "r") as banner_file:
#             banner = banner_file.read()
#             # Replace {VERSION} placeholder with actual version
#             print(banner.replace("{VERSION}", VERSION))
#     except FileNotFoundError:
#         print("Banner file not found. Proceeding without banner.\n")

def display_ascii_banner():
    """Prints the banner text from banner.txt with the version."""
    try:
        banner = pkg_resources.resource_string(__name__, "banner.txt").decode("utf-8")
        print(banner.replace("{VERSION}", VERSION))
    except Exception as e:
        print(f"Error reading banner file: {e}")


def prompt_user_to_stop_streaming(stop_event):
    """Prompt the user to stop streaming logs every 5 seconds."""
    while not stop_event.is_set(): 
        if stop_event.is_set():
            break # Loop until stop_event is set
        time.sleep(5)  # Wait for 5 seconds
        response = input("Do you want to stop streaming? (ctrl^c/no): ").strip().lower()
        if response == "yes":
            stop_event.set()
            print("Stopping log streaming...") 
            return
        elif response == "no":
            continue
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def start_service(service_name, yaml_file, docker_compose_command, action, show_logs=False):
    """
    Start or stop a specified service using docker-compose based on the action.
    
    Args:
        service_name (str): The name of the service.
        yaml_file (str): The path to the docker-compose YAML file.
        action (str): Action to perform ('install' or 'uninstall').
    """
    # Get the absolute path for the YAML file
    yaml_file_path = os.path.join(os.getcwd(), yaml_file) if not os.path.isabs(yaml_file) else yaml_file
    
    # Debugging: print the yaml file path
    print(f"YAML file path: {yaml_file_path}")

    if not os.path.isfile(yaml_file_path):
        print(f"Error: Configuration file '{yaml_file_path}' not found.")
        return

    if action == 'install':
        response = input(f"Do you want to start/install {service_name}? (yes/no): ").strip().lower()
        if response == "yes":
            print(f"Starting {service_name}... 🚀")
            command = docker_compose_command.split() + ["-f", yaml_file_path, "up", "-d"]
        else:
            print(f"{service_name} will not be installed 🛑.")
            exit(0)
    elif action == 'uninstall':
        response = input(f"Do you want to stop/uninstall {service_name}? (yes/no): ").strip().lower()
        if response == "yes":
            print(f"Stopping {service_name}... 🛑")
            command = docker_compose_command.split() + ["-f", yaml_file_path, "down"]
        else:
            print(f"{service_name} will not be stopped/uninstalled.")
            return

    try:
        # Execute the command in the directory where the YAML file is located
        result = subprocess.run(command, check=True, capture_output=True, text=True, cwd=os.path.dirname(yaml_file_path))
        if action == 'install':
            print(f"{service_name} is up and running! 🎉")
            if show_logs:
                print("Streaming logs for the service: 📡")
                log_command = docker_compose_command.split() + ["-f", yaml_file_path, "logs", "-f"]
                log_process = subprocess.Popen(log_command, cwd=os.path.dirname(yaml_file_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                try:
                    while True:
                        # Check if there's output to read
                        output = log_process.stdout.readline()
                        if output:
                            print(output.decode().strip())
                except KeyboardInterrupt:
                    print("\nKeyboard interrupt detected. Stopping log streaming...")
                finally:
                    # Clean up after stopping log streaming
                    log_process.terminate()  # Terminate the log process
                    log_process.wait()  # Wait for the process to exit
                    print("Log streaming has been stopped. 🛑")
                    
                
        elif action == 'uninstall':
            print(f"{service_name} has been stopped successfully! ✅")
    except subprocess.CalledProcessError as e:
        print(f"Failed to {action} {service_name}. Please check {yaml_file_path} and try again. ❗")
        print("Error:", e.stderr)


def get_service_env(service_name):
    """
    Get environment variables for a running service using the docker package.
    
    Args:
        service_name (str): The name of the service.
        
    Returns:
        dict: A dictionary containing the environment variables of the service.
    """
    client = docker.from_env()  # Initialize the Docker client
    try:
        # Get the list of containers
        containers = client.containers.list(filters={"name": service_name.lower()})

        if not containers:
            print(f"No running container found for {service_name}.")
            return {}

        # Assuming the first matching container is the one we want
        container = containers[0]
        env_vars = container.attrs['Config']['Env']
        
        return dict(var.split('=', 1) for var in env_vars)  # Split key=value into dict
    except Exception as e:
        print(f"Failed to get environment variables for {service_name}. ❗")
        print("Error:", str(e))
        return {}
    
def read_env_file(yaml_file):
    """
    Read the .env file associated with a service.

    Args:
        yaml_file (str): The path to the docker-compose YAML file.

    Returns:
        dict: A dictionary of environment variables read from the .env file.
    """
    env_file_path = os.path.join(os.path.dirname(yaml_file), '.env')
    env_vars = {}
    
    if os.path.isfile(env_file_path):
        with open(env_file_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    else:
        print(f"No .env file found at {env_file_path}.")
    
    return env_vars

def save_env_to_file(service_name, env_vars):
    """
    Save environment variables to a text file.
    
    Args:
        service_name (str): The name of the service.
        env_vars (dict): Dictionary containing environment variables.
    """
    file_name = f"{service_name}_env_variables.txt"
    with open(file_name, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    print(f"Environment variables for {service_name} saved to {file_name}.")
 
def main():
    parser = argparse.ArgumentParser(
        description="Start or stop Docker services using docker-compose.",
        epilog="Example usage: offlix install mysql --compose-file path/to/custom-compose.yaml"
    )
    parser.add_argument(
        "command", 
        choices=["install", "uninstall"],
        help="Action to perform. Use 'install' to start a service and 'uninstall' to stop a service."
    )
    parser.add_argument(
        "service", 
        help="Service to start/stop (e.g., 'mysql', 'mongodb', 'kafka'). If not found, use --compose-file to specify a custom Docker Compose file."
    )
    parser.add_argument(
        "--docker-compose-command", 
        help="Command to invoke docker-compose", 
        default="docker compose"
    )
    parser.add_argument(
        "--compose-file",  
        help="Optional: Path to a custom Docker Compose YAML file to use instead of predefined ones."
    )

    parser.add_argument(
        "--logs", 
        action="store_true", 
        help="If set, stream docker-compose logs during installation."
    )

    if len(sys.argv) == 1:
        display_ascii_banner()
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    display_ascii_banner()
    
    # Define services and their respective docker-compose YAML file paths
    services = {
        "mysql": "mysql/mysql-compose.yaml",
        "mongodb": "mongodb/mongo-compose.yaml",
        "kafka": "kafka/kafka-compose.yaml",
        "maildev": "maildev/compose.yaml",
        "postgres": "postgres/postgresql.yaml"
    }

    service_name = args.service.lower()
    yaml_file = args.compose_file if args.compose_file else services.get(service_name)

    # Iterate over each service and prompt the user
    if yaml_file:
        start_service(service_name.capitalize(), yaml_file, args.docker_compose_command, args.command, show_logs=args.logs)
        
        if args.command == "install":
            time.sleep(5)  # Wait a moment to ensure the service is up
            env_vars = get_service_env(service_name.capitalize())
            if env_vars:
                print(f"Environment variables for {service_name}:\n", json.dumps(env_vars, indent=2))
            env_file_vars = read_env_file(yaml_file)
            if env_file_vars:
                save_env_to_file(service_name.capitalize(), env_file_vars)
    else:
        print(f"Service '{service_name}' is not recognized. Available services: {', '.join(services.keys())}")

    print("All selected services have been processed.")
    # print(f"To stop any running services manually, use: ${args.docker_compose_command} down")
