# TGCF Service Management Guide

This guide explains how to manage the TGCF service as a persistent background process.

## Overview

TGCF runs as a background service using **tmux** for session management. This provides:
- ✅ Persistent operation (survives terminal closure)
- ✅ Easy management with simple scripts
- ✅ Session attachment for debugging
- ✅ Comprehensive logging
- ✅ State persistence across restarts

## Service Architecture

```
┌─────────────────────────────────────────┐
│  TGCF Service (tmux session)            │
│  ├─ tgcf-web command                    │
│  ├─ Streamlit web interface (port 8501)│
│  ├─ Configuration: tgcf.config.json     │
│  ├─ Environment: .env                   │
│  └─ Logs: tgcf-service.log              │
└─────────────────────────────────────────┘
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `./tgcf-start.sh` | Start the TGCF service |
| `./tgcf-stop.sh` | Stop the TGCF service |
| `./tgcf-restart.sh` | Restart the TGCF service |
| `./tgcf-status.sh` | Check service status and recent logs |
| `./tgcf-logs.sh` | View service logs |
| `./tgcf-logs.sh -f` | Follow logs in real-time |
| `./tgcf-autostart.sh` | Configure auto-start on login |

## Management Scripts

### 1. Starting the Service

```bash
cd /home/ubuntu/github_repos/tgcf
./tgcf-start.sh
```

**What it does:**
- Creates a detached tmux session named `tgcf-service`
- Loads environment variables from `.env`
- Starts the `tgcf-web` command
- Logs output to `tgcf-service.log`

**Output:**
```
Starting TGCF service in tmux session: tgcf-service
TGCF service started successfully!
Session: tgcf-service
Log file: /home/ubuntu/github_repos/tgcf/tgcf-service.log
```

**Note:** If the service is already running, it will inform you and exit.

### 2. Stopping the Service

```bash
cd /home/ubuntu/github_repos/tgcf
./tgcf-stop.sh
```

**What it does:**
- Kills the tmux session `tgcf-service`
- Gracefully stops all TGCF processes
- Configuration and state are preserved

**Output:**
```
Stopping TGCF service (tmux session: tgcf-service)...
TGCF service stopped successfully!
```

### 3. Restarting the Service

```bash
cd /home/ubuntu/github_repos/tgcf
./tgcf-restart.sh
```

**What it does:**
- Stops the service (if running)
- Waits 2 seconds
- Starts the service again

**Use cases:**
- After updating configuration
- After modifying `.env` file
- After system updates

### 4. Checking Service Status

```bash
cd /home/ubuntu/github_repos/tgcf
./tgcf-status.sh
```

**What it does:**
- Checks if tmux session exists
- Lists running TGCF processes
- Shows recent log entries (last 10 lines)
- Displays management commands

**Example Output:**
```
=========================================
TGCF Service Status
=========================================

Status: ✅ RUNNING
Session: tgcf-service

Tmux Session Info:
tgcf-service: 1 windows (created Wed Dec 31 09:18:49 2025)

Running Processes:
ubuntu  1022  /home/ubuntu/.local/bin/tgcf-web
ubuntu  1034  streamlit run ...

Recent Logs (last 10 lines):
---
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
---
```

### 5. Viewing Logs

#### View recent logs (last 50 lines)
```bash
cd /home/ubuntu/github_repos/tgcf
./tgcf-logs.sh
```

#### Follow logs in real-time
```bash
./tgcf-logs.sh -f
# or
./tgcf-logs.sh --follow
```
Press `Ctrl+C` to stop following.

#### View specific number of lines
```bash
./tgcf-logs.sh -n 100
# or
./tgcf-logs.sh --lines 100
```

#### Direct log access
```bash
tail -f /home/ubuntu/github_repos/tgcf/tgcf-service.log
```

### 6. Configuring Auto-Start

```bash
cd /home/ubuntu/github_repos/tgcf
./tgcf-autostart.sh
```

**What it does:**
- Adds auto-start configuration to `~/.bashrc`
- TGCF will start automatically on your next login

**To disable auto-start:**
Edit `~/.bashrc` and remove the line containing `tgcf-start.sh`.

## Advanced Usage

### Attaching to the tmux Session

To directly interact with the running TGCF process:

```bash
tmux attach -t tgcf-service
```

**To detach without stopping:**
Press `Ctrl+B`, then press `D`

**Warning:** If you exit the attached session normally (Ctrl+C or exit), the service will stop.

### Manual tmux Commands

```bash
# List all tmux sessions
tmux list-sessions

# Check if tgcf-service is running
tmux has-session -t tgcf-service && echo "Running" || echo "Not running"

# Kill the session manually
tmux kill-session -t tgcf-service
```

### Checking Process Details

```bash
# View all TGCF-related processes
ps aux | grep -E "tgcf|streamlit" | grep -v grep

# Check network ports
netstat -tulpn | grep 8501

# Or with ss
ss -tulpn | grep 8501
```

## State Persistence

### Configuration Files

TGCF maintains state across restarts through:

| File/Directory | Purpose |
|----------------|---------|
| `tgcf.config.json` | Main configuration (connections, forwarding rules, plugins) |
| `.env` | Environment variables (password, API keys) |
| `*.session` | Telegram session files (authentication) |
| `data/` | Persistent data directory |

### Backup Recommendations

```bash
# Backup configuration and sessions
cd /home/ubuntu/github_repos/tgcf
tar -czf tgcf-backup-$(date +%Y%m%d).tar.gz \
    tgcf.config.json \
    .env \
    *.session \
    data/

