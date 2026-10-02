#!/usr/bin/env python3
"""VR3 Appraisals static site generator.
PREVIEW=True adds noindex so the github.io preview doesn't compete with the real domain.
Flip to False at launch (when www.vr3appraisals.com points here)."""
import os, json, datetime

PREVIEW = False
DOMAIN = "https://www.vr3appraisals.com"
PHONE = "214-280-4464"
PHONE_TEL = "+12142804464"
EMAIL = "jr@vr3appraisals.com"
TALCB = "https://www.talcb.texas.gov/apps/license-holder-search"
COUNTIES = [
    ("Collin", "McKinney, Plano, Frisco, Allen, Prosper, Celina, Lucas, Wylie, Fairview, Murphy"),
    ("Dallas", "Dallas, Richardson, Garland, Mesquite, Irving, Rowlett, Sachse, Highland Park"),
    ("Denton", "Denton, Lewisville, Flower Mound, Little Elm, Aubrey, Argyle, The Colony"),
    ("Rockwall", "Rockwall, Heath, Royse City, Fate, McLendon-Chisholm"),
    ("Tarrant", "Fort Worth, Arlington, Grapevine, Southlake, Keller, Colleyville"),
    ("Kaufman", "Forney, Terrell, Kaufman, Crandall"),
    ("Hunt", "Greenville, Caddo Mills, Quinlan, Commerce"),
    ("Ellis", "Waxahachie, Midlothian, Red Oak, Ennis"),
    ("Johnson", "Burleson, Cleburne, Joshua, Keene"),
]

NAV = [("index.html", "Home"), ("services.html", "Services"), ("for-attorneys.html", "Attorneys"),
       ("service-areas.html", "Areas"), ("about.html", "About"), ("contact.html", "Contact")]

