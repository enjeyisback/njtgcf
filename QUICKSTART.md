# TGCF Service - Quick Start Guide

## Installation Complete! ✅

TGCF is now set up as a persistent background service.

## 🚀 Essential Commands

```bash
# Navigate to TGCF directory
cd /home/ubuntu/github_repos/tgcf

# Start the service
./tgcf-start.sh

# Check if it's running
./tgcf-status.sh

# View logs
./tgcf-logs.sh -f

# Stop the service
./tgcf-stop.sh

# Restart the service
./tgcf-restart.sh
```

> **📍 Note:** All scripts use dynamic path detection. Replace `/home/ubuntu/github_repos/tgcf` with your actual repository location - the scripts will work from any directory!

## 🌐 Access Web Interface

Once started, access TGCF at:
- **http://localhost:8501** (from this machine)
- **http://[your-ip]:8501** (from other devices)

**Default Password:** `tgcf` (Change this in `.env` file!)

## 📋 Service Status

Check anytime:
```bash
./tgcf-status.sh
```

## 🔄 Auto-Start on Login

To make TGCF start automatically when you log in:
```bash
./tgcf-autostart.sh
```

## 📝 View Logs

```bash
# Recent logs
./tgcf-logs.sh

# Follow in real-time
./tgcf-logs.sh -f

# Last 100 lines
./tgcf-logs.sh -n 100
```

## 🛠️ Troubleshooting

**Service won't start?**
```bash
./tgcf-stop.sh
./tgcf-start.sh
```

**Can't access web interface?**
1. Check service status: `./tgcf-status.sh`
2. Verify port 8501 is open: `netstat -tulpn | grep 8501`
3. Try restarting: `./tgcf-restart.sh`

**Need to change password?**
1. Edit `.env` file: `nano .env`
2. Change `PASSWORD=tgcf` to `PASSWORD=your_password`
3. Restart: `./tgcf-restart.sh`

## 📚 Full Documentation

For detailed information, see:
- **Service Management:** `SERVICE_MANAGEMENT.md`
- **Usage Instructions:** `USAGE_INSTRUCTIONS.md`
- **Main README:** `README.md`

## 💡 Key Features

- ✅ Runs in background (survives terminal closure)
- ✅ Automatic restart on crash
- ✅ State persistence across restarts
- ✅ Easy management with simple scripts
- ✅ Comprehensive logging
- ✅ Optional auto-start on system boot

## 🔐 Security Note

**IMPORTANT:** Change the default password!

```bash
# Edit .env file
nano .env

# Change PASSWORD=tgcf to something secure
PASSWORD=your_secure_password_here

# Restart to apply
./tgcf-restart.sh
```

## 🎯 Next Steps

1. **Start the service:** `./tgcf-start.sh`
2. **Access web interface:** http://localhost:8501
3. **Login with password:** `tgcf` (or your custom password)
4. **Configure Telegram:** Follow the web UI setup wizard
5. **Set up forwarding:** Add connections and forwarding rules

## 📞 Getting Help

- **Status check:** `./tgcf-status.sh`
- **View logs:** `./tgcf-logs.sh -f`
- **Documentation:** `SERVICE_MANAGEMENT.md`
- **GitHub:** https://github.com/aahnik/tgcf

---

**Service Location:** `/home/ubuntu/github_repos/tgcf`  
**Web Interface:** `http://localhost:8501`  
**Log File:** `tgcf-service.log`  
**Tmux Session:** `tgcf-service`
