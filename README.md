# ⚡ Ansible AWS AIOps Monitor & Auto-Remediation Engine

> An automated VM health monitor, CPU diagnostic engine, and self-healing incident remediation pipeline using Ansible, Python (`boto3`, `paramiko`), and AWS Dynamic Inventory.

---

## 📑 Table of Contents

* [Project Overview](#-project-overview)
* [Architecture](#-architecture)
* [Key Features](#-key-features)
* [Project Directory Structure](#-project-directory-structure)
* [Prerequisites](#-prerequisites)
* [Step-by-Step Implementation Guide](#-step-by-step-implementation-guide)
  * [Step 1: Set Up Python Virtual Environment](#step-1-set-up-python-virtual-environment)
  * [Step 2: Run Unit Tests (`pytest` + `moto`)](#step-2-run-unit-tests-pytest--moto)
  * [Step 3: AWS Configuration & Sequential Node Tagging](#step-3-aws-configuration--sequential-node-tagging)
  * [Step 4: Dynamic Inventory Discovery](#step-4-dynamic-inventory-discovery)
  * [Step 5: SMTP Alert Notification Setup](#step-5-smtp-alert-notification-setup)
  * [Step 6: Run the Master Automation Pipeline](#step-6-run-the-master-automation-pipeline)
  * [Step 7: Automate via Cron Schedule](#step-7-automate-via-cron-schedule)
* [Troubleshooting & Diagnostics](#-troubleshooting--diagnostics)
* [Sample Execution Outputs](#-sample-execution-outputs)

---

## 📌 Project Overview

Monitoring cloud virtual machines requires moving beyond passive alert notifications to active **self-healing infrastructure**. 

This repository provides an agentless, production-ready automation framework that:
1. **Discovers** AWS EC2 instances dynamically using cloud tags.
2. **Audits** system metrics (CPU %, Memory %, Disk %) and isolates CPU process offenders when usage spikes above 80%.
3. **Remediates** incidents automatically (cleans disk caches, restarts web services, or terminates runaway process PIDs).
4. **Dispatches** animated HTML alert emails detailing performance metrics, process diagnostics, and remediation actions taken.

---

## 🏗️ Architecture

```text
               +----------------------------------+
               |        AWS EC2 Instances         |
               |     (Tagged: Environment=dev)    |
               +----------------+-----------------+
                                |
                                | AWS API Discovery
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
## ✨ Key Features

🏷️ Dynamic AWS EC2 Discovery: Automatically targets running EC2 instances filtered by cloud tags (Environment=dev).

🔎 In-Depth CPU Process Diagnostics: When CPU exceeds 80%, captures the Top 3 PID offenders (process name, user, CPU usage) and breaks down load types (%user, %system, %iowait).

⚡ Self-Healing Auto-Remediation:

Disk > 85%: Cleans APT package caches and truncates journalctl logs.

CPU 80% – 95%: Restarts web application services (e.g., Nginx).

CPU > 95%: Safely terminates runaway CPU hogging processes.

📧 Animated HTML Email Alerts: Delivers card-based email alerts showing metrics, CPU diagnostic boxes, and remediation summaries.

🧪 Mock-backed Unit Testing (moto): Runs offline unit tests with pytest without invoking live AWS resources or incurring cloud costs.

---

## 📂 Project Directory Structure

```
ansible-aws-aiops-monitor/
├── .github/
│   └── workflows/              # GitHub Actions CI/CD configuration
├── group_vars/
│   └── all.yaml                # Global SMTP & notification credentials
├── inventory/
│   └── aws_ec2.yaml            # AWS EC2 dynamic inventory configuration
├── scripts/
│   ├── tag_instances.py        # Sequentially tags EC2 instances (web-01, web-02)
│   └── remediate.py            # Boto3 function to reboot unreachable instances
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
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation

```
---

## ⚙️ Prerequisites

```

Before executing the pipeline, ensure you have:

Linux / WSL / MacOS Control Node

Python 3.10+ and python3-venv

AWS Account with running EC2 instances tagged as Environment=dev

AWS CLI configured (aws configure) with valid Access & Secret Keys

SMTP Credentials (e.g., Gmail address + App Password)

```
---

### 🛠️ Step-by-Step Implementation Guide

## Step 1: Set Up Python Virtual Environment

```
Clone the repository and install all required Python dependencies and Ansible collections:

# 1. Initialize Python virtual environment
python3 -m venv ansible-env

# 2. Activate virtual environment
source ansible-env/bin/activate

# 3. Install required Python modules
pip install -r requirements.txt

# 4. Install required Ansible Galaxy collections
ansible-galaxy collection install amazon.aws community.general

```
---

## Step 2: Run Unit Tests (pytest + moto)

Before running playbooks against live AWS infrastructure, run the unit test suite to verify the Python EC2 reboot logic offline.
```
pytest -v

```
Note: moto intercepts all boto3 AWS API calls in memory, ensuring zero cloud calls or costs during testing.
---

---
## Step 3: AWS Configuration & Sequential Node Tagging

1. Ensure your AWS credentials are set up:
```
     aws configure
```
2. Execute scripts/tag_instances.py to assign sequential Name tags (web-01, web-02, ...) to running Environment=dev instances:
```
./scripts/tag_instances.py

```
---

## Step 4: Dynamic Inventory Discovery

Confirm that Ansible's dynamic inventory plugin can query AWS and detect your instances:
```
ansible-inventory -i inventory/aws_ec2.yaml --graph

```
Expected Output:

```
@all:
  |--@aws_ec2:
  |  |--web-01
  |  |--web-02

```
---

## Step 5: SMTP Alert Notification Setup

Update group_vars/all.yaml with your SMTP server credentials:
```
smtp_server: smtp.gmail.com
smtp_port: 587
sender_email: "your-email@gmail.com"
receiver_email: "admin-alert@gmail.com"
smtp_username: "your-email@gmail.com"
smtp_password: "your-16-digit-app-password"  # Google App Password

```

---

## Step 6: Run the Master Automation Pipeline

Execute the master orchestrator playbook. It will gather telemetry, diagnose CPU spikes, execute self-healing tasks if thresholds are breached, and dispatch the HTML alert email.

```
ansible-playbook playbook.yaml
```

---

## Step 7: Automate via Cron Schedule
To run the monitoring and self-healing engine continuously every hour, add a crontab entry:

```
crontab -e
```
Add the following schedule line:

```
0 * * * * /bin/bash -c "source /path/to/ansible-env/bin/activate && ansible-playbook /path/to/ansible-aws-aiops-monitor/playbook.yaml"

```

---

### 🧪 Troubleshooting & Diagnostics
```
Problem  Root Cause  Resolution
Host Unreachable via SSHMissing private key or closed Security GroupEnsure AWS Security Group allows inbound SSH (Port 22) from your Control Node IP.
boto3 / botocore missingAnsible running outside virtual environmentEnsure you run source ansible-env/bin/activate before executing playbooks.
Dynamic Inventory EmptyAWS tag mismatch or wrong regionVerify instances have Environment=dev tags and are in running state. Confirm the region in inventory/aws_ec2.yaml.
Email Not ArrivingInvalid SMTP credentials or blocked portConfirm port 587 is open outbound. For Gmail, ensure you are using an App Password, not your main Google account password.

```
---
### 📊 Sample Execution Outputs

Master Playbook Output
```
PLAY [Collect Performance Telemetry & CPU Diagnostics] ************************************
ok: [web-01]

TASK [Capture Top CPU Processes (if CPU > 80%)] ******************************************
changed: [web-01]

PLAY [Execute Automated Incident Remediation] ********************************************
changed: [web-01] => (item=Restarted Nginx service)

PLAY [Dispatch Alert Report] *************************************************************
changed: [localhost] => (Compiled HTML & dispatched email)
```

---

### Generated Email Alert

```

**Hostname,🔥 CPU Usage & Diagnostics,📥 Memory,📦 Disk,⚡ Auto-Remediation Status
web-01,"83.4%🔴 CRITICAL🔥 Top CPU Processes:• www-data, PID: 14201, CPU: 72.1% (nginx)📊 Load: User: 78.2%, System: 4.1%, IOwait: 1.1%",45%,41%,⚙️ Restarted Nginx service.
web-02,25.0%🟢 HEALTHY,40%,35%,No action required**

```
---


   