CSS = """
:root{--ink:#2B2B2B;--navy:#14213D;--ox:#7A1F2B;--ox-d:#5E1720;--paper:#F6F1E7;--line:#D9D2C3;--muted:#5f5a52;--card:#FBF8F2}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font:17px/1.6 "Inter",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--paper)}
h1,h2,h3{font-family:"Newsreader",Georgia,serif;font-optical-sizing:auto;line-height:1.1;color:var(--navy);margin:0 0 .5em;font-weight:500;font-variation-settings:"opsz" 72}
h1{font-size:clamp(2.45rem,10.2vw,4rem);font-weight:400;line-height:1.04;letter-spacing:-.02em}h2{font-size:clamp(1.45rem,3.6vw,1.95rem);margin-top:1.6em}h3{font-size:1.2rem}
a{color:var(--ox)}p{margin:0 0 1em}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header{background:var(--paper);position:sticky;top:0;z-index:5}
header .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:64px;flex-wrap:wrap}
.brand{color:var(--navy);text-decoration:none;font-family:"Newsreader",Georgia,serif;font-size:1.7rem;font-weight:500;letter-spacing:-.01em;font-variation-settings:"opsz" 72}
nav{display:flex;gap:2px;flex-wrap:wrap}
nav a{color:var(--navy);text-decoration:none;font-size:.95rem;padding:6px 10px;border-radius:4px}
nav a:hover{background:rgba(20,33,61,.06)}nav a[aria-current]{box-shadow:inset 0 -2px 0 var(--ox)}
.callbar{display:none}
.menu{display:none}
@media(max-width:720px){header nav{display:none}
 .menu{display:block;position:relative}.menu summary{list-style:none;cursor:pointer;padding:8px 2px}.menu summary::-webkit-details-marker{display:none}
 .menu summary svg{display:block}
 .menu[open] .drop{position:absolute;right:0;top:44px;background:var(--paper);border:1px solid var(--line);box-shadow:0 8px 24px rgba(20,33,61,.12);min-width:200px;padding:6px 0;display:flex;flex-direction:column}
 .menu .drop a{color:var(--navy);text-decoration:none;padding:12px 18px;font-size:1rem}
 .menu .drop a[aria-current]{color:var(--ox)}
 header .wrap{flex-wrap:nowrap}
 .callbar{display:flex;position:fixed;bottom:0;left:0;right:0;z-index:9;background:var(--navy)}
 .callbar a{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 8px 12px;color:#fff;font-weight:500;font-size:.92rem;text-decoration:none;border-right:1px solid rgba(255,255,255,.22);background:var(--navy)!important}
 .callbar svg{width:22px;height:22px}
 .callbar a:last-child{border-right:0}
 body{padding-bottom:70px}.hero .btn-p{display:block;text-align:center;margin-right:0}}
.hero{padding:12px 0 26px}
.hero p.lede{font-size:1.08rem;line-height:1.5;color:#45413b;max-width:600px;margin-top:-.1em}
.eyebrow{text-transform:uppercase;letter-spacing:.13em;font-size:clamp(.5rem,2.2vw,.74rem);white-space:nowrap;color:var(--navy);font-weight:600;margin-bottom:1.3em}
.btn{display:inline-block;padding:14px 24px;border-radius:3px;font-weight:700;text-decoration:none;margin:6px 10px 0 0}
.btn-p{background:var(--ox);color:#fff}.btn-p:hover{background:var(--ox-d)}
.btn-s{border:1.5px solid var(--navy);color:var(--navy)}
.verify{display:inline-block;margin-top:14px;font-size:.95rem;color:var(--navy)}
@media(max-width:720px){.hero .vwrap{text-align:center}}
.hrule{border:0;border-top:1px solid var(--line);margin:22px 0 0}
main{padding:8px 0 56px}.lede-sm{font-size:1.08rem;color:#45413b}
.crumb{margin-top:24px}
.rlist{list-style:none;padding:0;margin:16px 0;border:1px solid var(--line);background:var(--card)}
.rlist li{border-bottom:1px solid var(--line)}.rlist li:last-child{border-bottom:0}
.rlist a{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:15px 16px;text-decoration:none;color:var(--navy)}
.rlist a:hover{background:var(--card)}.rlist b{font-weight:500;font-size:1.02rem}
.rlist span{color:var(--muted);font-size:.95rem}.rlist a:after{content:"›";color:var(--navy);font-size:1.5rem;line-height:1}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin:22px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:20px}
.card h3 a{color:var(--navy);text-decoration:none}.card p{color:var(--muted);margin:0}
.note{background:var(--card);border-left:3px solid var(--ox);padding:14px 18px;margin:18px 0}
ul.check{padding-left:0;list-style:none}ul.check li{padding-left:24px;position:relative;margin:.45em 0}
ul.check li:before{content:"";position:absolute;left:4px;top:.68em;width:8px;height:1.5px;background:var(--ox)}
table{border-collapse:collapse;width:100%;background:var(--card);border:1px solid var(--line)}
td,th{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{color:var(--navy);font-family:"Newsreader",Georgia,serif;font-size:1.05rem}
.cta{border-top:2px solid var(--navy);border-bottom:1px solid var(--line);padding:26px 0;margin-top:40px}
.cta h2{margin-top:0}.cta p{color:var(--muted)}
footer{background:var(--navy);color:#b9c0cc;padding:30px 0;font-size:.9rem}footer a{color:#e8ebf0}
.crumb{font-size:.88rem;color:var(--muted);margin-bottom:12px;text-transform:uppercase;letter-spacing:.08em}.crumb a{color:var(--muted);text-decoration:none}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'

def schema():
    return {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "VR3 Appraisals", "url": DOMAIN + "/", "telephone": PHONE_TEL, "email": EMAIL,
        "description": "Certified residential real estate appraiser serving the Dallas-Fort Worth area.",
        "areaServed": [{"@type": "AdministrativeArea", "name": f"{c} County, Texas"} for c, _ in COUNTIES],
        "openingHours": "Mo-Fr 08:00-17:00",
        "founder": {"@type": "Person", "name": "Vicente \"J.R.\" Reyna III", "jobTitle": "Texas Certified Residential Appraiser"},
    }

def page(fname, title, desc, body, hero=None, crumb=None):
    navhtml = "".join(f'<a href="{h}"{" aria-current=page" if h == fname else ""}>{t}</a>' for h, t in NAV)
    robots = '<meta name="robots" content="noindex">' if PREVIEW else ""
    canon = DOMAIN + "/" + ("" if fname == "index.html" else fname)
    crumbs = f'<div class="crumb"><a href="index.html">Home</a> › {crumb}</div>' if crumb else ""
    ld = json.dumps(schema()) if fname == "index.html" else None
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">{robots}
<link rel="canonical" href="{canon}">{FONTS}<link rel="stylesheet" href="style.css">
{'<script type="application/ld+json">'+ld+'</script>' if ld else ''}
</head><body>
<header><div class="wrap"><a class="brand" href="index.html">VR3 Appraisals</a><nav>{navhtml}</nav>
<details class="menu"><summary aria-label="Menu"><svg width="26" height="20" viewBox="0 0 26 20" fill="none" stroke="#14213D" stroke-width="2"><path d="M1 2h24M1 10h24M1 18h24"/></svg></summary><div class="drop">{navhtml}</div></details></div></header>
{hero or ''}
<main><div class="wrap">{crumbs}{body}</div></main>
<footer><div class="wrap">
<p><b style="color:#fff">VR3 Appraisals</b> · Precision in Every Valuation<br>
Vicente "J.R." Reyna III, Texas Certified Residential Appraiser #1361202 · <a href="{TALCB}" target="_blank" rel="noopener">Verify</a><br>
<a href="tel:{PHONE_TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · Mon–Fri 8–5</p>
<p>Serving {", ".join(c for c,_ in COUNTIES[:-1])} and {COUNTIES[-1][0]} counties.</p>
<p>© {datetime.date.today().year} VR3 Management Corp LLC</p>
</div></footer>
<div class="callbar"><a href="tel:{PHONE_TEL}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>Call</a><a href="sms:{PHONE_TEL}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 21l2.1-5.2A8.5 8.5 0 1 1 21 11.5z"/></svg>Text</a><a href="mailto:{EMAIL}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3.5 6l8.5 7 8.5-7"/></svg>Email</a></div>
</body></html>"""

