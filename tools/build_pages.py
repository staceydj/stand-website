"""Build STAND's inner pages from index.html's nav and footer.

Usage: python3 tools/build_pages.py

Rewrites the shared links in index.html, then writes about.html, work.html,
track-her-case.html, board.html, founder.html, support.html and privacy.html.
Every word on these pages comes from standaction.co.za (tools/stand-source.txt).
Photo captions come from tools/stand-photos.json.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHOTOS = json.loads((ROOT / "tools/stand-photos.json").read_text())

# ---------------------------------------------------------------- links
SPECIFIC = {
    "Gender-Responsive Justice": "work.html#justice",
    "Substance-Related Harms": "work.html#harms",
    "Systems Strengthening": "work.html#systems",
    "Alternatives to Incarceration": "work.html#alternatives",
    "Training and facilitation": "work.html#training",
    "Stakeholder convening": "work.html#convening",
    "Research and assessment": "work.html#research",
    "Policy and technical writing": "work.html#writing",
    "Partner with us": "support.html#partner",
    "Fund the work": "support.html#fund",
    "Collaborate": "support.html#collaborate",
}
GENERIC = {
    "#about": "about.html",
    "#work": "work.html",
    "#trace": "track-her-case.html",
    "#board": "board.html",
    "#founder": "founder.html",
    "#support": "support.html",
    "#privacy": "privacy.html",
}


def relink(text):
    def specific(m):
        label = m.group(2)
        key = label.split(" <")[0].strip()
        target = SPECIFIC.get(key)
        return f'href="{target}">{label}' if target else m.group(0)

    text = re.sub(r'href="(https://standaction\.co\.za/#\w+)">([^<]+(?: <img[^>]*>)?)', specific, text)
    for frag, page in GENERIC.items():
        text = text.replace(f'href="https://standaction.co.za/{frag}"', f'href="{page}"')
    return text


index_path = ROOT / "index.html"
index = relink(index_path.read_text())
# The top-level nav links lead to the full pages.
index = index.replace('<a class="nav-link" href="#focus">Focus areas</a>', '<a class="nav-link" href="work.html#focus-areas">Focus areas</a>')
index = index.replace('<a class="nav-link" href="#capabilities">Our work</a>', '<a class="nav-link" href="work.html">Our work</a>')
index_path.write_text(index)

header = index[index.index("  <!-- ============ Navigation ============ -->"):index.index("  <main id=\"main\">")]
footer = index[index.index("  <!-- ============ Footer ============ -->"):index.index("  <script src=\"js/main.js\"")]
header = header.replace('href="#contact"', 'href="index.html#contact"')
head_tpl = index[:index.index("<body>")]


def page(slug, title, desc, body, current=None, share_img=None):
    head = head_tpl
    head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(title), head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), head)
    head = head.replace('<meta property="og:url" content="https://standaction.co.za/">', f'<meta property="og:url" content="https://standaction.co.za/{slug}">')
    if share_img:
        head = head.replace('assets/social/stand-share.jpg', share_img)
    head = head.replace('<link rel="stylesheet" href="css/styles.css">', '<link rel="stylesheet" href="css/styles.css">\n  <link rel="stylesheet" href="css/pages.css">')
    nav = header
    if current == "involved":
        nav = nav.replace('<button class="nav-toggle" aria-expanded="false" aria-controls="dd-involved"', '<button class="nav-toggle is-current" aria-expanded="false" aria-controls="dd-involved"', 1)
    elif current:
        nav = nav.replace(f'<a class="nav-link" href="{current}">', f'<a class="nav-link" href="{current}" aria-current="page">', 1)
    doc = (
        head
        + '<body class="page">\n  <a class="skip-link" href="#main">Skip to content</a>\n\n'
        + nav
        + '  <main id="main">\n'
        + body
        + "  </main>\n\n"
        + footer
        + '  <script src="js/main.js" defer></script>\n</body>\n</html>\n'
    )
    (ROOT / slug).write_text(doc)
    print("wrote", slug)


# ---------------------------------------------------------------- helpers
def e(s):
    return html.escape(s, quote=False)


def fig(name, cls="", label=None, caption=None, alt=None, eager=False):
    p = PHOTOS[name]
    label = p["label"] if label is None else label
    caption = p["caption"] if caption is None else caption
    alt = p["alt"] if alt is None else alt
    style = f' style="object-position:{p["pos"]}"' if p["pos"] else ""
    cap = ""
    if label or caption:
        cap = "<figcaption>" + (f"<b>{e(label)}</b>" if label else "") + e(caption) + "</figcaption>"
    lazy = "" if eager else ' loading="lazy"'
    return f'<figure class="photo reveal {cls}"><img src="assets/stand/{name}" alt="{html.escape(alt)}"{lazy}{style}>{cap}</figure>'


def hero(eyebrow, h1, lead, scene=None, extra=""):
    scene_html = f'\n      <img class="scene" src="assets/stand/{scene}" alt="" aria-hidden="true">' if scene else ""
    cls = "page-hero" if scene else "page-hero no-scene"
    return f"""
    <section class="{cls}" aria-labelledby="page-title">
      <div class="container">
        <p class="eyebrow">{e(eyebrow)}</p>
        <h1 id="page-title">{e(h1)}</h1>
        <p class="lead">{e(lead)}</p>{extra}
      </div>{scene_html}
    </section>
"""


def ul(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def cta(title, lead, buttons, small="", scene=None):
    btns = "".join(buttons)
    sm = f'<p class="small">{small}</p>' if small else ""
    sc = f'<img class="scene-end" src="assets/gen/{scene}" alt="" aria-hidden="true" loading="lazy">' if scene else ""
    return f"""
    <section class="band band--dark page-cta" aria-labelledby="cta-title">
      <img class="contours" src="assets/art/contours-footer.svg" alt="" aria-hidden="true" loading="lazy">
      <div class="container">
        <h2 class="title reveal" id="cta-title">{e(title)}</h2>
        <p class="lead reveal">{e(lead)}</p>
        <div class="actions reveal">{btns}</div>
        {sm}{sc}
      </div>
    </section>
