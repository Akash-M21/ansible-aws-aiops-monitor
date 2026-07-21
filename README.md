# ⚡ Ansible AWS AIOps Monitor & Auto-Remediation Engine

<p align="center">

![Ansible](https://img.shields.io/badge/Ansible-Automation-red?logo=ansible)
![AWS](https://img.shields.io/badge/AWS-EC2-orange?logo=amazonaws)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Production-success)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

> **Agentless infrastructure monitoring, automated incident remediation, and HTML reporting for AWS EC2 using Ansible, Python, boto3, Paramiko, and Dynamic Inventory.**

---

# 📑 Table of Contents

- Project Overview
- Architecture
- Workflow
- Key Features
- Tech Stack
- Project Structure
- Prerequisites
- Implementation Guide
- Troubleshooting
- Sample Output
- Future Enhancements
- License

---

# 📌 Project Overview

This project provides an automated AIOps workflow for AWS EC2 instances.

It automatically:

- Discovers EC2 instances using AWS Dynamic Inventory
- Collects CPU, Memory and Disk metrics
- Detects abnormal CPU usage
- Performs automated remediation
- Generates HTML reports
- Sends email notifications

---

# 🏗️ Architecture

```text
AWS EC2
   │
   ▼
Dynamic Inventory
   │
   ▼
Collect Metrics
   │
   ▼
CPU Diagnostics
   │
   ▼
Auto Remediation
   │
   ▼
Generate HTML Report
   │
   ▼
Email Notification
```

---

# 🔄 Workflow

```text
Discover Instances
      │
Collect Metrics
      │
CPU Analysis
      │
Auto Remediation
      │
Generate HTML Report
      │
Send Email
```

---

# ✨ Key Features

- 🏷 Dynamic AWS EC2 Discovery
- 📊 CPU / Memory / Disk Monitoring
- 🔍 Top CPU Process Diagnostics
- ⚡ Automatic Self-Healing
- 📧 HTML Email Reports
- 🧪 Offline Testing using pytest + moto

---

# 🛠 Tech Stack

- Ansible
- AWS EC2
- Python
- boto3
- Paramiko
- Jinja2
- SMTP
- Pytest
- Moto

---

# 📂 Project Structure

```text
ansible-aws-aiops-monitor/
├── .github/
├── group_vars/
├── inventory/
├── scripts/
├── tasks/
├── templates/
├── tests/
├── ansible.cfg
├── collect_metrics.yaml
├── playbook.yaml
├── send_report.yaml
├── requirements.txt
└── README.md
```

---

# ⚙️ Prerequisites

- [ ] Linux / WSL / macOS
- [ ] Python 3.10+
- [ ] Ansible
- [ ] AWS CLI configured
- [ ] EC2 instances tagged `Environment=dev`
- [ ] SMTP credentials

---

# 🚀 Implementation Guide

## 1. Create Virtual Environment

```bash
python3 -m venv ansible-env
source ansible-env/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install amazon.aws community.general
```

## 2. Run Unit Tests

```bash
pytest -v
```

## 3. Configure AWS

```bash
aws configure
./scripts/tag_instances.py
```

## 4. Verify Inventory

```bash
ansible-inventory -i inventory/aws_ec2.yaml --graph
```

## 5. Configure SMTP

```yaml
smtp_server: smtp.gmail.com
smtp_port: 587
sender_email: your-email@gmail.com
receiver_email: admin@example.com
smtp_username: your-email@gmail.com
smtp_password: your-app-password
```

## 6. Execute

```bash
ansible-playbook playbook.yaml
```

## 7. Schedule

```bash
0 * * * * /bin/bash -c "source /path/to/ansible-env/bin/activate && ansible-playbook /path/to/playbook.yaml"
```

---

# 🧰 Troubleshooting

| Problem | Cause | Resolution |
|---------|-------|------------|
| SSH Failure | SG blocks port 22 | Allow SSH |
| Empty Inventory | Wrong tags/region | Verify Environment=dev |
| boto3 Missing | venv inactive | Activate environment |
| Email Failure | Invalid SMTP | Use App Password |

---

# 📊 Sample Output

```console
PLAY [Collect Metrics]

TASK [CPU Diagnostics]
changed: [web-01]

TASK [Auto Remediation]
changed: [web-01]

TASK [Send Email]
ok: [localhost]
```

| Host | CPU | Memory | Disk | Action |
|------|----:|-------:|----:|--------|
| web-01 | 🔴83% |45%|41%|Restarted Nginx |
| web-02 | 🟢25% |40%|35%|No Action |

---

# 🚀 Future Enhancements

- CloudWatch Integration
- Slack Notifications
- Grafana Dashboards
- Prometheus Export
- Multi-region Support

---

# 👨‍💻 Author

**Akash M**

DevOps Engineer • AWS • Terraform • Docker • Kubernetes • Ansible • Python
