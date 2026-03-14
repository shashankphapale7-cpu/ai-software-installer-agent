# ai-software-installer-agent
This agent installs software in system using Ai
# AI Installer Agent


An **AI-powered installer-agent** that automatically installs software and its dependencies using a local AI model.

Instead of manually searching installation commands, this tool acts like a **local ai-installer-agent engineer** that installs software for you.

The system uses **Ollama** running **Llama 3.1** to:

* generate installation commands
* execute them automatically
* detect installation errors
* repair failed installations

---

# Features

• Install software by simply typing its name
• AI-generated installation commands
• Automatic dependency installation
• AI-based error repair
• Safe command filtering
• Works across multiple operating systems

Supported package managers:

* apt (Linux)
* brew (macOS)
* winget (Windows)
* pip
* npm

---

# Requirements

* Python 3
* Ollama
* Llama 3.1 model
* Python library: `requests`

Install dependency:

pip install requests

---

# Install Ollama

Install Ollama:

curl -fsSL https://ollama.com/install.sh | sh

Download the AI model:

ollama run llama3.1

---

# Run the Program

Run the script:

sudo python3 ai-installer-agent.py

Program output:

AI ai-installer-agent Engineer Running
Detected OS: linux

Then enter the software name:

Install software (exit to quit):

Example:

docker git nodejs

The agent automatically installs the software.

---

# Example Output

AI planning installation strategy...

sudo apt update
sudo apt install -y docker.io

Running commands...

SUCCESS via AI plan

---

# How It Works

1. User enters software name
2. AI generates installation commands
3. Commands execute automatically
4. Installation errors are detected
5. AI suggests repair commands
6. Installation retries until successful

---

# Safety System

Dangerous commands are blocked automatically.

Examples:

rm -rf /
mkfs
dd
shutdown
reboot
poweroff
fdisk

---

# Project Structure

ai-installer-agent.py

---

# Use Cases

This tool can be useful for:

* developer machine setup
* automated DevOps environments
* AI automation experiments
* learning AI system administration
* rapid software provisioning

---