"""


def pill(href, text, ghost=False, ext=False):
    cls = "btn-ghost" if ghost else "btn-pill"
    x = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="{cls}" href="{href}"{x}>{e(text)}</a>'


PARTNER = pill("index.html#contact", "Partner with STAND")
SUPPORT = pill("support.html#ways", "Support the work")

# Online giving pages live in tools/links.py, shared with the campaign page.
import sys
sys.path.insert(0, str(ROOT / "tools"))
from links import GLOBALGIVING_URL, BACKABUDDY_URL, SNAPSCAN_URL  # noqa: E402

# ================================================================ ABOUT
about = hero(
    "About STAND",
    "A specialist technical and implementation partner.",
    "We are a women-led technical and implementation partner working where justice, health, protection, and implementation meet.",
    scene="fasd-2026-a.jpg",
) + f"""
    <section class="band band--cream" aria-labelledby="who-title">
      <div class="container split">
        <div class="prose">
          <h2 class="title reveal" id="who-title">Who we are</h2>
          <div class="reveal" style="margin-top:1.5rem">
            <p>STAND (Social Transformation Action Defined) is a South African women-led nonprofit, a registered Public Benefit Organisation with Section 18A tax-exemption status, and a specialist technical platform working at the intersection of gender-responsive justice, gender-based violence, substance-related harms, public health, and systems accountability.</p>
            <p>Founded in 2018 and based in Cape Town, STAND operates as a lean, technically deep organisation, mobilising specialist consultants and collaborators according to programme scope and need. This model keeps STAND agile and responsive while holding the analytical and technical standards of a senior institutional partner.</p>
            <p>We are not a generalist development organisation. Our work is intersectional by design, sitting where gender-based violence, substance-related harms, justice and health meet, and we bring the expertise to close the gap between what the evidence shows and what actually gets done.</p>
          </div>
        </div>
        <div class="photo-stack">
          {fig("training-2020-a.jpg", "wide", label="STAND training", caption="Training and facilitation in practice.")}
          {fig("hr-session.jpg", "wide")}
        </div>
      </div>
    </section>

    <section class="band band--cream2" aria-labelledby="four-title">
      <img class="contours" src="assets/art/contours-signs.svg" alt="" aria-hidden="true" loading="lazy">
      <div class="container">
        <div class="head center">
          <h2 class="title reveal" id="four-title">Four things distinguish how we work</h2>
        </div>
        <div class="cards">
          <article class="card reveal"><span class="num">01</span><h3>We work in the hard middle ground.</h3><p>Policy commitments exist. Services are theoretically available. Institutions are willing. And yet systems fail. STAND operates in exactly the space where this happens, with the evidence, relationships, and implementation experience to address it.</p></article>
          <article class="card reveal"><span class="num">02</span><h3>Our credibility is earned, not claimed.</h3><p>STAND's positioning rests on documented work: assessments completed, training delivered, referral pathways designed, tools produced, coordination systems strengthened. We do not inflate. Every capacity we offer has been demonstrated.</p></article>
          <article class="card reveal"><span class="num">03</span><h3>We design for how systems actually work.</h3><p>Our outputs are shaped by operational reality, not only by what policy prescribes or theory recommends. When STAND designs a coordination mechanism or a training curriculum, it is built for the institutions, personnel, and conditions that will actually use it.</p></article>
          <article class="card reveal"><span class="num">04</span><h3>We combine technical depth with institutional fluency.</h3><p>STAND is equally credible in a donor briefing room, a law-enforcement training environment, a municipal coordination meeting, and a community-based assessment. That range, held without compromising substance, is what makes STAND a trusted partner across sectors.</p></article>
        </div>
      </div>
    </section>

    <section class="band band--cream" aria-labelledby="story-title">
      <div class="container split">
        <div class="sticky">
          {fig("un-sdg-vienna.jpg", "tall")}
        </div>
        <div class="prose">
          <h2 class="title reveal" id="story-title">Where we started. Where we are now.</h2>
          <div class="reveal" style="margin-top:1.5rem">
            <p>STAND began in 2018 in Cape Town, emerging from frontline community engagement and a clear-sighted recognition that the systems meant to protect the most vulnerable people were systematically failing them.</p>
            <p>Over time, STAND evolved from community-rooted practice into a highly credible implementation and systems-strengthening partner with growing regional and international relevance. Its earlier community-based treatment work was run in research partnership with the South African Medical Research Council. The work deepened. The evidence base expanded. The institutional relationships strengthened.</p>
            <p>Today STAND holds a distinctive position: the credibility of a senior technical partner with the agility of a specialist, senior-led organisation. It is led by <a href="founder.html">Stacey Doorly-Jones</a>, a strategist, qualitative researcher, technical writer, and systems adviser whose career has been built at the intersection of gender justice, substance-related harms, and institutional accountability.</p>
          </div>
          <div class="actions reveal">{pill("founder.html", "Meet the founder", ghost=True)}</div>
        </div>
      </div>
    </section>

    <section class="band band--teal" aria-labelledby="gov-title">
      <img class="contours" src="assets/art/contours-footer.svg" alt="" aria-hidden="true" loading="lazy">
      <div class="container split split--even">
        <h2 class="title reveal" id="gov-title">Formally constituted. Accountable by design.</h2>
        <div class="prose reveal">
          <p>STAND is registered as a South African Non-Profit Company (NPC) and Public Benefit Organisation (PBO No. 930063426) with Section 18A tax-exemption status, and holds Level 1 B-BBEE status.</p>
          <p>The organisation maintains formal governance structures including a Code of Conduct, financial accountability systems, and a commitment to transparent reporting. STAND is governed by a Board of Directors that provides independent, expert-led oversight. Donors and partners can expect the institutional rigour that serious organisations require.</p>
          <div class="actions">{pill("board.html", "Meet the Board")}</div>
        </div>
      </div>
    </section>

    <section class="band band--cream" aria-labelledby="values-title">
      <div class="container">
        <div class="head center">
          <h2 class="title reveal" id="values-title">What we stand by</h2>
        </div>
        <div class="cards">
          <article class="card reveal"><h3>Integrity</h3><p>We say what we can support and support what we say. Every claim is defensible. Every promise is kept.</p></article>
          <article class="card reveal"><h3>Accountability</h3><p>We track what we commit to, report honestly on what we achieve, and own responsibility for quality and governance.</p></article>
          <article class="card reveal"><h3>Dignity</h3><p>The people our work is meant to serve remain visible and respected throughout. No pity language. No saviour framing.</p></article>
          <article class="card reveal"><h3>Rigour</h3><p>Technical quality is non-negotiable. We distinguish between what has been done, what we are positioned to do, and what we propose.</p></article>
        </div>
      </div>
    </section>
""" + cta(
    "Work where evidence meets action.",
    "If you are a grantmaker, funder, government partner, civil society organisation or corporate partner looking for a technically credible implementation partner, we would welcome the conversation.",
    [PARTNER, pill("work.html", "See our work", ghost=True)],
    small='You don\'t have to be an institution to move this. Individuals can back the work directly. <a href="support.html#fund">Support the work</a>',
)
page("about.html", "About | STAND", "STAND is a South African women-led nonprofit and specialist technical partner working where justice, health, protection and implementation meet.", about, current="about.html")

# ================================================================ WORK
AREAS = [
    ("justice", "01", "icon-guidance-light.svg", "Gender-Responsive Justice and Gender-Based Violence (GBV) Systems Strengthening",
     "Government departments, municipalities, law-enforcement agencies, civil society organisations, and international partners working to strengthen institutional responses to gender-based violence.",
     ["STAND supports the design and strengthening of gender-responsive justice systems, from referral-pathway mapping and inter-agency coordination to law-enforcement training, survivor-centred protocol development, and district-level accountability mechanisms.",
      "Specific work includes multi-sector GBV coordination support, law-enforcement and multi-agency training design and facilitation, referral-pathway assessment and redesign, GBV accountability-system development, technical writing and policy drafting, and institutional capacity building for frontline and management personnel."],
     "STAND combines survivor-centred principles with implementation realism. We do not produce frameworks that cannot function in real institutions. Our outputs are tested against the actual capacity, culture, and constraints of the systems that will use them.",
     [("le-training-stand.jpg", ""), ("le-overstrand-2025.jpg", "tall"), ("le-training-2.jpg", "tall")]),
    ("harms", "02", "icon-sustainability-light.svg", "Evidence-Informed Responses to Substance-Related Harms",
     "Health and social-service providers, justice-sector partners, municipalities, and funders working to improve outcomes for marginalised and underserved women, and for populations affected by the intersection of poverty and substance use.",
     ["STAND develops and supports public-health-oriented, rights-based responses to substance-related harms, with particular expertise in the intersection of substance use, gender-based violence, and justice involvement.",
      "Specific work includes needs assessments and service-landscape analysis, training for health, law enforcement, justice and social services personnel, development of human-centred and gender-responsive service protocols, policy engagement and technical advocacy, systems design for integrated care pathways, and programme evaluation and learning."],
     "STAND understands the full continuum, from harm reduction through to abstinence-oriented approaches. We meet people where they are, without stigma, and support them to move towards health and wellness as their circumstances allow. We design for what the evidence and the context require, never defaulting to a single framework.",
     [("toolkit-1.jpg", "tall"), ("hr-training-group.jpg", ""), ("alcohol-poverty.jpg", "tall contain"), ("alcohol-tb.jpg", "tall contain"), ("fasd-2026-a.jpg", ""), ("fasd-2026-b.jpg", "")]),
    ("systems", "03", "icon-transformation-light.svg", "Systems Strengthening and Multi-Sector Coordination",
     "Governments, municipalities, international agencies, and civil-society networks working to improve coordination, reduce service fragmentation, and strengthen accountability across sectors.",
     ["STAND designs and implements coordinated response systems, helping institutions move from fragmented, siloed operations to practical, accountable, multi-sector action.",
      "Specific work includes inter-agency coordination framework design, stakeholder mapping and systems analysis, referral-pathway development and formalisation, monitoring and accountability system design, facilitation of multi-sector coordination processes, and technical drafting of coordination protocols and tools."],
     "STAND has direct implementation experience across district, municipal, and national levels. We understand how coordination works, and how it fails. Every framework we produce is designed to survive contact with real institutions and real constraints.",
     [("vpu-meeting.jpg", ""), ("wits-group.jpg", "tall"), ("wits-wide.jpg", "")]),
    ("alternatives", "04", "icon-culture-light.svg", "Alternatives to Incarceration and Restorative Justice",
     "Justice-sector partners, government departments, civil-society organisations, and international funders supporting diversion, restorative practice, and community-based justice responses.",
     ["STAND provides technical support for the development and implementation of evidence-based alternatives to incarceration, including diversion frameworks, restorative-justice programme design, and institutional capacity building for justice-sector personnel.",
      "Specific work includes diversion framework development and review, restorative-justice programme design, technical writing and policy engagement, institutional capacity building for justice and social-work personnel, and monitoring and learning support."],
     "STAND operates at the evidence-policy-practice interface, engaging both the research base and institutional realities to produce outputs that are analytically grounded, operationally feasible, and appropriately calibrated for the conditions in which they will run.",
     [("cnd2025-group.jpg", ""), ("hr25-panel-d.jpg", ""), ("hr25-panel-e.jpg", "")]),
]

chips = "".join(
    f'<a href="#{a[0]}"><img src="assets/art/{a[2].replace("-light", "")}" alt="" aria-hidden="true">{e(a[3].split(" and ")[0] if a[0] != "harms" else "Substance-Related Harms")}</a>'
    for a in AREAS
)
areas_html = ""
for i, (aid, num, icon, name, who, what, diff, photos) in enumerate(AREAS):
    tone = "band--teal" if i % 2 else "band--cream"
    ic = icon if i % 2 else icon.replace("-light", "")
    pics = "".join(fig(n, c) for n, c in photos)
    grid = "photos" if len(photos) > 2 else "photos photos--2"
    areas_html += f"""
    <section class="band {tone} focus" id="{aid}" aria-labelledby="{aid}-title">
      <div class="container">
        <div class="focus-head reveal">
          <img src="assets/art/{ic}" alt="" aria-hidden="true">
          <div><span class="kicker">Focus Area {num}</span><h2 class="title" id="{aid}-title" style="margin-top:.6rem">{e(name)}</h2></div>
        </div>
        <div class="focus-cols reveal">
          <div><h3>Who this is for</h3><p>{e(who)}</p></div>
          <div><h3>What STAND delivers</h3>{"".join(f"<p>{e(p)}</p>" for p in what)}</div>
          <div><h3>What distinguishes our approach</h3><p>{e(diff)}</p></div>
        </div>
        <div class="{grid}">{pics}</div>
      </div>
    </section>
