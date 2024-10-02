Below is an Ansible playbook that provisions a Linux user, generates an SSH key pair for that user, and outputs the public key:

### Playbook Structure:
1. **Create user**: Create a new Linux user with specific username.
2. **Generate SSH Key Pair**: Generates an SSH key pair for that user using Ansible's `openssl_privatekey` and `openssh_keypair` modules.
3. **Output Public Key**: Retrieve and display the public key for the created user.

### Playbook: `create_user_ssh_key.yml`

```yaml
---
- name: Provision Linux user and generate SSH key pair
  hosts: all
  become: true
  tasks:

    - name: Create a new user
      user:
        name: "{{ username }}"
        state: present
        shell: /bin/bash
        create_home: yes

    - name: Ensure .ssh directory exists
      file:
        path: "/home/{{ username }}/.ssh"
        state: directory
        mode: '0700'
        owner: "{{ username }}"
        group: "{{ username }}"

    - name: Generate SSH private key
      openssl_privatekey:
        path: "/home/{{ username }}/.ssh/id_rsa"
        type: RSA
        mode: '0600'
        owner: "{{ username }}"
        group: "{{ username }}"
      register: private_key

    - name: Generate SSH public key
      openssh_keypair:
        path: "/home/{{ username }}/.ssh/id_rsa"
        privatekey_path: "{{ private_key.path }}"
        owner: "{{ username }}"
        group: "{{ username }}"
      register: ssh_keypair

    - name: Set correct permissions on public key
      file:
        path: "/home/{{ username }}/.ssh/id_rsa.pub"
        mode: '0644'
        owner: "{{ username }}"
        group: "{{ username }}"

    - name: Display public key
      debug:
        msg: "{{ ssh_keypair.public_key }}"
```

### Key Explanations:

1. **Variables**:
   - `username`: This is the variable for the user that you want to create. You can define it when running the playbook.
   
2. **Tasks**:
   - **Create a new user**: Uses the `user` module to create the user with the provided name.
   - **Ensure .ssh directory exists**: The `.ssh` directory is required to store SSH keys.
   - **Generate SSH private key**: Uses the `openssl_privatekey` module to generate the private key.
   - **Generate SSH public key**: The `openssh_keypair` module generates the corresponding public key.
   - **Set correct permissions**: Ensures that the correct permissions are set on the generated public and private keys.
   - **Output the public key**: Displays the public key using the `debug` module.

### How to Run the Playbook:

You can run the playbook with:

```bash
ansible-playbook create_user_ssh_key.yml -e "username=mynewuser"
```

Replace `mynewuser` with the desired username. After running the playbook, the public key will be displayed as output.
