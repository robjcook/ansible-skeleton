To implement logging and configure multiple `rsync` services in parallel using Ansible and the `systemd` timer method, follow these steps:

---

### **1. Configure Systemd Service with Logging**

Modify the `rsync` service to include logging to a file.

#### Example `rsync-backup.service` with Logging:
```ini
[Unit]
Description=Rsync Backup Service for %i

[Service]
Type=oneshot
ExecStart=/usr/bin/rsync -avz /path/to/source/%i/ user@remote:/path/to/destination/%i/ > /var/log/rsync-%i.log 2>&1
```

- `%i` is a **template parameter**, allowing the service to handle multiple backups dynamically. Each instance (e.g., `rsync-backup@service1`) uses `%i` for differentiation.
- Logs are saved to `/var/log/rsync-%i.log` (e.g., `rsync-service1.log`).

---

### **2. Configure Systemd Timer**

#### Example `rsync-backup@.timer`:
```ini
[Unit]
Description=Timer for Rsync Backup Service for %i

[Timer]
OnCalendar=*:0/10
Persistent=true

[Install]
WantedBy=timers.target
```

- The `@` symbol in `rsync-backup@.timer` allows multiple timer instances to run in parallel.

---

### **3. Ansible Code to Deploy Multiple Rsync Services**

Here's an Ansible playbook that sets up multiple `rsync` services and timers in parallel with logging.

#### **Playbook: `rsync_systemd.yml`**
```yaml
---
- name: Setup Rsync Backup with Systemd Timers
  hosts: all
  become: yes

  vars:
    rsync_services:
      - name: service1
        source_path: /path/to/source/service1/
        dest_path: user@remote:/path/to/destination/service1/
        interval: "0/10"  # Every 10 minutes
      - name: service2
        source_path: /path/to/source/service2/
        dest_path: user@remote:/path/to/destination/service2/
        interval: "0/5"  # Every 5 minutes

  tasks:
    - name: Create systemd service file for rsync
      copy:
        dest: "/etc/systemd/system/rsync-backup@.service"
        content: |
          [Unit]
          Description=Rsync Backup Service for %i

          [Service]
          Type=oneshot
          ExecStart=/usr/bin/rsync -avz {{ source_path }}/%i/ {{ dest_path }}/%i/ > /var/log/rsync-%i.log 2>&1

    - name: Create systemd timer file for rsync
      copy:
        dest: "/etc/systemd/system/rsync-backup@.timer"
        content: |
          [Unit]
          Description=Timer for Rsync Backup Service for %i

          [Timer]
          OnCalendar=*:{{ item.interval }}
          Persistent=true

          [Install]
          WantedBy=timers.target
      loop: "{{ rsync_services }}"
      loop_control:
        loop_var: item

    - name: Reload systemd daemon
      command: systemctl daemon-reload

    - name: Enable and start rsync timer for each service
      systemd:
        name: "rsync-backup@{{ item.name }}.timer"
        state: started
        enabled: true
      loop: "{{ rsync_services }}"
      loop_control:
        loop_var: item
```

---

### **4. Explanation of the Ansible Playbook**

1. **Variables**:
   - `rsync_services` defines multiple `rsync` tasks, with:
     - `name`: Unique name for each service.
     - `source_path` and `dest_path`: Paths for synchronization.
     - `interval`: Timer interval (e.g., every 10 minutes).

2. **Tasks**:
   - **Create Service File**: Deploys a parameterized `rsync-backup@.service` template.
   - **Create Timer File**: Deploys a parameterized `rsync-backup@.timer` template with custom intervals.
   - **Reload Systemd**: Ensures new services and timers are recognized.
   - **Enable and Start Timers**: Activates timers for all defined services.

3. **Logging**:
   - Each service logs output to `/var/log/rsync-service_name.log`.

---

### **5. Verification**

1. Run the playbook:
   ```bash
   ansible-playbook -i inventory rsync_systemd.yml
   ```

2. Check systemd timers:
   ```bash
   systemctl list-timers --all
   ```

3. Verify logs:
   ```bash
   cat /var/log/rsync-service1.log
   cat /var/log/rsync-service2.log
   ```

---

### **6. Advantages of This Setup**
- **Parallel Services**: Each `rsync` service runs independently and simultaneously.
- **Custom Intervals**: Use different schedules for each backup task.
- **Centralized Logging**: Easily monitor output and errors for each service.