"""

work = hero(
    "Our Work",
    "Technically rigorous. Grounded in practice.",
    "Every programme is grounded in evidence, designed for implementation, and shaped by the realities of the people it serves.",
    scene="interpol-2025-group.jpg",
) + f"""
    <section class="band band--cream band--tight" id="focus-areas" aria-labelledby="areas-title">
      <div class="container center">
        <h2 class="title reveal" id="areas-title">Four interconnected focus areas</h2>
        <p class="lead reveal" style="margin-top:1rem">STAND's work is intersectional by design: gender-based violence, substance-related harms, justice and health meet at the same point. We deliver across four technically demanding areas where the distance between evidence and action is longest.</p>
        <nav class="chips reveal" aria-label="Focus areas">{chips}</nav>
      </div>
    </section>
{areas_html}
    <section class="band band--dark" aria-labelledby="flag-title">
      <img class="contours" src="assets/art/contours-footer.svg" alt="" aria-hidden="true" loading="lazy">
      <div class="container split split--even">
        <div>
          <p class="eyebrow reveal" style="text-align:left">Flagship Programme</p>
          <h2 class="title reveal" id="flag-title">Track Her Case.</h2>
          <p class="lead reveal" style="margin-top:1rem">Our flagship closes the gap where GBV systems most often fail: the handovers between the institutions meant to protect survivors. Its live pilot, the Red Dot Process, is working in the Overstrand and dispatched its first case three days after launch.</p>
          <div class="actions reveal">{pill("track-her-case.html", "Explore the flagship")}</div>
        </div>
        <div class="reveal">
          <span class="kicker">Live in the field</span>
          <h3 class="title" style="font-size:clamp(1.5rem,2.4vw,2rem);margin:.6rem 0 1.25rem">Overstrand pilot, live since August 2026</h3>
          {ul(["GBV reporting function activated on an existing municipal Citizen App",
               "Non-identifying reference number protects the survivor's identity",
               "Statutory handovers mapped and signed off through the Violence Prevention Unit",
               "First incident dispatched to law enforcement within three days of going live"])}
        </div>
      </div>
    </section>

    <section class="band band--cream" id="capabilities" aria-labelledby="cap-title">
      <div class="container">
        <div class="head center">
          <h2 class="title reveal" id="cap-title">Technical capabilities across every programme</h2>
          <p class="lead reveal" style="margin-top:1rem">Cross-cutting services available to partners in any focus area.</p>
        </div>
        <div class="caps">
          <article class="cap reveal" id="training" aria-labelledby="training-title">
            <img src="assets/art/icon-workshop.svg" alt="" aria-hidden="true">
            <h3 id="training-title">Training design and facilitation</h3>
            <p>STAND designs and facilitates training for law-enforcement, health, justice and social-services personnel, and for community ambassadors. Recent work includes the first regional Gender and Harm Reduction Workshop for INTERPOL and SARPCCO, with representatives from 11 SADC member states; two-day sensitisation training for Overstrand Law Enforcement and South African Police Service officers; and the training of 31 gender-based violence (GBV) ambassadors. Across her career, Stacey Doorly-Jones has trained and facilitated more than 3,500 people.</p>
          </article>
          <article class="cap reveal" id="convening" aria-labelledby="convening-title">
            <img src="assets/art/icon-groups.svg" alt="" aria-hidden="true">
            <h3 id="convening-title">Stakeholder engagement and convening</h3>
            <p>We bring separate institutions to one table and keep them working together. For the Red Dot Process, STAND convened statutory partners through the Western Cape Violence Prevention Unit to map legal mandates, response timelines and handovers. We hosted the national dialogue for Harm Reduction International's South Africa rapid assessment, and convened <em>Decriminalisation of Drug Use: The Plight of the African Woman</em> at the 68th Commission on Narcotic Drugs in Vienna.</p>
          </article>
          <article class="cap reveal" id="research" aria-labelledby="research-title">
            <img src="assets/art/icon-strategy.svg" alt="" aria-hidden="true">
            <h3 id="research-title">Rapid assessment and qualitative research</h3>
            <p>Rapid assessment and situational analysis, qualitative research and key-informant interviewing. STAND led the South Africa country rapid assessment of the impact of donor-funding withdrawal on harm reduction: 34 key-informant interviews, 128 desk reviews and a national dialogue. Its earlier community-based treatment work was run in research partnership with the South African Medical Research Council.</p>
          </article>
          <article class="cap reveal" id="writing" aria-labelledby="writing-title">
            <img src="assets/art/icon-notes.svg" alt="" aria-hidden="true">
            <h3 id="writing-title">Policy drafting and technical writing</h3>
            <p>Technical reports, policy drafts, protocols, proposals and capability statements. Recent outputs include <em>Breaking Point: The Impact of US Funding Cuts on Harm Reduction in South Africa</em>; three published Divest/Invest country studies (South Africa, Mauritius and Ghana); the advocacy report <em>From Field Evidence to National Endorsement</em>, which secured written support from the National Department of Health; and the INTERPOL and SARPCCO report setting out ten regional recommendations.</p>
          </article>
        </div>
        <div class="split" style="margin-top:clamp(3rem,6vw,5rem)">
          <div class="reveal">
            <h3 class="title" style="font-size:clamp(1.4rem,2.2vw,1.9rem)">Also available</h3>
            <div style="margin-top:1.25rem">
            {ul(["Monitoring, evaluation, and learning frameworks",
                 "Strategic and institutional planning support",
                 "Proposal and concept-note development",
                 "Capability statement and positioning document production",
                 "Technical report writing and documentation",
                 "Policy drafting and technical advocacy"])}
            </div>
          </div>
          <div class="photo-stack">
            {fig("suicide-risk-training.jpg", "wide")}
            {fig("wits-podium.jpg")}
          </div>
        </div>
        <div class="photos" style="margin-top:clamp(3rem,6vw,5rem)">
          {fig("training-2022.jpg")}
          {fig("inhsu-delegate.jpg")}
          {fig("hr25-panel-c.jpg")}
          {fig("interpol-2025-group.jpg", caption="")}
          {fig("inhsu-2025.jpg")}
          {fig("hr25-sign.jpg", "tall")}
        </div>
      </div>
    </section>
