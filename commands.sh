pip install --user ansible
ansible datacenter -i inventory.yml -m ping
ansible-playbook -i inventory.yml playbook.yml 
mkdir ansible-testing
cd ansible-testing
mkdir roles
ansible-galaxy init test-role
