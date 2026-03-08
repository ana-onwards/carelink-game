# 🌉 Project Bridge

A spin-the-wheel web app for a group dynamics exercise. Built with Streamlit.

## What It Does

8 directors log in, spin a wheel to get a **department role** (CFO, CMO, etc.), then spin again for a **behavior profile** (The Prize Hire, The Connector, etc.). They then role-play a leadership meeting in character.

The app handles concurrent spins from 8 people simultaneously — no duplicate assignments, no race conditions.

## Quick Start

```bash
pip install streamlit
streamlit run app.py
```

## Login Credentials

**Directors:** `director1` through `director8`, password: `bridge2026`

**Facilitator:** username `facilitator`, password: `facilitator`

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect the repo → select `app.py` → Deploy
4. Share the URL with your directors

## Built With

- [Streamlit](https://streamlit.io) — UI framework
- SQLite — concurrent state management
- HTML5 Canvas — spinning wheel animation

## The Exercise

**Company:** CareLink Solutions (elderly care SaaS)

**The Mission:** Plan a 500-person customer conference in 4 months. $200K budget. The National Veterans Care Alliance will be evaluating CareLink as a partner — this could 3x the business.

**The Twist:** Each director is secretly playing a behavioral archetype — from the team-oriented Connector to the turf-protecting Empire Builder. Dysfunction is by design. The debrief is where the real learning happens.
