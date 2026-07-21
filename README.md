# ⚡ Ansible AWS AIOps Monitor & Auto-Remediation Engine

<p align="center">

![Ansible](https://img.shields.io/badge/Ansible-E00000?style=for-the-badge&logo=ansible&logoColor=white)
![AWS](https://img.shields.io/badge/AWS_EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge)

</p>

> **Agentless infrastructure monitoring, automated incident remediation, and HTML reporting for AWS EC2 using Ansible, Python, boto3, Paramiko, and Dynamic Inventory.**

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Workflow](#-workflow)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Implementation Guide](#-implementation-guide)
- [Troubleshooting](#-troubleshooting)
- [Sample Output](#-sample-output)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

---

## 📌 Project Overview

This project provides an automated AIOps workflow for AWS EC2 instances to move beyond passive monitoring to active **self-healing infrastructure**.

It automatically:
- **Discovers** EC2 instances dynamically using AWS Dynamic Inventory filters.
- **Collects** CPU, Memory, and Disk utilization metrics.
- **Isolates** abnormal CPU spikes and top process PID offenders.
- **Executes** self-healing auto-remediation (disk cleanup, service restarts, process termination).
- **Compiles** an animated HTML performance and incident report.
- **Dispatches** email notifications via SMTP.

---

## 🏗️ Architecture

```text
               +----------------------------------+
               |        AWS EC2 Instances         |
               |     (Tagged: Environment=dev)    |
               +----------------+-----------------+
                                |
                                | Dynamic Inventory Discovery
                                v
               +----------------------------------+
               |  Ansible Dynamic Inventory Plugin |
               |     (inventory/aws_ec2.yaml)     |
               +----------------+-----------------+
                                |
                                v
               +----------------------------------+
               |      Ansible Control Node        |
               +----------------+-----------------+
                                |
                   playbook.yaml Orchestrator
                                |
         +----------------------+----------------------+
         |                      |                      |
         v                      v                      v
+------------------+  +------------------+  +------------------+
|collect_metrics.yaml| |auto_remediation  | | send_report.yaml |
|                  |  |      .yaml       |  |                  |
| - CPU % & Top 3  |  | - Disk Clean (>85%)| | - Jinja2 Template|
|   Process PIDs   |  | - Service Restart|  |   Compilation    |
| - Memory & Disk  |  |   (CPU > 80%)    |  | - SMTP Mail Alert|
| - Load Breakdown |  | - Process Kill   |  |   Dispatch       |
|   (%us, %sy, %wa)|  |   (CPU > 95%)    |  |                  |
+------------------+  +------------------+  +------------------+
```

---

## 🔄 Workflow

```text
  [ Discover Instances ] ──► Filter EC2 tags (Environment=dev)
           │
           ▼
  [ Collect Telemetry ] ──► Audit CPU %, Memory %, Disk %
           │
           ▼
  [ CPU Diagnostics ]   ──► Extract Top 3 Process PIDs & Load Type (%us, %sy, %wa)
           │
           ▼
  [ Auto-Remediation ]  ──► Trigger automated cleanup, service restart, or kill
           │
           ▼
  [ HTML Rendering ]    ──► Compile Jinja2 animated email template
           │
           ▼
  [ Dispatch Alert ]    ──► Send SMTP notification report
```

---

## ✨ Key Features

- 🏷️ **Dynamic AWS EC2 Discovery:** Automatically targets running EC2 instances using tag filters (`Environment=dev`).
- 📊 **Resource Telemetry:** Real-time tracking for CPU, Memory, and Disk volume usage.
- 🔍 **Top CPU Process Diagnostics:** Captures top PID offenders, users, and CPU load breakdown when CPU breaches 80%.
- ⚡ **Automatic Self-Healing:**
  - **Disk > 85%:** Cleans APT caches and truncates system logs.
  - **CPU 80%–95%:** Restarts web application services (e.g., Nginx).
  - **CPU > 95%:** Safely terminates runaway CPU hogging processes.
- 📧 **HTML Email Alerting:** Dispatches styled, card-based email alerts showing status badges and diagnostic logs.
- 🧪 **Offline Testing Framework:** Mock-backed unit tests using `pytest` and `moto` without incurring cloud charges.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Automation Engine** | Ansible |
| **Cloud Infrastructure** | AWS EC2, AWS Dynamic Inventory |
| **Scripting & SDKs** | Python 3.10+, `boto3`, `paramiko` |
| **Templates & Alerts** | Jinja2, SMTP Mail |
| **Testing Suite** | `pytest`, `moto[ec2]` |

---

## 📂 Project Structure

```text
ansible-aws-aiops-monitor/
├── .github/
│   └── workflows/              # GitHub Actions CI/CD pipeline
├── group_vars/
│   └── all.yaml                # Global SMTP & credential configurations
├── inventory/
│   └── aws_ec2.yaml            # AWS EC2 dynamic inventory plugin setup
├── scripts/
│   ├── tag_instances.py        # Python/Boto3 script to sequentially tag nodes
│   └── remediate.py            # Python/Boto3 script to reboot unreachable instances
├── tasks/
│   └── auto_remediation.yaml   # Self-healing play tasks for disk & CPU issues
├── templates/
│   └── report_email_animated.html.j2 # Jinja2 HTML alert template
├── tests/
│   └── test_remediate.py       # Pytest unit tests backed by Moto
├── ansible.cfg                 # Ansible default settings
├── collect_metrics.yaml        # Metric gathering & CPU diagnostic playbook
├── playbook.yaml               # Master pipeline orchestrator
├── send_report.yaml            # Jinja2 rendering & email dispatch playbook
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## ⚙️ Prerequisites

- [x] Linux / WSL / macOS Control Node
- [x] Python 3.10+ and `python3-venv`
- [x] Ansible installed (`ansible --version`)
- [x] AWS CLI configured (`aws configure`) with valid credentials
- [x] Running AWS EC2 instances tagged as `Environment=dev`
- [x] SMTP credentials (e.g., Gmail App Password)

---

## 🚀 Implementation Guide

### 1. Create Virtual Environment

```bash
# Initialize and activate Python virtual environment
python3 -m venv ansible-env
source ansible-env/bin/activate

# Install dependencies and Galaxy collections
pip install -r requirements.txt
ansible-galaxy collection install amazon.aws community.general
```

### 2. Run Unit Tests

Execute offline unit tests to verify Boto3 remediation logic without touching live AWS resources:

```bash
pytest -v
```

### 3. Configure AWS & Tag Nodes

Assign sequential `Name` tags (`web-01`, `web-02`, ...) to running instances:

```bash
aws configure
./scripts/tag_instances.py
```

### 4. Verify Dynamic Inventory Discovery

```bash
ansible-inventory -i inventory/aws_ec2.yaml --graph
```

### 5. Configure SMTP Settings

Update `group_vars/all.yaml` with your SMTP account details:

```yaml
smtp_server: smtp.gmail.com
smtp_port: 587
sender_email: your-email@gmail.com
receiver_email: admin@example.com
smtp_username: your-email@gmail.com
smtp_password: your-16-digit-app-password
```

### 6. Execute Master Playbook

```bash
ansible-playbook playbook.yaml
```

### 7. Schedule Continuous Monitoring

Add a `crontab` entry to run the pipeline automatically every hour:

```cron
0 * * * * /bin/bash -c "source /path/to/ansible-env/bin/activate && ansible-playbook /path/to/ansible-aws-aiops-monitor/playbook.yaml"
```

---

## 🧰 Troubleshooting

| Problem | Likely Cause | Resolution |
| :--- | :--- | :--- |
| **SSH Failure** | Security Group blocking port 22 | Update AWS Security Group inbound rules to allow SSH from Control Node IP. |
| **Empty Inventory** | Mismatched tags or region | Verify target instances have `Environment=dev` tags and are in `running` state. |
| **`boto3` Missing** | Virtual environment not active | Run `source ansible-env/bin/activate` before executing playbooks. |
| **Email Failure** | Incorrect SMTP credentials | Use a 16-character **App Password** for Gmail instead of standard account password. |

---

## 📊 Sample Output

### Terminal Playbook Summary

```console
PLAY [Collect Metrics & CPU Diagnostics] ****************************************************
changed: [web-01]

PLAY [Execute Automated Incident Remediation] **********************************************
changed: [web-01] => (item=Restarted Nginx web service)

PLAY [Dispatch Alert Report] ***************************************************************
changed: [localhost] => (Compiled Jinja2 report & dispatched SMTP email)

PLAY RECAP *********************************************************************************
web-01                     : ok=8    changed=3    unreachable=0    failed=0
web-02                     : ok=5    changed=1    unreachable=0    failed=0
```

### HTML Email Notification Preview

| Host | CPU Usage & Diagnostics | Memory | Disk | Auto-Remediation Status |
| :--- | :--- | :---: | :---: | :--- |
| **web-01** | **🔴 83.4%** (Critical)<br>`Top PID: 14201 (nginx)` | 45% | 41% | ⚙️ **Restarted Nginx service** |
| **web-02** | **🟢 25.0%** (Healthy) | 40% | 35% | *No action required* |

---

## 🚀 Future Enhancements

- [ ] CloudWatch alarm integration for event-driven playbook triggers
- [ ] Slack & Microsoft Teams incoming webhook alert channels
- [ ] Prometheus metrics exporter compatibility
- [ ] Grafana operational dashboard templates
- [ ] Multi-region AWS deployment filtering support

---

## 👨‍💻 Author

**Akash M**  
DevOps Engineer • AWS • Terraform • Docker • Kubernetes • Ansible • Python