def cta(line="Tell me the property, the purpose, and the date you need the value as of. I'll come back with a quote and a turnaround date."):
    return f'<div class="cta"><h2>Get a quote</h2><p>{line}</p><a class="btn btn-p" href="tel:{PHONE_TEL}">Call {PHONE}</a><a class="btn btn-s" href="mailto:{EMAIL}?subject=Appraisal%20quote%20request">Email</a></div>'

SERVICES = [
 dict(f="divorce-appraisals.html", name="Divorce appraisals",
  title="Divorce Home Appraisal | Collin, Dallas & Rockwall County TX | VR3 Appraisals",
  desc="Independent divorce home appraisals for Texas property division. Current or retrospective values for attorneys, mediators and both spouses. DFW.",
  short="Independent values for property division, by either spouse, both, or counsel.",
  body="""<h1>Divorce appraisals</h1>
<p>When a marriage ends, the house is often the biggest asset on the table. Both sides need a value they can rely on in mediation or court. I provide an independent appraisal of the home. I don't advocate for either spouse.</p>
<h2>What you get</h2><ul class="check">
<li>A full appraisal report with sales comparisons, my measurements and photos</li>
<li>Value as of today, or <b>as of a past date</b> (date of separation or filing) when the case calls for it</li>
<li>Can be ordered by one spouse, both spouses jointly, or either attorney</li></ul>
<h2>Good to know</h2>
<div class="note">If one spouse is still living in the home, I'll coordinate access with whoever ordered the report and keep both sides informed of the inspection time when asked.</div>
<p>Texas is a community property state, so the value of the house often decides who keeps it and what the other spouse receives instead. Getting that number from an independent appraiser, rather than an online estimate or a listing agent's opinion, removes one argument from the case.</p>"""),
 dict(f="estate-date-of-death-appraisals.html", name="Estate & date-of-death appraisals",
  title="Date of Death & Estate Appraisals | DFW Probate | VR3 Appraisals",
  desc="Retrospective date-of-death and estate appraisals for executors, heirs and probate attorneys across Dallas-Fort Worth.",
  short="Retrospective values for probate, inheritance and tax basis.",
  body="""<h1>Estate &amp; date-of-death appraisals</h1>
<p>When someone passes, the estate usually needs the value of their home <b>as of the date of death</b>. That date may be months or years in the past. I research the sales that happened around that date and appraise the home as it was then.</p>
<h2>Common reasons</h2><ul class="check">
<li>Probate and estate inventories</li>
<li>Establishing cost basis for heirs who later sell (talk to your CPA about how this affects capital gains)</li>
<li>Dividing a property among heirs, or one heir buying out the others</li>
<li>Estate tax filings when required</li></ul>
<h2>How it works</h2>
<p>I inspect the home as it is today and document anything that has changed since the date of death, such as repairs, updates or damage. Then I appraise it as of the date your attorney or CPA needs.</p>
<div class="note">Executors are often out of town. I can usually work with a family member, Realtor or attorney's office for access and send the finished report by email.</div>"""),
 dict(f="pmi-removal-appraisals.html", name="PMI removal appraisals",
  title="PMI Removal Appraisal | McKinney, Frisco, Plano & DFW | VR3 Appraisals",
  desc="Appraisals to support removing private mortgage insurance. Check your servicer's requirements first. DFW certified appraiser.",
  short="Show your equity has grown so the monthly PMI charge can come off.",
  body="""<h1>PMI removal appraisals</h1>
<p>If your home has gone up in value, you may have reached the equity your lender requires to drop private mortgage insurance. That can save a few hundred dollars a month. An appraisal is how you prove the new value.</p>
<div class="note"><b>Call your loan servicer before ordering any appraisal.</b> Many servicers require that they order the appraisal themselves, or that it go through a specific company. Ask them three questions: what loan-to-value they need, how they want the appraisal ordered, and whether they require a certain form.</div>
<h2>If your servicer accepts an appraisal you order</h2><ul class="check">
<li>I'll appraise the home on the form your servicer asks for</li>
<li>You get the report directly to submit with your request</li>
<li>Have any recent updates or repairs listed for the inspection, since they can affect value</li></ul>"""),
 dict(f="pre-listing-appraisals.html", name="Pre-listing appraisals",
  title="Pre-Listing Home Appraisal | Price Your Home Right | DFW | VR3 Appraisals",
  desc="Know your home's value before you list. Independent pre-listing appraisals for sellers and for-sale-by-owner across Dallas-Fort Worth.",
  short="Know what the home is worth before you set the price.",
  body="""<h1>Pre-listing appraisals</h1>
<p>Pricing too high costs you time on the market. Pricing too low costs you money. A pre-listing appraisal gives you an independent value before you list, using the same method a buyer's lender will use.</p>
<h2>Who it helps</h2><ul class="check">
<li><b>Sellers</b> who want a number not tied to winning their listing</li>
<li><b>For-sale-by-owner</b> sellers with no agent pricing the home</li>
<li><b>Unusual homes</b> (acreage, custom builds, big renovations) where sales comparisons are hard</li>
<li><b>Realtors</b> who want backup for a price conversation with a seller</li></ul>
<p>It won't replace the buyer's lender appraisal. But it tells you early whether the price will hold up when that appraisal comes.</p>"""),
 dict(f="property-tax-protest-appraisals.html", name="Property tax protest appraisals",
  title="Property Tax Protest Appraisal | Collin, Dallas, Denton CAD | VR3 Appraisals",
  desc="Independent appraisals to support a property tax protest with your county appraisal district (CAD). DFW counties.",
  short="An independent value to bring to your appraisal district hearing.",
  body="""<h1>Property tax protest appraisals</h1>
<p>If your appraisal district's value is higher than what your home would actually sell for, an independent appraisal is strong evidence for your protest.</p>
<h2>Timing</h2>
<div class="note">In Texas, the deadline to protest is generally <b>May 15 or 30 days after your notice was mailed, whichever is later</b>. Check your notice for the exact date. File the protest first; the appraisal can follow before your hearing.</div>
<h2>What helps most</h2><ul class="check">
<li>Value as of <b>January 1</b> of the tax year, which is the date the district uses</li>
<li>Documented condition issues the district can't see from the street, like foundation, roof or outdated interiors</li>
<li>Sales comparisons that actually match your home, not just your neighborhood</li></ul>
<p>I work with appraisal district records in all nine counties I serve.</p>"""),
]

