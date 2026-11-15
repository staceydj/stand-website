"""Build the WhatsApp share kit (share/index.html) for Stacey, the Board and campaign champions.

Usage: python3 tools/build_share.py

Not linked from the site menu and hidden from search engines; share the address
standaction.co.za/share with champions. Every message has a one-tap "Send on
WhatsApp" button (opens WhatsApp with the text ready) and a Copy button.
Messages come from the Fund the 16 Days campaign pack.
"""
import html
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from links import GLOBALGIVING_URL  # noqa: E402

GIVE = "standaction.co.za/give"
ABROAD = GLOBALGIVING_URL or "https://standaction.co.za/give"


def a(s):
    return html.escape(s, quote=True)


WA = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')

MESSAGES = [
    ("everyone", "Forward-friendly message", "For groups, and for anyone passing it on. Works as it is.",
     "\U0001F499 When a woman asks for help, the system should answer.\n\n"
     "Too often in South Africa, a woman's case gets lost between the police station, the hospital and the court. "
     "Track Her Case, live in the Overstrand, gives every case a private tracking number and follows it all the way to justice.\n\n"
     "During the 16 Days of Activism we're raising R150,000 to keep it running through the festive season, the most dangerous time of year for women.\n\n"
     "\U0001F1FF\U0001F1E6 R150 keeps it running for an hour\n\U0001F30D Abroad? $10 or £8 goes much further here\n\n"
     f"{GIVE}\n\nPlease forward this to one person \U0001F64F\U0001F3FD"),
    ("personal", "Personal ask to someone you know", "Send one by one. Replace [name] and [your name] before sending.",
     "Hi [name] \U0001F499 Can I ask you something personal?\n\n"
     "I'm supporting Track Her Case. In the Overstrand, every reported case of violence against a woman now gets a private tracking number "
     "and is followed from the police station to court. It's live and it's working.\n\n"
     "During the 16 Days of Activism we're raising R150,000 to keep it running through the festive season. R150 keeps it running for an hour.\n\n"
     f"{GIVE}\n\nWould you be one of the first? And if you can, forward this to one person who'd care. Thank you. [your name]"),
    ("overseas", "Friends and family overseas", "Replace [name] and [your name]. The link opens the giving page for donors abroad.",
     "Hi [name] \U0001F499 I'd love your help with something close to my heart. In South Africa a system called Track Her Case follows every "
     "reported case of violence against a woman, from the police station to the court, so no case gets lost. During the 16 Days of Activism "
     "we're raising R150,000 to keep it running through the festive season. Because of the exchange rate, £20 or $25 becomes about R440 here, "
     "almost three hours of the system running. You can give securely in your own currency, with UK Gift Aid or US tax relief:\n\n"
     f"{ABROAD}\n\nAnd if you could share it with a few friends there, it would mean the world. [your name]"),
    ("business", "Business owners: sponsor a day", "Replace [name], [business name] and [your name].",
     "Hi [name], I have an unusual ask. For R3,370, [business name] could keep Track Her Case running for a full day this festive season, "
     "tracking every case of violence against a woman in the Overstrand from report to court. With your permission, STAND will thank you "
     f"publicly by date, and the gift is Section 18A tax-deductible.\n\n{GIVE}\n\nCould I count you in? [your name]"),
    ("nudge", "Follow-up, three or four days later", "Only to people who haven't replied. Replace [name] and [amount].",
     f"Hi [name], just a gentle nudge in case my message got buried. We're [amount] towards R150,000 already. If you'd like to be part of it:\n\n{GIVE}\n\n"
     "Either way, thank you for cheering us on \U0001F499"),
    ("thanks", "Thank you, within 24 hours", "To every donor you know. Replace [name], [amount] and [time] (R150 = more than an hour, R500 = more than three hours, R1,000 = about seven hours, R3,370 = a full day).",
     "Hi [name], I just saw your gift and wanted to say thank you personally. Your [amount] keeps Track Her Case running for [time], which means a "
     "woman's case keeps moving from the police station to the court. It means a great deal to me. If you know anyone else who might help, please pass it on \U0001F499"),
]
STACEY = ("stacey", "Stacey's personal message", "Stacey's own story, for her inner circle. Replace [name].",
          "Hi [name] \U0001F499 Can I ask you something personal?\n\n"
          "I once watched a man ram a woman's head into a car. I called the police five times. When they came, he said everything was fine, and they left.\n\n"
          "So we built Track Her Case. In the Overstrand, every reported case of violence against a woman now gets a private tracking number and is "
          "followed from the police station to court. It's live and it's working.\n\n"
          "During the 16 Days of Activism I'm raising R150,000 to keep it running through the festive season. R150 keeps it running for an hour.\n\n"
          f"{GIVE}\n\nWould you be one of the first? And if you can, forward this to one person who'd care. Thank you. Stace")

