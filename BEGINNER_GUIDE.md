# Utility Monitor - Complete Beginner's Guide
## Deploy Your Own Web App in 15 Minutes (No Coding Required!)

This guide will help you deploy a professional utility municipalization monitoring web application that you can access from any browser. **No coding experience needed!**

---

## 📋 What You'll Need

1. A computer with internet access
2. An email address
3. 15 minutes of time
4. The ZIP file I provided (`utility-monitor-webapp.zip`)

**Cost: $0** - We'll use free hosting!

---

## 🎯 Overview - What We're Doing

We're going to:
1. Extract the app files from the ZIP
2. Create a free GitHub account (to store your files)
3. Upload the files to GitHub
4. Create a free Render account (to host your website)
5. Connect Render to GitHub
6. Launch your app!

Your app will be live at a URL like: `https://utility-monitor.onrender.com`

---

## Step 1: Extract the ZIP File (2 minutes)

### Windows:
1. Find the `utility-monitor-webapp.zip` file in your Downloads folder
2. **Right-click** on it
3. Select **"Extract All..."**
4. Click **"Extract"**
5. You'll see a new folder called `webapp`

### Mac:
1. Find the `utility-monitor-webapp.zip` file in your Downloads folder
2. **Double-click** it
3. It will automatically extract to a folder called `webapp`

**✓ Checkpoint:** You should now have a folder called `webapp` with files inside it.

---

## Step 2: Create a GitHub Account (3 minutes)

GitHub is where we'll store your app files (like Google Drive for code).

1. Go to **https://github.com**
2. Click the **"Sign up"** button (top right)
3. Enter your email address
4. Create a password (make it strong!)
5. Choose a username (like `yourname-utilities`)
6. Verify you're human (solve the puzzle)
7. Click **"Create account"**
8. Check your email and click the verification link
9. You can skip the questionnaire by clicking **"Skip personalization"**

**✓ Checkpoint:** You're now logged into GitHub and see your dashboard.

---

## Step 3: Upload Your Files to GitHub (5 minutes)

Now we'll create a repository (storage space) and upload your app files.

### 3.1: Create a New Repository

1. On GitHub, click the **green "New"** button (or the **"+"** in top right → **"New repository"**)
2. Fill in these fields:
   - **Repository name**: `utility-monitor` (exactly like this, no spaces)
   - **Description**: `Utility municipalization monitoring application`
   - **Public or Private**: Choose **"Public"**
   - **Initialize repository**: ✓ Check **"Add a README file"**
3. Click **"Create repository"** (green button at bottom)

**✓ Checkpoint:** You now see a page with your repository name at the top.

### 3.2: Upload Files

1. Click the **"Add file"** button
2. Select **"Upload files"**
3. Open the `webapp` folder you extracted earlier
4. **Drag ALL the files** from inside the `webapp` folder into the GitHub upload area
   - Make sure you're dragging the **files**, not the `webapp` folder itself
   - You should see: `app.py`, `crawler.py`, `requirements.txt`, `Procfile`, `DEPLOY.md`, etc.
5. At the bottom, click **"Commit changes"** (green button)

**✓ Checkpoint:** You should see all your files listed in the repository (app.py, crawler.py, static folder, etc.)

---

## Step 4: Create a Render Account (2 minutes)

Render is where we'll host your website (like a computer that runs 24/7 to serve your app).

1. Go to **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. Click **"Sign up with GitHub"** (easiest option)
4. Click **"Authorize Render"**
5. You're now logged into Render!

**✓ Checkpoint:** You see the Render dashboard with a button to create new services.

---

## Step 5: Deploy Your App on Render (5 minutes)

This is where the magic happens - we'll make your app live on the internet!

### 5.1: Create a Web Service

1. On Render dashboard, click **"New +"** (top right)
2. Select **"Web Service"**
3. You'll see **"Connect a repository"**
4. Find your `utility-monitor` repository in the list
5. Click **"Connect"** next to it
   - If you don't see it, click "Configure account" and give Render access to your repositories

### 5.2: Configure Your Service

Fill in these exact settings:

- **Name**: `utility-monitor` (or choose your own)
- **Region**: Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch**: `main` (should be auto-selected)
- **Root Directory**: Leave blank
- **Runtime**: **Python 3** (should auto-detect)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: **Free** (select this!)

### 5.3: Deploy!

1. Scroll to bottom
2. Click **"Create Web Service"** (big button)
3. Wait 3-5 minutes while Render builds your app
   - You'll see a log with lots of text scrolling - this is normal!
   - Look for "Build successful" and "Deploy live"

**✓ Checkpoint:** At the top, you'll see your app URL (like `https://utility-monitor.onrender.com`)

---

## Step 6: Access Your App! (1 minute)

1. Copy the URL shown at the top of your Render dashboard
   - It looks like: `https://utility-monitor-xxxx.onrender.com`
2. Paste it into your browser
3. **You're live!** 🎉

You should see:
- A dark blue interface
- "Utility Monitor" at the top
- Stats showing 0 items (Today, Pending, Approved, Deleted)
- A "Run Crawl Now" button

---

## Step 7: Run Your First Crawl (1 minute)

Let's collect some data!

1. Click the **"Run Crawl Now"** button
2. Wait 30-60 seconds (it will say "Crawling...")
3. You'll see a message like "✓ Crawl complete! Found 5 new mentions"
4. New items will appear in the **"Review Queue"**

Now you can:
- Click on any item to see details
- Click **"Approve"** to save relevant items
- Click **"Delete"** to remove irrelevant ones

**Congratulations! Your app is live and working!** 🎉

---

## 🎁 Bonus: Add Free API Keys (Optional - Better Results!)

Want to supercharge your crawling? Add these free APIs:

