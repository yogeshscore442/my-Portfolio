# YOGESH // Cybersecurity Portfolio

A cinematic, cyberpunk-inspired portfolio built with React, Vite, Three.js, React Three Fiber, Drei and GSAP.

## Features

- 3D interactive hero using Three.js / React Three Fiber
- Animated particle field and glass transmission Torus Knot
- Smooth route/page-entry transitions
- Responsive mobile navigation
- Magnetic / hover-reactive buttons
- Project slideshow with auto-rotation + manual controls
- Terminal-style SOC visualizations
- Animated radar / orbit graphics
- Responsive layout for desktop, tablet and mobile
- Resume download
- Profile photo from the supplied image
- Content populated from the supplied resume

## Run locally

```bash
npm install
npm run dev
```

Then open the local Vite URL shown in the terminal.

## Production build

```bash
npm run build
npm run preview
```

## Customize

The main content is in `src/App.jsx`.
Visual styling and responsive behavior are in `src/styles.css`.
Replace `src/assets/profile.png` if you want a different portrait.

## Notes

The visual "video-like" effects are generated in-browser with WebGL/CSS so the project has no large MP4 dependency. If you later want an actual looping MP4 hero background, add it under `public/` and replace the hero background layer with a `<video>` element.
