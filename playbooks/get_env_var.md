To get the current environment variables set on a server via Ansible, you can use the `setup` module, which gathers facts about the remote system, including environment variables. Here's a step-by-step guide:

1. **Create an Ansible playbook**:
   Create a playbook file, e.g., `get_env_vars.yml`.

2. **Use the `setup` module**:
   The `setup` module collects all the facts, including environment variables, from the remote host. You can filter the output to show only the environment variables.

Here's an example of how you can achieve this:

```yaml
---
- name: Gather environment variables from remote hosts
  hosts: all
  gather_facts: yes
  tasks:
    - name: Get environment variables
      setup:
        filter: ansible_env
    - name: Display environment variables
      debug:
        var: ansible_facts.ansible_env
```

3. **Run the playbook**:
   Execute the playbook with the following command:

   ```sh
   ansible-playbook -i inventory get_env_vars.yml
   ```

   Replace `inventory` with your actual inventory file.

This will gather and display the environment variables from all the hosts specified in your inventory.

### Explanation:

- **hosts: all**: This line specifies that the playbook should be run on all hosts in your inventory.
- **gather_facts: yes**: This tells Ansible to gather facts about the remote system, which includes environment variables.
- **setup: filter: ansible_env**: This task uses the `setup` module to gather only the environment variables.
- **debug: var: ansible_facts.ansible_env**: This task prints out the collected environment variables.

### Inventory File Example:

If you don't have an inventory file, create one named `inventory` with the following content:

```ini
[servers]
server1 ansible_host=your_server_ip
server2 ansible_host=your_server_ip
```

Replace `server1`, `server2`, and `your_server_ip` with your actual server names and IP addresses.

To gather environment variables for a specific user on the server via Ansible, you can use a combination of the `command` or `shell` module to switch to that user and then print the environment variables. Here's how you can achieve this:

1. **Create an Ansible playbook**:
   Create a playbook file, e.g., `get_user_env_vars.yml`.

2. **Use the `command` or `shell` module**:
   Use one of these modules to switch to the specified user and print the environment variables.

Here's an example of how you can achieve this:

```yaml
---
- name: Gather environment variables for a specific user
  hosts: all
  become: yes
  tasks:
    - name: Get environment variables for a specific user
      shell: |
        sudo -i -u specific_user /bin/bash -c 'env'
      register: env_output

    - name: Display environment variables
      debug:
        var: env_output.stdout_lines
```

3. **Run the playbook**:
   Execute the playbook with the following command:

   ```sh
   ansible-playbook -i inventory get_user_env_vars.yml
   ```

   Replace `inventory` with your actual inventory file and `specific_user` with the actual username you want to query.

### Explanation:

- **hosts: all**: This line specifies that the playbook should be run on all hosts in your inventory.
- **become: yes**: This tells Ansible to execute tasks with elevated privileges (e.g., using `sudo`).
- **shell**: The `shell` module is used to execute the command on the remote server.
- **sudo -i -u specific_user /bin/bash -c 'env'**: This command switches to the specified user and runs `env` to print the environment variables.
- **register: env_output**: This saves the output of the command in a variable named `env_output`.
- **debug: var: env_output.stdout_lines**: This prints out the environment variables collected.

### Inventory File Example:

If you don't have an inventory file, create one named `inventory` with the following content:

```ini
[servers]
server1 ansible_host=your_server_ip
server2 ansible_host=your_server_ip
```

Replace `server1`, `server2`, and `your_server_ip` with your actual server names and IP addresses.

This playbook will gather and display the environment variables for the specified user on all the hosts specified in your inventory.