### Get Google Custom Search (100 free searches/day)

1. Go to **https://console.cloud.google.com**
2. Sign in with your Google account
3. Click **"Create Project"** → Name it "Utility Monitor" → Click "Create"
4. In the search bar, type "Custom Search API" → Click it → Click "Enable"
5. Click **"Credentials"** (left sidebar) → **"Create Credentials"** → **"API Key"**
6. Copy your API key and save it somewhere

Now create a search engine:
1. Go to **https://programmablesearchengine.google.com**
2. Click **"Add"** → Choose "Search the entire web"
3. Name it "Utility Monitor" → Click "Create"
4. Click "Customize" → Copy your "Search engine ID"

### Get NewsAPI (100 free requests/day)

1. Go to **https://newsapi.org**
2. Click **"Get API Key"**
3. Fill in the form (choose Developer plan - it's free!)
4. Check your email for confirmation
5. Copy your API key from the dashboard

### Add Keys to Render

1. Go back to your Render dashboard
2. Click on your **"utility-monitor"** service
3. Click **"Environment"** (left sidebar)
4. Click **"Add Environment Variable"**
5. Add three variables:
   - Key: `GOOGLE_API_KEY` → Value: (paste your Google API key)
   - Key: `GOOGLE_CSE_ID` → Value: (paste your Search Engine ID)
   - Key: `NEWS_API_KEY` → Value: (paste your NewsAPI key)
6. Your app will automatically redeploy with the new keys!

Now your crawls will find 10x more mentions! 🚀

---

## 📱 How to Use Your App

### Running Crawls
- **Manual**: Click "Run Crawl Now" whenever you want
- **Automatic**: Set up a cron job (I'll explain below) to crawl every 6 hours

### Reviewing Items
1. New items appear in **"Review Queue"**
2. Click an item to see full details
3. Click **"Approve"** for relevant mentions
4. Click **"Delete"** for spam/irrelevant items
5. Approved items move to **"Approved Items"** tab

### Searching & Filtering
- Use the **search bar** to find specific cities, utilities, or keywords
- Click **"Filters"** to filter by:
  - Source (news sites, city councils, etc.)
  - Location (specific cities/states)
  - Priority (high/normal)
  - Utility type (Electric, Gas, Water)

### Viewing Stats
The dashboard shows:
- **Today**: Items collected today
- **Pending**: Items needing review
- **Approved**: Items you've approved
- **Deleted**: Items you've removed

---

## 🤖 Set Up Automatic Crawling (Optional)

Want your app to crawl automatically every 6 hours? Use a free cron service:

1. Go to **https://cron-job.org**
2. Click **"Sign up"** (free account)
3. Verify your email
4. Click **"Create cron job"**
5. Fill in:
   - **Title**: "Utility Monitor Crawl"
   - **URL**: `https://YOUR-APP-URL.onrender.com/api/crawl`
     (replace YOUR-APP-URL with your actual URL)
   - **Schedule**: 
     - Every: 6 hours
     - Or use: `0 */6 * * *` (runs at midnight, 6am, noon, 6pm)
   - **Request method**: POST
   - **Request headers**: Add one header:
     - Name: `Content-Type`
     - Value: `application/json`
6. Click **"Create"**

Now your app will automatically crawl 4 times per day! ✨

---

## 🆘 Troubleshooting

### "My app URL shows an error"
- Wait 5 minutes - first deploy can be slow
- Check Render logs (Dashboard → Your service → Logs)
- Make sure all files uploaded correctly to GitHub

### "Run Crawl Now doesn't work"
- Check that your app finished deploying (look for "Deploy live" in Render)
- Try refreshing your browser
- Check Render logs for errors

### "I don't see any results after crawling"
- This is normal if there's no recent news
- Try running the crawl a few times
- Add API keys for better results (see Bonus section above)

### "My app stopped working"
- Free Render apps "sleep" after 15 minutes of inactivity
- Just visit your URL - it will wake up in ~30 seconds
- Upgrade to paid tier ($7/month) for always-on hosting

---

## 💡 Tips & Best Practices

1. **Bookmark your app URL** for easy access
2. **Run crawls 2-3 times per day** for fresh data
3. **Add API keys** for 10x better coverage
4. **Review items regularly** to keep your database clean
5. **Use filters** to focus on specific locations or utilities
6. **Export data** (click API endpoints in DEPLOY.md) to download your database

---

## 🎓 What You've Accomplished

You now have:
- ✅ A live web application accessible from anywhere
- ✅ Automated data collection from multiple sources
- ✅ A professional admin interface to manage data
- ✅ The ability to track utility municipalization nationwide
- ✅ All of this for **$0/month**!

You didn't write a single line of code, but you deployed a full-stack web application. That's impressive! 🎉

---

## 📞 Need Help?

If you get stuck:

1. **Check the logs**: Render Dashboard → Your Service → Logs tab
2. **Re-read the relevant section** of this guide carefully
3. **Start over**: You can delete and recreate everything - it's all free!
4. **Common issues are in Troubleshooting section** above

---

## 🚀 Next Steps

Want to do more?

1. **Customize the app**: 
   - Change colors/styling in `static/index.html`
   - Add more cities to monitor in `crawler.py`
   
2. **Upgrade hosting**: 
   - Pay $7/month on Render for:
     - Always-on (no sleeping)
     - Custom domain (utility-monitor.com)
     - Faster performance

3. **Share your app**:
   - Give the URL to colleagues
   - Multiple people can use it simultaneously
   - Data is shared across all users

---

## 🎉 Congratulations!

You've successfully deployed a production web application with no coding experience. You're now tracking utility municipalization conversations across the United States with your own custom tool!

**Your app is live at: [your-render-url]**

Welcome to the world of web applications! 🌐
