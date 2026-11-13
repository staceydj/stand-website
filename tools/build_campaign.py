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
from links import (BACKABUDDY_URL, CAMPAIGN_VIDEO, CAMPAIGN_VIDEO_POSTER, GLOBALGIVING_URL,  # noqa: E402
                   MATCH_AMOUNT, MATCH_NAME, SNAPSCAN_URL)

SITE = "https://standaction.co.za/"
PAGE_URL = SITE + "campaign.html"
SHORT_URL = "standaction.co.za/give"
TITLE = "When a woman asks for help, the system should answer."
DESC = ("Track Her Case follows every reported case of violence against women in the Overstrand "
        "through police, health, social services and the courts. Give now and pass it on.")
WA_TEXT = ("When a woman asks for help, the system should answer.\n\n"
           "Track Her Case follows every reported case of violence against women in the Overstrand "
           "through the police, health, social services and the courts, until it is resolved. "
           "During the 16 Days of Activism we're raising R150,000 to keep it running through the festive season. "
           "R150 keeps it running for an hour.\n\nGive or share: " + PAGE_URL)
GOAL = 150000
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


# Fund the 16 Days: R150 keeps Track Her Case running for an hour (full year R1,230,870).
# Overseas amounts follow the playbook's ladder at USD 1 = ZAR 16.43 (19 October 2026).
LADDER = {
    "ZAR": [("R150", "keeps it running for an hour"), ("R500", "more than three hours"), ("R1,000", "about seven hours"),
            ("R3,370", "a full day"), ("R23,600", "a full week"), ("R54,000", "all 16 days"),
            ("R150,000", "six weeks: the whole 16 Days target")],
    "USD": [("$10", "more than an hour"), ("$25", "almost three hours"), ("$50", "about six hours"), ("$100", "half a day"),
            ("$205", "a full day"), ("$500", "more than two days"), ("$1,440", "a full week"), ("$9,000", "six weeks")],
    "GBP": [("£10", "more than an hour"), ("£20", "almost three hours"), ("£40", "about six hours"), ("£80", "half a day"),
            ("£155", "a full day"), ("£400", "more than two days"), ("£1,080", "a full week"), ("£6,860", "six weeks")],
    "EUR": [("€10", "more than an hour"), ("€25", "about three hours"), ("€50", "about six hours"), ("€95", "half a day"),
            ("€185", "a full day"), ("€450", "more than two days"), ("€1,280", "a full week"), ("€8,120", "six weeks")],
}
CUR_LABEL = {"ZAR": "Rand", "USD": "Dollars", "GBP": "Pounds", "EUR": "Euros"}
cur_buttons = "".join(
    f'<button type="button" data-cur="{c}" aria-pressed="{"true" if c == "ZAR" else "false"}">{CUR_LABEL[c]}</button>' for c in LADDER)
ladders = "".join(
    f'<ul class="ladder" data-cur="{c}"{"" if c == "ZAR" else " hidden"}>'
    + "".join(f'<li><a href="#give" data-door="{"sa" if c == "ZAR" else "abroad"}"><b>{e(amt)}</b><span>{e(txt)}</span>'
              f'<i aria-hidden="true">&rarr;</i></a></li>' for amt, txt in rows)
    + "</ul>" for c, rows in LADDER.items())

match_html = ""
if MATCH_NAME and MATCH_AMOUNT:
    match_html = (f'<p class="match"><b>Every gift doubled.</b> {e(MATCH_NAME)} will match every gift made during the '
                  f'16 Days of Activism, up to {e(MATCH_AMOUNT)}.</p>')