# Restore from backup
tar -xzf tgcf-backup-YYYYMMDD.tar.gz
```

### Session Files

Telegram session files (`.session`) are automatically created when you authenticate via the web interface. These files:
- Store authentication tokens
- Prevent re-authentication on restart
- Should be backed up regularly
- Are sensitive and should be kept secure

## Accessing the Web Interface

Once the service is running, access the TGCF web interface at:

- **Local:** http://localhost:8501
- **Network:** http://[your-ip]:8501

**Security Note:** The default password is `tgcf`. Change it in the `.env` file:

```bash
# Edit .env
nano .env

# Set a strong password
PASSWORD=your_secure_password_here

# Restart the service
./tgcf-restart.sh
```

## Troubleshooting

### Service Won't Start

1. **Check if already running:**
   ```bash
   ./tgcf-status.sh
   ```

2. **Stop existing instance:**
   ```bash
   ./tgcf-stop.sh
   ```

3. **Check for port conflicts:**
   ```bash
   netstat -tulpn | grep 8501
   # Or kill the conflicting process
   lsof -ti:8501 | xargs kill -9
   ```

4. **Start again:**
   ```bash
   ./tgcf-start.sh
   ```

### Service Keeps Crashing

1. **Check logs for errors:**
   ```bash
   ./tgcf-logs.sh -f
   ```

2. **Verify configuration:**
   ```bash
   cat tgcf.config.json | python3 -m json.tool
   ```

3. **Check environment variables:**
   ```bash
   cat .env
   ```

4. **Verify tgcf-web command:**
   ```bash
   which tgcf-web
   tgcf-web --version
   ```

### Cannot Access Web Interface

1. **Verify service is running:**
   ```bash
   ./tgcf-status.sh
   ```

2. **Check if Streamlit is listening:**
   ```bash
   netstat -tulpn | grep 8501
   ```

3. **Check firewall rules:**
   ```bash
   sudo ufw status
   # If port 8501 is blocked, allow it:
   sudo ufw allow 8501/tcp
   ```

4. **Try accessing from localhost first:**
   ```bash
   curl http://localhost:8501
   ```

### Lost tmux Session

If you lose track of the tmux session:

```bash
# List all sessions
tmux list-sessions

# If tgcf-service exists, attach to it
tmux attach -t tgcf-service

# If not, check if processes are still running
ps aux | grep tgcf-web

# Kill orphaned processes
pkill -f tgcf-web

# Start fresh
./tgcf-start.sh
```

### Logs Growing Too Large

```bash
# Check log size
ls -lh tgcf-service.log

# Rotate logs (create backup and clear)
mv tgcf-service.log tgcf-service.log.$(date +%Y%m%d)
touch tgcf-service.log

# Or truncate logs
> tgcf-service.log

# Restart to continue logging
./tgcf-restart.sh
```

## System Integration

### Adding to System Startup (Systemd Alternative)

Since systemd is not available in this environment, we use shell-based auto-start:

1. **Run the auto-start configuration:**
   ```bash
   ./tgcf-autostart.sh
   ```

2. **Manual configuration:**
   Add to `~/.bashrc`:
   ```bash
   # TGCF Auto-Start
   [ -f "/home/ubuntu/github_repos/tgcf/tgcf-start.sh" ] && \
     cd "/home/ubuntu/github_repos/tgcf" && \
     ./tgcf-start.sh > /dev/null 2>&1 &
   ```

3. **For system-wide startup (if you have root access):**
   Add to `/etc/rc.local` (if available):
   ```bash
   su - ubuntu -c 'cd /home/ubuntu/github_repos/tgcf && ./tgcf-start.sh'
   ```

### Cron-Based Monitoring (Optional)

Set up a cron job to ensure the service stays running:

```bash
# Edit crontab
crontab -e

# Add this line to check every 5 minutes
*/5 * * * * cd /home/ubuntu/github_repos/tgcf && tmux has-session -t tgcf-service 2>/dev/null || ./tgcf-start.sh >> /home/ubuntu/github_repos/tgcf/cron.log 2>&1
```

## Best Practices

1. **Regular Backups:** Backup `tgcf.config.json`, `.env`, and `.session` files regularly
2. **Monitor Logs:** Check logs periodically for errors or warnings
3. **Update Password:** Change the default password in `.env`
4. **Graceful Restarts:** Always use `./tgcf-restart.sh` instead of killing processes
5. **Log Rotation:** Implement log rotation to prevent disk space issues
6. **Session Security:** Keep `.session` files secure and never share them

## Files Reference

### Management Scripts

- `tgcf-start.sh` - Start the service
- `tgcf-stop.sh` - Stop the service
- `tgcf-restart.sh` - Restart the service
- `tgcf-status.sh` - Check service status
- `tgcf-logs.sh` - View service logs
- `tgcf-autostart.sh` - Configure auto-start

### Configuration Files

- `tgcf.config.json` - Main TGCF configuration
- `.env` - Environment variables (password, etc.)
- `tgcf.service` - Systemd service file (for reference, not used in this environment)

### Logs

- `tgcf-service.log` - Main service log file
- `streamlit.log` - Streamlit-specific logs (if any)

### Data

- `data/` - Directory for persistent storage
- `*.session` - Telegram session files

## Support

For more information:
- **TGCF Documentation:** https://github.com/aahnik/tgcf
- **Usage Instructions:** See `USAGE_INSTRUCTIONS.md`
- **GitHub Issues:** https://github.com/aahnik/tgcf/issues

## Summary

The TGCF service management system provides a robust, easy-to-use solution for running TGCF persistently:

- ✅ Simple commands for start/stop/restart
- ✅ Comprehensive status checking and logging
- ✅ Survives terminal closure (tmux-based)
- ✅ State persistence across restarts
- ✅ Auto-start capability
- ✅ Easy troubleshooting and debugging

All state is preserved in configuration files, making the service resilient and easy to manage.
