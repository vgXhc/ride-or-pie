#!/usr/bin/env python3
"""
Self-host post images using your Google Takeout originals.

Most Blogger image URLs embed the original filename directly, e.g.:

    https://blogger.googleusercontent.com/img/b/.../s1600/IMG_20141010_180430.jpg
                                                            ^^^^^^^^^^^^^^^^^^^^^^
This script pulls that filename straight out of the URL and looks it up in
your Takeout "Blogger/Albums/<blog name>/" folder -- no network requests, no
guessing, just a direct filename match. Only the small number of newer-style
URLs that don't carry a filename (.../img/a/<opaque-id>) are left unhandled
here, since they're a small minority (see the printed count).

Run locally, from the root of the Hugo site (where hugo.toml lives):

    python3 scripts/match_and_copy_images.py --album-dir "/path/to/Blogger/Albums/Ride or Pie_!" --dry-run
    python3 scripts/match_and_copy_images.py --album-dir "/path/to/Blogger/Albums/Ride or Pie_!"

Safe to re-run -- already-copied images are skipped.
"""
import argparse
import glob
import hashlib
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_GLOBS = [str(ROOT / "content" / "posts" / "*.md"), str(ROOT / "content" / "*.md")]
IMAGES_DIR = ROOT / "static" / "images"

URL_RE = re.compile(r'https://blogger\.googleusercontent\.com/[^"\s\)]+')
OLD_STYLE_RE = re.compile(r'^https://blogger\.googleusercontent\.com/img/b/[^/]+/[^/]+/[^/]+/([^/]+)$')
NEW_STYLE_RE = re.compile(r'^(https://blogger\.googleusercontent\.com/img/a/[^=]+)(=.*)?$')

CONTENT_TYPE_EXT = {
    "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/png": ".png",
    "image/gif": ".gif", "image/webp": ".webp", "image/bmp": ".bmp",
}


def gather_content_images():
    files = []
    for pattern in CONTENT_GLOBS:
        files.extend(glob.glob(pattern))

    urls = set()
    for f in files:
        text = Path(f).read_text(encoding="utf-8")
        urls.update(URL_RE.findall(text))

    return files, urls


def new_style_key(u):
    return NEW_STYLE_RE.match(u).group(1)


def pick_best_new_variant(variants):
    bare = [v for v in variants if v == new_style_key(v)]
    if bare:
        return bare[0]

    def score(v):
        m = re.search(r"=s(\d+)$", v)
        if m:
            return int(m.group(1))
        m = re.search(r"=w(\d+)-h(\d+)$", v)
        if m:
            return int(m.group(1)) * int(m.group(2))
        return 0

    return max(variants, key=score)


def group_new_style(urls):
    """Group opaque-ID URL variants (different sizes of the same photo)."""
    groups = {}
    for u in urls:
        groups.setdefault(new_style_key(u), set()).add(u)
    return groups


def download_new_style(key, variants, dry_run):
    stem = hashlib.sha1(key.encode()).hexdigest()[:16]
    for ext in (".jpg", ".png", ".gif", ".webp", ".bmp"):
        existing = IMAGES_DIR / f"{stem}{ext}"
        if existing.exists():
            return existing.name

    best_url = pick_best_new_variant(list(variants))

    if dry_run:
        return f"{stem}.jpg (dry-run, not fetched)"

    try:
        import requests
    except ImportError:
        print("  requests not installed -- run: pip install requests")
        return None

    try:
        r = requests.get(best_url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        ctype = r.headers.get("Content-Type", "").split(";")[0].strip()
        ext = CONTENT_TYPE_EXT.get(ctype, ".jpg")
        out_path = IMAGES_DIR / f"{stem}{ext}"
        out_path.write_bytes(r.content)
        return out_path.name
    except Exception as e:
        print(f"  FAILED: {best_url} -> {e}")
        return None


def build_filename_index(album_dir):
    """Map filename -> local path, for every file in the Takeout album."""
    album_dir = Path(album_dir)
    index = {}
    for p in album_dir.iterdir():
        if p.is_file() and p.suffix.lower() != ".json":
            index[p.name] = p
    print(f"Indexed {len(index)} original files in {album_dir}.")
    return index


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--album-dir", required=True,
                     help='Path to Takeout\'s "Blogger/Albums/<blog name>" folder')
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    filename_index = build_filename_index(args.album_dir)
    files, urls = gather_content_images()
    print(f"Found {len(urls)} image URL references across {len(files)} content files.")

    url_to_local = {}
    matched, missing_local = 0, 0
    new_style_urls = []

    for u in urls:
        m = OLD_STYLE_RE.match(u)
        if m:
            filename = urllib.parse.unquote(m.group(1))
            local_src = filename_index.get(filename)
            if local_src:
                out_path = IMAGES_DIR / filename
                if not args.dry_run and not out_path.exists():
                    out_path.write_bytes(local_src.read_bytes())
                url_to_local[u] = f"/images/{filename}"
                matched += 1
            else:
                missing_local += 1
                print(f"  no local file found for: {filename}")
            continue

        if NEW_STYLE_RE.match(u):
            new_style_urls.append(u)

    # Opaque URLs (no embedded filename) -- fall back to downloading from
    # Blogger's CDN, deduping the different size variants of each photo.
    new_style_groups = group_new_style(new_style_urls)
    downloaded = 0
    for key, variants in new_style_groups.items():
        filename = download_new_style(key, variants, args.dry_run)
        if filename:
            local_path = f"/images/{filename}"
            for v in variants:
                url_to_local[v] = local_path
            downloaded += 1

    print(f"\nMatched from your Takeout originals: {matched}")
    print(f"Old-style URLs with no matching local file: {missing_local}")
    print(f"New-style opaque URLs, downloaded from Blogger CDN: {downloaded} "
          f"(covering {len(new_style_urls)} references)")

    if args.dry_run:
        print("\nDry run -- not rewriting content files.")
        return

    print("\nRewriting content files...")
    changed = 0
    for f in files:
        p = Path(f)
        text = p.read_text(encoding="utf-8")
        new_text = text
        for orig_url, local_path in url_to_local.items():
            if orig_url in new_text:
                new_text = new_text.replace(orig_url, local_path)
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            changed += 1

    print(f"Rewrote {changed} content files.")
    print(f"Images saved under: {IMAGES_DIR}")
    print("Review with: hugo server -D")


if __name__ == "__main__":
    main()