doc = f"""<!doctype html>
<html lang="en-ZA" class="no-js">
<head>
  <meta charset="utf-8">
  <script>document.documentElement.classList.remove('no-js');</script>
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
    <a class="brand" href="index.html" aria-label="STAND home"><img src="assets/stand/stand-mark-colour.png" alt="" width="400" height="330"><span class="brand-words"><span>STAND</span><small>Evidence. Advocacy. Justice.</small></span></a>
    <a class="btn btn--give btn--sm" href="#give">Give now</a>
  </header>

  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap hero-grid">
        <div class="hero-head">
          <p class="eyebrow">Track Her Case · Fund the 16 Days</p>
          <h1 id="hero-title">When a woman asks for help, <em>the system should answer.</em></h1>
        </div>
        <figure class="hero-photo">
          <img src="assets/stand/ambassador-smile.jpg" alt="A smiling Track Her Case ambassador holding up her phone" width="1200" height="800" fetchpriority="high">
          <figcaption>A trained ambassador, ready to log and follow cases on her phone.</figcaption>
        </figure>
        <div class="hero-body">
          <p class="lead">We built a live system in the Overstrand that follows every reported case of violence against women until it is resolved. During the 16 Days of Activism we're raising R150,000 to keep it running through the festive season. <b>R150 keeps it running for an hour.</b></p>
          <div class="cta-row">
            <a class="btn btn--give" href="#give">Give now</a>
            <a class="btn btn--wa" href="{a(wa_href)}" target="_blank" rel="noopener">{WA_ICON}Share on WhatsApp</a>
          </div>
          <div class="progress" data-goal="{GOAL}" hidden>
            <p class="progress-line"><b data-raised>R0</b> raised of R150,000 for the 16 Days</p>
            <div class="bar" role="progressbar" aria-label="Raised towards R150,000" aria-valuemin="0" aria-valuemax="{GOAL}" aria-valuenow="0"><span></span></div>
          </div>
          {match_html}
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
        <p class="why-now"><b>Why now.</b> South Africa has classified gender-based violence as a national disaster and committed billions to fight it. More social workers, more courts and more care centres mean more handovers, and every handover is a place where a woman's case can be lost. Track Her Case makes sure it isn't.</p>
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
        <h2 id="gift-title">R150 keeps Track Her Case running for an hour</h2>
        <p class="gift-lead">Every gift keeps the whole system running: the coordinator following each case, the ambassadors walking alongside women, and the partners making sure cases reach court.</p>
        <div class="cur-switch" role="group" aria-label="Show amounts in">{cur_buttons}</div>
        {ladders}
        <p class="small cur-note">Because of the exchange rate, £20 or $25 becomes about R410 to R440 here, almost three hours of Track Her Case. Amounts in other currencies are approximate, at $1 = R16.43 (19 October 2026). The full year costs R1,230,870, everything included.</p>
        <aside class="sponsor">
          <h3>Sponsor a day</h3>
          <p><b>R3,370</b>, about <b>$205</b>, <b>£155</b> or <b>€185</b>, keeps Track Her Case running for a full day. Choose your date and, if you'd like, we'll thank you publicly on it.</p>
          <a class="btn btn--give btn--sm" href="mailto:info@standaction.co.za?subject=Sponsor%20a%20day%20of%20Track%20Her%20Case">Sponsor a day</a>
        </aside>
      </div>
    </section>

    <section class="sec sec--dark" id="give" aria-labelledby="give-title">
      <div class="wrap">
        <p class="eyebrow">Give now</p>
        <h2 id="give-title">Where are you giving from?</h2>
        <div class="doors" role="tablist" aria-label="Where are you giving from?">
          <button type="button" role="tab" id="tab-sa" aria-controls="door-sa" aria-selected="true">South Africa</button>
          <button type="button" role="tab" id="tab-abroad" aria-controls="door-abroad" aria-selected="false">Outside South Africa</button>
        </div>

        <div class="door" id="door-sa" role="tabpanel" aria-labelledby="tab-sa">
          <div class="give-grid">
            <article class="give-card give-card--snap">
              <h3>SnapScan</h3>
              <p>The quickest way to give from your phone. Tap the button, or scan the code with the SnapScan app on a computer. STAND never sees your card details.</p>
              <a class="snap-badge" href="{a(SNAPSCAN_URL)}" target="_blank" rel="noopener"><img src="assets/stand/snapscan-badge.png" alt="SnapScan code: snap here to pay STAND" width="520" height="741" loading="lazy"></a>
              <a class="btn btn--give" href="{a(SNAPSCAN_URL)}" target="_blank" rel="noopener">Give now with SnapScan</a>
            </article>

            <article class="give-card give-card--eft">
              <h3>EFT (bank transfer)</h3>
              <dl class="bank">
                {copy_row("Account name", "Social Transformation Action Defined")}
                {copy_row("Bank", "First National Bank (FNB)", copy=False)}
                {copy_row("Account number", "62759591623")}
                {copy_row("Branch code", "250655")}
                {copy_row("Reference", "Your name + TRACK", copy=False)}
              </dl>
              <p class="small">Use <b>your name + TRACK</b> as the reference so we can tell campaign gifts apart.</p>
            </article>
{online("BackaBuddy", BACKABUDDY_URL, "Prefer to give by card? Give online through BackaBuddy.", BB_NOTE)}
          </div>
          <p class="note-18a"><b>Section 18A.</b> STAND is a registered Public Benefit Organisation (PBO 930063426), so South African gifts are tax-deductible. For a certificate, email <a href="mailto:info@standaction.co.za?subject=Section%2018A%20certificate">info@standaction.co.za</a> with your EFT reference or the date of your gift.</p>
        </div>

        <div class="door" id="door-abroad" role="tabpanel" aria-labelledby="tab-abroad">
          <div class="give-grid">
{online("GlobalGiving", GLOBALGIVING_URL, "Give securely in your own currency, by card, from anywhere in the world. You can also give monthly, and many employers match their staff's gifts.", GG_NOTE)}
            <article class="give-card">
              <h3>International bank transfer</h3>
              <dl class="bank">
                {copy_row("Account name", "Social Transformation Action Defined")}
                {copy_row("Bank", "First National Bank (FNB), South Africa", copy=False)}
                {copy_row("Account number", "62759591623")}
                {copy_row("SWIFT", "FIRNZAJJ")}
                {copy_row("Reference", "Your name + TRACK", copy=False)}
              </dl>
              <p class="small">Email <a href="mailto:info@standaction.co.za?subject=International%20gift">info@standaction.co.za</a> and we'll confirm when your gift arrives.</p>
            </article>
          </div>
        </div>
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
