"""Build the Track Her Case campaign landing page (campaign.html).

Usage: python3 tools/build_campaign.py

Phone first: most visitors arrive from a WhatsApp link. The page is
standalone (slim header, no site menu) so nothing competes with giving.
Giving links come from tools/links.py.
"""
import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from links import BACKABUDDY_URL, CAMPAIGN_VIDEO, CAMPAIGN_VIDEO_POSTER, GLOBALGIVING_URL, SNAPSCAN_URL  # noqa: E402

SITE = "https://standaction.co.za/"
PAGE_URL = SITE + "campaign.html"
SHORT_URL = "standaction.co.za/give"
TITLE = "When a woman asks for help, the system should answer."
DESC = ("Track Her Case follows every reported case of violence against women in the Overstrand "
        "through police, health, social services and the courts. Give now and pass it on.")
WA_TEXT = ("When a woman asks for help, the system should answer.\n\n"
           "STAND's Track Her Case follows every reported case of violence against women in the Overstrand "
           "through the police, health, social services and the courts, until it is resolved. "
           "R150 keeps a trained ambassador on duty for a day.\n\nGive or share: " + PAGE_URL)
SOCIAL_TEXT = "When a woman asks for help, the system should answer. Back Track Her Case:"

PHOTOS = json.loads((ROOT / "tools/stand-photos.json").read_text())


def e(s):
    return html.escape(s, quote=False)


def a(s):
    return html.escape(s, quote=True)


def slide(name, caption):
    p = PHOTOS.get(name, {})
    pos = f' style="object-position:{p["pos"]}"' if p.get("pos") else ""
    return (f'<figure class="slide"><img src="assets/stand/{name}" alt="{a(p.get("alt", caption))}" '
            f'loading="lazy" width="900" height="600"{pos}><figcaption>{e(caption)}</figcaption></figure>')


def copy_row(label, value, copy=True, shown=None):
    btn = (f'<button class="copy" type="button" data-copy="{a(value)}" aria-label="Copy {a(label.lower())}">Copy</button>'
           if copy else "")
    return f'<div class="row"><dt>{e(label)}</dt><dd><span>{e(shown or value)}</span>{btn}</dd></div>'


def online(name, url, blurb, note):
    if url:
        btn = f'<a class="btn btn--give" href="{a(url)}" target="_blank" rel="noopener">Give through {e(name)}</a>'
    else:
        btn = f'<span class="btn btn--pending" aria-disabled="true">{e(name)} link coming soon</span>'
    return f"""
          <article class="give-card">
            <h3>{e(name)}</h3>
            <p>{blurb}</p>
            {btn}
            <details class="note"><summary>{note[0]}</summary><p>{note[1]}</p></details>
          </article>"""


GG_NOTE = ("Tax relief by country",
           "GlobalGiving is a US 501(c)(3) charity (EIN 30-0108263), so gifts are tax-deductible for US taxpayers. "
           "UK taxpayers giving in pounds can add Gift Aid at checkout, an extra 25p for every £1. "
           "Donors in Belgium, Bulgaria, France, Germany, Greece, Hungary, Italy, Spain and Switzerland can claim "
           "local tax relief through Transnational Giving Europe. Gifts in euros, Canadian or Australian dollars are "
           "generally not deductible; Canadian donors may qualify under the Canada-US tax treaty. Please check with your tax adviser.")
BB_NOTE = ("Section 18A certificate",
           'South African donors can request a Section 18A tax certificate from STAND. Email '
           '<a href="mailto:info@standaction.co.za?subject=Section%2018A%20certificate">info@standaction.co.za</a> '
           "with your name and the date of your gift.")

wa_href = "https://wa.me/?text=" + quote(WA_TEXT)
fb_href = "https://www.facebook.com/sharer/sharer.php?u=" + quote(PAGE_URL, safe="")
li_href = "https://www.linkedin.com/sharing/share-offsite/?url=" + quote(PAGE_URL, safe="")
x_href = "https://x.com/intent/post?text=" + quote(SOCIAL_TEXT) + "&url=" + quote(PAGE_URL, safe="")
mail_href = ("mailto:?subject=" + quote("When a woman asks for help, the system should answer")
             + "&body=" + quote(WA_TEXT))

WA_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')

video_html = ""
if CAMPAIGN_VIDEO:
    poster = f' poster="{a(CAMPAIGN_VIDEO_POSTER)}"' if CAMPAIGN_VIDEO_POSTER else ""
    video_html = f"""
    <section class="sec sec--dark watch" id="watch" aria-labelledby="watch-title">
      <div class="wrap watch-grid">
        <div>
          <p class="eyebrow">Watch · 80 seconds</p>
          <h2 id="watch-title">Two women asked for help. The system sent them home.</h2>
          <p class="watch-lead">Our founder, Stacey Doorly-Jones, on why we built Track Her Case.</p>
        </div>
        <video class="film" controls playsinline preload="none"{poster} width="720" height="1280">
          <source src="{a(CAMPAIGN_VIDEO)}" type="video/mp4">
        </video>
      </div>
    </section>"""


