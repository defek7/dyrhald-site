# Dyrhald website

A plain static website: HTML pages, one stylesheet, a little JavaScript and WebP images.
No database, no server code and nothing to install on the host. Any web hosting that serves files can run it.

## What's in here

| File / folder | What it is |
|---|---|
| `index.html` | Home page |
| `world.html` | The world, depth bands, the two species, creatures, the Den |
| `media.html` | Screenshot gallery (click a picture to see it big) |
| `news.html` | Release notes, built from the game's `ReleaseNotes.json` |
| `join.html` | How to join the alpha: Discord, and the launcher from its Testing channel |
| `faq.html` | Questions and answers |
| `404.html` | The "page not found" page |
| `css/style.css` | All the colours, fonts and layout |
| `js/site.js` | Menu on phones, gallery viewer, and **the Discord invite link** |
| `img/` | Pictures (WebP, already compressed) |
| `data/ReleaseNotes.json` | A copy of the game's release notes |
| `partials/` | The menu bar and footer that every page shares |
| `tools/` | Two small Python scripts (not needed on the web host) |
| `.htaccess` | Settings for GoDaddy's web server (cPanel only; GitHub Pages ignores it) |
| `CNAME`, `.nojekyll` | Tell GitHub Pages the site is dyrhald.com and to serve the files as they are |
| `robots.txt`, `sitemap.xml` | Help search engines find the pages |

## The Discord invite and the launcher

The site is for **dyrhald.com**, and every Discord button points to `https://discord.gg/HhMNbjZHPn`.
The launcher zip is **not** on the website: the Join page tells testers it's pinned in the Discord's Testing channel.

To change the invite, search the folder for `discord.gg/HhMNbjZHPn` and replace it everywhere: in `js/site.js` (top line),
`partials/footer.html`, `index.html` and `join.html`. Then run `tools/build.py` and upload the changed files.

## Update the news after a release

1. Update `Assets/Resources/ReleaseNotes.json` in the game as usual.
2. Run:

   ```bash
   python Website/tools/build.py
   ```

   This copies the release notes in, rewrites `news.html` (every release, newest first) and the "Latest news" box on the home page.
   It also copies `partials/header.html` and `partials/footer.html` into every page, so if you change the menu, edit those and run it again.
3. Upload the changed files (`news.html`, `index.html`, `data/ReleaseNotes.json`).

## Add a screenshot

```bash
python Website/tools/add_shot.py "path/to/screenshot.png" my-shot-name
```

That makes `img/my-shot-name.webp` (big) and `img/my-shot-name-sm.webp` (small). Add `--crop 380,70,1660,930` to cut the HUD off a 1920×1080 shot.
Then, in `media.html`, copy one `<figure>` line and change the names and caption. It needs Pillow (`pip install pillow`), which is already installed on this PC.

## Look at it on your own PC first

```bash
python -m http.server 8765 --directory Website
```

Then open http://127.0.0.1:8765 in a browser. Stop it with Ctrl+C.

## Put it online (GoDaddy Website Builder + free GitHub Pages)

GoDaddy's **Website Builder** ("Websites + Marketing") can't take uploaded files. So the site lives on **GitHub Pages**, which is free,
and the **domain stays at GoDaddy**. You only change where dyrhald.com points. Nothing to buy.

### A. Publish the files on GitHub Pages (once)

1. Make a new **public** GitHub repository, e.g. `defek7/dyrhald-site`, with the *contents* of `Website/` at its top level
   (`index.html` next to `CNAME`). Any Claude session can do this with `gh` once you say so.
2. On GitHub: the repository → **Settings** → **Pages** → Source **Deploy from a branch**, branch `main`, folder `/ (root)` → **Save**.
3. The `CNAME` file tells GitHub the site is **dyrhald.com**. You should see it under **Custom domain** on that page.

### B. Point dyrhald.com at it (in GoDaddy, you do this part)

1. godaddy.com → **My Products** → next to **dyrhald.com**, click **DNS** (or **Manage DNS**).
   If GoDaddy says the domain is connected to your Website Builder site, disconnect it there first
   (Websites + Marketing → your site → **Settings** → domain → disconnect), then come back to DNS.
2. Delete the existing **A** record(s) whose name is **@** (today that's GoDaddy's "parked" page), and the **www** record if it
   points somewhere other than GitHub. **Leave MX, TXT, SRV and any email-looking CNAME records (autodiscover, email, etc.) alone.**
   dyrhald.com has GoDaddy email, and those records keep it working.
3. Add four **A** records, each with name **@**:
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
4. Add a **CNAME** record: name **www**, value **defek7.github.io**
5. Wait. It usually works within an hour, sometimes up to a day. Then go back to GitHub → Settings → Pages and tick
   **Enforce HTTPS** once it lets you, so the site loads as `https://dyrhald.com`.

After that, the Website Builder site isn't used any more. You can cancel it if you pay for it; the domain isn't affected.

### Updating the live site

Change files in `Website/`, run `tools/build.py`, then copy the changed files into the `dyrhald-site` repository, commit and push.
GitHub puts it live within a minute or two. A Claude session can do all of this for you after each release.

## Upload to GoDaddy (cPanel / "Web Hosting"), only if you ever switch to a hosting plan

This is for GoDaddy's paid **Web Hosting (cPanel)** plans. You don't need it with GitHub Pages.

1. Sign in at godaddy.com → **My Products** → next to Web Hosting, click **Manage** → **cPanel Admin**.
2. In cPanel, open **File Manager** and go into the `public_html` folder. That folder is your website.
   If an old site is in there and you want to keep a copy, select everything, **Compress** it into a zip and download it first.
3. Upload everything *inside* `Website/`, not the `Website` folder itself, so `index.html` sits directly in `public_html`.
   The easy way is to zip it: on Windows, open the `Website` folder, select everything inside it (including `.htaccess`; turn on
   View → Show → Hidden items if you can't see it), right-click → **Compress to ZIP file**. In File Manager, click **Upload**, pick the zip,
   then go back, right-click the zip in `public_html` → **Extract**, and delete the zip afterwards.
4. You don't need to upload `tools/`, `partials/` or `README.md`. They're harmless if you do.
5. Visit your domain. If you still see the old page, press Ctrl+F5 to skip the browser's saved copy.

To update later, upload only the files that changed. Uploading a file with the same name replaces the old one.

**FTP instead of File Manager:** in cPanel, under **FTP Accounts**, you can make an FTP login and use a program like FileZilla.
Connect to your domain on port 21 (or SFTP on 22 if your plan offers it) and drag the contents of `Website/` into `public_html`.
Type the password into FileZilla yourself. Don't paste it into chats or into files in this project.

**HTTPS:** most GoDaddy hosting plans include a free SSL certificate. In cPanel, look for **SSL/TLS Status** and run AutoSSL, so the site loads as `https://`.
