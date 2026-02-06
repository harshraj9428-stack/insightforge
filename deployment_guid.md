# Deployment Guide: Host Your Dashboard Online (Free, 10 Mins)

For Premium packages, I'll deploy to Streamlit Cloud (free tier) – clients access via URL (e.g., yourbusiness.streamlit.app). No server needed.

## Step-by-Step Setup
1. **Prepare GitHub Repo** (Free Account):
   - Go to [github.com](https://github.com) > Sign up/login.
   - New Repo: Name "analytics-dashboard-[clientname]" > Public > Create.
   - Upload Files: Drag/drop ZIP contents (app.py, scripts, requirements.txt, README.md, sample_data).
     - Exclude: cleaned_data, reports, secrets.toml, venv.
   - Commit: "Initial dashboard files" > Push.

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io) > Sign up with GitHub.
   - New App > Select your repo > Branch "main" > Main file "app.py".
   - Advanced: Settings > Paste secrets.toml content into "Secrets" tab (auth password, email config).
   - Deploy: "Deploy" button – takes 1-2 mins.
   - URL: Copy (e.g., https://your-app.streamlit.app) – share with client.

3. **Test Deployment**:
   - Open URL > Login with password from secrets.
   - Upload sample CSV > Filter/charts work.
   - Email: "Email Report" sends from your Gmail (test to yourself).
   - Custom Data: Client uploads their CSV via sidebar.

## Maintenance
- Updates: Edit files in GitHub > Redeploy (auto).
- Private Access: Upgrade to $10/mo (password-protected URL).
- Automation: For scheduled emails, use GitHub Actions (I can set up for +$20).
- Cost: Free for public; scales to 1,000 users/mo.
- Issues: Check logs in Streamlit dashboard; message me for fixes.

Your live dashboard is ready – no local install needed! Questions? Zoom call included.