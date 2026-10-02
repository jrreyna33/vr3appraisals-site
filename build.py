#!/usr/bin/env python3
"""VR3 Appraisals static site generator.
PREVIEW=True adds noindex so the github.io preview doesn't compete with the real domain.
Flip to False at launch (when www.vr3appraisals.com points here)."""
import os, json, datetime

PREVIEW = True
DOMAIN = "https://www.vr3appraisals.com"
PHONE = "214-280-4464"
PHONE_TEL = "+12142804464"
EMAIL = "jr@vr3appraisals.com"
LICENSE = "TX-1361202-R"  # display; state cert number 1361202
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
:root{--ink:#14202e;--navy:#1b2d45;--brass:#b08d57;--brass-d:#8f703f;--paper:#faf8f4;--line:#e4ded3;--muted:#5d6672}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font:17px/1.6 "Source Sans 3",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--paper)}
h1,h2,h3{font-family:"Fraunces",Georgia,serif;line-height:1.2;color:var(--navy);margin:0 0 .5em}
h1{font-size:clamp(2rem,5vw,3rem);font-weight:600}h2{font-size:clamp(1.4rem,3.4vw,1.9rem);font-weight:600;margin-top:1.6em}h3{font-size:1.2rem}
a{color:var(--brass-d)}p{margin:0 0 1em}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
header{background:var(--navy);color:#fff;position:sticky;top:0;z-index:5}
header .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:64px;flex-wrap:wrap}
.brand{color:#fff;text-decoration:none;font-family:"Fraunces",Georgia,serif;font-size:1.35rem;font-weight:600;letter-spacing:.3px}
.brand span{color:var(--brass)}
nav{display:flex;gap:4px;flex-wrap:wrap}
nav a{color:#dfe5ec;text-decoration:none;font-size:.95rem;padding:6px 10px;border-radius:6px}
nav a:hover,nav a[aria-current]{background:rgba(255,255,255,.1);color:#fff}
.callbar{display:none}
@media(max-width:720px){nav{width:100%;overflow-x:auto;flex-wrap:nowrap;padding-bottom:8px}nav a{white-space:nowrap}
 .callbar{display:flex;position:fixed;bottom:0;left:0;right:0;z-index:9;background:var(--navy);padding:10px 12px;gap:10px;box-shadow:0 -2px 10px rgba(0,0,0,.2)}
 .callbar a{flex:1;text-align:center;padding:12px;border-radius:8px;font-weight:700;text-decoration:none}
 body{padding-bottom:72px}}
.hero{background:linear-gradient(160deg,var(--navy),#24395a);color:#fff;padding:64px 0 56px}
.hero h1{color:#fff}.hero p{color:#d6dde6;font-size:1.15rem;max-width:620px}
.eyebrow{text-transform:uppercase;letter-spacing:2px;font-size:.8rem;color:var(--brass);font-weight:700;margin-bottom:.6em}
.btn{display:inline-block;padding:13px 22px;border-radius:8px;font-weight:700;text-decoration:none;margin:6px 8px 0 0}
.btn-p{background:var(--brass);color:#fff}.btn-p:hover{background:var(--brass-d)}
.btn-s{border:2px solid rgba(255,255,255,.5);color:#fff}
.callbar .btn-p{background:var(--brass);color:#fff}.callbar .btn-s{border:2px solid rgba(255,255,255,.5);color:#fff}
main{padding:40px 0 56px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px;margin:24px 0}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:22px}
.card h3 a{color:var(--navy);text-decoration:none}.card p{color:var(--muted);margin:0}
.facts{display:flex;flex-wrap:wrap;gap:10px 28px;margin-top:22px;color:#c7d0db;font-size:.95rem}
.facts b{color:#fff}
.note{background:#fff;border-left:4px solid var(--brass);padding:14px 18px;border-radius:0 8px 8px 0;margin:18px 0}
ul.check{padding-left:0;list-style:none}ul.check li{padding-left:26px;position:relative;margin:.45em 0}
ul.check li:before{content:"";position:absolute;left:4px;top:.55em;width:10px;height:10px;border-radius:2px;background:var(--brass)}
table{border-collapse:collapse;width:100%;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden}
td,th{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:#f2eee6;color:var(--navy)}
.cta{background:var(--navy);color:#fff;border-radius:14px;padding:28px;margin-top:36px}
.cta h2{color:#fff;margin-top:0}.cta p{color:#d6dde6}
footer{background:#0f1a28;color:#9aa6b4;padding:30px 0;font-size:.9rem}footer a{color:#cdd5df}
.crumb{font-size:.9rem;color:var(--muted);margin-bottom:10px}.crumb a{color:var(--muted)}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Source+Sans+3:wght@400;700&display=swap" rel="stylesheet">'

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
<header><div class="wrap"><a class="brand" href="index.html">VR3 <span>Appraisals</span></a><nav>{navhtml}</nav></div></header>
{hero or ''}
<main><div class="wrap">{crumbs}{body}</div></main>
<footer><div class="wrap">
<p><b style="color:#fff">VR3 Appraisals</b> · Precision in Every Valuation<br>
Vicente "J.R." Reyna III, Texas Certified Residential Appraiser #1361202<br>
<a href="tel:{PHONE_TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · Mon–Fri 8–5</p>
<p>Serving {", ".join(c for c,_ in COUNTIES[:-1])} and {COUNTIES[-1][0]} counties.</p>
<p>© {datetime.date.today().year} VR3 Management Corp LLC</p>
</div></footer>
<div class="callbar"><a class="btn-p" href="tel:{PHONE_TEL}">Call</a><a class="btn-s" href="sms:{PHONE_TEL}">Text</a><a class="btn-s" href="mailto:{EMAIL}">Email</a></div>
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

def build(out):
    os.makedirs(out, exist_ok=True)
    W = lambda n, s: open(os.path.join(out, n), "w").write(s)
    W("style.css", CSS)
    cards = "".join(f'<div class="card"><h3><a href="{s["f"]}">{s["name"]}</a></h3><p>{s["short"]}</p></div>' for s in SERVICES)
    hero = f"""<section class="hero"><div class="wrap"><div class="eyebrow">Precision in Every Valuation</div>
<h1>Residential appraisals for homeowners, attorneys and estates across DFW</h1>
<p>Independent, certified home appraisals for divorce, estates, PMI removal, pre-listing and property tax protests. Nine North Texas counties.</p>
<a class="btn btn-p" href="tel:{PHONE_TEL}">Call {PHONE}</a><a class="btn btn-s" href="contact.html">Request a quote</a>
<div class="facts"><span><b>Texas Certified</b> Residential Appraiser #1361202</span><span><b>Since 2020</b> appraising in DFW</span><span><b>9 counties</b> served</span></div></div></section>"""
    home = f"""<h2 style="margin-top:0">How can I help?</h2><div class="grid">{cards}</div>
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
        f'<h1>Services</h1><p>Every appraisal comes with an inspection, my measurements and photos, verified sales comparisons, and a full written report.</p><div class="grid">{cards}</div>'
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
        f"<h1>Service areas</h1><p>I'm based in Collin County and travel across nine North Texas counties. If your town isn't listed, call. If it's in one of these counties, I cover it.</p><table><tr><th>County</th><th>Including</th></tr>{rows}</table>" + cta(), crumb="Service areas"))
    W("about.html", page("about.html", "About J.R. Reyna | Certified Residential Appraiser | VR3 Appraisals",
        "Vicente \"J.R.\" Reyna III, Texas Certified Residential Appraiser #1361202, serving Dallas-Fort Worth since 2020.",
        f"""<h1>About</h1><p>I'm Vicente "J.R." Reyna III, a Texas Certified Residential Appraiser (#1361202). I've appraised homes across Dallas-Fort Worth since 2020, for lenders and directly for homeowners, attorneys and estates.</p>
<p>I also hold a Texas real estate license. That means I see how homes are priced, shown and negotiated, not just how they close.</p>
<p>Before appraisal, I spent twenty years in the restaurant and bar business. That's where I learned that showing up on time and returning calls matters as much as the work itself.</p>
<p>VR3 Appraisals is part of VR3 Management Corp LLC.</p>""" + cta(), crumb="About"))
    W("contact.html", page("contact.html", "Contact | Request an Appraisal Quote | VR3 Appraisals",
        "Call, text or email VR3 Appraisals for a residential appraisal quote anywhere in Dallas-Fort Worth.",
        f"""<h1>Request a quote</h1><p>The fastest way to reach me is a call or text. I'm often in the field, so if I don't pick up, leave a message and I'll call you back.</p>
<div class="grid"><div class="card"><h3>Call or text</h3><p><a href="tel:{PHONE_TEL}">{PHONE}</a></p></div>
<div class="card"><h3>Email</h3><p><a href="mailto:{EMAIL}?subject=Appraisal%20quote%20request">{EMAIL}</a></p></div>
<div class="card"><h3>Hours</h3><p>Monday–Friday, 8am–5pm</p></div></div>
<h2>Helpful to include</h2><ul class="check"><li>Property address</li><li>Purpose (divorce, estate, PMI, pre-listing, tax protest, other)</li><li>The date the value is needed as of, if not today</li><li>Your deadline</li><li>Who will provide access</li></ul>""", crumb="Contact"))
    urls = ["index.html", "services.html"] + [s["f"] for s in SERVICES] + ["for-attorneys.html", "service-areas.html", "about.html", "contact.html"]
    W("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"<url><loc>{DOMAIN}/{'' if u=='index.html' else u}</loc></url>\n" for u in urls) + "</urlset>\n")
    W("robots.txt", ("User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n"))
    W(".nojekyll", "")
    W("404.html", page("404.html", "Page not found | VR3 Appraisals", "Page not found.", '<h1>Page not found</h1><p><a href="index.html">Back to the home page</a></p>'))

if __name__ == "__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs"))
    print("built")