""" + cta(
    "Need a technically credible implementation partner?",
    "STAND scopes every engagement specifically, from short technical assignments to multi-year programme partnerships. Scope is agreed, outputs are specified, and reporting is thorough, transparent and evidence-based.",
    [PARTNER, pill("founder.html", "Meet the founder", ghost=True)],
)
page("work.html", "Our Work | STAND", "STAND's four focus areas: gender-responsive justice, substance-related harms, systems strengthening and alternatives to incarceration.", work, current="work.html")

# ================================================================ TRACK HER CASE
trace = hero(
    "Flagship Programme",
    "Track Her Case.",
    "Every case, followed through the system to justice. A survivor's journey through the justice system should never disappear in the handover between the services meant to protect her.",
    scene="vpu-meeting.jpg",
) + f"""
    <section class="band band--cream" aria-labelledby="gap-title">
      <div class="container">
        <div class="center head">
          <p class="pull reveal" id="gap-title">Gender-based violence systems rarely fail at the policy. They fail where one service hands her over to the next.</p>
        </div>
        <div class="split split--even prose" style="max-width:none">
          <p class="reveal">Across South Africa and the wider region, the mandates, laws and services to respond to gender-based violence (GBV) largely exist. What breaks is the coordination between them. A report opened with law enforcement stalls before it reaches the prosecutor. A survivor referred for health care is lost before social development ever hears of her. Information degrades as it passes between institutions, so that by the time a case reaches court it is often incomplete or illegible, and is struck from the court roll for want of clarity rather than merit. Each part of the system does its job, and the woman still falls through the spaces in between.</p>
          <p class="reveal">Track Her Case is STAND's response: a privacy-conscious way to follow a case across every institution that touches it, from first report through health, social services, policing and the courts, so that no handover becomes a dead end and the information holds together at each step. It makes the breakdowns visible and strengthens accountability across the whole system, while protecting the survivor's privacy and working within each department's existing mandate.</p>
        </div>
      </div>
    </section>

    <section class="band band--teal" aria-labelledby="dot-title">
      <img class="contours" src="assets/art/contours-footer.svg" alt="" aria-hidden="true" loading="lazy">
      <div class="container split split--even">
        <div class="prose">
          <h2 class="title reveal" id="dot-title">The Red Dot Process: live and working in the Overstrand</h2>
          <div class="reveal" style="margin-top:1.5rem">
            <p>The Red Dot Process is the working pilot of Track Her Case, operating now in the Overstrand.</p>
            <p>Designed by STAND in collaboration with Overstrand Municipality and the Overberg Violence Prevention Unit, with the support of the DG Murray Trust and AIDSFONDS, the Red Dot Process is a seven-stage, privacy-conscious GBV track-and-trace workflow built onto Overstrand Municipality's existing Citizen App. The GBV reporting function went live on 24 August 2026. The first incident was dispatched to law enforcement (the South African Police Service) on 27 August 2026.</p>
          </div>
        </div>
        <div class="phones">
          {fig("gbv-home.png", "contain", label="", caption="GBV Incident, live on the Citizen App")}
          {fig("gbv-service.png", "contain", label="", caption="One tap to medical or police help")}
        </div>
      </div>
    </section>

    <section class="band band--cream2" aria-labelledby="how-title">
      <div class="container split">
        <div class="sticky">
          <span class="kicker reveal">How it works</span>
          <h2 class="title reveal" id="how-title">Seven stages, one non-identifying reference number</h2>
          <a class="reveal" href="assets/stand/tracking-process.jpg" style="display:block;margin-top:2rem;text-decoration:none">
            {fig("tracking-process.jpg", "wide contain", label="", caption="Tap and zoom to read each stage")}
          </a>
        </div>
        <ol class="stages">
          <li class="reveal">A report is logged through the municipality's existing Citizen App, with no new system for anyone to learn</li>
          <li class="reveal">The case is assigned a non-identifying reference number, so it can be tracked without sharing client records or names</li>
          <li class="reveal">Statutory partners were convened through the Western Cape Violence Prevention Unit to map legal mandates, response timelines, and handovers</li>
          <li class="reveal">Handovers are defined across law enforcement and its specialised Family Violence, Child Protection and Sexual Offences (FCS) units, the Department of Justice, the National Prosecuting Authority, the Department of Health, Hermanus Hospital, the Department of Social Development, child protection non-profit organisations and municipal structures</li>
          <li class="reveal">The Violence Prevention Unit signed off the workflow; Health confirmed its stage in the pathway</li>
          <li class="reveal">A trained community layer, embedded in the Department of Social Development's existing GBV Ambassador Programme, supports survivors and peer-led safety systems</li>
          <li class="reveal">The case is traced to resolution, producing a replicable, district-level record of where justice moves and where it stalls. No identifying data is visible, and no departmental statutory systems or mandates are impeded</li>
        </ol>
      </div>
    </section>

    <section class="band band--cream" aria-labelledby="built-title">
      <div class="container">
        <div class="split split--even">
          <div class="prose">
            <h2 class="title reveal" id="built-title">Built on what already exists</h2>
            <div class="reveal" style="margin-top:1.5rem">
              <p>The design discipline is deliberate. The Red Dot Process adds no parallel database, requires no institution to change its mandate, and shares no identifying client records. It works through the systems that partners already use, and the roles they already hold. That is why it went from design to a live dispatch to law enforcement inside a single programme cycle.</p>
              <p>The community layer is equally grounded. STAND equipped and further trained 31 screened gender-based violence (GBV) ambassadors within the Department of Social Development's existing GBV Ambassador Programme, supported testing and peer-led safety systems, and documented a replicable district model.</p>
            </div>
          </div>
          <div class="stats reveal" style="align-self:center">
            <div class="stat"><b>24 Aug</b><span>System went live, 2026</span></div>
            <div class="stat"><b>3 days</b><span>Until the first case was dispatched to the police</span></div>
            <div class="stat"><b>31</b><span>Trained community ambassadors</span></div>
            <div class="stat"><b>130,000+</b><span>People living in the Overstrand</span></div>
          </div>
        </div>
        <p class="center reveal" style="margin-top:2rem;font-weight:600">Designed by STAND with Overstrand Municipality and the Overberg Violence Prevention Unit, with the support of the DG Murray Trust and AIDSFONDS.</p>
        <div class="photos" style="margin-top:clamp(2.5rem,5vw,4rem)">
          {fig("redot-focus-group.jpg", "wide")}
          {fig("ambassadors-certificates.jpg", "wide")}
          {fig("overstrand-gbv-2025.jpg")}
          {fig("redot-mapping.jpg")}
          {fig("citizen-app-design.jpg")}
          {fig("ambassador-phone.jpg")}
          {fig("vpu-meeting.jpg")}
          {fig("le-overstrand-2025.jpg")}
          {fig("ambassador-training.jpg")}
          {fig("le-training-hall.jpg")}
          {fig("citizen-app-guide.jpg", "contain")}
          {fig("le-training-stand.jpg")}
        </div>
        <div class="actions center reveal" style="justify-content:center">{pill("assets/docs/STAND_Track_Her_Case_Project_Brief.pdf", "Download the project brief (PDF)", ghost=True)}</div>
      </div>
    </section>

    <section class="band band--dark" aria-labelledby="scale-title">
      <img class="contours" src="assets/art/contours-footer.svg" alt="" aria-hidden="true" loading="lazy">
      <div class="container split split--even">
        <div>
          <p class="eyebrow reveal" style="text-align:left">Live now, ready to scale</p>
          <h2 class="title reveal" id="scale-title">A working district model, designed to travel across the Global South.</h2>
          <div class="phases reveal">
            <div class="phase phase--done">Phase 1 · built &amp; live</div>
            <div class="phase phase--next">Phase 2 · ready to fund</div>
          </div>
        </div>
        <div class="prose reveal">
          <p>The Red Dot Process is live in the Overstrand and dispatched its first case three days after launch. Phase 1 is built and running, and the back end is ready for the next step. Phase 2 takes it across the whole district, and that is where funding partners come in. With the right support, it scales.</p>
          <h3>What we are seeking</h3>
          <p>Track Her Case is the vision the Red Dot Process proves: a model that any district can adopt to make GBV response visible, coordinated, and accountable, without new systems or new mandates. The pilot is working. The method is documented. The next step is scale.</p>
          <p>We are seeking grantmakers, funders, corporate social investment partners and individual supporters to carry this across the Global South, beginning with Phase 2 of the Overstrand rollout and extending into new districts.</p>
        </div>
      </div>
    </section>
