import os
import re
from pathlib import Path

print("=" * 80)
print("CHECKING FOR DEPRECATED CODE PATTERNS")
print("=" * 80)

issues = []

def check_file(filepath):
    """Check a single Python file for deprecated patterns."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Check for pydantic import issues (old style)
    if 'from pydantic import' in content:
        for i, line in enumerate(lines, 1):
            # Check for old-style validator imports that might need updating
            if 'pydantic' in line and 'validator' in line:
                issues.append({
                    'file': filepath,
                    'line': i,
                    'type': 'Pydantic',
                    'message': 'Validator import - check compatibility with pydantic 2.x migration',
                    'code': line.strip()
                })
    
    # Check for telethon deprecated patterns
    deprecated_telethon = [
        (r'\.get_peer_id\(', 'get_peer_id() may have newer alternatives'),
        (r'StringSession\(', 'StringSession usage - verify with Telethon 1.42+'),
    ]
    
    for pattern, message in deprecated_telethon:
        if re.search(pattern, content):
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    issues.append({
                        'file': filepath,
                        'line': i,
                        'type': 'Telethon',
                        'message': message,
                        'code': line.strip()
                    })
    
    # Check for old Python patterns
    if 'from typing import' in content:
        for i, line in enumerate(lines, 1):
            # Check for Optional, Union usage that could use | syntax (Python 3.10+)
            if 'Optional[' in line or 'Union[' in line:
                issues.append({
                    'file': filepath,
                    'line': i,
                    'type': 'Python 3.10+',
                    'message': 'Can use | syntax instead of Optional/Union (Python 3.10+)',
                    'code': line.strip()
                })
                break  # Only report once per file
    
    # Check for old asyncio patterns
    if 'asyncio.run(' in content or 'async def' in content:
        for i, line in enumerate(lines, 1):
            if 'asyncio.get_event_loop()' in line:
                issues.append({
                    'file': filepath,
                    'line': i,
                    'type': 'Asyncio',
                    'message': 'asyncio.get_event_loop() is deprecated, use asyncio.run()',
                    'code': line.strip()
                })

# Scan all Python files
python_files = list(Path('/home/ubuntu/tgcf_analysis/tgcf').glob('**/*.py'))

for filepath in python_files:
    check_file(filepath)

# Group and display issues
from collections import defaultdict
issues_by_type = defaultdict(list)
for issue in issues:
    issues_by_type[issue['type']].append(issue)

print(f"\nFound {len(issues)} potential deprecation issues:\n")

for issue_type, type_issues in issues_by_type.items():
    print(f"\n{issue_type} Issues ({len(type_issues)}):")
    # Show unique files
    files = set(issue['file'].relative_to(Path('/home/ubuntu/tgcf_analysis')) for issue in type_issues)
    for file in sorted(files):
        count = sum(1 for i in type_issues if i['file'].relative_to(Path('/home/ubuntu/tgcf_analysis')) == file)
        print(f"  • {file}: {count} occurrence(s)")

print("\n" + "=" * 80)
print("Check complete. Review these patterns when migrating to newer versions.")
print("=" * 80)

