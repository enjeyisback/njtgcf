import json
import subprocess
import sys
from packaging import version

# Current dependencies from pyproject.toml
current_deps = {
    "requests": "^2.28.1",
    "typer": "^0.7.0",
    "python-dotenv": "^0.21.0",
    "pydantic": "^1.10.2",
    "Telethon": "1.26.0",
    "cryptg": "^0.4.0",
    "Pillow": ">=9.3,<11.0",
    "hachoir": "^3.1.3",
    "aiohttp": "^3.8.3",
    "tg-login": "^0.0.4",
    "watermark.py": "^0.0.3",
    "pytesseract": "^0.3.7",
    "rich": "^12.6.0",
    "verlat": "^0.1.0",
    "streamlit": "^1.15.2",
    "PyYAML": "^6.0",
    "pymongo": "^4.3.3"
}

print("=" * 80)
print("DEPENDENCY ANALYSIS FOR TGCF")
print("=" * 80)
print("\nChecking for latest versions of each package...\n")

results = []

for package, current_ver in current_deps.items():
    try:
        # Get latest version from PyPI
        result = subprocess.run(
            [sys.executable, "-m", "pip", "index", "versions", package],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Available versions:' in line:
                    versions = line.split(':')[1].strip().split(',')
                    latest = versions[0].strip()
                    results.append({
                        'package': package,
                        'current': current_ver,
                        'latest': latest
                    })
                    print(f"{package:20} | Current: {current_ver:15} | Latest: {latest}")
                    break
    except Exception as e:
        print(f"Error checking {package}: {e}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)

