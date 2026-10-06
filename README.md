# AI Notebook — Personal AI Blog

A minimal, clean personal blog focused on AI, LLMs, AI Agents, AI Movies, AI Animation and AI Manga. Built with [Astro](https://astro.build), posts written in Markdown, hosted on **Cloudflare Pages**.

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

## Development

```bash
npm install
npm run dev       # local dev server
npm run build     # production build to ./dist
npm run preview   # preview the production build
```

## Deploying to Cloudflare Pages

1. Push this repo to GitHub.
2. In the Cloudflare dashboard: **Workers & Pages → Create → Pages → Connect to Git** and select the repo.
3. Build settings (usually auto-detected):
   - **Framework preset:** Astro
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
4. Deploy. Every push to the main branch auto-deploys; PRs get preview URLs.

Or deploy from your machine:

```bash
npm run build
npx wrangler pages deploy dist
```

## Configuration

Edit `src/config.ts` to change the site title, author, description, social links, and newsletter subscribe URL. Update `site` in `astro.config.mjs` to your final domain.

## Newsletter

The subscribe form on `/subscribe` currently points to a placeholder endpoint. Swap the `action` in `src/pages/subscribe.astro` and the homepage form for your provider (Buttondown, Listmonk, Mailchimp, etc.). RSS and JSON feeds are available at `/rss.xml` and `/feed.json`.
