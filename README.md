# 송태의 · AI & 제품

Taieui Song's personal blog about applied AI, product engineering, research, and making things. Built with [Astro](https://astro.build), with Markdown posts and GitHub Pages hosting.

Public site: https://kofboy2000.github.io/personal-blog/

The `drafts/` directory holds material awaiting author review. It is outside `src/pages/` and is not published to the website. Existing posts are preserved; a new author introduction is available as a draft.

## Writing posts

Add a `.md` file to `src/pages/posts/`:

```markdown
---
title: 'My Post Title'
description: 'A short excerpt shown on the homepage and in feeds.'
date: '2025-04-01'
tags: ['llm', 'agents']
---

Your content here...
```

Set `draft: true` in the frontmatter to hide a post.

## Posting Jupyter notebooks

You can turn a Jupyter notebook into a blog post **without writing any Markdown** — the notebook itself becomes the post, including its code, outputs, and plots.

1. Put your notebook in `notebooks/` (e.g. `notebooks/my-tutorial.ipynb`).
2. Add a **raw cell at the very top** of the notebook containing the post metadata as JSON:

   ```json
   {
     "title": "My Tutorial Title",
     "description": "Short excerpt for the homepage and feeds.",
     "date": "2025-04-01",
     "tags": ["tutorial", "machine-learning"]
   }
   ```

3. Run the conversion script:

   ```bash
   pip install nbconvert jupyter matplotlib  # plus whatever your notebook imports
   python scripts/notebook_to_post.py        # converts all notebooks in notebooks/
   ```

The script **executes the notebook** (so plots/outputs are always fresh) and converts it to Markdown with outputs embedded, copies the generated images to `public/notebook-assets/<notebook-name>/`, and writes the final post to `src/pages/posts/<notebook-name>.md` with front matter prepended. Commit and push — the post goes live with the rest of the blog.

The script also generates **nbconvert HTML notebook versions** of each notebook, embedded as-is on dedicated pages in two layouts so you can compare designs:

* `/notebooks/<notebook-name>-full` — notebook content spans the full screen width (like the [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/05.06-linear-regression.html) pages)
* `/notebooks/<notebook-name>-centered` — notebook content is centered and occupies a fixed max width (920px)

The classic Markdown post remains available at `/posts/<notebook-name>`.

The converted `.md` and assets are checked in, so the GitHub Pages build does not need Python — the notebook pipeline runs only on your machine.

## Development

```bash
npm install
npm run dev       # local dev server
npm run build     # production build to ./dist
npm run preview   # preview the production build
```

## Deploying to GitHub Pages

The existing `.github/workflows/deploy.yml` builds with Node.js 20 and publishes `dist` to GitHub Pages after a push to `main` or a manual workflow dispatch. Pull requests do not automatically deploy. Review changes on a branch before merging.

The Astro configuration uses `site: 'https://kofboy2000.github.io'` and `base: '/personal-blog'`. Keep that base path in internal links.

## Configuration

Edit `src/config.ts` to change the site title, author, description, and verified profile links. Add X, Threads, or YouTube links only after selecting the author's branding accounts. Update `site` and `base` in `astro.config.mjs` if the public URL changes.

## Subscription

Email subscriptions are not enabled. `/subscribe` points readers to RSS; it does not collect email addresses. RSS and JSON feeds are available at `/personal-blog/rss.xml` and `/personal-blog/feed.json`.
