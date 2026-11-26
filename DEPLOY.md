# Putting the app online (Streamlit Community Cloud, free)

1. Push this folder to a GitHub repo (all files, including `security_bodies_data1.py`, `security_bodies_data2.py`
   `security_bodies_data3.py`, `assets/`, `logos/`, `.streamlit/`). Each file is under GitHub's 100 MB limit.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app** -> **Deploy a public app from GitHub**.
   - Repository: your repo
   - Branch: `main`
   - Main file path: `app.py`
   - (Advanced settings) Python version: 3.11 or 3.12
4. Click **Deploy**. The first build installs `requirements.txt` (a few minutes) and gives a public URL
   like `https://<your-app>.streamlit.app`. You can set a custom subdomain in the app settings.
5. Every `git push` redeploys automatically.

Notes
- The optional AI-agent features need `requirements-agents.txt` / `requirements-crewai.txt` and API keys.
  Add keys under **App settings -> Secrets**, never in the repo.
- Free apps sleep after inactivity and wake on the next visit. The large logo modules make the first load slower.
- Other hosts (Render, Railway, Hugging Face Spaces) work too: start command
  `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`.
