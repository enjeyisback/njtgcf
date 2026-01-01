import os
import sys
import subprocess
def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True
def fix_installation():
    print("--- TGCF Server Fixer (Root/Absolute Path Version) ---")
    
    current_dir = os.getcwd() # Should be /home/ubuntu/njtgcf
    print(f"Current Directory (Source Code): {current_dir}")
    
    # HARDCODED TARGET VENV based on your traceback
    # Traceback said imports came from here:
    target_venv = "/home/ubuntu/tgcf/.venv"
    
    print(f"Target Venv: {target_venv}")
    python_exe = os.path.join(target_venv, "bin", "python3")
    pip_exe = os.path.join(target_venv, "bin", "pip")
    if not os.path.exists(python_exe):
        print(f"Error: Could not find virtual environment at {target_venv}")
        print("Checking for local .venv in current directory...")
        local_venv = os.path.join(current_dir, ".venv")
        if os.path.exists(os.path.join(local_venv, "bin", "python3")):
            print(f"Found local venv at {local_venv}. Using that instead.")
            python_exe = os.path.join(local_venv, "bin", "python3")
            pip_exe = os.path.join(local_venv, "bin", "pip")
        else:
            print("No suitable venv found. Please ensure you have a venv.")
            return
    print(f"Using Python: {python_exe}")
    
    # 1. Uninstall existing tgcf from that venv to check libraries
    print("\nStep 1: Uninstalling old tgcf package (if exists)...")
    run_command(f"{pip_exe} uninstall -y tgcf")
    
    # 2. Install CURRENT directory in editable mode into THAT venv
    print(f"\nStep 2: Installing {current_dir} in editable mode...")
    if run_command(f"{pip_exe} install -e ."):
        print("\nSuccess! Package installed.")
    else:
        print("\nFailed to install package.")
        return
    # 3. Restart Service
    print("\nStep 3: Restarting Service...")
    run_command("systemctl restart tgcf")
    print("Service restarted.")
if __name__ == "__main__":
    fix_installation()
