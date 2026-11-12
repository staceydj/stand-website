# STAND homepage

STAND's homepage, built on the layout of a remade consultancy site, with STAND's own pictures and copy. Plain HTML, CSS and a small vanilla JS file. No build step and no framework.

## Run it

```bash
cd stand-website && python3 -m http.server 8000
```

Then open http://localhost:8000. Use a local server rather than opening the file directly, because browsers block the font preload over `file://`.

## Structure

- `index.html`: the page, in 11 sections (hero, signpost, services, offers, testimonials, about, resources, CTA, summit, contact, footer)
- `css/styles.css`: the design tokens (brand colours, Montserrat, Bonvivant serif, handwritten accent font) and all the layout
- `js/main.js`: nav and dropdowns, mobile menu, scroll reveals, parallax, the recognition slider and the contact form
- `assets/`: STAND's photos and logo, the generated scenery, the line art and the two custom fonts, all served locally
- `tools/verify.js`: the automated checks that write `REMAKE_REPORT.md`

## Verify

```bash
node tools/verify.js tools/original-en.html <original-image-dir> tools/stand-source.txt
```

The two TO TOP comparison checks need local copies of the original page and images. Those are deliberately not in this repository, so without them those two checks report as not run.

This checks that every image comes from the new STAND sets, and that none of the original site's images, names, contacts or sentences remain. It also checks that every figure on the page appears on standaction.co.za and that all links resolve. Finally, it checks for JS errors, broken images and horizontal scroll at 375, 768 and 1440px, and tests the key interactions. The report ends with `REMAKE COMPLETE` only when every check passes.

## Copy

The page keeps the remake's layout. Every word comes from STAND's own site (standaction.co.za), saved in `tools/stand-source.txt` so it can be checked.

- Sections map to STAND's content. The hero becomes "coordinated action", followed by why systems fail in the handovers, the four focus areas, delivery capabilities, recognition and track record, About STAND and its values, field results, support, the Track Her Case scale-up, and contact.
- The original testimonial slider held client quotes, and STAND's site publishes none. The slider now shows STAND's recognition record as statements attributed to the bodies involved, not as quotes.
- Links point to the matching sections of standaction.co.za. Contact details are stacey@standaction.co.za and +27 82 554 8831.
- Removed because they belonged to TO TOP: the info video, the German language switch, the terms PDF, the booking link and the "Created by" credit.
- The contact form opens the visitor's e-mail program, addressed to stacey@standaction.co.za. There's no server behind it.

## Where every picture comes from

Every photograph is STAND's own, from standaction.co.za or supplied by STAND, and graded to the brand teal. No AI-generated imagery is used.

- `assets/stand/`: STAND's logo mark, headshots, work and conference photos, app screenshots and the share image.
- `assets/docs/`: the Track Her Case project brief.
- `assets/art/`: line icons, dashed paths, contour lines and the route map, drawn in code by `tools/make_art.py`.
- `incoming/`: STAND's original uploads, kept as supplied. The site uses the resized copies in `assets/stand/`.

Run `python3 tools/build_pages.py` after changing copy or photos. It rebuilds every inner page from the homepage's nav and footer.

## November 2026 update

- `campaign.html` is the Track Her Case giving campaign. It is the only page that says "Give now".
- Paste the GlobalGiving and BackaBuddy page links into `GLOBALGIVING_URL` and `BACKABUDDY_URL` in `tools/build_pages.py`, then run `python3 tools/build_pages.py`. Until then their cards show "page opening soon".
- Fonts are free (SIL Open Font License) and served from `assets/fonts`: Playfair Display for headings, Montserrat for text.
- WhatsApp and social previews use the `og:image` tags. The site-wide card is `assets/social/stand-share.jpg`; the campaign uses `assets/stand/give-share.jpg`. These need the live domain to work.
