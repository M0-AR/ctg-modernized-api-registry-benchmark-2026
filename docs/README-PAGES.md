# Publishing `docs/preview.html` with GitHub Pages (2026)

This repository serves its visual summary as a static site. No build step, no framework.

## One-time setup (about 2 minutes)

1. Push this repository to GitHub (public repository works on free accounts).
2. Open **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Choose Branch **`main`** and Folder **`/docs`**, then **Save**.
5. Wait about 1 minute. Open `https://YOUR-USER.github.io/YOUR-REPO/`.

GitHub serves `docs/preview.html`. To make it the default landing page you can either
rename a copy to `docs/index.html` (both files are kept in sync here) or link to
`.../preview.html` directly from the README.

## Verify it worked

- The page header shows `LIVE verified 2026-10-05 · 605,599 studies`.
- Status bars render without network (values are embedded).
- `fig_status_top8.png`, `screenshot.png`, `demo.gif`/`demo.mp4` load from the same folder.

## Upgrades (optional)

- Custom domain: Settings → Pages → Custom domain.
- Actions deploy: use an artifact workflow instead of branch deploy for previews per pull request.
- Keep `docs/` under 1 GB; images here are under 200 KB total except the demo video.