""" + cta(
    "The next step is scale.",
    "You don't have to be an institution to move this. Your gift pays for the people and systems that keep a live case tracking system running, and helps it reach more women.",
    [PARTNER, pill("campaign.html", "Back the campaign", ghost=True), pill("support.html#ways", "Support the work", ghost=True)],
)
page("track-her-case.html", "Track Her Case | STAND", "STAND's flagship programme follows a GBV case across every institution that touches it. Its live pilot, the Red Dot Process, is working in the Overstrand.", trace, current="work.html")

# ================================================================ BOARD
BOARD = [
    ("charity", "board-charity.jpg", "Charity Monareng", "Chairperson · Member since 2021",
     "https://www.linkedin.com/in/charity-monareng-9877b065/",
     ["Charity Monareng is a public-law scholar, drug-policy reform advocate, and non-profit leader with a distinguished track record in harm reduction, human rights, and evidence-based policy development at national, regional, and international levels.",
      "She is completing her PhD in Public Law at the University of Cape Town (expected 2027), and has been active in the drug-policy field since 2018, representing South Africa at the United Nations Commission on Narcotic Drugs (CND) in Vienna, engaging international harm-reduction platforms, and leading reform initiatives focused on youth, gender, and marginalised communities. As Executive Director of Students for Sensible Drug Policy International, she leads organisational strategy across a global network.",
      "Charity brings to STAND's governance the policy-architecture expertise and international network that STAND's work requires."],
     ["Drug-policy reform and decriminalisation", "Public law and human rights", "Harm reduction, strategy and advocacy", "International drug-policy engagement (CND, Vienna)", "Youth and gender-responsive policy", "Non-profit organisational leadership"],
     [("Current position:", "Executive Director, Students for Sensible Drug Policy International."),
      ("Credentials:", "PhD in Public Law (in progress, expected 2027), University of Cape Town; Honours in Social Development, UCT; BA in Criminology and International Studies, Monash South Africa.")]),
    ("julie", "board-julie.jpg", "Julie Mac Donnell", "Treasurer · Associated with STAND since 2019",
     "https://www.linkedin.com/in/julie-mac-donnell",
     ["Julie Mac Donnell is a harm-reduction specialist, human-rights consultant, trainer, and project manager with over a decade of frontline and technical experience in South Africa's drug-policy, healthcare, and civil-society sectors.",
      "Her career spans operational harm-reduction delivery, research and training commissioned by the United Nations Office on Drugs and Crime (UNODC) and the United Nations Development Programme (UNDP), national policy advocacy, and international engagement. At TB HIV Care, where she served for a decade, she established drop-in centres, designed programme frameworks for people who use drugs, and delivered training on harm reduction, gender-based violence (GBV), and the health and rights of women affected by substance use. She is the editor and lead for the internationally developed Pregnancy and Substance Use Toolkit for Health Care Workers, and co-authored the published account of SANPUD's COVID-19 emergency response for the International Drug Policy Consortium.",
      "She brings to STAND's governance a grounded, community-tested understanding of what implementation actually requires."],
     ["Harm reduction, operational delivery and programme design", "Human rights and drug policy", "UNODC, HRI and UNDP-commissioned research", "Women affected by substance use: health, rights and justice (a special interest)", "Rural and remote implementation", "Financial governance and organisational management"],
     [("Current position:", "Director, JMD Consulting & Training."),
      ("Selected affiliations:", "Technical adviser and consultant to the South African Network of People Who Use Drugs (SANPUD); External Consultant to the UNODC Regional Office for Southern Africa.")]),
    ("leon", "board-leon.jpg", "Prof. Leon Holtzhausen", "Director & Secretary · Member since January 2021", None,
     ["Professor Leon Holtzhausen is a senior academic, researcher, and practitioner with deep expertise in criminal-justice social work, substance use disorders, and interpersonal violence. He serves as Associate Professor and Head of the Department of Social Work and Social Development at the University of Cape Town, a position he has held since 2010.",
      "His career began with more than six years of clinical social work in a super-maximum prison, specialising in offender profiling, assessment, and the mental-health treatment of adult and juvenile offenders. He was promoted by the National Department of Correctional Services to Deputy Director for Research, overseeing research across the Department, and then Deputy Director for Correctional Programmes, before taking up an Assistant Professorship at the United Arab Emirates University, where he extended his work into transnational and cross-cultural social work. His published research spans adverse childhood experiences as a risk factor for antisocial behaviour, compassion fatigue among child-protection workers, and the user-centred development of the web-based Western Cape Substance Use Assessment Tool (WC-SUDAT). He co-led a major Open Society Foundation study on services for people experiencing homelessness during COVID-19, and serves on the National and Provincial Accreditation Committee of the Department of Social Development, the Child Justice Alliance, and the South African Violence and Safety Initiative.",
      "He brings to STAND's governance the combination of University of Cape Town academic credibility, criminal-justice practice depth, and active national advisory roles that serious institutional donors require."],
     ["Criminal-justice social work", "Substance use disorders, assessment and intervention", "Adverse childhood experiences and interpersonal violence", "Academic research and evidence production", "Government advisory and accreditation", "Child and youth justice"],
     [("Current position:", "Associate Professor and Head of Department, Social Work and Social Development, University of Cape Town."),
      ("Credentials:", "D Litt et Phil in Social Work, specialisation Criminal Justice, University of Johannesburg (2003); MSW (Community Development), University of Johannesburg; BA Social Work, University of North West.")])
]
profiles = ""
for pid, img, name, role, li, bio, tags, creds in BOARD:
    link = f'<a class="btn-learn" href="{li}" target="_blank" rel="noopener">LinkedIn profile <span class="arrow" aria-hidden="true">&rarr;</span></a>' if li else ""
    profiles += f"""
        <article class="profile" id="{pid}" aria-labelledby="{pid}-name">
          <div class="profile-side">{fig(img, label="", caption="", alt=name)}{link}</div>
          <div>
            <h2 class="reveal" id="{pid}-name">{e(name)}</h2>
            <p class="role reveal">{e(role)}</p>
            <div class="prose reveal">{"".join(f"<p>{e(p)}</p>" for p in bio)}</div>
            {ul(tags, "tags reveal")}
            <div class="creds reveal">{"".join(f"<p><b>{e(k)}</b> {e(v)}</p>" for k, v in creds)}</div>
          </div>
        </article>"""

board = hero(
    "Governance",
    "Board of Directors",
    "STAND is governed by directors who bring substantive expertise in criminal justice, public law, drug-policy reform, harm reduction, and human rights, grounded in implementation experience and international engagement.",
    scene="cnd2025-group.jpg",
) + f"""
    <section class="band band--cream" aria-labelledby="ov-title">
      <div class="container split split--even">
        <h2 class="title reveal" id="ov-title">Accountable governance. Independent oversight.</h2>
        <div class="prose reveal">
          <p>STAND is a registered South African Non-Profit Company and Public Benefit Organisation, governed by a formal Board of Directors that provides independent oversight, strategic guidance, and fiduciary accountability.</p>
          <p>The Board is deliberately constituted to reflect the technical and policy domains in which STAND operates, so that governance is substantively informed as well as procedurally sound. Members are selected for sector expertise, independence, and their capacity to strengthen STAND's institutional credibility and strategic direction. The Board oversees STAND's programme strategy, financial governance, risk and organisational development, with regular engagement between formal meetings.</p>
        </div>
      </div>
    </section>

    <section class="band band--cream2" aria-label="Board members">
      <div class="container">{profiles}
      </div>
    </section>
