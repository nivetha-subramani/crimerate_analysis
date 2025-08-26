
# Crime Rate Analysis (Streamlit)

A simple, host-ready Streamlit dashboard to analyze crime data (with a sample India-like dataset).  
Filter by year, state and crime type; view trends, rates per 100k, and city-level bubbles.

## 🗂 Project Structure
```bash
crime-rate-analysis/
├─ app.py
├─ requirements.txt
├─ Procfile
├─ data/
│  └─ sample_crime_data.csv
└─ .gitignore
```

## ▶️ Local Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ One-click Hosting (Streamlit Community Cloud)
1. Push this folder to **GitHub** as a public repo.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. **New app** → select your repo → `branch: main` → `file: app.py` → Deploy.
4. Add these **Secrets** if needed (not required for the sample): none by default.

## 🌐 Alternative Hosting (Render)
1. Push to GitHub.
2. On [Render](https://render.com), create a **Web Service** from the repo.
3. Set **Runtime**: Python 3.x.  
   **Build Command**: `pip install -r requirements.txt`  
   **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Deploy.

## 📄 CSV Format
Your CSV must include columns:
`year, month, state, city, crime_type, incidents, population`

The app calculates **crime_rate_per_100k = incidents / population * 100000**.

## 🛠 Customize
- Replace `data/sample_crime_data.csv` with your data.
- Adjust charts inside `app.py` (Plotly).
- Add new pages via Streamlit’s `pages/` directory.

---
_Generated on 2025-08-26 04:19 ._
