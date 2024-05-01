import subprocess

ansible_command = "ansible-playbook your_playbook.yml"

try:
    subprocess.run(ansible_command, shell=True, check=True)
    print("Ansible playbook executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing Ansible playbook: {e}")