""" + cta(
    "Governance that reflects the work",
    "Together, the Board brings expertise spanning University of Cape Town academic research, international public law, drug-policy reform at Commission on Narcotic Drugs level, frontline harm-reduction delivery, UNODC-commissioned research, criminal-justice practice, and non-profit financial governance. This is the governance depth serious institutional partners should expect.",
    [pill("mailto:board@standaction.co.za", "board@standaction.co.za"), pill("founder.html", "Meet the founder", ghost=True)],
    small="For governance enquiries, please contact the Board directly at <a href=\"mailto:board@standaction.co.za\">board@standaction.co.za</a>.",
)
page("board.html", "Board of Directors | STAND", "STAND's Board of Directors brings expertise in criminal justice, public law, drug-policy reform, harm reduction and human rights.", board, current="board.html")

# ================================================================ FOUNDER
founder = hero(
    "Founder & CEO",
    "Stacey Doorly-Jones",
    "Senior-level technical expertise, analytical rigour, and donor-literate strategic thinking, brought to complex assignments at the intersection of gender justice, public health, and systems accountability.",
    extra=f"""
        <p class="roles">Senior Consultant · Strategist · Qualitative Researcher · Technical Writer · Facilitator</p>
        <img class="portrait" src="assets/stand/stacey-studio.jpg" alt="{html.escape(PHOTOS['stacey-studio.jpg']['alt'])}" style="order:-1">""",
) + f"""
    <section class="band band--cream" aria-labelledby="range-title">
      <div class="container split">
        <div class="sticky">{fig("apw-2023-speaking.jpg")}</div>
        <div class="prose">
          <h2 class="title reveal" id="range-title">A practitioner with institutional range and implementation depth</h2>
          <div class="reveal" style="margin-top:1.5rem">
            <p>Stacey Doorly-Jones is the founder and Chief Executive of STAND, and an independent senior consultant. She designs, leads, and delivers complex programmes, and builds the systems, relationships, and processes that let separate institutions deliver as one.</p>
            <p>Over three decades her career has moved from financial services and corporate change management into public health, gender justice and complex institutional reform. That arc is unusual, and it is the point: she pairs the discipline of enterprise change leadership with the credibility of someone who has held her own at the executive boardroom table and in district coordination rooms, law-enforcement training environments and rural referral pathways. Her corporate years, including senior roles at TMA and Old Mutual, grounded her in disciplined delivery and client accountability. Her defining strength is translating strategy and evidence into implementation that functions in practice.</p>
            <p>She operates with equal fluency in a donor briefing room, a municipal coordination meeting, a community-based field assessment, and a high-stakes proposal process, adapting how she communicates to each audience without ever diluting the substance.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="band band--teal band--tight" aria-label="Career in numbers">
      <div class="container stats">
        <div class="stat reveal"><b>30+ yrs</b><span>Leading strategy, programmes and institutional change</span></div>
        <div class="stat reveal"><b>R28m+</b><span>In donor and philanthropic funds designed and managed across her career</span></div>
        <div class="stat reveal"><b>3,500+</b><span>People trained and facilitated across her career</span></div>
        <div class="stat reveal"><b>11</b><span>SADC states reached through INTERPOL regional training</span></div>
      </div>
    </section>

    <section class="band band--cream" aria-labelledby="assign-title">
      <div class="container split">
        <div class="sticky">
          <h2 class="title reveal" id="assign-title">Selected recent assignments</h2>
          <p class="lead reveal" style="margin-top:1rem">Current and recent work at the evidence-policy-practice interface.</p>
          <div class="photo-stack" style="margin-top:2rem">
            {fig("hri-national-dialogue.jpg", "wide")}
            {fig("interpol-workshop-blur.jpg", "wide")}
          </div>
        </div>
        <ol class="timeline">
          <li class="reveal"><span class="kicker">Aug 2025 to Aug 2026 · Programme Lead, STAND / DG Murray Trust</span><h3>Breaking the Cycle: gender-based violence (GBV) systems design and the Red Dot Process</h3><p>Designed the Red Dot Process, a seven-stage, privacy-conscious GBV track-and-trace workflow on Overstrand Municipality's Citizen App. The GBV function went live on 24 August 2026; the first incident was dispatched to law enforcement on 27 August. Convened statutory partners through the Western Cape Violence Prevention Unit, which signed off the workflow, and embedded a community layer of 31 trained GBV ambassadors.</p></li>
          <li class="reveal"><span class="kicker">2025 to 2026 · Senior Technical Specialist and Advocacy Lead</span><h3>Pregnancy and Substance Use Toolkit, national advocacy (EJAF / JMD Consulting &amp; Training / SANPUD)</h3><p>Led district-to-national advocacy to position a practical, rights-based clinical toolkit for pregnant women affected by substance use within South African maternal and primary healthcare systems. The work was supported by the Elton John AIDS Foundation (EJAF), with the grant channelled through SANPUD, and delivered with JMD Consulting &amp; Training. Authored the final advocacy report, <em>From Field Evidence to National Endorsement</em>, and secured formal written support from the National Department of Health in June 2026, conditional on defined revisions. The Western Cape confirmed routes to incorporate the content into antenatal and community health-worker training.</p></li>
          <li class="reveal"><span class="kicker">Mar 2025 · Key Facilitator and Technical Consultant</span><h3>INTERPOL Regional Bureau for Southern Africa / SARPCCO</h3><p>Key facilitator at the first regional Gender and Harm Reduction Workshop, convened with SARPCCO (the Southern African Regional Police Chiefs Cooperation Organisation), with representatives from 11 SADC member states. Developed evidence-informed policing modules and co-authored the report setting out ten regional recommendations, recognised with a formal Letter of Appreciation from the Head of the INTERPOL Regional Bureau / SARPCCO Coordination Office.</p></li>
          <li class="reveal"><span class="kicker">Jul 2025 to Aug 2026 · Consultant and Lead African Consultant</span><h3>Harm Reduction International, Breaking Point and the Divest/Invest series</h3><p>Led the South Africa country rapid assessment of the impact of donor-funding withdrawal (34 key-informant interviews, 128 desk reviews and a national dialogue) and authored <em>Breaking Point: The Impact of US Funding Cuts on Harm Reduction in South Africa</em>. As Lead African Consultant for the Divest/Invest case-study series, authored three published country studies: South Africa (on the Community Oriented Substance Use Programme, COSUP), Mauritius, and Ghana.</p></li>
        </ol>
      </div>
    </section>

    <section class="band band--cream2" aria-labelledby="rel-title">
      <div class="container center">
        <h2 class="title reveal" id="rel-title">Where her independent consulting is most relevant</h2>
        {ul(["Gender-responsive justice and GBV systems",
             "Substance-related harms: policy, practice, and the health-justice interface",
             "Qualitative research design and implementation",
             "Technical writing: reports, proposals, frameworks, tools",
             "Strategic positioning and organisational communications",
             "Training design and facilitation",
             "Stakeholder engagement and multi-sector convening",
             "Bid writing and proposal development",
             "Capability statement and EOI preparation",
             "Monitoring, evaluation, and learning support"], "tags reveal").replace('class="tags reveal"', 'class="tags reveal" style="justify-content:center;margin-top:2rem;color:var(--green-700)"')}
      </div>
    </section>

    <section class="band band--dark" aria-labelledby="rec-title">
      <img class="contours" src="assets/art/contours-footer.svg" alt="" aria-hidden="true" loading="lazy">
      <div class="container">
        <div class="head center"><h2 class="title reveal" id="rec-title">Appointments, platforms and recognition</h2></div>
        <div class="photos">
          {fig("hr25-unodc-workshop.jpg", caption="Workshop with UNODC's Fariba Soltani: Addressing Gender Based Violence (GBV) among Women and People of Diverse Gender Identity and Expression who Use Drugs.")}
          {fig("hr25-wangari.jpg")}
          {fig("hr25-nombulelo.jpg")}
          {fig("awwhr-founders.jpg")}
          {fig("wfad-gender-2020.jpg")}
          {fig("cnd2020-stand-place.jpg")}
          {fig("cnd2020-plenary.jpg")}
          {fig("cnd2020-regina.jpg")}
          {fig("cnd2025-group.jpg")}
          {fig("zambia-1.jpg")}
          {fig("cross-sectionality.jpg")}
          {fig("interpol-2025-delegate.jpg")}
          {fig("inhsu-plenary.jpg")}
          {fig("inhsu-2025.jpg")}
          {fig("inhsu-delegate.jpg")}
        </div>
        <div class="split split--even" style="margin-top:clamp(3rem,6vw,5rem)">
          <ul class="years reveal">
            <li><b>2025</b><span>Convenor of <em>Decriminalisation of Drug Use: The Plight of the African Woman</em> at the 68th Commission on Narcotic Drugs, United Nations Vienna (March), and presenter at the 29th International Harm Reduction Conference (HR25), Bogotá (April).</span></li>
            <li><b>2023</b><span>Co-founder of the African Women Working in Harm Reduction Coalition; panellist at the United Nations Economic and Social Council Partnership Forum (January).</span></li>
            <li><b>2020</b><span>Presenter at the 63rd Commission on Narcotic Drugs, United Nations Vienna; founding member of the Global Gender Committee of the World Federation Against Drugs; and member of the Vienna NGO Committee on Drugs.</span></li>
            <li><b>2019</b><span>Finalist, Impumelelo Innovation Awards, for a rural, evidence-based outpatient community treatment model.</span></li>
          </ul>
          <div class="prose reveal">
            <p>She has also taken part in the forums of the International Network on Health and Hepatitis in Substance Users (INHSU), including its 13th international conference at the Century City Conference Centre in Cape Town.</p>
            <p><b>Education and specialist training:</b> Higher Certificate in Counselling and Interpersonal Skills (SACAP, 2016); Certificate in Leading Financial Sustainability (TSIBA, 2017); UNODC Training of Trainers, Evidence-Based Opioid Agonist Services (2023); Gender-Based Violence and Harm Reduction, UNODC / WHRIN (2024).</p>
          </div>
        </div>
      </div>
    </section>
