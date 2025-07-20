# 🚀 Oral Health AI Deployment Guide (Railway + Vercel)

This guide explains how to deploy your full-stack ML-powered app:
- **Backend (Flask + ML):** Railway
- **Frontend (React):** Vercel

---

## 1. Backend Deployment (Railway)

1. **Push all code to GitHub** (including `api/`, `models/`, `Procfile`, `requirements.txt`).
2. Go to [railway.app](https://railway.app) and log in.
3. Click **New Project** → **Deploy from GitHub repo**.
4. Select your repo (`oral-health`).
5. Railway will auto-detect Python and use your `Procfile`:
   - Should run: `web: python api/app.py`
6. Wait for build and deployment to finish.
7. **Copy your Railway public API URL** (e.g., `https://your-app-name.up.railway.app`).
8. Test the API: visit `/` for health check, `/upload` for predictions.

---

## 2. Frontend Deployment (Vercel)

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard).
2. Click **New Project** and import your GitHub repo.
3. Set **Root Directory**: `dental-image-upload`.
4. **Build Command**: `npm run build`
5. **Output Directory**: `build`
6. **Add Environment Variable**:
   - **Key:** `REACT_APP_API_URL`
   - **Value:** Your Railway API URL (e.g., `https://your-app-name.up.railway.app`)
7. Deploy!
8. After deployment, open your Vercel frontend URL and test image upload.

---

## 3. Environment Variable Recap

- **Vercel (Frontend):**
  - `REACT_APP_API_URL` = Railway backend URL
- **Railway (Backend):**
  - No special variables needed unless you add secrets/config

---

## 4. Troubleshooting

- **Image upload fails/405 error:**
  - Make sure `REACT_APP_API_URL` is set in Vercel and points to your Railway backend.
- **Model not found:**
  - Ensure `models/` directory is inside `api/` and files are present in Railway.
- **CORS issues:**
  - Your backend uses Flask-CORS with `origins=['*']`. For production, restrict to your frontend domain.
- **Logs:**
  - Check Railway and Vercel dashboards for build/runtime logs.

---

## 5. Useful Links
- [Railway Dashboard](https://railway.app/dashboard)
- [Vercel Dashboard](https://vercel.com/dashboard)
- [React Create React App Docs](https://create-react-app.dev/)
- [Flask Docs](https://flask.palletsprojects.com/)

---

## 6. Next Steps & Improvements
- Add custom domains to Vercel/Railway for a professional URL
- Add user authentication, history, or more ML features
- Monitor logs and errors for reliability
- Optimize your ML model for speed/accuracy

---

**Congratulations! Your ML-powered web app is live and ready for users!** 