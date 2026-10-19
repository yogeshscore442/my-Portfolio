# Yogesh M S — 3D Cybersecurity Portfolio

A high-end single-page cybersecurity portfolio with:

- Three.js 3D hero and contact visuals
- GSAP scroll reveals and page transitions
- Animated video background
- Magnetic buttons and cursor effects
- 3D tilt cards
- Project slideshow with autoplay, arrows and dots
- Responsive mobile navigation
- Cybersecurity-focused visual language
- Resume-based content and profile image

## Run locally

Because the site loads Three.js/GSAP from CDN, use a local web server instead of opening `index.html` directly.

### Option 1 — VS Code
Install the **Live Server** extension, then right-click `index.html` → **Open with Live Server**.

### Option 2 — Python
```bash
cd yogesh-3d-portfolio
python -m http.server 5500
```
Open `http://localhost:5500`.

## Files

- `index.html` — page structure and portfolio content
- `styles.css` — responsive UI, animations and effects
- `script.js` — Three.js, GSAP, navigation, cursor, tilt and slideshow
- `assets/profile.png` — profile photo supplied for the portfolio
- `assets/cyber-loop.mp4` — abstract cyber background video

## Customize

1. Replace `assets/profile.png` if you want a different profile photo.
2. Replace `assets/cyber-loop.mp4` with your own cyber-themed video if desired.
3. Update email/phone/LinkedIn inside `index.html`.
4. Add GitHub/project links to the project cards.
5. For deployment, upload the folder to Netlify, Vercel, GitHub Pages, or another static host.

# my-Portfolio