STATUS = [
    ("Day 1", "track-her-case-square.jpg", "image", "Square campaign image",
     f"R150 keeps Track Her Case running for an hour. {GIVE}"),
    ("Day 3", "track-her-case-24s.mp4", "video", "24-second film",
     f"When a woman asks for help, the system should answer. Give or share: {GIVE}"),
    ("Day 5", "track-her-case-status.jpg", "image", "Status image with QR code",
     f"[X] people have given so far. Thank you \U0001F499 Help us reach R150,000: {GIVE}"),
    ("Day 7", "ambassador.jpg", "image", "Ambassador photo",
     f"She walks alongside women whose cases are moving through the system. Keep her going this festive season: {GIVE}"),
]


def card(mid, title, hint, text):
    return f"""
      <article class="msg" id="{mid}">
        <h3>{html.escape(title)}</h3>
        <p class="hint">{html.escape(hint)}</p>
        <pre class="text">{html.escape(text)}</pre>
        <div class="row">
          <a class="btn btn--wa" href="https://wa.me/?text={a(quote(text))}" target="_blank" rel="noopener">{WA}Send on WhatsApp</a>
          <button class="btn btn--ghost" type="button" data-copy="{a(text)}">Copy text</button>
        </div>
      </article>"""


def status_card(day, f, kind, label, caption):
    media = (f'<video src="../assets/share/{f}" poster="../assets/share/track-her-case-24s.jpg" controls playsinline preload="none"></video>'
             if kind == "video" else f'<img src="../assets/share/{f}" alt="{a(label)}" loading="lazy">')
    return f"""
      <article class="status">
        <p class="day">{day}</p>
        {media}
        <p class="cap">{html.escape(caption)}</p>
        <div class="row">
          <a class="btn btn--give btn--sm" href="../assets/share/{f}" download>Save {'video' if kind == 'video' else 'image'}</a>
          <button class="btn btn--ghost btn--sm" type="button" data-copy="{a(caption)}">Copy caption</button>
        </div>
      </article>"""


