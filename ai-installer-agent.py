import subprocess
import requests
import shutil
import re
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1"

MAX_RETRIES = 3
APT_UPDATED = False

BLOCKED_COMMANDS = [
    "rm -rf /",
    "mkfs",
    "dd ",
    "shutdown",
    "reboot",
    "poweroff",
    "halt"
]


############################################################
# SAFETY CHECK
############################################################

def safe_command(cmd):

    c = cmd.lower()

    for bad in BLOCKED_COMMANDS:
        if bad in c:
            return False

    return True


############################################################
# RUN COMMAND
############################################################

def run_command(cmd):

    print("\n>>>", cmd)

    try:

        process = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )

        output = process.stdout + process.stderr

        print(output)

        return process.returncode, output

    except Exception as e:

        return 1, str(e)


############################################################
# CHECK OLLAMA
############################################################

def check_ollama():

    try:
        r = requests.get("http://localhost:11434")
        return r.status_code == 200
    except:
        return False


############################################################
# AI REQUEST
############################################################

def ask_ai(prompt):

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:

        r = requests.post(OLLAMA_URL, json=data, timeout=120)

        return r.json()["response"]

    except:

        return ""


############################################################
# CLEAN AI OUTPUT
############################################################

def clean_commands(text):

    commands = []

    for line in text.split("\n"):

        line = line.replace("```", "")
        line = line.replace("bash", "")
        line = line.strip()

        line = re.sub(r'^\d+[\.\)]', '', line)

        if line and safe_command(line):

            commands.append(line.strip())

    return commands


############################################################
# CHECK TOOL
############################################################

def exists(tool):

    return shutil.which(tool) is not None


############################################################
# INSTALLERS
############################################################

def apt_install(pkg):

    global APT_UPDATED

    if not APT_UPDATED:

        run_command("apt update -y")
        APT_UPDATED = True

    return run_command(
        f"DEBIAN_FRONTEND=noninteractive apt install -y {pkg}"
    )


def pip_install(pkg):

    if not exists("pip3"):
        run_command("apt install -y python3-pip")

    return run_command(f"pip3 install {pkg}")


def npm_install(pkg):

    if not exists("npm"):
        run_command("apt install -y npm")

    return run_command(f"npm install -g {pkg}")


def snap_install(pkg):

    if not exists("snap"):
        run_command("apt install -y snapd")

    return run_command(f"snap install {pkg}")


def cargo_install(pkg):

    if not exists("cargo"):
        run_command("apt install -y cargo")

    return run_command(f"cargo install {pkg}")


############################################################
# TRY INSTALLERS
############################################################

def try_installers(pkg):

    installers = [

        ("apt", apt_install),
        ("snap", snap_install),
        ("pip", pip_install),
        ("npm", npm_install),
        ("cargo", cargo_install)
    ]

    for name, installer in installers:

        print(f"\nTrying {name} installer...\n")

        code, output = installer(pkg)

        if code == 0:

            print(f"\nSUCCESS installing {pkg} via {name}\n")

            return True, output

    return False, output


############################################################
# AI INSTALL PLAN
############################################################

def ai_install_plan(pkg):

    prompt = f"""
You are a Linux DevOps engineer.

Install software: {pkg}

Return shell commands only.

Rules:
one command per line
no explanation
always use -y
non-interactive
"""

    response = ask_ai(prompt)

    return clean_commands(response)


############################################################
# AI FIX
############################################################

def ai_fix(error, pkg):

    prompt = f"""
Installation of {pkg} failed.

Error log:

{error}

Return ONE shell command to fix the issue.

Command only.
"""

    response = ask_ai(prompt)

    commands = clean_commands(response)

    if commands:
        return commands[0]

    return None


############################################################
# INSTALL LOGIC
############################################################

def install_package(pkg):

    print(f"\n===== Installing {pkg} =====\n")

    plan = ai_install_plan(pkg)

    if plan:

        print("AI suggested plan:\n")

        for step in plan:

            code, output = run_command(step)

            if code != 0:

                print("\nAI plan failed\n")
                break

        else:

            print(f"\nInstalled {pkg} successfully via AI plan\n")
            return


    print("\nUsing fallback installers\n")

    success, last_error = try_installers(pkg)

    if success:
        return


    retry = 0

    while retry < MAX_RETRIES:

        fix = ai_fix(last_error, pkg)

        if not fix:
            break

        print("\nAI suggested fix:\n", fix)

        run_command(fix)

        success, last_error = try_installers(pkg)

        if success:
            return

        retry += 1


    print(f"\nFailed to install {pkg}\n")


############################################################
# MAIN
############################################################

def main():

    print("\n===== SMART AI SOFTWARE INSTALLER =====\n")

    if not check_ollama():

        print("Ollama is not running.")
        print("Run: ollama run llama3.1")
        return


    user_input = input(
        "Enter software names to install (space separated): "
    ).strip()

    if not user_input:

        print("No software specified.")
        return


    packages = user_input.split()


    for pkg in packages:

        install_package(pkg)

        time.sleep(1)


    print("\nAll tasks completed.\n")


if __name__ == "__main__":
    main()
