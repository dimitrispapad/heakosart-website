# TheakosArt — website rebuild

A full rebuild of theakosart.gr as a fast static site: Greek at the root, English under `/en`,
57 pages in total (home, services, works, 23 project pages, studio, contact, per language).
No framework and no build tools beyond Python 3.

## Run it

```bash
python3 scripts/fetch_images.py   # once: copies the photos from the old site into assets/img
python3 build.py                  # regenerates every page
python3 -m http.server 8000       # open http://localhost:8000
```

Until `fetch_images.py` has been run, photos load directly from the current theakosart.gr
media library. Run it before the old WordPress site is switched off.

## Edit it

Everything lives in `build.py`: copy in both languages, the project list, services, team, and
which photo goes where (`HERO`, `WALK`, `P`). Change it there and run `python3 build.py`.
Design tokens are at the top of `assets/css/main.css`; motion is in `assets/js/main.js`.

## What each discipline delivered

| Role | Delivered |
|---|---|
| Brand strategy | Positioning "no two projects are alike", tone of voice, the door/threshold idea that ties brand to motion |
| Marketing & copy | All copy rewritten in Greek and English; services regrouped from 12 loose items into 6 clear offers; a six-step process |
| UX | New sitemap, a page per project, category filter, one contact path on every page, bilingual switch |
| UI & graphic design | Palette from the island (plaster, granite, night sea), GFS Didot + Commissioner type, Θ monogram and favicon |
| Motion | Door intro and page transitions, hero aperture slideshow, the outside-to-inside scroll walk, horizontal works rail, parallax, word reveals, counters, custom cursor |
| Development | Static generator, responsive down to phones, keyboard focus, reduced-motion support, works without JavaScript |
| SEO | Titles and descriptions per page, hreflang, canonical, sitemap.xml, robots.txt, schema.org GeneralContractor |

## Check before launch

- Photo order: the hero and the outside-to-inside walk were assigned from file names and captions,
  without viewing the photos. Check `HERO` and `WALK` in `build.py` and reorder if an interior sits where an exterior should.
- Each project has one photo on the old site. Add more to `assets/img` to build real galleries.
- Project years are the publication years on the old site, not confirmed completion years.
- Team names and titles are transliterated for English; confirm the preferred spelling.
- The contact form opens the visitor's email app. Swap in a form backend if messages should be sent from the page.
- Fonts load from Google Fonts. Self-host them if the client wants no third-party requests.
- Old WordPress URLs (`/works/...`, `/team`, `/contacts`) need redirects to the new ones on the final host.

## Publish with GitHub Pages

Repository → Settings → Pages → Source: "Deploy from a branch" → `main` / root. For the live domain,
add `www.theakosart.gr` under "Custom domain" and point the domain's DNS to GitHub Pages.
