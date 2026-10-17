# GAJAN Instagram Operations — Windows / VS Code local demo

## Prerequisites
- Windows 10/11, Python 3.10 or newer, VS Code, Chrome/Edge.
- No pip install or external API keys required.

## First run
1. Right-click the ZIP → **Extract All**.
2. In VS Code, **File → Open Folder** → select `gajan_instagram_ops` (the folder containing `seed_demo.py`).
3. Open **Terminal → New Terminal** (PowerShell) and run:

```powershell
py -3 --version
py -3 seed_demo.py
py -3 -m unittest discover -s tests -v
py -3 -m app.web
```

If `py` is not recognized, replace `py -3` with `python` in each command. If VS Code opens in the wrong folder, run `cd path\to\gajan_instagram_ops` first.

4. Open **http://localhost:8000** in Chrome/Edge.
5. To stop the server, press **Ctrl+C** in the terminal.

**Alternative:** After running `seed_demo.py`, double-click `START_WINDOWS.bat` to start the dashboard.

## Browser test checklist
1. Confirm three fictional demo accounts and six demo tasks are shown.
2. Register a new test brand, owner and handle.
3. Create a task for that brand, then click **Complete**.
4. Change an account status using the dropdown.
5. Click **Run audit** to see missing-control findings and follow-up tasks.
6. Click **Queue manual reminders** to record reminders; these are **not** sent to anyone.
7. Check the recent activity log, then click **Refresh**. Restart the server and confirm records persist.

## Troubleshooting
- `No module named app`: open the terminal in the `gajan_instagram_ops` directory.
- `Address already in use`: stop an earlier server with Ctrl+C; port 8000 is already occupied.
- `python not found`: install Python 3.10+ from python.org, enable PATH, and restart VS Code.
- Blank browser: check the terminal for errors, use `http://localhost:8000` (not HTTPS), and refresh.
- Reset local demo: stop server, delete `ops.db` and run `py -3 seed_demo.py` again. Do not delete a database with data you want to keep.

## Boundaries / security
- This is a **local demo**, bound to `127.0.0.1`; it is **not** a hosted or production service.
- No Instagram sign-up, Meta API integration, automated role removal, or message delivery is performed.
- Browser endpoints have a per-process session token, but **no user authentication**. Do not expose port 8000 to the internet.
- Do not enter real passwords, backup codes, customer PII, or production credentials.
- Existing CLI is preserved; see the original README for its commands.
