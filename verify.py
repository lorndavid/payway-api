#!/usr/bin/env python3
"""
Quick verification script to test your payment system setup
Run this before deploying to Railway
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_file(path, description):
    """Check if a file exists"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_directory(path, description):
    """Check if directory exists"""
    exists = os.path.isdir(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_python_imports():
    """Check if all required packages are installed"""
    required = ['flask', 'requests', 'reportlab', 'gunicorn']
    all_good = True
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            all_good = False
    
    return all_good

def check_flask_app():
    """Check if Flask app is syntactically valid"""
    try:
        with open('app.py', 'r') as f:
            code = f.read()
        compile(code, 'app.py', 'exec')
        print("✅ app.py is valid Python")
        
        # Check for required routes
        required_routes = ['/generate', '/checkout', '/health', '/status-stream', '/download-receipt', '/static/']
        for route in required_routes:
            if route in code or route.replace('/', '') in code:
                print(f"  ✓ Route {route} found")
            else:
                print(f"  ⚠ Route {route} not found")
        
        return True
    except Exception as e:
        print(f"❌ app.py has errors: {e}")
        return False

def check_html_files():
    """Check if HTML files are present and valid"""
    files_ok = True
    
    for html_file in ['templates/index.html', 'templates/checkout.html']:
        if not os.path.exists(html_file):
            print(f"❌ {html_file} - MISSING")
            files_ok = False
            continue
        
        with open(html_file, 'r') as f:
            content = f.read()
        
        # Basic HTML validation
        if '<html' not in content.lower():
            print(f"❌ {html_file} - Invalid HTML")
            files_ok = False
            continue
        
        print(f"✅ {html_file} - Valid")
    
    return files_ok

def check_static_files():
    """Check if static files exist"""
    files_ok = True
    
    required_files = [
        ('static/aba-checkout.min.js', 'ABA Checkout SDK')
    ]
    
    for file_path, description in required_files:
        if not os.path.exists(file_path):
            print(f"❌ {description}: {file_path} - MISSING")
            files_ok = False
        else:
            with open(file_path, 'r') as f:
                size = len(f.read())
            if size < 1000:
                print(f"⚠  {description}: {file_path} - File seems too small ({size} bytes)")
            else:
                print(f"✅ {description}: {file_path} ({size} bytes)")
    
    return files_ok

def check_deployment_files():
    """Check deployment configuration files"""
    files_ok = True
    
    required_files = [
        ('Dockerfile', 'Docker configuration'),
        ('railway.json', 'Railway configuration'),
        ('Procfile', 'Process file'),
        ('requirements.txt', 'Python dependencies')
    ]
    
    for file_path, description in required_files:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"{status} {description}: {file_path}")
        files_ok = files_ok and exists
    
    return files_ok

def check_documentation():
    """Check if documentation exists"""
    docs_ok = True
    
    docs = [
        ('README.md', 'Main README'),
        ('ABA_INTEGRATION.md', 'Integration guide'),
        ('QUICK_DEPLOY.md', 'Quick deployment'),
        ('IMPLEMENTATION_SUMMARY.md', 'Implementation summary')
    ]
    
    for file_path, description in docs:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "⚠"
        print(f"{status} {description}: {file_path}")
        docs_ok = docs_ok and exists
    
    return docs_ok

def test_imports():
    """Try importing the Flask app"""
    try:
        sys.path.insert(0, os.getcwd())
        import app
        print("✅ app.py imports successfully")
        
        # Check if app has the routes
        if hasattr(app, 'app'):
            print("✅ Flask app object found")
            return True
        else:
            print("❌ Flask app object not found")
            return False
    except Exception as e:
        print(f"❌ Error importing app.py: {e}")
        return False

def main():
    print_header("🔍 Payment System Verification")
    
    all_good = True
    
    # Check project structure
    print_header("📁 Project Structure")
    all_good &= check_directory('templates', 'Templates directory')
    all_good &= check_directory('static', 'Static files directory')
    all_good &= check_file('app.py', 'Flask application')
    all_good &= check_file('requirements.txt', 'Dependencies file')
    
    # Check required files
    print_header("📄 Required Files")
    all_good &= check_file('templates/index.html', 'Fast KHQR UI')
    all_good &= check_file('templates/checkout.html', 'ABA Checkout UI')
    all_good &= check_file('static/aba-checkout.min.js', 'ABA SDK')
    
    # Check deployment files
    print_header("🚀 Deployment Files")
    all_good &= check_deployment_files()
    
    # Check documentation
    print_header("📚 Documentation")
    check_documentation()  # Not critical
    
    # Check Python environment
    print_header("🐍 Python Environment")
    all_good &= check_python_imports()
    
    # Check Flask app
    print_header("⚙️ Flask Application")
    all_good &= check_flask_app()
    
    # Check HTML files
    print_header("🌐 HTML Files")
    all_good &= check_html_files()
    
    # Check static files
    print_header("📦 Static Files")
    all_good &= check_static_files()
    
    # Try importing
    print_header("✅ Import Check")
    all_good &= test_imports()
    
    # Final summary
    print_header("📊 Verification Summary")
    
    if all_good:
        print("""
✅ ALL CHECKS PASSED! 

Your payment system is ready to:
1. Run locally:    python app.py
2. Deploy to Railway: git push

Next steps:
1. Test locally: http://localhost:5000/
2. Test checkout: http://localhost:5000/checkout
3. Push to GitHub: git push
4. Deploy to Railway (auto)
        """)
        return 0
    else:
        print("""
❌ SOME CHECKS FAILED

Please fix the issues marked with ❌ above.

Common fixes:
- Missing dependencies: pip install -r requirements.txt
- Missing files: Check they exist in the correct folders
- Flask syntax error: Check app.py for Python errors
        """)
        return 1

if __name__ == '__main__':
    sys.exit(main())
