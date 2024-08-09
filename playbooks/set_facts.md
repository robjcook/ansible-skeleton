In Ansible, "facts" refer to variables that are automatically discovered by the `setup` module or manually defined by users. When you set a fact in Ansible, you're creating a new variable that you can use later in your playbook. You can output or print these facts to see their values during playbook execution.

Here's how you can output facts after setting them:

### 1. **Setting a Fact with `set_fact`**

You can set a fact using the `set_fact` module. For example:

```yaml
- name: Set a custom fact
  set_fact:
    my_custom_fact: "Hello, Ansible!"

- name: Show the custom fact
  debug:
    var: my_custom_fact
```

### 2. **Outputting Facts with `debug`**

After setting a fact, you can output it using the `debug` module. Here's how you can do it:

```yaml
- name: Output a fact after setting it
  hosts: localhost
  tasks:
    - name: Set a custom fact
      set_fact:
        my_custom_fact: "Hello, Ansible!"

    - name: Show the custom fact
      debug:
        var: my_custom_fact
```

### 3. **Outputting All Facts**

If you want to output all facts, you can use the `setup` module along with the `debug` module:

```yaml
- name: Output all facts
  hosts: localhost
  tasks:
    - name: Gather all facts
      setup:

    - name: Show all gathered facts
      debug:
        var: ansible_facts
```

### 4. **Outputting Selected Facts**

You can also output a selection of facts:

```yaml
- name: Output selected facts
  hosts: localhost
  tasks:
    - name: Gather all facts
      setup:

    - name: Show selected facts
      debug:
        msg: "{{ ansible_facts['ansible_hostname'] }} running on {{ ansible_facts['ansible_distribution'] }}"
```

### Example Playbook

Here's a complete playbook example:

```yaml
---
- name: Set and output facts
  hosts: localhost
  tasks:
    - name: Set a custom fact
      set_fact:
        my_custom_fact: "Hello, Ansible!"

    - name: Show the custom fact
      debug:
        var: my_custom_fact

    - name: Gather all facts
      setup:

    - name: Show the ansible_hostname fact
      debug:
        var: ansible_hostname
```

### Running the Playbook

When you run this playbook, it will output the value of the custom fact `my_custom_fact` and also show the hostname of the machine using the fact `ansible_hostname`.

### Summary

- **`set_fact`**: To set a custom fact.
- **`debug`**: To output the value of a fact.
- **`setup`**: To gather all facts (only needed if you're outputting default system facts).

Using this approach, you can easily set and output facts within your Ansible playbooks.