GIFTS = [
    ("R150", "One day's stipend for an ambassador on active duty"),
    ("R250", "A month of data so an ambassador can log and follow cases"),
    ("R3,000", "A month of community awareness on how to get help"),
    ("R7,750", "Data for all 31 ambassadors for a full month"),
    ("R12,000", "A month of case tracing across police, health, social services and the courts"),
]
gifts_html = "".join(
    f'<li><a href="#give"><b>{e(amt)}</b><span>{e(txt)}</span><i aria-hidden="true">&rarr;</i></a></li>' for amt, txt in GIFTS)

doc = f"""<!doctype html>
<html lang="en-ZA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Track Her Case: Give now | STAND</title>
  <meta name="description" content="{a(DESC)}">
  <link rel="canonical" href="{PAGE_URL}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="STAND">
  <meta property="og:url" content="{PAGE_URL}">
  <meta property="og:title" content="{a(TITLE)}">
  <meta property="og:description" content="{a(DESC)}">
  <meta property="og:image" content="{SITE}assets/stand/give-share.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="A smiling Track Her Case ambassador holding her phone, beside the words: When a woman asks for help, the system should answer.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@STANDactionZA">
  <meta name="theme-color" content="#08343c">
  <link rel="icon" href="assets/stand/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/stand/webclip.png">
  <link rel="preload" href="assets/fonts/poppins-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/campaign.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="top">
    <a class="brand" href="index.html" aria-label="STAND home"><img src="assets/stand/stand-mark-teal.svg" alt="" width="34" height="35"><span>STAND</span></a>
    <a class="btn btn--give btn--sm" href="#give">Give now</a>
  </header>

  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap hero-grid">
        <div class="hero-head">
          <p class="eyebrow">Track Her Case</p>
          <h1 id="hero-title">When a woman asks for help, <em>the system should answer.</em></h1>
        </div>
        <figure class="hero-photo">
          <img src="assets/stand/ambassador-smile.jpg" alt="A smiling Track Her Case ambassador holding up her phone" width="1200" height="800" fetchpriority="high">
          <figcaption>A trained ambassador, ready to log and follow cases on her phone.</figcaption>
        </figure>
        <div class="hero-body">
          <p class="lead">We built a live system in the Overstrand that follows every reported case of violence against women until it is resolved. Help us keep it running and take it across the district.</p>
          <div class="cta-row">
            <a class="btn btn--give" href="#give">Give now</a>
            <a class="btn btn--wa" href="{a(wa_href)}" target="_blank" rel="noopener">{WA_ICON}Share on WhatsApp</a>
          </div>
        </div>
      </div>
    </section>
{video_html}
    <section class="sec" id="why" aria-labelledby="why-title">
      <div class="wrap">
        <p class="eyebrow">Why it matters</p>
        <h2 id="why-title">The laws exist. The handover breaks.</h2>
        <div class="two">
          <p>South Africa has some of the strongest laws on gender-based violence (GBV) in the world. What fails is the handover between services. A woman reports to the police and her case stalls before it reaches the prosecutor. She is referred for medical care and social services never hear of her.</p>
          <p>Track Her Case closes those gaps. Each case gets a private tracking number, so no names are shared, and every handover is followed to the end.</p>
        </div>
        <ul class="proof" aria-label="Proof it works">
          <li><b>24 Aug</b><span>Live in the Overstrand since 24 August 2026</span></li>
          <li><b>3 days</b><span>From going live to the first case dispatched to the police</span></li>
          <li><b>31</b><span>Trained community ambassadors</span></li>
          <li><b>130,000+</b><span>People living in the Overstrand</span></li>
        </ul>
      </div>
    </section>

    <section class="sec sec--tint" id="how" aria-labelledby="how-title">
      <div class="wrap">
        <p class="eyebrow">How it works</p>
        <h2 id="how-title">Four steps, from a tap to a court outcome</h2>
        <ol class="steps">
          <li><b>One tap to report.</b> An ambassador or survivor presses the help button on the municipality's Citizen App.</li>
          <li><b>Help is sent.</b> Police and an ambulance go straight to the location, and the case gets a private number.</li>
          <li><b>Every handover is tracked.</b> The number travels with the case through the police docket, the hospital and social services.</li>
          <li><b>Followed to court.</b> Each appearance is tracked until the case reaches an outcome, so we can see where the system holds and where it needs strengthening.</li>
        </ol>
      </div>
      <div class="carousel" aria-label="Photos from the Overstrand" tabindex="0">
        {slide("redot-mapping.jpg", "Ambassadors and Overstrand Municipality map where support is needed most.")}
        {slide("le-training-stand.jpg", "Police and law enforcement officers in training.")}
        {slide("ambassadors-certificates.jpg", "Our ambassadors, trained with the Department of Social Development.")}
        {slide("ambassador-training.jpg", "STAND's community GBV response training, multi-sectoral referral networking.")}
      </div>
      <p class="wrap swipe-hint" aria-hidden="true">Swipe for more &rarr;</p>
      <p class="wrap credit">Designed by STAND with Overstrand Municipality and the Overberg Violence Prevention Unit, with the support of the DG Murray Trust and AIDSFONDS.</p>
    </section>

    <section class="sec" id="gift" aria-labelledby="gift-title">
      <div class="wrap">
        <p class="eyebrow">What your gift does</p>
        <h2 id="gift-title">Every rand keeps a case moving</h2>
        <ul class="gifts">{gifts_html}</ul>
        <p class="small">Amounts are taken from the approved programme budget.</p>
      </div>
    </section>

    <section class="sec sec--dark" id="give" aria-labelledby="give-title">
      <div class="wrap">
        <p class="eyebrow">Give now</p>
        <h2 id="give-title">Choose the way that suits you</h2>
        <div class="give-grid">
          <article class="give-card give-card--snap">
            <h3>SnapScan</h3>
            <p>The quickest way to give from your phone.</p>
            <a class="btn btn--give" href="{a(SNAPSCAN_URL)}" target="_blank" rel="noopener">Give with SnapScan</a>
            <figure class="qr"><img src="assets/stand/snapscan-qr.png" alt="SnapScan QR code for STAND" width="396" height="396" loading="lazy"><figcaption>On a computer? Scan this with the SnapScan app.</figcaption></figure>
          </article>

          <article class="give-card give-card--eft">
            <h3>EFT (bank transfer)</h3>
            <dl class="bank">
              {copy_row("Account name", "Social Transformation Action Defined")}
              {copy_row("Bank", "First National Bank (FNB)", copy=False)}
              {copy_row("Account number", "62759591623")}
              {copy_row("Branch code", "250655")}
              {copy_row("Reference", "Your name + TRACK", copy=False)}
              {copy_row("SWIFT (international)", "FIRNZAJJ")}
            </dl>
            <p class="small">Use <b>your name + TRACK</b> as the reference so we can tell campaign gifts apart.</p>
          </article>
{online("GlobalGiving", GLOBALGIVING_URL, "Give online from anywhere in the world, by card.", GG_NOTE)}
{online("BackaBuddy", BACKABUDDY_URL, "Give online in South Africa.", BB_NOTE)}
        </div>
        <p class="note-18a"><b>Section 18A.</b> STAND is a registered Public Benefit Organisation (PBO 930063426). South African gifts are tax-deductible. For a certificate, email <a href="mailto:info@standaction.co.za?subject=Section%2018A%20certificate">info@standaction.co.za</a> with your EFT reference.</p>
      </div>
    </section>

    <section class="sec" id="share" aria-labelledby="share-title">
      <div class="wrap center">
        <p class="eyebrow">Pass it on</p>
        <h2 id="share-title">Sharing costs nothing and reaches people we never could alone.</h2>
        <a class="btn btn--wa btn--lg" href="{a(wa_href)}" target="_blank" rel="noopener">{WA_ICON}Share on WhatsApp</a>
        <div class="share-more" aria-label="Share elsewhere">
          <a href="{a(fb_href)}" target="_blank" rel="noopener">Facebook</a>
          <a href="{a(li_href)}" target="_blank" rel="noopener">LinkedIn</a>
          <a href="{a(x_href)}" target="_blank" rel="noopener">X</a>
          <a href="{a(mail_href)}">Email</a>
          <button type="button" data-copy="{PAGE_URL}">Copy link</button>
        </div>
      </div>
    </section>
  </main>

  <footer class="foot">
    <div class="wrap">
      <p><a href="track-her-case.html">About Track Her Case</a> · <a href="index.html">standaction.co.za</a> · <a href="privacy.html">Privacy</a></p>
      <p>STAND, Social Transformation Action Defined NPC · PBO 930063426 · Section 18A · Level 1 B-BBEE</p>
    </div>
  </footer>

  <nav class="dock" aria-label="Give or share">
    <a class="btn btn--give" href="#give">Give now</a>
    <a class="btn btn--wa" href="{a(wa_href)}" target="_blank" rel="noopener" data-share data-share-text="{a(WA_TEXT)}" data-share-url="{PAGE_URL}">{WA_ICON}Share</a>
  </nav>

  <script src="js/campaign.js" defer></script>
</body>
</html>
"""
(ROOT / "campaign.html").write_text(doc)
print("wrote campaign.html")

# Short link for posters, video end cards and speaking: standaction.co.za/give
# It carries the same preview tags, because WhatsApp reads the page it is given.
give = f"""<!doctype html>
<html lang="en-ZA">
<head>
  <meta charset="utf-8">
  <title>Track Her Case: Give now | STAND</title>
  <link rel="canonical" href="{PAGE_URL}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{PAGE_URL}">
  <meta property="og:title" content="{a(TITLE)}">
  <meta property="og:description" content="{a(DESC)}">
  <meta property="og:image" content="{SITE}assets/stand/give-share.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta http-equiv="refresh" content="0; url=../campaign.html">
  <script>location.replace('../campaign.html' + location.hash);</script>
</head>
<body><p><a href="../campaign.html">Track Her Case: Give now</a></p></body>
</html>
"""
(ROOT / "give").mkdir(exist_ok=True)
(ROOT / "give/index.html").write_text(give)
print("wrote give/index.html")
