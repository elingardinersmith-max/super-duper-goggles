# Troubleshooting: "Internal Server Error"

If you're seeing `{"error":"Internal server error"}`, don't worry! This is fixable. Let's diagnose and fix it.

## 🔍 Step 1: Check the Render Logs (Most Important!)

The logs will tell us exactly what's wrong.

### How to View Logs:

1. Go to your **Render Dashboard** (https://dashboard.render.com)
2. Click on your **"utility-monitor"** service
3. Click **"Logs"** tab (left sidebar)
4. Look at the most recent messages (scroll to bottom)

### What to Look For:

Look for red text or lines that say "ERROR" or "FAILED". Common issues:

---

## 🔧 Common Issue #1: Missing `static` Folder

**Error in logs looks like:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'static'
```

**Fix:**
You need to create the static folder and upload the HTML file.

1. Go to your GitHub repository
2. Click **"Add file"** → **"Create new file"**
3. In the filename box, type: `static/index.html`
4. Copy the entire contents from the `index.html` file in your ZIP
5. Click **"Commit changes"**

Render will automatically redeploy (wait 2-3 minutes).

---

## 🔧 Common Issue #2: Wrong File Structure

**Error in logs looks like:**
```
ModuleNotFoundError: No module named 'crawler'
```

**The Problem:**
Files might be nested in a subfolder instead of at the root.

**Fix:**

### Check your GitHub repository structure. It should look like this:

```
your-repository/
├── app.py
├── crawler.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── static/
│   └── index.html
└── (other files)
```

### NOT like this (WRONG):
```
your-repository/
└── webapp/
    ├── app.py
    ├── crawler.py
    └── (etc)
```

**If your files are in a `webapp` subfolder:**

1. In Render, go to your service settings
2. Find **"Root Directory"**
3. Set it to: `webapp`
4. Click **"Save Changes"**

OR

Re-upload files directly to the root (delete the webapp folder, upload files directly).

---

## 🔧 Common Issue #3: Missing Dependencies

**Error in logs looks like:**
```
ImportError: cannot import name 'CORS' from 'flask_cors'
```

**Fix:**

1. Make sure `requirements.txt` is in your repository
2. In Render settings, make sure **Build Command** is exactly:
   ```
   pip install -r requirements.txt
   ```
3. Click **"Manual Deploy"** → **"Clear build cache & deploy"**

---

## 🔧 Common Issue #4: Wrong Start Command

**Error in logs looks like:**
```
bash: gunicorn: command not found
```

**Fix:**

1. Go to Render settings
2. Check **"Start Command"** is exactly:
   ```
   gunicorn app:app
   ```
3. Make sure `gunicorn` is in your `requirements.txt`
4. Click **"Save Changes"**

---

## 🔧 Common Issue #5: Port Configuration

**Error in logs looks like:**
```
Error: Can't connect to port 5000
```

**Fix:**
The app needs to use Render's PORT variable. This should be automatic, but let's verify:

1. Go to **"Environment"** tab in Render
2. Check if there's a `PORT` variable
3. If not, Render sets it automatically - don't add it manually
4. The app.py file already handles this correctly

---

## 🔧 Common Issue #6: Data Directory Permissions

**Error in logs looks like:**
```
PermissionError: [Errno 13] Permission denied: 'data'
```

**Fix:**
This happens with file system permissions. The app should create the directory automatically, but:

1. Check that `data/` is NOT in your GitHub repository
2. The app creates it on first run
3. If error persists, add to **Environment** variables:
   - Key: `DATA_DIR`
   - Value: `/tmp/data`

---

## ✅ Step 2: Try These Quick Fixes

### Quick Fix #1: Redeploy

1. In Render, click **"Manual Deploy"**
2. Select **"Clear build cache & deploy"**
3. Wait 3-5 minutes
4. Try accessing your app again

### Quick Fix #2: Check Environment

Make sure these Render settings are EXACTLY right:

- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: Free

### Quick Fix #3: Verify All Files Uploaded

Your GitHub repo must have these files at minimum:
- ✅ `app.py`
- ✅ `crawler.py`
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `static/index.html`

---

## 📋 Step 3: Send Me the Logs

If none of the above fixes work, I need to see your logs. 

**Copy the last 20-30 lines from your Render logs** and share them. Look for:
- Lines with "ERROR"
- Lines with "FAILED"
- The last few lines before it stops

The logs will tell us exactly what's wrong!

---

## 🆘 Nuclear Option: Start Fresh

If nothing works, let's start completely fresh:

### Delete Everything and Restart:

1. **Delete Render Service:**
   - Go to Render dashboard
   - Click your service
   - Settings → Scroll to bottom → "Delete Web Service"

2. **Delete GitHub Repository:**
   - Go to your GitHub repo
   - Settings → Scroll to bottom → "Delete this repository"

3. **Start Over:**
   - Create new repository
   - Upload files again (make sure they're at root level, not in a subfolder!)
   - Create new Render service
   - Make sure Root Directory is blank (unless files are in a subfolder)

---

## 💡 Most Likely Solutions

Based on common issues, try these IN ORDER:

### 1. Check File Structure (90% of issues)
- Files should be at repository root
- NOT in a webapp subfolder
- Unless you set Root Directory to "webapp" in Render

### 2. Check static/index.html exists
- Go to your GitHub repo
- You should see a "static" folder
- Click it - index.html should be inside

### 3. Redeploy with cleared cache
- Render → Manual Deploy → Clear build cache & deploy

### 4. Check the logs
- They'll tell you exactly what's wrong

---

## 📞 Need More Help?

Share these details and I can give you an exact fix:

1. **Your Render logs** (last 20-30 lines)
2. **Screenshot of your GitHub repository** (showing file structure)
3. **Your Render service settings** (Build Command, Start Command, Root Directory)

The error message itself doesn't tell us much - the logs have the real answer!

---

## ✨ Expected Successful Deployment

When everything works, your Render logs should end with something like:

```
==> Starting service with 'gunicorn app:app'
[2024-02-09 10:00:00] [1] [INFO] Starting gunicorn 21.2.0
[2024-02-09 10:00:00] [1] [INFO] Listening at: http://0.0.0.0:10000
[2024-02-09 10:00:00] [1] [INFO] Using worker: sync
[2024-02-09 10:00:00] [8] [INFO] Booting worker with pid: 8
Starting Utility Monitor on port 10000
Frontend: http://0.0.0.0:10000
API: http://0.0.0.0:10000/api/health
```

And when you visit your URL, you should see the blue Utility Monitor interface, NOT a JSON error message.

---

**Let me know what you see in the logs and we'll get this fixed!** 🔧
