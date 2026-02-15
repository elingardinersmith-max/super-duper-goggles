# 🔥 FRESH START - Complete File Set

## Step 1: DELETE EVERYTHING in GitHub

1. Go to your GitHub repository
2. Delete ALL files:
   - app.py → delete
   - crawler.py → delete
   - requirements.txt → delete
   - Procfile → delete
   - runtime.txt → delete
   - Any other files → delete
3. Repo should be EMPTY

---

## Step 2: CREATE FILES (Copy/Paste Each One)

I'll give you 5 files. For each one:

1. GitHub → "Add file" → "Create new file"
2. Name it (exact name shown)
3. Copy the content
4. Paste
5. Commit

---

### FILE 1: Procfile

**Filename:** `Procfile` (no extension)

**Content:**
```
web: gunicorn app:app --timeout 300 --workers 1
```

---

### FILE 2: runtime.txt

**Filename:** `runtime.txt`

**Content:**
```
python-3.11.9
```

---

### FILE 3: requirements.txt

**Filename:** `requirements.txt`

**Content:**
```
Flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
beautifulsoup4==4.12.2
lxml==5.1.0
feedparser==6.0.10
python-dotenv==1.0.0
gunicorn==21.2.0
APScheduler==3.10.4
html5lib==1.1
urllib3==2.1.0
psycopg[binary]==3.1.18
```

---

### FILE 4: crawler.py

**Filename:** `crawler.py`

**This file is LONG (650 lines).** 

Download it from: FRESH-START/crawler.py (I'll provide)

OR get it from the ZIP file.

Then:
1. GitHub → "Add file" → "Upload files"
2. Drag crawler.py
3. Commit

---

### FILE 5: app.py

**Filename:** `app.py`

**This file is LONG (625 lines).**

Download it from: FRESH-START/app.py (I'll provide)

OR get it from the ZIP file.

Then:
1. GitHub → "Add file" → "Upload files"
2. Drag app.py
3. Commit

---

## Step 3: Verify Files

Your GitHub repo should now have EXACTLY these 5 files:
- ✅ Procfile
- ✅ runtime.txt
- ✅ requirements.txt
- ✅ crawler.py
- ✅ app.py

---

## Step 4: Deploy

1. Render → Your service → "Manual Deploy"
2. Click "Clear build cache & deploy"
3. Wait 5 minutes
4. Check logs for "Database initialized successfully"

---

## Step 5: Test

1. Visit your app
2. Run a crawl
3. Should work!

---

## What These Files Do:

- **Procfile:** 5-minute timeout so crawls don't get killed
- **runtime.txt:** Python 3.11.9 (stable)
- **requirements.txt:** psycopg3 (Python 3.13 compatible)
- **crawler.py:** Enhanced search (14 queries) + NewsAPI + demo fallback
- **app.py:** Database + URL links + everything working

---

## Download All Files:

I'll provide a ZIP with all 5 files ready to upload.

Extract → Upload all 5 → Done!
