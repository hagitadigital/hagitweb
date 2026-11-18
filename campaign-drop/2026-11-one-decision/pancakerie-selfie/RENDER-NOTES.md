# One decision · Pancakerie selfie reel — render notes

- `one-decision-pancakerie-9x16.mp4` — 1080×1920, 30fps, 19.4s. `one-decision-pancakerie-4x5.mp4` — feed version (frame45.sh).
- A-roll: `src/hagit-panc.mp4` — Seedance 2.5 video edit of the selfie (first 480p draft, upscaled to 1080×1920 with ffmpeg), background replaced with the Pancakerie patisserie. Muted in the comp.
- Voice: `src/voice.m4a` — the original selfie audio (first 16.5s).
- Motion: HyperFrames composition (`src/index.html`, GSAP timeline). Render: `npx hyperframes render -q high -o out.mp4` inside `src/`.
- Caption timings were set from speech pauses, not from a transcript.
