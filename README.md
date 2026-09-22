# Ride or Pie?! — Hugo site

This is your blog, migrated from Blogger (`ride-or-pie.blogspot.com`) to a
static [Hugo](https://gohugo.io) site using the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

## What's here

- `content/posts/` — 268 published posts, converted from your Blogger
  export. Each keeps its original title, publish date, labels (as tags),
  and **exact original URL** (e.g. `/2026/09/some-new-alps-videos.html`),
  so old links, bookmarks, and search results keep working with no redirects
  needed.
- `content/touring.md`, `content/coffeeneuring2016.md`,
  `content/ibob-unmeeting.md` — your three Blogger pages, same URLs as
  before (`/p/....html`).
- `themes/PaperMod/` — the theme, vendored as plain files (not a git
  submodule) so there's nothing extra to set up.
- `hugo.toml` — site config: title, menu, taxonomies, and
  `markup.goldmark.renderer.unsafe = true`, which is what lets the
  raw HTML in your posts (iframes, embedded videos, tables, styled divs)
  keep rendering exactly as Blogger produced it.
- `netlify.toml` — build settings for Netlify.
- 55 draft/unpublished Blogger entries were **not** migrated (they were never
  public). If you want any of them, let me know and I can pull them in too.

## What did NOT carry over automatically

- **Comments.** A static site has no server to store them. Your options:
  - [Giscus](https://giscus.app) (free, backed by GitHub Discussions)
  - [utterances](https://utteranc.es) (free, backed by GitHub Issues)
  - A hosted service like [Disqus](https://disqus.com) (free tier available,
    but ad-supported)
  Say the word and I can wire one of these into the theme.
- **Images** still point to Blogger's own CDN
  (`blogger.googleusercontent.com`) — that's fine, it works today and isn't
  going away with the migration. If you'd rather self-host every image
  (fully independent of Google), I can write a script to download them all
  into `static/images/` and rewrite the post HTML — it's a bigger job given
  hundreds of images, so only worth doing if you want it.

## Run it locally

```bash
# macOS
brew install hugo

# then, from this folder:
hugo server -D
# open http://localhost:1313
```

## Deploy: GitHub + Netlify

1. **Create a GitHub repo** (e.g. `ride-or-pie`), then from this folder:
   ```bash
   git init
   git add -A
   git commit -m "Migrate from Blogger to Hugo"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ride-or-pie.git
   git push -u origin main
   ```
2. **Connect Netlify:**
   - New site from Git → pick the repo
   - Build command: `hugo --gc --minify` (already set in `netlify.toml`)
   - Publish directory: `public` (already set in `netlify.toml`)
   - Deploy — Netlify auto-detects the Hugo version from `netlify.toml`
     (`HUGO_VERSION = "0.147.9"`)
3. **Custom domain (optional):** if you want a domain other than
   `<sitename>.netlify.app`, add it under Site settings → Domain management,
   and update `baseURL` in `hugo.toml` to match before your next deploy.
4. Once you're happy with the new site, update Blogger's own settings to stop
   serving traffic (or just leave it — Blogger will keep working in parallel
   until you're ready to fully cut over).

## Notes on search & archive pages

The menu includes a full-text **Search** page and a yearly **Archive**
page — both built into PaperMod, no extra service needed.
