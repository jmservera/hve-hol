# HyperVelocity Engineering · Hands-on workshop exercise guide

A static website for participants of the HyperVelocity Engineering (HVE) hands-on workshop: a step-by-step guide
through ten team exercises and three intermissions, with fill-in templates and every link for the day.
No build step, frameworks, external fonts, trackers or third-party scripts: the site only loads its own files.

## What's inside

```text
docs/                 the website (what GitHub Pages publishes)
  index.html          home: goals for the day, how to use the guide, step-by-step index
  agenda.html …       one page per step: get started, exercises 1–10, intermissions A–C, playback, scorecard
  resources.html      every link grouped by topic, links by exercise and the template index
  404.html            "page not found"
  assets/             site.css, site.js, favicon.svg
  .nojekyll           tells GitHub Pages to serve the files as they are
tools/
  content.py          all page text, steps, templates, tips and links
  build_site.py       regenerates docs/*.html from content.py (Python 3.8+, standard library only)
```

## Publish on GitHub Pages

1. Create a new public repository on GitHub, for example `hve-workshop-guide`.
2. Push this folder:

   ```bash
   cd hve-workshop-guide
   git init
   git add .
   git commit -m "HVE hands-on workshop guide"
   git branch -M main
   git remote add origin https://github.com/<your-account>/hve-workshop-guide.git
   git push -u origin main
   ```

3. In the repository, open **Settings → Pages**. Under **Build and deployment**, set **Source** to
   **Deploy from a branch**, **Branch** to `main` and the folder to **`/docs`**, then select **Save**.
4. After a minute or two the site is live at `https://<your-account>.github.io/hve-workshop-guide/`.

All links are relative, so the site works under any repository name or a custom domain.

## Preview locally

```bash
python -m http.server 8000 --directory docs
```

Then open <http://localhost:8000>. Opening `docs/index.html` directly in a browser also works.

## Change the content

1. Edit `tools/content.py`: page texts, steps, hand-ins, templates, tips and links. The suggested agenda is the
   `agenda` entry.
2. Rebuild:

   ```bash
   python tools/build_site.py
   ```

   The script rewrites `docs/*.html` and checks that every internal link and `#anchor` resolves.
3. Commit and push; GitHub Pages republishes automatically.

Inline formatting in any text: `` `code` ``, `**bold**`, `[link text](url)`.
Styles live in `docs/assets/site.css` and behaviour in `docs/assets/site.js`; both are edited directly.

## What participants get

- One page per step, with previous / next buttons, a sidebar on desktop and a **Steps** menu on phones.
- Each exercise has a brief (objective, input, best use, roles, steps, hand-in) and a hand-in and toolkit section
  (templates, how to run it with HVE Core or HVE-Squad, links, "done when" and tips).
- Template cells can be typed into. **Copy as Markdown** copies a template, with whatever was typed, to paste into a
  repository, wiki or issue. Typed text and hand-in ticks stay in the participant's browser (localStorage) and are
  never sent anywhere.
- The Exercise 1 reveal stays collapsed until the team opens it.
- Links to Intermissions A–C from the exercises they run alongside, and an intermissions overview on the home page.
- A resources page with a filter box, links by exercise and an index of all templates.
- Light and dark mode follow the device setting, and pages print cleanly.
