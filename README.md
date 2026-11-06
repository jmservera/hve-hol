---
title: HyperVelocity Engineering · Hands-on workshop exercise guide
description: Static participant guide with workshop exercises, starting guidance and editable templates.
---

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

   The script rewrites `docs/*.html` and checks that every internal link and `#anchor` resolves. Run the
   standard-library regression checks after rebuilding:

   ```bash
   python -m unittest discover -s tools -p "test_*.py"
   ```
3. Commit and push; GitHub Pages republishes automatically.

Inline formatting in any text: `` `code` ``, `**bold**`, `[link text](url)`.
Styles live in `docs/assets/site.css` and behaviour in `docs/assets/site.js`; both are edited directly.

Keep public content organization-neutral. Do not publish source presentations, customer-branded images,
private source paths or facilitator-only answer keys.

Workshop examples use Azure DevOps and GitHub for delivery. SharePoint documents and Microsoft Teams
notes can supply evidence through optional Work IQ MCP, subject to approved read tools, user access,
tenant policy and preview retrieval/billing readiness. The fictional source pack works without a live
Microsoft 365 connection. Source retrieval is read-only for the workshop; Work IQ is not inherently
read-only, and delivery writes still need approval.

Exercise numbers and URLs follow the workshop order: Exercise 5 is the RPI run, 6 reuses a correction from
its review, 9 is adoption and 10 is the optional comparison. The backup section follows playback in navigation,
but is only attempted before the fixed close if time remains.

Renumbered pages keep their original `storage_slug` so saved answers and hand-in ticks follow the activity,
not the number. Preserve existing template IDs and editable-cell order when updating them. The replacement
Exercise 1 has a new namespace and worksheet IDs so old recorded-run answers or ticks cannot complete it;
legacy browser values are left untouched.

## What participants get

- One page per step, with previous / next buttons, a sidebar on desktop and a **Steps** menu on phones.
- Each exercise has a brief (objective, input, best use, roles, steps, hand-in) and a toolkit. Exercises 2–10
  also have four numbered **How to start** steps, practical advice and **Watch out** traps. Exercise 5
  includes a named-role split panel so Exercise 7 starts while implementation runs.
- Template cells can be typed into. **Copy as Markdown** copies a template, with whatever was typed, to paste into a
  repository, wiki or issue. Typed text and hand-in ticks stay in the participant's browser (localStorage) and are
  never sent anywhere.
- Exercise 1 is a no-agent fictional appointment scenario: six questions, a blank scored answer sheet,
  and six separately collapsed illustrative reveals. Facilitator-only coaching and answer keys are not included.
- Exercise 6 captures a real correction from Exercise 5 and records a step re-run without that correction.
- Optional Exercise 10 compares one changed variable on the same item, commit and request. Short runs compare
  research and plan on both sides; cross-team observations are labelled separately.
- Links to Intermissions A–C from the exercises they run alongside, and an intermissions overview on the home page.
- A resources page with a filter box, links by exercise and an index of all templates.
- Light and dark mode follow the device setting, and pages print cleanly.