CITIES = [
 dict(f="lucas-tx-home-appraisal.html", city="Lucas", county="Collin",
  intro="Lucas is where I'm based. It's a small Collin County city between Allen and Lake Lavon, known for large lots, acreage and custom-built homes rather than tract subdivisions.",
  points=["Few truly similar sales. A custom home on several acres may have no twin nearby, so comparable sales often come from Parker, Fairview, Murphy or rural Allen and McKinney, with careful adjustments.",
          "Land is a big part of the value. Lot size, usable versus flood-prone acreage, frontage and road access all matter.",
          "Outbuildings, barns, shops, pools and arenas are common, and each one has to be measured and valued on its own merits.",
          "Many homes run on septic and some on well water, which affects both condition review and marketability."],
  nearby="Parker, Fairview, Allen, Wylie and St. Paul"),
 dict(f="rockwall-tx-home-appraisal.html", city="Rockwall", county="Rockwall",
  intro="Rockwall is the county seat of Rockwall County, the smallest county in Texas by area, on the east shore of Lake Ray Hubbard. The market runs from older neighborhoods near downtown to newer master-planned communities and waterfront homes.",
  points=["Waterfront and water-view homes on Lake Ray Hubbard sell at a premium, and that premium has to be supported with sales that share the same view and access.",
          "Rockwall, Heath, Fate, Royse City and McLendon-Chisholm all sit close together, but buyers treat them differently, so where comparable sales come from matters.",
          "Fast-growing areas east of I-30 bring lots of new construction, where builder incentives can distort the sale price."],
  nearby="Heath, Fate, Royse City, Rowlett and McLendon-Chisholm"),
 dict(f="prosper-tx-home-appraisal.html", city="Prosper", county="Collin and Denton",
  intro="Prosper straddles Collin and Denton counties and is one of the fastest-growing towns in North Texas, with large master-planned communities such as Windsong Ranch alongside estate lots on the older side of town.",
  points=["Lots of new construction means builder sales, where incentives and upgrades can make the contract price look higher or lower than the home's market value.",
          "A home may sit on one side of the county line, which changes the appraisal district, tax rate and sometimes school district.",
          "Upgrade packages, lot premiums and community amenities all need to be weighed against resale evidence, not just the builder's price sheet."],
  nearby="Celina, Frisco, McKinney, Aubrey and Little Elm"),
 dict(f="wylie-tx-home-appraisal.html", city="Wylie", county="Collin",
  intro="Wylie sits on the south side of Lake Lavon. Most of it is in Collin County, with small parts reaching into Dallas and Rockwall counties. It mixes established neighborhoods, newer subdivisions and some properties near the lake.",
  points=["The city crosses county lines, so I confirm the correct appraisal district and tax record before anything else.",
          "Subdivisions built in different decades sit side by side. Comparing a 1990s home with a 2020s build takes careful condition and quality adjustments.",
          "Homes backing to open space or near Lake Lavon can carry a premium that needs to be supported by sales, not assumed."],
  nearby="Sachse, Murphy, Lucas, St. Paul and Lavon"),
 dict(f="celina-tx-home-appraisal.html", city="Celina", county="Collin and Denton",
  intro="Celina, in northern Collin County and reaching into Denton County, has grown from a small farm town with a historic downtown square into one of the busiest new-home markets in the region.",
  points=["Neighborhoods often have only a few years of resale history, so builder sales and nearby communities carry more weight in the analysis.",
          "Rural acreage and brand-new subdivisions sit right next to each other, and they don't compare directly.",
          "Infrastructure like new roads and schools changes what buyers pay from one year to the next, so the date of the value matters."],
  nearby="Prosper, McKinney, Weston, Gunter and Aubrey"),
 dict(f="fairview-tx-home-appraisal.html", city="Fairview", county="Collin",
  intro="Fairview sits between Allen and McKinney in Collin County. It's known for larger lots, custom homes and the Heritage Ranch active-adult community.",
  points=["Larger lots and custom homes mean fewer close comparisons, much like neighboring Lucas.",
          "Age-restricted communities such as Heritage Ranch have their own buyer pool, so their sales compare best with each other.",
          "Golf-course, greenbelt and estate lots can add value, but only by as much as the sales support."],
  nearby="Lucas, Allen, McKinney and Parker"),
]

