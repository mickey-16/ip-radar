# 🔧 Virtual Environment - Quick Commands

## ✅ Your Virtual Environment is Ready!

All packages are installed in the isolated `venv` folder - nothing installed globally on your system!

---

## 📝 Essential Commands

### Activate Virtual Environment (Do this first every time!)
```powershell
.\venv\Scripts\Activate.ps1
```
You'll see `(venv)` appear in your terminal prompt when it's active.

### Deactivate Virtual Environment
```powershell
deactivate
```

### Run the Application (after activating venv)
```powershell
python app.py
```

---

## 🚀 Quick Start Workflow

Every time you work on the project:

```powershell
# 1. Navigate to project
cd "d:\TICE hackthaon project"

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Run the application
python app.py
```

---

## 📦 Package Management (in venv)

### Install a new package
```powershell
# Make sure venv is activated first!
pip install package-name
```

### Update requirements.txt
```powershell
pip freeze > requirements.txt
```

### Reinstall all packages
```powershell
pip install -r requirements.txt
```

---

## ✅ Verify Installation

### Check Python version
```powershell
python --version
```

### Check installed packages
```powershell
pip list
```

### Check if Flask is installed
```powershell
python -c "import flask; print('Flask version:', flask.__version__)"
```

---

## 🗑️ Clean Restart (if needed)

If something goes wrong, you can completely reset:

```powershell
# Deactivate if active
deactivate

# Delete virtual environment
Remove-Item -Recurse -Force venv

# Recreate from scratch
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🎯 Current Status

- ✅ Virtual environment created: `venv\`
- ✅ All packages installed (Flask, requests, etc.)
- ✅ `.env` file created
- ⚠️ **TODO: Add your API keys to `.env`**

---

## 🔑 API Keys Setup

Edit `.env` file:
```powershell
notepad .env
```

Add your keys:
```env
ABUSEIPDB_API_KEY=your_key_here
VIRUSTOTAL_API_KEY=your_key_here
IPGEOLOCATION_API_KEY=your_key_here
```

Get FREE keys:
- AbuseIPDB: https://www.abuseipdb.com/api
- VirusTotal: https://www.virustotal.com/gui/join-us
- IPGeolocation: https://ipgeolocation.io/signup

---

## 💡 Benefits of Virtual Environment

✅ **Isolated** - Doesn't affect your system Python
✅ **Clean** - No conflicts with other projects
✅ **Portable** - Easy to recreate on another machine
✅ **Safe** - Can delete and start fresh anytime

---

## 🆘 Troubleshooting

### "Activate.ps1 cannot be loaded" error
Run this once:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Packages not found after installing
Make sure virtual environment is activated (look for `(venv)` in prompt)

### Want to use a different Python version
```powershell
# Use specific Python version
C:\Path\To\Python39\python.exe -m venv venv
```

---

**Remember:** Always activate the virtual environment before working on the project! 🚀
