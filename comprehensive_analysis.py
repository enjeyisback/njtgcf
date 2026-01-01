import os
import ast
import re
from pathlib import Path
from collections import defaultdict

class CodeAnalyzer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.results = {
            'files': [],
            'total_lines': 0,
            'total_functions': 0,
            'total_classes': 0,
            'imports': defaultdict(int),
            'issues': [],
            'complexity': [],
            'documentation': {'with_docstring': 0, 'without_docstring': 0}
        }
    
    def analyze_file(self, filepath):
        """Analyze a single Python file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Parse AST
            tree = ast.parse(content, filename=str(filepath))
            
            file_info = {
                'path': str(filepath.relative_to(self.project_root)),
                'lines': len(lines),
                'functions': 0,
                'classes': 0,
                'imports': []
            }
            
            for node in ast.walk(tree):
                # Count functions
                if isinstance(node, ast.FunctionDef):
                    file_info['functions'] += 1
                    if ast.get_docstring(node):
                        self.results['documentation']['with_docstring'] += 1
                    else:
                        self.results['documentation']['without_docstring'] += 1
                
                # Count classes
                if isinstance(node, ast.ClassDef):
                    file_info['classes'] += 1
                
                # Track imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        file_info['imports'].append(alias.name)
                        self.results['imports'][alias.name] += 1
                
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        file_info['imports'].append(node.module)
                        self.results['imports'][node.module] += 1
            
            # Check for potential issues
            self.check_code_issues(content, filepath, lines)
            
            self.results['files'].append(file_info)
            self.results['total_lines'] += file_info['lines']
            self.results['total_functions'] += file_info['functions']
            self.results['total_classes'] += file_info['classes']
            
        except SyntaxError as e:
            self.results['issues'].append({
                'file': str(filepath),
                'type': 'SyntaxError',
                'message': str(e)
            })
        except Exception as e:
            self.results['issues'].append({
                'file': str(filepath),
                'type': 'AnalysisError',
                'message': str(e)
            })
    
    def check_code_issues(self, content, filepath, lines):
        """Check for common code issues."""
        issues = []
        
        # Check for hardcoded credentials (basic check)
        patterns = [
            (r'password\s*=\s*["\'](?!.*{)(?!.*\$)(?!.*%)[\w\W]{8,}["\']', 'Potential hardcoded password'),
            (r'api[_-]?key\s*=\s*["\'](?!.*{)(?!.*\$)[\w\W]{10,}["\']', 'Potential hardcoded API key'),
            (r'token\s*=\s*["\'](?!.*{)(?!.*\$)(?!.*%)[\w\W]{10,}["\']', 'Potential hardcoded token'),
        ]
        
        for pattern, message in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_no = content[:match.start()].count('\n') + 1
                issues.append({
                    'file': str(filepath.relative_to(self.project_root)),
                    'line': line_no,
                    'type': 'Security',
                    'message': message
                })
        
        # Check for bare excepts
        if 'except:' in content or 'except :' in content:
            for i, line in enumerate(lines, 1):
                if re.search(r'except\s*:', line):
                    issues.append({
                        'file': str(filepath.relative_to(self.project_root)),
                        'line': i,
                        'type': 'Code Quality',
                        'message': 'Bare except clause - should specify exception type'
                    })
        
        # Check for TODO/FIXME comments
        for i, line in enumerate(lines, 1):
            if 'TODO' in line or 'FIXME' in line:
                issues.append({
                    'file': str(filepath.relative_to(self.project_root)),
                    'line': i,
                    'type': 'TODO',
                    'message': line.strip()
                })
        
        self.results['issues'].extend(issues)
    
    def analyze_project(self):
        """Analyze all Python files in the project."""
        python_files = list(self.project_root.glob('**/*.py'))
        
        # Exclude common directories
        excluded = {'.git', '__pycache__', '.venv', 'venv', 'env', '.pytest_cache'}
        
        for filepath in python_files:
            if not any(excluded_part in filepath.parts for excluded_part in excluded):
                self.analyze_file(filepath)
        
        return self.results
    
    def print_report(self):
        """Print analysis report."""
        print("\n" + "=" * 80)
        print("CODE ANALYSIS REPORT FOR TGCF")
        print("=" * 80)
        
        print(f"\n📊 PROJECT STATISTICS:")
        print(f"  • Total Python files: {len(self.results['files'])}")
        print(f"  • Total lines of code: {self.results['total_lines']:,}")
        print(f"  • Total functions: {self.results['total_functions']}")
        print(f"  • Total classes: {self.results['total_classes']}")
        
        print(f"\n📚 DOCUMENTATION COVERAGE:")
        total_funcs = self.results['documentation']['with_docstring'] + self.results['documentation']['without_docstring']
        if total_funcs > 0:
            coverage = (self.results['documentation']['with_docstring'] / total_funcs) * 100
            print(f"  • Functions with docstrings: {self.results['documentation']['with_docstring']} ({coverage:.1f}%)")
            print(f"  • Functions without docstrings: {self.results['documentation']['without_docstring']}")
        
        print(f"\n📦 TOP 10 MOST USED IMPORTS:")
        sorted_imports = sorted(self.results['imports'].items(), key=lambda x: x[1], reverse=True)[:10]
        for imp, count in sorted_imports:
            print(f"  • {imp}: {count} times")
        
        print(f"\n⚠️  ISSUES FOUND: {len(self.results['issues'])}")
        
        # Group issues by type
        issues_by_type = defaultdict(list)
        for issue in self.results['issues']:
            issues_by_type[issue['type']].append(issue)
        
        for issue_type, issues in issues_by_type.items():
            print(f"\n  {issue_type} ({len(issues)} issues):")
            for issue in issues[:5]:  # Show first 5 of each type
                print(f"    - {issue['file']}:{issue.get('line', '?')} - {issue['message']}")
            if len(issues) > 5:
                print(f"    ... and {len(issues) - 5} more")
        
        print("\n" + "=" * 80)

if __name__ == '__main__':
    analyzer = CodeAnalyzer('/home/ubuntu/tgcf_analysis')
    analyzer.analyze_project()
    analyzer.print_report()