def build(out):
    os.makedirs(out, exist_ok=True)
    W = lambda n, s: open(os.path.join(out, n), "w").write(s)
    W("style.css", CSS)
    cards = '<ul class="rlist">' + "".join(f'<li><a href="{s["f"]}"><div><b>{s["name"]}</b><br><span>{s["short"]}</span></div></a></li>' for s in SERVICES) + '</ul>'
    rows = '<ul class="rlist">' + "".join(f'<li><a href="{s["f"]}"><b>{s["name"]}</b></a></li>' for s in SERVICES) + '</ul>' 
    hero = f"""<section class="hero"><div class="wrap"><div class="eyebrow">Texas Certified Residential Appraiser · License #1361202</div>
<h1>Residential appraisals for homeowners, attorneys and estates across DFW</h1>
<p class="lede">Independent appraisals for divorce, probate, PMI removal, pre-listing and tax protests. Nine North Texas counties.</p>
<a class="btn btn-p" href="tel:{PHONE_TEL}">Call {PHONE}</a><div class="vwrap"><a class="verify" href="{TALCB}" target="_blank" rel="noopener">Verify my license with TALCB</a></div><hr class="hrule"></div></section>"""
    home = f"""<h2 style="margin-top:0">Services</h2>{rows}
<h2>Why an independent appraisal</h2>
<p>Online estimates can't see inside your home, and a listing agent's price is a sales pitch. An appraisal is a licensed, independent opinion of value. It's backed by measured square footage, documented condition, and sales I've verified.</p>
<p>I'm J.R. Reyna, a Texas Certified Residential Appraiser based in Collin County. I also hold a Texas real estate license, so I know the market from both sides of the closing table.</p>
<h2>Where I work</h2><p>{", ".join(c for c,_ in COUNTIES)} counties. <a href="service-areas.html">See cities served</a>.</p>{cta()}"""
    W("index.html", page("index.html", "VR3 Appraisals | Certified Residential Appraiser | Dallas-Fort Worth",
        "Independent home appraisals for divorce, estates, PMI removal, pre-listing and tax protests across Collin, Dallas, Denton, Rockwall and 5 more DFW counties.", home, hero))
    for s in SERVICES:
        W(s["f"], page(s["f"], s["title"], s["desc"], s["body"] + cta(), crumb=f'<a href="services.html">Services</a> › {s["name"]}'))
    W("services.html", page("services.html", "Appraisal Services | VR3 Appraisals | DFW",
        "Residential appraisal services for homeowners, attorneys and estates in Dallas-Fort Worth.",
        f'<h1>Services</h1><p>Every appraisal comes with an inspection, my measurements and photos, verified sales comparisons, and a full written report.</p>{cards}'
        '<h2>Also available</h2><ul class="check"><li>Retrospective (past-date) appraisals for any purpose</li><li>New construction and custom homes</li><li>Acreage and rural residential</li><li>Lender and AMC assignments</li></ul>' + cta(), crumb="Services"))
    W("for-attorneys.html", page("for-attorneys.html", "Appraisals for Family Law & Probate Attorneys | DFW | VR3 Appraisals",
        "Independent residential appraisals for family law and probate attorneys in Collin, Dallas, Denton, Rockwall and surrounding counties.",
        """<h1>For attorneys</h1><p>I appraise residential property for family law and probate matters across nine North Texas counties. My job is the number, not either side's position.</p>
<table><tr><th>You need</th><th>I provide</th></tr>
<tr><td>A value as of a specific past date</td><td>Retrospective appraisals as of separation, filing or date of death</td></tr>
<tr><td>A report that holds up to scrutiny</td><td>Full USPAP-compliant report: measured square footage, photos, verified sales, written reasoning</td></tr>
<tr><td>Neutrality</td><td>Engagement by one party, both parties jointly, or counsel</td></tr>
<tr><td>Access coordination</td><td>I schedule directly with the occupant and keep your office copied</td></tr>
</table>"""
        + cta("Send the property address, the effective date, and who is engaging me. I'll confirm availability and a fee."), crumb="For attorneys"))
    rows = "".join(f"<tr><td><b>{c} County</b></td><td>{cities}</td></tr>" for c, cities in COUNTIES)
    W("service-areas.html", page("service-areas.html", "Service Areas | 9 DFW Counties | VR3 Appraisals",
        "VR3 Appraisals serves Collin, Dallas, Denton, Rockwall, Tarrant, Kaufman, Hunt, Ellis and Johnson counties in North Texas.",
        f"<h1>Service areas</h1><p>I'm based in Collin County and travel across nine North Texas counties. If your town isn't listed, call. If it's in one of these counties, I cover it.</p><h2>City guides</h2><ul class='rlist'>" + "".join(f'<li><a href="{c["f"]}"><b>{c["city"]}</b></a></li>' for c in CITIES) + f"</ul><h2>All counties</h2><table><tr><th>County</th><th>Including</th></tr>{rows}</table>" + cta(), crumb="Service areas"))
    W("about.html", page("about.html", "About J.R. Reyna | Certified Residential Appraiser | VR3 Appraisals",
        "Vicente \"J.R.\" Reyna III, Texas Certified Residential Appraiser #1361202, serving Dallas-Fort Worth since 2020.",
        f"""<h1>About</h1><p>I'm Vicente "J.R." Reyna III, a Texas Certified Residential Appraiser (#1361202). I've appraised homes across Dallas-Fort Worth since 2020, for lenders and directly for homeowners, attorneys and estates.</p>
<p>I also hold a Texas real estate license. That means I see how homes are priced, shown and negotiated, not just how they close.</p>
<p>VR3 Appraisals is part of VR3 Management Corp LLC.</p>""" + cta(), crumb="About"))
    W("contact.html", page("contact.html", "Contact | Request an Appraisal Quote | VR3 Appraisals",
        "Call, text or email VR3 Appraisals for a residential appraisal quote anywhere in Dallas-Fort Worth.",
        f"""<h1>Request a quote</h1><p>The fastest way to reach me is a call or text. I'm often in the field, so if I don't pick up, leave a message and I'll call you back.</p>
<div class="grid"><div class="card"><h3>Call or text</h3><p><a href="tel:{PHONE_TEL}">{PHONE}</a></p></div>
<div class="card"><h3>Email</h3><p><a href="mailto:{EMAIL}?subject=Appraisal%20quote%20request">{EMAIL}</a></p></div>
<div class="card"><h3>Hours</h3><p>Monday–Friday, 8am–5pm</p></div></div>
<h2>Helpful to include</h2><ul class="check"><li>Property address</li><li>Purpose (divorce, estate, PMI, pre-listing, tax protest, other)</li><li>The date the value is needed as of, if not today</li><li>Your deadline</li><li>Who will provide access</li></ul>""", crumb="Contact"))

    for c in CITIES:
        svc = "".join(f'<li><a href="{x["f"]}"><b>{x["name"]}</b></a></li>' for x in SERVICES)
        body = (f'<h1>Home appraisals in {c["city"]}, TX</h1><p class="lede-sm">{c["intro"]}</p>'
                f'<h2>What makes appraising in {c["city"]} different</h2><ul class="check">' + "".join(f"<li>{p}</li>" for p in c["points"]) + '</ul>'
                f'<h2>Services in {c["city"]}</h2><ul class="rlist">{svc}</ul>'
                f'<p>I also cover nearby {c["nearby"]}, plus the rest of {c["county"]} County. <a href="service-areas.html">See all service areas</a>.</p>')
        W(c["f"], page(c["f"], f'{c["city"]}, TX Home Appraisal | Certified Appraiser | VR3 Appraisals',
            f'Independent home appraisals in {c["city"]}, TX ({c["county"]} County) for divorce, estates, PMI removal, pre-listing and tax protests.',
            body + cta(), crumb=f'<a href="service-areas.html">Service areas</a> › {c["city"]}'))
    urls = ["index.html", "services.html"] + [s["f"] for s in SERVICES] + ["for-attorneys.html", "service-areas.html", "about.html", "contact.html"] + [c["f"] for c in CITIES]
    W("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"<url><loc>{DOMAIN}/{'' if u=='index.html' else u}</loc></url>\n" for u in urls) + "</urlset>\n")
    W("robots.txt", ("User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n"))
    W(".nojekyll", "")
    W("CNAME", "www.vr3appraisals.com\n")
    W("404.html", page("404.html", "Page not found | VR3 Appraisals", "Page not found.", '<h1>Page not found</h1><p><a href="index.html">Back to the home page</a></p>'))

if __name__ == "__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs"))
    print("built")