""" + cta(
    "Available for specialist assignments",
    "Stacey takes independent consulting assignments on a scoped, fee-for-service basis: technical writing, qualitative research, strategic advisory, facilitation, or bid and proposal support.",
    [pill("mailto:stacey@standaction.co.za?subject=Consulting%20assignment", "Discuss an assignment"),
     pill("https://www.linkedin.com/in/stacey-doorly-jones", "Connect on LinkedIn", ghost=True, ext=True),
     pill("about.html", "About STAND", ghost=True)],
)
page("founder.html", "Stacey Doorly-Jones | STAND", "Stacey Doorly-Jones, founder and CEO of STAND: strategist, qualitative researcher, technical writer and facilitator.", founder.replace('<h1 id="page-title">', '<h1 id="page-title" class="name">', 1), current="board.html")

# ================================================================ SUPPORT
def online_card(name, text, url, label, note=""):
    nt = f'<p class="give-note">{note}</p>' if note else ""
    if url:
        btn = f'<a class="btn-pill" href="{url}" target="_blank" rel="noopener">{e(label)}</a>'
    else:  # until the page link is pasted in above
        btn = f'<span class="btn-pill is-pending" aria-disabled="true">{e(name)} page opening soon</span>'
    return f'<article class="card reveal"><p class="for">{e(name)}</p><h3>{e(text)}</h3>{nt}{btn}</article>'


GG_NOTE = ("<b>Tax relief by country</b>GlobalGiving is a US 501(c)(3) charity (EIN 30-0108263), so gifts are tax-deductible for US taxpayers. "
           "UK taxpayers giving in pounds can add Gift Aid at checkout (an extra 25p for every £1). "
           "Donors in Belgium, Bulgaria, France, Germany, Greece, Hungary, Italy, Spain and Switzerland can claim local relief through Transnational Giving Europe. "
           "Gifts in euros, Canadian or Australian dollars are generally not deductible; Canadian donors may qualify under the Canada-US tax treaty. Check with your tax adviser.")
BB_NOTE = ("<b>Section 18A</b>South African donors can request a Section 18A tax certificate from STAND. "
           'Email <a href="mailto:info@standaction.co.za">info@standaction.co.za</a> with your name and the date of your gift.')


def bank_row(k, v, copy=True):
    btn = f'<button class="copy" type="button" data-copy="{html.escape(v)}" aria-label="Copy {html.escape(k)}">Copy</button>' if copy else ""
    return f"<div><dt>{e(k)}</dt><dd>{e(v)}{btn}</dd></div>"


def ways(ref="Your name, plus “donation”", cta="Give with SnapScan"):
    return f"""        <div class="ways">
          <article class="card reveal">
            <p class="for">SnapScan</p>
            <h3>The quickest way to give from your phone.</h3>
            <p class="give-note"><b>Scan or tap to give</b>On your phone, tap the button. On a computer, scan the code with the SnapScan app. Payments are handled securely by SnapScan; STAND never sees your card details.</p>
            <a class="snap-badge" href="{SNAPSCAN_URL}" target="_blank" rel="noopener"><img src="assets/stand/snapscan-badge.png" alt="SnapScan code: snap here to pay STAND" width="520" height="741" loading="lazy"></a>
            <a class="btn-pill" href="{SNAPSCAN_URL}" target="_blank" rel="noopener">{cta}</a>
          </article>
          {online_card("GlobalGiving", "Give online from anywhere in the world.", GLOBALGIVING_URL, "Give through GlobalGiving", GG_NOTE)}
          {online_card("BackaBuddy", "Give online in South Africa.", BACKABUDDY_URL, "Give through BackaBuddy", BB_NOTE)}
          <article class="card reveal ways-eft">
            <p class="for">EFT (bank transfer)</p>
            <dl class="bank">
              {bank_row("Account name", "Social Transformation Action Defined")}
              {bank_row("Bank", "First National Bank (FNB)", copy=False)}
              {bank_row("Account number", "62759591623")}
              {bank_row("Branch code", "250655")}
              {bank_row("SWIFT (international)", "FIRNZAJJ")}
              {bank_row("Reference", ref, copy=False)}
            </dl>
            <p class="give-note"><b>International donors</b>You can give by international bank transfer using the SWIFT code in the EFT details. Email us and we will confirm receipt.</p>
            <p class="give-note">For a South African Section 18A certificate, email <a href="mailto:info@standaction.co.za">info@standaction.co.za</a> with your EFT reference.</p>
          </article>
