import os
import subprocess
import shutil
import time
def run_cmd(cmd, shell=True):
    print(f"[EXEC] {cmd}")
    res = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
    if res.stdout: print(res.stdout.strip())
    if res.stderr: print(f"[ERR] {res.stderr.strip()}")
    return res.returncode == 0
def clean_reinstall():
    print("=== TGCF Clean Reinstall Tool ===")
    
    # 1. Stop everything
    print("\n--- Step 1: Stopping existing processes ---")
    run_cmd("pkill -f streamlit")
    run_cmd("pkill -f tgcf")
    run_cmd("tmux kill-session -t tgcf-service 2>/dev/null")
    time.sleep(2)
    
    # 2. Clean old environments
    # We want to use ~/njtgcf, so let's clean the confusing ~/tgcf/.venv if it exists
    print("\n--- Step 2: Cleaning old environments ---")
    old_venv = os.path.expanduser("~/tgcf/.venv")
    if os.path.exists(old_venv):
        print(f"Removing old venv: {old_venv}")
        shutil.rmtree(old_venv, ignore_errors=True)
        
    # Clean local .venv in current dir if exists
    if os.path.exists(".venv"):
        print("Removing local .venv")
        shutil.rmtree(".venv", ignore_errors=True)
    # 3. Setup New Environment
    print("\n--- Step 3: Setting up fresh environment ---")
    if not run_cmd("python3 -m venv .venv"):
        print("Failed to create venv!")
        return
    pip = ".venv/bin/pip"
    
    # 4. Install
    print("\n--- Step 4: Installing dependencies (this may take a minute) ---")
    run_cmd(f"{pip} install -U pip wheel setuptools")
    if not run_cmd(f"{pip} install -e ."):
        print("Failed to install tgcf!")
        return
    # 5. Start
    print("\n--- Step 5: Starting Application ---")
    # Using the existing start script but ensuring it uses our new venv
    # We need to make sure tgcf-start.sh uses 'poetry run' or we bypass it.
    # Since we aren't using poetry explicitly here (we used pip venv), 
    # let's write a simple start command or use the direct python launch.
    
    # Let's try to launch it in tmux directly
    check_tmux = run_cmd("tmux new-session -d -s tgcf-service '.venv/bin/tgcf-web'")
    
    if check_tmux:
        print("\nSUCCESS! Application started in tmux session 'tgcf-service'.")
        print("You can verify by visiting your site.")
        print("View logs with: tmux attach -t tgcf-service")
    else:
        print("\nApplication installed but failed to auto-start in tmux.")
        print("Try running manually: source .venv/bin/activate && tgcf-web")
if __name__ == "__main__":
    # Ensure we are in the project dir
    if not os.path.exists("setup.py") and not os.path.exists("pyproject.toml"):
        print("ERROR: Please run this script from inside the njtgcf folder.")
    else:
        clean_reinstall()