doc = f"""<!doctype html>
<html lang="en-ZA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>WhatsApp share kit: Track Her Case | STAND</title>
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#08343c">
  <link rel="icon" href="../assets/stand/favicon.png" type="image/png">
  <link rel="stylesheet" href="../css/campaign.css">
  <style>
    .kit {{ padding-bottom: 2rem; }}
    .tips {{ background: #fff; border-radius: var(--radius); padding: 1.1rem 1.25rem; box-shadow: 0 6px 18px rgba(8,52,60,.07); margin-top: 1.25rem; }}
    .tips ol {{ margin: .5rem 0 0; padding-left: 1.2rem; display: grid; gap: .35rem; }}
    .msg, .status {{ background: #fff; border-radius: var(--radius); padding: 1.15rem; box-shadow: 0 6px 18px rgba(8,52,60,.07); }}
    .msgs, .statuses {{ display: grid; gap: 1rem; margin-top: 1.25rem; }}
    .msg h3 {{ color: var(--ink); }}
    .hint {{ margin: .3rem 0 .7rem; font-size: .85rem; color: var(--muted); }}
    .text {{ white-space: pre-wrap; font: inherit; font-size: .92rem; line-height: 1.5; background: #e7f6e9; border-radius: .9rem .9rem .9rem .25rem; padding: .9rem 1rem; margin: 0 0 .9rem; }}
    .row {{ display: flex; flex-wrap: wrap; gap: .5rem; }}
    .row .btn {{ flex: 1 1 10rem; }}
    .btn--ghost {{ background: transparent; color: var(--teal-2); border: 1.5px solid var(--teal-2); }}
    .copy-done {{ background: var(--teal-2) !important; color: #fff !important; }}
    .status img, .status video {{ width: 100%; max-height: 26rem; object-fit: contain; background: #0b4a55; border-radius: .8rem; display: block; }}
    .day {{ margin: 0 0 .5rem; font: 700 .78rem/1 var(--head); letter-spacing: .16em; text-transform: uppercase; color: var(--teal-2); }}
    .cap {{ font-size: .9rem; margin: .7rem 0; }}
    .voice {{ background: var(--ink); color: #fff; border-radius: var(--radius); padding: 1.15rem; margin-top: 1rem; }}
    .voice h3 {{ color: var(--yellow); }}
    .voice p {{ margin: .5rem 0 0; color: #d6eef1; }}
    @media (min-width: 760px) {{ .msgs {{ grid-template-columns: 1fr 1fr; }} .statuses {{ grid-template-columns: repeat(4, 1fr); }} }}
    body {{ padding-bottom: 0; }}
  </style>
</head>
<body>
  <header class="top">
    <a class="brand" href="../campaign.html" aria-label="Track Her Case campaign"><img src="../assets/stand/stand-mark-colour.png" alt="" width="400" height="330"><span class="brand-words"><span>STAND</span><small>Evidence. Advocacy. Justice.</small></span></a>
    <a class="btn btn--give btn--sm" href="../campaign.html#give">Give now</a>
  </header>
  <main class="kit">
    <section class="hero" style="padding-bottom:1.75rem">
      <div class="wrap">
        <p class="eyebrow">Fund the 16 Days · Share kit</p>
        <h1 style="font-size:clamp(1.8rem,7vw,3rem)">Share Track Her Case on WhatsApp</h1>
        <p class="lead">Thank you for helping. Tap <b>Send on WhatsApp</b> on any message below: WhatsApp opens with the text ready, and you choose who to send it to.</p>
      </div>
    </section>

    <section class="sec" style="padding-top:1.75rem">
      <div class="wrap">
        <div class="tips">
          <h3 style="color:var(--ink)">What works best</h3>
          <ol>
            <li>Send to people one by one, by name. Personal messages raise far more than broadcasts.</li>
            <li>Keep the link on its own line, so WhatsApp shows the preview with the headline and the ambassador photo.</li>
            <li>Send between 18:00 and 20:30, or on a Sunday afternoon.</li>
            <li>Follow up once, three or four days later. Post in groups only where you're active, and ask the admin first.</li>
            <li>Ask every donor to forward the message to one person.</li>
          </ol>
        </div>

        <h2 style="margin-top:2.25rem">Messages</h2>
        <div class="msgs">{card(*MESSAGES[0])}{card(*STACEY)}{"".join(card(*m) for m in MESSAGES[1:])}
        </div>

        <h2 style="margin-top:2.5rem">WhatsApp Status: post every second day</h2>
        <p class="hint" style="font-size:.95rem">Save the image or video to your phone, add it to your Status, then paste the caption.</p>
        <div class="statuses">{"".join(status_card(*s) for s in STATUS)}
        </div>

        <div class="voice">
          <h3>Voice note (30 to 45 seconds)</h3>
          <p>A voice note from someone you know is one of the most trusted things on WhatsApp. In your own words, say who you are and why this matters to you; that Track Her Case follows every case of violence against a woman in the Overstrand from report to court; that we're raising R150,000 during the 16 Days and R150 keeps it running for an hour; then ask them to give and forward. Send it straight after your personal message.</p>
        </div>
      </div>
    </section>
  </main>
  <footer class="foot"><div class="wrap"><p><a href="../campaign.html">Campaign page</a> · <a href="../index.html">standaction.co.za</a></p><p>STAND NPC · PBO 930063426 · Section 18A</p></div></footer>
  <script>
  document.querySelectorAll('[data-copy]').forEach(function (b) {{
    var label = b.textContent;
    b.addEventListener('click', function () {{
      var done = function () {{ b.textContent = 'Copied'; b.classList.add('copy-done'); setTimeout(function () {{ b.textContent = label; b.classList.remove('copy-done'); }}, 2000); }};
      if (navigator.clipboard) navigator.clipboard.writeText(b.dataset.copy).then(done, function () {{ b.textContent = 'Press and hold the text to copy'; }});
    }});
  }});
  </script>
</body>
</html>
"""
(ROOT / "share").mkdir(exist_ok=True)
(ROOT / "share/index.html").write_text(doc)
print("wrote share/index.html")