"""


support = hero(
    "Get involved",
    "Support the systems that reach people.",
    "STAND is lean and senior-led by design. Your support pays for the people and systems that deliver the work. There are three ways to work with us.",
    scene="plenary-wide.jpg",
    extra=f'\n        <div class="hero-actions">{SUPPORT}</div>',
) + f"""
    <section class="band band--cream" aria-label="Three ways to work with us">
      <div class="container cards">
        <article class="card give-card reveal" id="partner">
          <p class="for">For funders &amp; institutions</p>
          <h3>Partner with us</h3>
          <p>Commission STAND to strengthen GBV response, justice pathways, or coordinated health-justice systems, as a focused programme or specialist depth within a larger consortium.</p>
          <a class="btn-learn" href="index.html#contact">Start a conversation <span class="arrow" aria-hidden="true">&rarr;</span></a>
        </article>
        <article class="card give-card reveal" id="fund">
          <p class="for">For donors</p>
          <h3>Fund the work</h3>
          <p>Direct giving helps us carry Track Her Case from the Overstrand into new districts. Give in the way that suits you.</p>
          <a class="btn-learn" href="#ways">Support the work <span class="arrow" aria-hidden="true">&rarr;</span></a>
        </article>
        <article class="card give-card reveal" id="collaborate">
          <p class="for">For organisations</p>
          <h3>Collaborate</h3>
          <p>Bring STAND in as a technical partner on research, training, assessments, or systems design, from community level through to regional and UN-facing work.</p>
          <a class="btn-learn" href="mailto:info@standaction.co.za?subject=Collaboration%20with%20STAND">Explore collaboration <span class="arrow" aria-hidden="true">&rarr;</span></a>
        </article>
      </div>
    </section>

    <section class="band band--cream2" aria-labelledby="does-title">
      <div class="container">
        <div class="head center">
          <h2 class="title reveal" id="does-title">What your support does</h2>
          <p class="lead reveal">Your support pays for the people and systems that deliver the work.</p>
        </div>
        <div class="cards cards--3">
          <article class="card reveal"><h3>Ambassadors on active duty</h3><p>Stipends for trained community ambassadors who support survivors on the ground and help them follow their cases through every service.</p></article>
          <article class="card reveal"><h3>Data to log and follow cases</h3><p>Mobile data so ambassadors can log and follow cases.</p></article>
          <article class="card reveal"><h3>Case tracing</h3><p>Day-to-day follow-up of every case through each handover, across police, health, social services and the courts.</p></article>
          <article class="card reveal"><h3>Training</h3><p>Training sessions for ambassadors, police and service providers.</p></article>
          <article class="card reveal"><h3>Community awareness</h3><p>Community information on how to get help and how to use the system.</p></article>
          <article class="card reveal"><h3>Evidence for scale</h3><p>Independent analysis of case outcomes and handover gaps, building the evidence to take the model into new districts across South Africa and the Global South.</p></article>
        </div>
      </div>
    </section>

    <section class="band band--teal" id="ways" aria-labelledby="ways-title">
      <img class="contours" src="assets/art/contours-footer.svg" alt="" aria-hidden="true" loading="lazy">
      <div class="container">
        <div class="head center">
          <h2 class="title reveal" id="ways-title">Support the work</h2>
          <p class="lead reveal">Give in the way that suits you. All South African giving is Section 18A tax-deductible (PBO 930063426).</p>
        </div>
{ways()}
        </div>
      </div>
    </section>

    <section class="band band--cream" aria-labelledby="partners-title">
      <div class="container">
        <div class="head center"><h2 class="title reveal" id="partners-title">Who we work alongside</h2></div>
        <div class="cards cards--plain">
          <article class="card reveal"><h3>Funders and commissioning partners</h3>{ul(["UN Office on Drugs & Crime", "Netherlands Ministry of Foreign Affairs", "DG Murray Trust", "AIDSFONDS", "Elton John AIDS Foundation", "Graham & Rhona Beck Development Trust", "Harm Reduction International"])}</article>
          <article class="card reveal"><h3>Research and delivery partners</h3>{ul(["University of Cape Town", "SA Medical Research Council", "Open Society Foundations", "Harm Reduction International", "United Nations Office on Drugs and Crime", "SANPUD"])}</article>
          <article class="card reveal"><h3>Government partners we work alongside</h3>{ul(["National Department of Health", "Western Cape Department of Health and Wellness", "National and Western Cape Departments of Social Development", "Department of Justice", "National Prosecuting Authority", "South African Police Service, including the FCS units", "Western Cape Violence Prevention Unit", "Overstrand Municipality", "INTERPOL Regional Bureau for Southern Africa and SARPCCO", "Drug Enforcement Commission, Zambia"])}</article>
        </div>
        <div class="photos" style="margin-top:clamp(3rem,6vw,5rem)">
          {fig("cnd2025-group.jpg")}
          {fig("interpol-2025-group.jpg")}
          {fig("hr25-panel-c.jpg")}
        </div>
      </div>
    </section>
""" + cta(
    "Pass it on",
    "Sharing costs nothing and reaches people we never could alone.",
    ['<a class="btn-pill" href="https://wa.me/" data-share-wa data-share-url="https://standaction.co.za/support.html" data-share-text="When a woman asks for help, the system should answer. STAND follows every reported case of gender-based violence through police, health, social services and the courts. Support the work and pass it on:" target="_blank" rel="noopener">Share on WhatsApp</a>',
     pill("index.html#contact", "Send an enquiry", ghost=True)],
    small="You don't have to be an institution to move this. Individuals can back the work directly and help a live system reach more women.",
)
page("support.html", "Support the work | STAND", "Partner with STAND, fund the work or collaborate. All giving is Section 18A tax-deductible.", support, current="involved")

# CAMPAIGN: see tools/build_campaign.py

# ================================================================ PRIVACY
privacy = hero(
    "Privacy and terms",
    "How we handle information.",
    "STAND treats personal information with the same care and accountability we bring to our programmes.",
) + """
    <section class="band band--cream">
      <div class="container">
        <div class="prose" style="margin-inline:auto">
          <h3>Your privacy</h3>
          <p>STAND complies with South Africa's Protection of Personal Information Act (POPIA). We collect only the information you choose to give us, such as your name, email address and EFT reference when you make an enquiry, a donation or a request for a Section 18A certificate. We use it to respond to you, to issue receipts and certificates, and to keep you informed where you have asked us to. We do not sell, rent or share your information with third parties, except where the law requires it. We keep it only for as long as it is needed for these purposes or for our legal and audit obligations.</p>
          <p>You may ask to see, correct or delete the personal information we hold about you at any time. Our Information Officer is Stacey Doorly-Jones, Founder and Chief Executive, contactable at <a href="mailto:stacey@standaction.co.za">stacey@standaction.co.za</a>.</p>
          <h3>Donations</h3>
          <p>Donations made through SnapScan or other online giving platforms are processed securely by those platforms under their own privacy and security policies. STAND never receives or stores your card details. EFT donations are received directly into STAND's registered bank account.</p>
          <h3>Figures and data</h3>
          <p>The figures on this site are drawn from STAND's programme records, donor reports and published research. They are reported conservatively and are accurate as of October 2026. Where a figure combines several programmes, people counted in more than one programme are counted once.</p>
          <h3>Photographs and consent</h3>
          <p>Photographs are used with the permission of those pictured. No person on this site is identified as a survivor or service user. If you appear in an image and would like it removed, please contact us and we will act promptly.</p>
          <h3>Publications and copyright</h3>
          <p>Reports and publications by partner organisations, including Harm Reduction International, remain the property of their publishers and are referenced with acknowledgement. All other content on this site, including text, design and the STAND name and logo, is © 2026 Social Transformation Action Defined NPC. All rights reserved. Content may be quoted for non-commercial purposes with clear attribution to STAND.</p>
          <h3>Cookies</h3>
          <p>This site does not use advertising or tracking cookies. Its fonts are served from this site, so no third party receives your details when you visit.</p>
        </div>
      </div>
    </section>
"""
page("privacy.html", "Privacy and terms | STAND", "How STAND handles personal information, donations, photographs and copyright.", privacy)
