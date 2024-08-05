To remove a line in a file that matches a specific string using Ansible, you can use the `lineinfile` module with the `state` set to `absent`. Here's an example of how you can do this:

### Playbook Example

```yaml
---
- name: Remove line from file
  hosts: localhost
  tasks:
    - name: Remove line containing specific string
      ansible.builtin.lineinfile:
        path: /path/to/your/file
        regexp: 'your_matching_string'
        state: absent
```

### Explanation:
- **`path`**: The path to the file from which you want to remove the line.
- **`regexp`**: The regular expression that matches the line you want to remove. This can be a plain string or a regex pattern.
- **`state`**: Setting this to `absent` tells Ansible to remove any line that matches the `regexp`.

### Example Usage:

Suppose you have a file `/etc/myconfig.conf` with the following content:

```
# some config options
option1=value1
option2=value2
# disable this feature
disable_feature=true
```

If you want to remove the line that contains `disable_feature=true`, your Ansible task would look like this:

```yaml
---
- name: Remove disable_feature line from myconfig.conf
  hosts: localhost
  tasks:
    - name: Remove line with disable_feature=true
      ansible.builtin.lineinfile:
        path: /etc/myconfig.conf
        regexp: '^disable_feature=true'
        state: absent
```

This would remove the line with `disable_feature=true` from the file.

