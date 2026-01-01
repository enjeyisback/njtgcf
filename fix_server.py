import os
import sys
import subprocess
import site
def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True
def fix_installation():
    print("--- TGCF Server Fixer ---")
    
    # 1. Identify where we are
    current_dir = os.getcwd()
    print(f"Current Directory: {current_dir}")
    
    # 2. Check stricture
    if not os.path.basename(current_dir) in ['njtgcf', 'tgcf']:
        print("WARNING: You might be in the wrong directory. Expected 'njtgcf' or 'tgcf'.")
    
    # 3. Target Virtual Environment
    # The traceback showed usage of ~/tgcf/.venv
    target_venv = os.path.expanduser("~/tgcf/.venv")
    python_exe = os.path.join(target_venv, "bin", "python3")
    pip_exe = os.path.join(target_venv, "bin", "pip")
    if not os.path.exists(python_exe):
        print(f"Error: Could not find virtual environment at {target_venv}")
        print("Please verify where your service is pointing.")
        return
    print(f"Target Python: {python_exe}")
    
    # 4. Uninstall existing tgcf from that venv
    print("\nStep 1: Uninstalling old tgcf package...")
    run_command(f"{pip_exe} uninstall -y tgcf")
    
    # 5. Install CURRENT directory in editable mode into THAT venv
    print(f"\nStep 2: Installing {current_dir} in editable mode...")
    if run_command(f"{pip_exe} install -e ."):
        print("\nSuccess! Package installed.")
    else:
        print("\nFailed to install package.")
        return
    # 6. Verify Import
    print("\nStep 3: Verifying import...")
    verify_cmd = f"{python_exe} -c \"from tgcf.web_ui.utils import switch_theme; print('Verification: switch_theme found!')\""
    run_command(verify_cmd)
    # 7. Restart Service
    print("\nStep 4: Restarting Service...")
    run_command("sudo systemctl restart tgcf")
    print("Service restarted.")
if __name__ == "__main__":
    fix_installation()