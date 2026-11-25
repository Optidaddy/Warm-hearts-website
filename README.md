# Warm Hearts — African Child Charity & NGO Platform

A modern, responsive web application dedicated to nourishing, educating, and empowering African children.

## Features
- **Warm Golden Yellow & Charcoal Black Identity** with custom geometric SVG logo & inline favicon.
- **Persistent Light & Dark Mode** with automatic system theme detection.
- **Multi-Page Views**: Home, About & Programs, Stories & Articles (with category filters & full Article Reader), and Get Involved / Contact.
- **Meshlex AI Assistant**: Interactive floating guide with quick replies and direct M-Pesa donation triggers.
- **M-Pesa Express (STK Push) & Direct Send Money**: Supports Safaricom Daraja STK Push prompts and direct transfers to `+254741913043`.

## Quick Start
1. **Static Hosting (GitHub Pages)**: Push `index.html` to your GitHub repository and enable GitHub Pages.
2. **Full-Stack Hosting (Render with Live Daraja STK Push)**:
   ```bash
   pip install -r requirements.txt
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```
   Set your Safaricom Daraja credentials in `.env` (see `.env.example`).

## Contact
- **Phone / M-Pesa**: +254741913043
- **Email**: meshlinksolutions@gmail.com
