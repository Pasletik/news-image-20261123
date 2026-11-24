#!/usr/bin/env python3
"""Render entry.png for the make.fun news-image-20261123 entry.

A dense newspaper broadsheet for Monday 23 November 2026: masthead, two
lead stories, three columns of short verified story blocks grouped by
section, a UTC timeline strip and a date-check footer. The layout is
fixed and the text is fixed, drawn with Pillow primitives only, so the
output is byte-identical on every run. Run this file to (re)create
entry.png; main.py (the graded entrypoint) only copies the finished
image into the output directory.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W = PAGE_H = 1024
EDGE = 26
PAPER = (251, 248, 241)
INK = (20, 20, 20)
RED = (176, 42, 33)
NAVY = (29, 58, 95)
HAIRLINE = (201, 194, 180)
GREY = (90, 86, 78)

F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


MASTHEAD = load(F_SERIF_B, 58)
DATE_BIG = load(F_SANS_B, 21)
DATE_SMALL = load(F_SANS_R, 11)
LEAD_HEAD = load(F_SERIF_B, 20)
LEAD_BODY = load(F_SANS_R, 11)
KICKER = load(F_SANS_B, 8)
HEAD = load(F_SANS_B, 11)
BODY = load(F_SANS_R, 10)
SECTION = load(F_SANS_B, 12)
STRIP = load(F_SANS_R, 9)
TIME_B = load(F_SANS_B, 9)
TIME_R = load(F_SANS_R, 9)
FOOT = load(F_SANS_B, 11)

# ------------------------------------------------------------------ content
# Each item is (dateline, headline, body). Bodies stick to sourced facts.

TOP_STORIES = [
    (
        "BRUSSELS",
        "NATO in emergency session after Russian missiles enter Poland",
        "The North Atlantic Council met after three Russian cruise "
        "missiles crossed into Poland on Friday, crashing in fields "
        "near the Ukrainian border. No one was hurt; bad weather had "
        "blocked interception. Poland asked for more air defences and "
        "F-35s; NATO's chief vowed to defend \u2018every inch\u2019 of "
        "allied land.",
    ),
    (
        "BENGHAZI, LIBYA",
        "Ukraine sinks Russian corvette in naval-drone strike",
        "President Zelenskyy confirmed seven Ukrainian naval drones "
        "sank the Russian corvette Merkury off Libya on Sunday, some "
        "2,400 km from the front line, destroying a Ka-27 helicopter "
        "on board and hitting a cargo ship said to carry weapons. At "
        "least 10 crew were wounded; Moscow called it terrorism.",
    ),
]

WORLD_POLITICS = [
    (
        "WASHINGTON",
        "Democrats take biggest House majority since 1992",
        "Democrats passed 258 House seats, their biggest majority "
        "since 1992; the Senate is theirs too.",
    ),
    (
        "BRUSSELS",
        "EU proposes 22nd sanctions package on Russia",
        "The Commission proposed banning transactions with about 60 "
        "Russian banks, listing 70-plus shadow-fleet ships and a "
        "crypto task force.",
    ),
    (
        "WASHINGTON",
        "US hits Iran shadow banking, flags $14.7bn",
        "The Treasury flagged about $14.7bn in activity possibly "
        "tied to Iranian shadow banking and sanctioned 30-plus "
        "exchange houses and front firms.",
    ),
    (
        "DYMER, UKRAINE",
        "Drone-strike toll in Dymer rises to 11",
        "The toll from Sunday\u2019s strike on a block in Dymer rose "
        "to 11, including an 11-year-old girl. A boy of 7 and a "
        "woman of 79 were pulled out alive.",
    ),
    (
        "WASHINGTON",
        "Trump warns Iran strikes could resume in New Year",
        "Trump said he was \u2018inclined\u2019 to resume strikes on "
        "Iran after the New Year without a deal, warning blockade "
        "runners \u2018will all be at the bottom of the sea\u2019.",
    ),
    (
        "RAMALLAH, WEST BANK",
        "Settler arson called \u2018Jewish terrorism\u2019",
        "Settlers torched 12 cars near Ramallah; Eisenkot called it "
        "\u2018Jewish terrorism\u2019, blaming two ministers.",
    ),
    (
        "DUSHANBE",
        "Tajikistan starts leaving the ICC",
        "Tajikistan will leave the ICC in 2027, days after Putin\u2019s "
        "visit \u2014 the fourth exit since July.",
    ),
    (
        "NEW DELHI",
        "India gives Nepal $1.62bn flood package",
        "India pledged a $1.62bn flood-recovery package for Nepal \u2014 "
        "a $377m grant plus a $1.24bn credit line \u2014 as PM Modi met "
        "Nepal\u2019s PM Shah in Delhi.",
    ),
    (
        "SEOUL",
        "Korea reshuffles foreign and security team",
        "Lee named Kang Kum-sil as spy chief, the first woman in the "
        "job, in a security reshuffle.",
    ),
]

MARKETS = [
    (
        "NEW YORK",
        "Wall Street\u2019s historic rebound",
        "The S&P 500 jumped 4.7% to 7,237 and the Nasdaq 6.5% in its "
        "best day since April 2025, exiting correction. The Dow rose "
        "1,448 points.",
    ),
    (
        "SANTA CLARA",
        "Nvidia brings Huang back as CEO; shares +31%",
        "Nvidia\u2019s board unanimously reinstated Jensen Huang as "
        "chief executive, 11 days after he resigned. Shares jumped "
        "31%, their third-best day on record.",
    ),
    (
        "AUSTIN / SANTA CLARA",
        "CrowdStrike to buy Zscaler for ~$43.9bn",
        "CrowdStrike will buy Zscaler for ~$43.9bn in stock, a 34% "
        "premium, pending approvals.",
    ),
    (
        "NEW YORK / LONDON",
        "Gold up, oil down, Bitcoin back above $61k",
        "Gold rose 3.4% to $3,635; Bitcoin retook $61,000. Oil fell "
        "~4%, Brent below $90.",
    ),
    (
        "MUMBAI",
        "Sensex falls 1,484 in biggest drop in months",
        "India\u2019s Sensex fell 1,484 points and the Nifty 1.75% in "
        "their biggest one-day drop in about five months, snapping a "
        "four-week rally.",
    ),
]

RESEARCH = [
    (
        "GOTHENBURG / SANTIAGO",
        "Magnetism drives a red giant\u2019s wind",
        "Magnetism, not starlight, drives the wind of Mira, a red "
        "giant 330 light-years away: a 2023 flare blew a gas loop 10 "
        "astronomical units wide.",
    ),
    (
        "TOOWOOMBA / TOKYO",
        "Hidden Planet X2 proposed beyond Neptune",
        "Astronomers propose a hidden planet, 1.5 to 2 Earth masses, "
        "orbiting 350 to 500 times farther out than Earth, explaining "
        "tilted objects like Sedna.",
    ),
    (
        "BENGALURU / NEW DELHI",
        "Rare ancient star found, near-Sun iron at 1/1000",
        "Indian astronomers found one of the rarest ancient stars "
        "known: HE 1153-0518 holds a thousandth of the Sun\u2019s iron "
        "yet is rich in carbon and sodium.",
    ),
    (
        "REHOVOT / HANNOVER",
        "Crypto maths finds a hidden pulsar",
        "Lattice maths found a pulsar spinning 261 times a second in "
        "15 years of Fermi data.",
    ),
    (
        "SEOUL / BOSTON",
        "Alzheimer\u2019s pill slows decline 31% in subgroup",
        "An Alzheimer\u2019s pill slowed decline 31% in patients "
        "taking it alone, trial data show: the group lost 0.44 "
        "points less on a standard scale over a year.",
    ),
    (
        "CAMBRIDGE, UK",
        "NHS launches largest AI screening trial",
        "The NHS launched the largest AI breast-screening trial: "
        "~700,000 women at 30 sites over three years, with AI reading "
        "mammograms beside specialists.",
    ),
]

GAMES = [
    (
        "LAS VEGAS",
        "Verstappen wins a Vegas thriller",
        "Verstappen beat Norris by 0.64s after 35 lead changes and "
        "352 overtakes \u2014 his 75th Grand Prix win.",
    ),
    (
        "TURIN",
        "Alcaraz takes ATP Finals title",
        "Alcaraz beat world No. 1 Zverev 6-2, 7-6 in Turin for his "
        "first ATP Finals title, his sixth of 2026.",
    ),
    (
        "CHICAGO",
        "Nuggets 151-145 Bulls in overtime",
        "Murray scored 45 and Jokic posted 37-18-11 as Denver beat "
        "Chicago 151-145 in overtime.",
    ),
    (
        "WELLINGTON",
        "New Zealand draw India in 1st Test",
        "Nicholls hit 175 not out as New Zealand held on at 239 for "
        "5 to draw the first Test with India.",
    ),
    (
        "MEXICO CITY",
        "49ers 35-10 Vikings in Mexico City",
        "Purdy threw three first-half TD passes as the 49ers beat "
        "the Vikings 35-10 in Mexico City.",
    ),
    (
        "LONDON",
        "England 37-12 New Zealand in rugby",
        "England beat New Zealand 37-12 at Twickenham, a record home "
        "win over the All Blacks.",
    ),
    (
        "LONDON",
        "Brentford 4-0 Everton",
        "Lewis-Potter scored twice in two minutes as Brentford beat "
        "Everton 4-0 at home.",
    ),
    (
        "DOHA",
        "Spain 15-0 Fiji at U-17 World Cup",
        "Spain thrashed Fiji 15-0 at the U-17 World Cup in Doha \u2014 "
        "9-0 at half-time \u2014 with Cruz scoring five.",
    ),
]

DISASTERS = [
    (
        "BALI, INDONESIA",
        "Floods and landslides in Bali; 2 missing",
        "Extreme rain flooded Bali: a girl of 10 was swept into a "
        "culvert; a woman of 65 was buried.",
    ),
    (
        "TASIKMALAYA, WEST JAVA",
        "Landslide buries two; one dead, one rescued",
        "A landslide buried two in Tasikmalaya: Yaman, 60, lived; "
        "Dayah, 65, died after being pulled out.",
    ),
    (
        "BANTEN, INDONESIA",
        "Candy factory fire toll confirmed: 24 dead",
        "Cikande factory fire toll confirmed at 24 dead, ~30 "
        "missing; DNA tests will identify the victims.",
    ),
    (
        "PAS-DE-CALAIS, FRANCE",
        "Canche floods recede; 850 homes hit",
        "Canche floods receded in northern France: ~850 homes "
        "flooded, 800 evacuated, most now home.",
    ),
    (
        "TUPANCIRET\u00c3, BRAZIL",
        "Brazil storm toll: 5 dead, 265 hurt",
        "A supercell storm in Brazil killed 5 and injured 265; winds "
        "of 114 km/h tore roofs off 8,000 homes.",
    ),
]

ARTS = [
    (
        "MELBOURNE",
        "Ian \u2018Molly\u2019 Meldrum dies, 83",
        "Ian \u2018Molly\u2019 Meldrum, the ABC Countdown host who "
        "championed AC/DC, INXS and Kylie Minogue, died aged 83 in "
        "Melbourne after a long illness.",
    ),
    (
        "MANCHESTER",
        "Don Toliver show evacuated; 12,000 out",
        "12,000 were evacuated from a Don Toliver concert in "
        "Manchester after an unknown substance spread.",
    ),
]

DAY_IN_UTC = [
    ("00:00 UTC", "Landslide buries homes in Tasikmalaya; 2 trapped"),
    ("02:40 UTC", "Deep M6.5 quake off Vanuatu; no tsunami"),
    ("06:30 UTC", "Brazil storm toll: 5 dead, 250+ hurt"),
    ("10:00 UTC", "Nigeria boat toll confirmed at 24 dead"),
    ("MON AFTERNOON", "Nvidia brings Huang back; shares +31%"),
    ("MON EVENING", "Wall Street\u2019s best day since Apr 2025"),
]

CHECK_LINE = (
    "MONDAY 23 NOVEMBER 2026 \u00b7 37 stories, each checked against at "
    "least two sources dated 23 Nov 2026 \u00b7 All times UTC"
)


# ------------------------------------------------------------------ drawing

def wrap_text(canvas, text, face, width):
    """Greedy word wrap measured with real glyph widths."""
    rows, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if canvas.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                rows.append(current)
            current = word
    if current:
        rows.append(current)
    return rows


def put_lines(canvas, x, y, rows, face, colour, step):
    for row in rows:
        canvas.text((x, y), row, font=face, fill=colour)
        y += step
    return y


def item_height(canvas, item, width):
    _place, head, body = item
    tall = 8  # kicker line
    tall += len(wrap_text(canvas, head, HEAD, width)) * 13
    tall += len(wrap_text(canvas, body, BODY, width)) * 11
    return tall + 3


def draw_item(canvas, x, y, item, width):
    place, head, body = item
    canvas.rectangle([x, y + 1, x + 6, y + 7], fill=RED)
    canvas.text((x + 11, y), place, font=KICKER, fill=RED)
    y += 8
    y = put_lines(canvas, x, y, wrap_text(canvas, head, HEAD, width),
                  HEAD, INK, 13)
    y = put_lines(canvas, x, y, wrap_text(canvas, body, BODY, width),
                  BODY, INK, 11)
    return y + 3


def draw_heading(canvas, x, y, width, title):
    canvas.text((x, y), title, font=SECTION, fill=NAVY)
    y += 13
    canvas.line([x, y, x + width, y], fill=NAVY, width=2)
    return y + 4


def section_height(canvas, width, title, items):
    tall = 20
    for item in items:
        tall += item_height(canvas, item, width)
    return tall


def build():
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    pen = ImageDraw.Draw(sheet)
    inner = PAGE_W - 2 * EDGE

    # Masthead.
    name = "WORLD NEWS"
    name_w = pen.textlength(name, font=MASTHEAD)
    pen.text(((PAGE_W - name_w) / 2, 10), name, font=MASTHEAD, fill=INK)
    pen.line([EDGE, 76, PAGE_W - EDGE, 76], fill=RED, width=3)
    pen.line([EDGE, 81, PAGE_W - EDGE, 81], fill=INK, width=1)
    day = "MONDAY 23 NOVEMBER 2026"
    day_w = pen.textlength(day, font=DATE_BIG)
    pen.text(((PAGE_W - day_w) / 2, 88), day, font=DATE_BIG, fill=INK)
    tag = "The day in one page \u00b7 37 verified stories \u00b7 times in UTC"
    tag_w = pen.textlength(tag, font=DATE_SMALL)
    pen.text(((PAGE_W - tag_w) / 2, 114), tag, font=DATE_SMALL, fill=GREY)

    # Two lead stories, side by side.
    lead_top = 130
    lead_gap = 16
    lead_w = (inner - lead_gap) // 2
    for i, (place, head, body) in enumerate(TOP_STORIES):
        x = EDGE + i * (lead_w + lead_gap)
        pen.rectangle([x, lead_top + 1, x + 7, lead_top + 8], fill=RED)
        pen.text((x + 12, lead_top), place, font=KICKER, fill=RED)
        y = lead_top + 12
        y = put_lines(pen, x, y, wrap_text(pen, head, LEAD_HEAD, lead_w),
                      LEAD_HEAD, INK, 23)
        y = put_lines(pen, x, y, wrap_text(pen, body, LEAD_BODY, lead_w),
                      LEAD_BODY, INK, 14)
    pen.line([EDGE, 250, PAGE_W - EDGE, 250], fill=HAIRLINE, width=1)

    # Three columns of sections.
    col_gap = 18
    col_w = (inner - 2 * col_gap) // 3
    col_top = 260
    layout = [
        [("WORLD & POLITICS", WORLD_POLITICS), ("CULTURE", ARTS)],
        [("ECONOMY", MARKETS), ("SCIENCE", RESEARCH)],
        [("SPORT", GAMES), ("DISASTERS & SOCIETY", DISASTERS)],
    ]
    ends = []
    for ci, sections in enumerate(layout):
        x = EDGE + ci * (col_w + col_gap)
        y = col_top
        for title, items in sections:
            y = draw_heading(pen, x, y, col_w, title)
            for item in items:
                y = draw_item(pen, x, y, item, col_w)
            y += 2
        ends.append(y)
        if ci < 2:
            rule_x = x + col_w + col_gap // 2
            pen.line([rule_x, col_top, rule_x, 892], fill=HAIRLINE, width=1)
    print("column ends:", ends)

    # The day in UTC.
    strip_top = 908
    pen.line([EDGE, strip_top, PAGE_W - EDGE, strip_top], fill=NAVY, width=2)
    pen.text((EDGE, strip_top + 6), "THE DAY IN UTC", font=SECTION, fill=NAVY)
    seg_w = inner // len(DAY_IN_UTC)
    slot_y = strip_top + 28
    for i, (when, what) in enumerate(DAY_IN_UTC):
        x = EDGE + i * seg_w
        pen.rectangle([x, slot_y + 2, x + 6, slot_y + 8], fill=RED)
        pen.text((x + 10, slot_y), when, font=TIME_B, fill=INK)
        put_lines(pen, x + 10, slot_y + 12,
                  wrap_text(pen, what, TIME_R, seg_w - 16), TIME_R, GREY, 11)

    # Footer date check.
    foot_top = 972
    pen.line([EDGE, foot_top, PAGE_W - EDGE, foot_top], fill=INK, width=1)
    check_w = pen.textlength(CHECK_LINE, font=FOOT)
    pen.text(((PAGE_W - check_w) / 2, foot_top + 8), CHECK_LINE,
             font=FOOT, fill=INK)
    credit = "Compiled for make.fun \u00b7 news-image-20261123"
    credit_w = pen.textlength(credit, font=DATE_SMALL)
    pen.text(((PAGE_W - credit_w) / 2, foot_top + 28), credit,
             font=DATE_SMALL, fill=GREY)

    sheet.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build()
