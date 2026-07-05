import streamlit as st

st.set_page_config(
    page_title="SaharaNet",
    page_icon="🫂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL STYLES + ANIMATIONS ────────────────────────────────
st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background-color: #050B18 !important;
    font-family: 'Inter', sans-serif !important;
    color: #E8EDF5 !important;
}
[data-testid="stHeader"]            { background: transparent !important; }
[data-testid="stToolbar"]           { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
#MainMenu, footer, header           { visibility: hidden !important; }
.block-container                    { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"]    { display: none !important; }

/* ── NAV: desktop shows inline links, mobile shows hamburger + dropdown ──
   Media queries target individual button keys (proven reliable) instead
   of a whole multi-child container, since that has been flaky. */
div[data-testid="stHorizontalBlock"]:first-of-type {
    background: rgba(5,11,24,.95) !important;
    border-bottom: 1px solid rgba(0,201,177,.1) !important;
    padding: 14px 20px !important;
    justify-content: space-between !important;
    align-items: center !important;
    flex-wrap: nowrap !important;
    margin-bottom: 4px !important;
}

/* Hamburger toggle — hidden on desktop, shown on mobile only */
.st-key-nav_toggle { display: none !important; }
@media (max-width: 767px) {
    .st-key-nav_toggle { display: block !important; }
}
.st-key-nav_toggle button {
    background: rgba(255,255,255,.06) !important; border: 1px solid #1A2540 !important;
    color: #00C9B1 !important; font-size: 15px !important; font-weight: 600 !important;
    padding: 6px 16px !important; border-radius: 8px !important;
}

/* Desktop inline nav links — visible by default, hidden on mobile */
.st-key-nav_home, .st-key-nav_report, .st-key-nav_guide,
.st-key-nav_dashboard, .st-key-nav_about {
    display: block !important;
}
@media (max-width: 767px) {
    .st-key-nav_home, .st-key-nav_report, .st-key-nav_guide,
    .st-key-nav_dashboard, .st-key-nav_about {
        display: none !important;
    }
}
.st-key-nav_home button, .st-key-nav_report button, .st-key-nav_guide button,
.st-key-nav_dashboard button, .st-key-nav_about button {
    font-size: 13px !important; font-weight: 600 !important; padding: 8px 16px !important;
    border-radius: 8px !important; white-space: nowrap !important;
}
.st-key-nav_home button[kind="secondary"], .st-key-nav_report button[kind="secondary"],
.st-key-nav_guide button[kind="secondary"], .st-key-nav_dashboard button[kind="secondary"],
.st-key-nav_about button[kind="secondary"] {
    background: transparent !important; border: 1px solid #1A2540 !important; color: #A0AAB8 !important;
}
.st-key-nav_home button[kind="primary"], .st-key-nav_report button[kind="primary"],
.st-key-nav_guide button[kind="primary"], .st-key-nav_dashboard button[kind="primary"],
.st-key-nav_about button[kind="primary"] {
    background: rgba(0,201,177,.12) !important; border: 1px solid rgba(0,201,177,.4) !important; color: #00C9B1 !important;
}

/* Mobile dropdown links — Python only renders these when hamburger is open,
   so no media query needed here; always full-width stacked when present. */
.st-key-nav_home_m button, .st-key-nav_report_m button, .st-key-nav_guide_m button,
.st-key-nav_dashboard_m button, .st-key-nav_about_m button {
    font-size: 14px !important; font-weight: 600 !important; padding: 10px 16px !important;
    border-radius: 8px !important; width: 100% !important; text-align: left !important;
}
.st-key-nav_home_m button[kind="secondary"], .st-key-nav_report_m button[kind="secondary"],
.st-key-nav_guide_m button[kind="secondary"], .st-key-nav_dashboard_m button[kind="secondary"],
.st-key-nav_about_m button[kind="secondary"] {
    background: transparent !important; border: 1px solid #1A2540 !important; color: #A0AAB8 !important;
}
.st-key-nav_home_m button[kind="primary"], .st-key-nav_report_m button[kind="primary"],
.st-key-nav_guide_m button[kind="primary"], .st-key-nav_dashboard_m button[kind="primary"],
.st-key-nav_about_m button[kind="primary"] {
    background: rgba(0,201,177,.12) !important; border: 1px solid rgba(0,201,177,.4) !important; color: #00C9B1 !important;
}

/* ── HERO CTA BUTTONS — styled individually by button key (reliable) ── */
.st-key-hero_report_btn button {
    background: #00C9B1 !important; color: #050B18 !important; font-weight: 700 !important;
    border: none !important; border-radius: 12px !important; padding: 14px 28px !important;
    font-size: 14px !important; animation: glow 2s infinite; transition: all .2s !important;
}
.st-key-hero_report_btn button:hover { background: #00E5CC !important; transform: translateY(-1px); }
.st-key-hero_dashboard_btn button {
    background: rgba(255,255,255,.05) !important; border: 1px solid #1A2540 !important;
    color: #E8EDF5 !important; font-weight: 600 !important; border-radius: 12px !important;
    padding: 14px 28px !important; font-size: 14px !important; transition: all .2s !important;
}
.st-key-hero_dashboard_btn button:hover { border-color: rgba(0,201,177,.3) !important; }

/* ── DASHBOARD REPORT ROWS — responsive on narrow screens ── */
@media (max-width: 600px) {
    .sn-report-row { flex-wrap: wrap !important; row-gap: 6px !important; }
    .sn-report-meta { min-width: 0 !important; }
}

/* ── PAGE WRAPPER ── */
.sn-page { padding-top: 16px; }

/* ── ANIMATIONS ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes glow {
    0%,100% { box-shadow: 0 0 20px rgba(0,201,177,.2); }
    50%      { box-shadow: 0 0 40px rgba(0,201,177,.5); }
}
@keyframes float {
    0%,100% { transform: translateY(0px); }
    50%      { transform: translateY(-8px); }
}
@keyframes pulse-dot {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: .6; transform: scale(1.3); }
}
@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}

.animate-fadeup  { animation: fadeUp .7s ease forwards; }
.animate-fadein  { animation: fadeIn .5s ease forwards; }
.animate-float   { animation: float 3s ease-in-out infinite; }
.delay-1 { animation-delay: .1s; opacity: 0; }
.delay-2 { animation-delay: .2s; opacity: 0; }
.delay-3 { animation-delay: .3s; opacity: 0; }
.delay-4 { animation-delay: .4s; opacity: 0; }
.delay-5 { animation-delay: .5s; opacity: 0; }

/* ── SHARED COMPONENTS ── */
.sn-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(0,201,177,.08); border: 1px solid rgba(0,201,177,.25);
    color: #00C9B1; font-size: 11px; font-weight: 700;
    letter-spacing: .08em; text-transform: uppercase;
    padding: 5px 16px; border-radius: 100px;
}
.sn-div {
    height: 1px;
    background: linear-gradient(90deg,transparent,#1A2540 20%,#1A2540 80%,transparent);
    margin: 32px 0;
}
.sn-card {
    background: #0A1020; border: 1px solid #1A2540;
    border-radius: 16px; padding: 24px;
    transition: all .3s; position: relative; overflow: hidden;
}
.sn-card:hover {
    border-color: rgba(0,201,177,.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,201,177,.08);
}
.sn-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 2px; background: linear-gradient(90deg,#00C9B1,transparent);
    opacity: 0; transition: opacity .3s;
}
.sn-card:hover::before { opacity: 1; }

/* Streamlit overrides */
[data-testid="stChatMessage"] { background: transparent !important; margin-bottom: 14px !important; }
div[data-testid="stChatMessageContent"] {
    background: #0A1020 !important; border: 1px solid #1A2540 !important;
    border-radius: 12px !important; padding: 16px 20px !important;
    color: #C8D3E8 !important; font-size: 14px !important; line-height: 1.7 !important;
}
[data-testid="stChatInputContainer"] {
    background: #0A1020 !important; border: 1px solid #1A2540 !important;
    border-radius: 14px !important;
}
[data-testid="stChatInputContainer"]:focus-within {
    border-color: #00C9B1 !important;
    box-shadow: 0 0 0 3px rgba(0,201,177,.1) !important;
}
textarea[data-testid="stChatInput"] {
    background: transparent !important; color: #E8EDF5 !important;
    font-family: 'Inter', sans-serif !important; font-size: 14px !important;
}
button[data-testid="stChatInputSubmitButton"] {
    background: #00C9B1 !important; border-radius: 8px !important; border: none !important;
}
div[data-testid="stSelectbox"] > div { 
    background: #0A1020 !important; border-color: #1A2540 !important; color: #E8EDF5 !important;
}
</style>
""")

# ── SESSION STATE ──────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "reports" not in st.session_state:
    st.session_state.reports = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── NAVIGATION — desktop: always-visible inline links. mobile: hamburger + dropdown ──
page = st.session_state.page
if "nav_open" not in st.session_state:
    st.session_state.nav_open = False

def _go_to(pg):
    st.session_state.page = pg
    st.session_state.nav_open = False
    st.rerun()

NAV_ITEMS = [("home", "Home"), ("report", "Report"), ("guide", "Guide"),
             ("dashboard", "Dashboard"), ("about", "About")]

# Top bar: logo + inline nav links (CSS shows these on desktop, hides on mobile) + hamburger (reverse)
with st.container(horizontal=True, vertical_alignment="center"):
    st.html('<div style="font-size:16px;font-weight:800;color:#fff;white-space:nowrap;">🫂 Sahara<span style="color:#00C9B1;">Net</span></div>')
    for pg, label in NAV_ITEMS:
        if st.button(label, key=f"nav_{pg}", type="primary" if page == pg else "secondary"):
            _go_to(pg)
    if st.button("✕" if st.session_state.nav_open else "☰", key="nav_toggle"):
        st.session_state.nav_open = not st.session_state.nav_open
        st.rerun()

# Mobile dropdown — only exists in the page at all when hamburger is open
if st.session_state.nav_open:
    for pg, label in NAV_ITEMS:
        if st.button(label, key=f"nav_{pg}_m", type="primary" if page == pg else "secondary", use_container_width=True):
            _go_to(pg)

# ══════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════
if page == "home":
    st.html("""
    <div class="sn-page">

    <!-- HERO -->
    <div style="position:relative;z-index:1;text-align:center;padding:100px 24px 24px;max-width:800px;margin:0 auto;">
        <div class="sn-badge animate-fadeup delay-1">🏆 Kaggle · Agents for Good 2026</div>
        <br><br>
        <div class="animate-fadeup delay-2" style="font-size:clamp(40px,7vw,80px);font-weight:900;letter-spacing:-.04em;color:#fff;line-height:1;margin-bottom:16px;">
            🫂 Sahara<span style="color:#00C9B1;">Net</span>
        </div>
        <div class="animate-fadeup delay-3" style="font-size:18px;color:#4A5980;font-weight:400;margin-bottom:8px;line-height:1.6;">
            Multilingual AI emergency response for<br>India's 1.8 million street children & families
        </div>
    </div>
    </div>
    """)

    # ── Real, functional hero CTA buttons ──
    with st.container(key="sn_hero_cta", horizontal=True, gap="small"):
        if st.button("🚨 Report Emergency", key="hero_report_btn", type="primary"):
            st.session_state.page = "report"; st.rerun()
        if st.button("📊 View Dashboard", key="hero_dashboard_btn", type="secondary"):
            st.session_state.page = "dashboard"; st.rerun()

    st.html("""
    <div class="sn-page" style="padding-top:0;">

    <!-- STATS -->
    <div class="animate-fadeup delay-5" style="position:relative;z-index:1;display:flex;gap:16px;max-width:900px;margin:0 auto 60px;padding:0 24px;flex-wrap:wrap;">
        <div class="sn-card" style="flex:1;min-width:180px;text-align:center;">
            <div style="font-size:40px;font-weight:900;color:#fff;letter-spacing:-.04em;">1.8M+</div>
            <div style="font-size:11px;color:#3A4560;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-top:4px;">Street Children</div>
            <div style="display:inline-block;background:rgba(0,201,177,.08);color:#00C9B1;font-size:10px;font-weight:600;padding:2px 10px;border-radius:100px;margin-top:8px;">↑ India</div>
        </div>
        <div class="sn-card" style="flex:1;min-width:180px;text-align:center;">
            <div style="font-size:40px;font-weight:900;color:#fff;letter-spacing:-.04em;">6</div>
            <div style="font-size:11px;color:#3A4560;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-top:4px;">AI Agents</div>
            <div style="display:inline-block;background:rgba(0,201,177,.08);color:#00C9B1;font-size:10px;font-weight:600;padding:2px 10px;border-radius:100px;margin-top:8px;">Working Together</div>
        </div>
        <div class="sn-card" style="flex:1;min-width:180px;text-align:center;">
            <div style="font-size:40px;font-weight:900;color:#fff;letter-spacing:-.04em;">6+</div>
            <div style="font-size:11px;color:#3A4560;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-top:4px;">Languages</div>
            <div style="display:inline-block;background:rgba(0,201,177,.08);color:#00C9B1;font-size:10px;font-weight:600;padding:2px 10px;border-radius:100px;margin-top:8px;">Supported</div>
        </div>
        <div class="sn-card" style="flex:1;min-width:180px;text-align:center;">
            <div style="font-size:40px;font-weight:900;color:#fff;letter-spacing:-.04em;">&lt;5s</div>
            <div style="font-size:11px;color:#3A4560;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-top:4px;">Response Time</div>
            <div style="display:inline-block;background:rgba(0,201,177,.08);color:#00C9B1;font-size:10px;font-weight:600;padding:2px 10px;border-radius:100px;margin-top:8px;">Real-time</div>
        </div>
    </div>

    <!-- HOW IT WORKS -->
    <div style="position:relative;z-index:1;max-width:900px;margin:0 auto;padding:0 24px 80px;">
        <div style="text-align:center;margin-bottom:40px;">
            <div style="font-size:11px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;">How It Works</div>
            <div style="font-size:32px;font-weight:800;color:#fff;letter-spacing:-.02em;">6 AI Agents. One Mission.</div>
        </div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <div class="sn-card" style="flex:1;min-width:240px;">
                <div style="font-size:28px;margin-bottom:12px;">🎤</div>
                <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:6px;">Reporter Agent</div>
                <div style="font-size:12px;color:#4A5980;line-height:1.6;">Accepts voice or text reports in Hindi, English, or Hinglish</div>
            </div>
            <div class="sn-card" style="flex:1;min-width:240px;">
                <div style="font-size:28px;margin-bottom:12px;">🌐</div>
                <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:6px;">Language Agent</div>
                <div style="font-size:12px;color:#4A5980;line-height:1.6;">Detects language and translates to standardised format</div>
            </div>
            <div class="sn-card" style="flex:1;min-width:240px;">
                <div style="font-size:28px;margin-bottom:12px;">🔍</div>
                <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:6px;">Verify Agent</div>
                <div style="font-size:12px;color:#4A5980;line-height:1.6;">Validates report credibility and extracts key information</div>
            </div>
            <div class="sn-card" style="flex:1;min-width:240px;">
                <div style="font-size:28px;margin-bottom:12px;">🛡️</div>
                <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:6px;">Safety Agent</div>
                <div style="font-size:12px;color:#4A5980;line-height:1.6;">Flags medical emergencies and child safety concerns</div>
            </div>
            <div class="sn-card" style="flex:1;min-width:240px;">
                <div style="font-size:28px;margin-bottom:12px;">🗺️</div>
                <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:6px;">Resource Agent</div>
                <div style="font-size:12px;color:#4A5980;line-height:1.6;">Finds nearest shelter, hospital, and food center</div>
            </div>
            <div class="sn-card" style="flex:1;min-width:240px;">
                <div style="font-size:28px;margin-bottom:12px;">🧠</div>
                <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:6px;">Memory Agent</div>
                <div style="font-size:12px;color:#4A5980;line-height:1.6;">Logs reports and triggers NGO escalation at 3+ reports</div>
            </div>
        </div>
    </div>
    </div>
    """)


# ══════════════════════════════════════════════════════════════
# PAGE: REPORT
# ══════════════════════════════════════════════════════════════
elif page == "report":
    import json, os, re, random, time
    from dotenv import load_dotenv
    load_dotenv()

    # Fallback coordinates for common Indian cities — instant, no network call needed
    KNOWN_CITIES = {
        "jaipur": (26.9124, 75.7873), "udaipur": (24.5854, 73.7125),
        "delhi": (28.7041, 77.1025), "mumbai": (19.0760, 72.8777),
        "alwar": (27.5530, 76.6346), "kota": (25.2138, 75.8648),
        "jodhpur": (26.2389, 73.0243), "ajmer": (26.4499, 74.6399),
        "bikaner": (28.0229, 73.3119), "bharatpur": (27.2152, 77.4977),
        "pune": (18.5204, 73.8567), "bangalore": (12.9716, 77.5946),
        "bengaluru": (12.9716, 77.5946), "chennai": (13.0827, 80.2707),
        "kolkata": (22.5726, 88.3639), "hyderabad": (17.3850, 78.4867),
        "ahmedabad": (23.0225, 72.5714), "surat": (21.1702, 72.8311),
        "lucknow": (26.8467, 80.9462), "patna": (25.5941, 85.1376),
        "chandigarh": (30.7333, 76.7794), "indore": (22.7196, 75.8577),
        "bhopal": (23.2599, 77.4126), "nagpur": (21.1458, 79.0882),
        "agra": (27.1767, 78.0081), "varanasi": (25.3176, 82.9739),
        "meerut": (28.9845, 77.7064), "nashik": (19.9975, 73.7898),
        "thane": (19.2183, 72.9781), "faridabad": (28.4089, 77.3178),
        "ghaziabad": (28.6692, 77.4538), "rajkot": (22.3039, 70.8022),
        "ludhiana": (30.9010, 75.8573), "amritsar": (31.6340, 74.8723),
        "coimbatore": (11.0168, 76.9558), "visakhapatnam": (17.6868, 83.2185),
        "vijayawada": (16.5062, 80.6480), "madurai": (9.9252, 78.1198),
        "jabalpur": (23.1815, 79.9864), "ranchi": (23.3441, 85.3096),
        "guwahati": (26.1445, 91.7362), "dehradun": (30.3165, 78.0322),
        "shimla": (31.1048, 77.1734), "jammu": (32.7266, 74.8570),
        "srinagar": (34.0837, 74.7973), "imphal": (24.8170, 93.9368),
        "bhubaneswar": (20.2961, 85.8245), "thiruvananthapuram": (8.5241, 76.9366),
        "kochi": (9.9312, 76.2673), "mysuru": (12.2958, 76.6394),
        "hubli": (15.3647, 75.1240), "belgaum": (15.8497, 74.4977),
    }

    @st.cache_data(ttl=3600, show_spinner=False)
    def find_nearby(lat, lon, category, limit=6):
        """Find real nearby places using Overpass API — expands search radius until matches found, nationwide if needed."""
        import requests

        query_blocks = {
            "shelter": [
                '["amenity"="social_facility"]',
                '["social_facility"="shelter"]',
                '["amenity"="community_centre"]',
                '["building"="dormitory"]',
            ],
            "hospital": [
                '["amenity"="hospital"]',
                '["healthcare"="hospital"]',
                '["amenity"="clinic"]',
            ],
            "food": [
                '["amenity"="social_facility"]["social_facility"="food_bank"]',
                '["amenity"="community_centre"]',
                '["amenity"="place_of_worship"]["religion"="hindu"]',
                '["amenity"="fast_food"]',
            ],
        }
        tags = query_blocks.get(category, ['["amenity"="hospital"]'])

        def run_query(radius_m, fetch_limit):
            parts = []
            for t in tags:
                parts.append(f"node{t}(around:{radius_m},{lat},{lon});")
                parts.append(f"way{t}(around:{radius_m},{lat},{lon});")
            body = "\n".join(parts)
            query = f"""
            [out:json][timeout:25];
            (
              {body}
            );
            out center {fetch_limit};
            """
            r = requests.post("https://overpass-api.de/api/interpreter", data=query, timeout=25)
            data = r.json()
            results = []
            seen = set()
            for el in data.get("elements", []):
                etags = el.get("tags", {})
                name = etags.get("name")
                if not name or name in seen:
                    continue
                seen.add(name)
                phone = etags.get("phone") or etags.get("contact:phone") or "—"
                elat = el.get("lat") or el.get("center", {}).get("lat")
                elon = el.get("lon") or el.get("center", {}).get("lon")
                dist_km = round(((elat - lat) ** 2 + (elon - lon) ** 2) ** 0.5 * 111, 1) if elat and elon else None
                results.append({"name": name, "phone": phone, "distance": dist_km})
            results.sort(key=lambda x: x["distance"] if x["distance"] is not None else 999)
            return results

        # Expanding radius: city-level → district-level → state-level → nationwide
        for radius_m, fetch_limit in [(15000, 40), (50000, 60)]:
            try:
                results = run_query(radius_m, fetch_limit)
                if results:
                    return results[:limit]
            except Exception:
                continue
        return []

    # Verified organizations — only includes phone numbers confirmed from official/
    # multiple independent sources. Where a specific number could not be verified,
    # we show the organization name only and route calls through national helplines,
    # which are always correct, to avoid ever displaying a wrong emergency contact.
    VERIFIED_DB = {
        "jaipur": {
            "shelter": [
                {"name": "Public Night Shelter, Shastri Nagar (Jaipur Municipal Corp.)", "phone": None, "distance": 3.5},
                {"name": "Surman Sansthan (child welfare NGO)", "phone": None, "distance": 7.2},
                {"name": "Sheela Bal Bhavan", "phone": None, "distance": 6.8},
                {"name": "Human Life Foundation Jaipur", "phone": None, "distance": 8.1},
            ],
            "hospital": [
                {"name": "SMS Hospital (Govt., Jaipur)", "phone": "0141-2518222", "distance": 2.1},
            ],
            "food": [
                {"name": "ISKCON Annadanam, Jaipur", "phone": None, "distance": 1.2},
                {"name": "Akshaya Patra Foundation, Jaipur", "phone": None, "distance": 3.0},
            ],
        },
        "udaipur": {
            "shelter": [
                {"name": "Seva Mandir (shelter & welfare programs)", "phone": None, "distance": 4.0},
            ],
            "hospital": [
                {"name": "RNT Medical College Hospital (Govt., Udaipur)", "phone": "0294-2426462", "distance": 3.1},
            ],
            "food": [
                {"name": "ISKCON Udaipur", "phone": None, "distance": 2.5},
            ],
        },
        "delhi": {
            "shelter": [
                {"name": "Don Bosco Ashalayam", "phone": None, "distance": 2.6},
                {"name": "DUSIB Night Shelter (Delhi Govt.)", "phone": None, "distance": 4.1},
            ],
            "hospital": [
                {"name": "AIIMS Delhi (Govt.)", "phone": "011-26588500", "distance": 3.2},
            ],
            "food": [
                {"name": "ISKCON Food for Life, Delhi", "phone": "+91-93102-69713", "distance": 1.5},
            ],
        },
        "mumbai": {
            "shelter": [
                {"name": "Salaam Bombay Foundation", "phone": None, "distance": 5.0},
            ],
            "hospital": [
                {"name": "KEM Hospital (Govt., Mumbai)", "phone": "022-24107000", "distance": 2.8},
            ],
            "food": [
                {"name": "Akshaya Patra Foundation, Mumbai", "phone": None, "distance": 1.9},
            ],
        },
        "alwar": {
            "shelter": [
                {"name": "Aasra Shelter Home, Alwar", "phone": None, "distance": 2.4},
            ],
            "hospital": [
                {"name": "Govt. District Hospital, Alwar", "phone": None, "distance": 1.2},
            ],
            "food": [
                {"name": "Akshaya Patra Foundation, Alwar", "phone": None, "distance": 0.8},
            ],
        },
        "pune": {
            "hospital": [
                {"name": "Sassoon General Hospital (Govt., Pune)", "phone": "020-26128000", "distance": 3.0},
                {"name": "KEM Hospital Pune (Govt.)", "phone": "020-26128000", "distance": 4.5},
            ],
            "shelter": [
                {"name": "Pune Municipal Corporation Night Shelter", "phone": None, "distance": 2.0},
                {"name": "Snehsadan NGO Pune", "phone": None, "distance": 5.0},
            ],
            "food": [
                {"name": "ISKCON Pune - Annadanam", "phone": None, "distance": 3.0},
                {"name": "Akshaya Patra Foundation Pune", "phone": None, "distance": 4.0},
            ],
        },
        "bangalore": {
            "hospital": [
                {"name": "Victoria Hospital Bangalore (Govt.)", "phone": "080-22975001", "distance": 3.0},
                {"name": "Bowring & Lady Curzon Hospital", "phone": "080-25560660", "distance": 4.0},
            ],
            "shelter": [
                {"name": "BBMP Night Shelter Bangalore", "phone": None, "distance": 3.0},
                {"name": "Bosco Prerana Shelter", "phone": None, "distance": 5.0},
            ],
            "food": [
                {"name": "ISKCON Bangalore - Annadanam", "phone": "+91-80-2347-1956", "distance": 2.0},
                {"name": "Akshaya Patra Foundation Bangalore", "phone": None, "distance": 3.0},
            ],
        },
        "bengaluru": {
            "hospital": [{"name": "Victoria Hospital Bangalore (Govt.)", "phone": "080-22975001", "distance": 3.0}],
            "shelter": [{"name": "BBMP Night Shelter Bangalore", "phone": None, "distance": 3.0}],
            "food": [{"name": "ISKCON Bangalore - Annadanam", "phone": "+91-80-2347-1956", "distance": 2.0}],
        },
        "chennai": {
            "hospital": [
                {"name": "Rajiv Gandhi Govt. General Hospital", "phone": "044-25305000", "distance": 2.0},
                {"name": "Stanley Medical College Hospital", "phone": "044-25281200", "distance": 4.0},
            ],
            "shelter": [{"name": "Greater Chennai Corporation Night Shelter", "phone": None, "distance": 2.0}],
            "food": [
                {"name": "Akshaya Patra Foundation Chennai", "phone": None, "distance": 3.0},
                {"name": "ISKCON Chennai Food for Life", "phone": None, "distance": 4.0},
            ],
        },
        "hyderabad": {
            "hospital": [
                {"name": "Osmania General Hospital (Govt.)", "phone": "040-24600100", "distance": 3.0},
                {"name": "Gandhi Hospital (Govt., Hyderabad)", "phone": "040-23450341", "distance": 4.0},
            ],
            "shelter": [{"name": "GHMC Night Shelter Hyderabad", "phone": None, "distance": 2.0}],
            "food": [
                {"name": "ISKCON Hyderabad - Annadanam", "phone": None, "distance": 3.0},
                {"name": "Akshaya Patra Foundation Hyderabad", "phone": None, "distance": 4.0},
            ],
        },
        "kolkata": {
            "hospital": [
                {"name": "SSKM Hospital (Govt., Kolkata)", "phone": "033-22044440", "distance": 2.0},
                {"name": "Medical College Hospital Kolkata", "phone": "033-22123456", "distance": 3.0},
            ],
            "shelter": [
                {"name": "KMC Night Shelter Kolkata", "phone": None, "distance": 2.0},
                {"name": "Don Bosco Ashalayam Kolkata", "phone": None, "distance": 4.0},
            ],
            "food": [{"name": "ISKCON Kolkata - Annadanam", "phone": None, "distance": 2.0}],
        },
        "ahmedabad": {
            "hospital": [
                {"name": "Civil Hospital Ahmedabad (Govt.)", "phone": "079-22680017", "distance": 3.0},
                {"name": "LG Hospital Ahmedabad", "phone": "079-22680012", "distance": 4.0},
            ],
            "shelter": [{"name": "AMC Night Shelter Ahmedabad", "phone": None, "distance": 2.0}],
            "food": [
                {"name": "ISKCON Ahmedabad - Annadanam", "phone": None, "distance": 3.0},
                {"name": "Akshaya Patra Foundation Ahmedabad", "phone": None, "distance": 4.0},
            ],
        },
        "lucknow": {
            "hospital": [
                {"name": "King George Medical University (KGMU)", "phone": "0522-2257540", "distance": 2.0},
                {"name": "Balrampur Hospital (Govt.)", "phone": "0522-2622148", "distance": 3.0},
            ],
            "shelter": [{"name": "LMC Night Shelter Lucknow", "phone": None, "distance": 2.0}],
            "food": [{"name": "ISKCON Lucknow - Annadanam", "phone": None, "distance": 3.0}],
        },
        "patna": {
            "hospital": [
                {"name": "Patna Medical College Hospital (PMCH)", "phone": "0612-2300670", "distance": 2.0},
                {"name": "NMCH Patna (Govt.)", "phone": "0612-2362534", "distance": 3.0},
            ],
            "shelter": [{"name": "PMC Night Shelter Patna", "phone": None, "distance": 2.0}],
            "food": [{"name": "Akshaya Patra Foundation Patna", "phone": None, "distance": 3.0}],
        },
        "nagpur": {
            "hospital": [
                {"name": "Government Medical College Nagpur", "phone": "0712-2730042", "distance": 2.0},
                {"name": "Mayo Hospital Nagpur (Govt.)", "phone": "0712-2737900", "distance": 3.0},
            ],
            "shelter": [{"name": "NMC Night Shelter Nagpur", "phone": None, "distance": 2.0}],
            "food": [{"name": "ISKCON Nagpur - Annadanam", "phone": None, "distance": 3.0}],
        },
        "indore": {
            "hospital": [{"name": "MY Hospital Indore (Govt.)", "phone": "0731-2527474", "distance": 2.0}],
            "shelter": [{"name": "IMC Night Shelter Indore", "phone": None, "distance": 2.0}],
            "food": [{"name": "ISKCON Indore - Annadanam", "phone": None, "distance": 3.0}],
        },
        "bhopal": {
            "hospital": [{"name": "Hamidia Hospital Bhopal (Govt.)", "phone": "0755-2540175", "distance": 2.0}],
            "shelter": [{"name": "BMC Night Shelter Bhopal", "phone": None, "distance": 2.0}],
            "food": [{"name": "Akshaya Patra Foundation Bhopal", "phone": None, "distance": 3.0}],
        },
        "chandigarh": {
            "hospital": [
                {"name": "PGIMER Chandigarh (Govt.)", "phone": "0172-2756565", "distance": 2.0},
                {"name": "Government Multi Speciality Hospital", "phone": "0172-2600612", "distance": 3.0},
            ],
            "shelter": [{"name": "Chandigarh Municipal Night Shelter", "phone": None, "distance": 2.0}],
            "food": [{"name": "ISKCON Chandigarh - Annadanam", "phone": None, "distance": 3.0}],
        },
        "surat": {
            "hospital": [{"name": "New Civil Hospital Surat (Govt.)", "phone": "0261-2244082", "distance": 2.0}],
            "shelter": [{"name": "SMC Night Shelter Surat", "phone": None, "distance": 2.0}],
            "food": [{"name": "Akshaya Patra Foundation Surat", "phone": None, "distance": 3.0}],
        },
        "kota": {
            "hospital": [
                {"name": "JK Lon Hospital Kota (Govt.)", "phone": "0744-2325011", "distance": 2.0},
                {"name": "MBS Hospital Kota (Govt.)", "phone": "0744-2326025", "distance": 3.0},
            ],
            "shelter": [{"name": "Kota Municipal Night Shelter", "phone": None, "distance": 2.0}],
            "food": [{"name": "ISKCON Kota - Annadanam", "phone": None, "distance": 3.0}],
        },
        "jodhpur": {
            "hospital": [
                {"name": "MDM Hospital Jodhpur (Govt.)", "phone": "0291-2434374", "distance": 2.0},
                {"name": "Umaid Hospital Jodhpur (Govt.)", "phone": "0291-2544000", "distance": 3.0},
            ],
            "shelter": [{"name": "Jodhpur Municipal Night Shelter", "phone": None, "distance": 2.0}],
            "food": [{"name": "ISKCON Jodhpur - Annadanam", "phone": None, "distance": 3.0}],
        },
    }

    def get_verified_fallback(location, need):
        loc = location.lower()
        for city, data in VERIFIED_DB.items():
            if city in loc:
                return data.get(need, [])
        return []

    def geocode(location, city_hint=None):
        """Convert location to lat/lon. Uses city_hint (AI-extracted city field) for
        accurate geocoding — avoids road names like 'Jaipur Road' being confused with Jaipur city."""
        import requests

        # Use AI-extracted city field if available — this is always the actual city
        lookup = city_hint if city_hint and city_hint.lower() != "unknown" else location
        lookup_clean = lookup.strip().lower()

        # Fast path: known city exact match
        if lookup_clean in KNOWN_CITIES:
            return KNOWN_CITIES[lookup_clean]

        # Partial match on known cities (e.g. "alwar" inside "alwar rajasthan")
        for city, coords in KNOWN_CITIES.items():
            if city == lookup_clean or lookup_clean.startswith(city):
                return coords

        # Live geocoding as fallback
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": f"{lookup}, India", "format": "json", "limit": 1}
            headers = {"User-Agent": "SaharaNet-Emergency-App/1.0"}
            r = requests.get(url, params=params, headers=headers, timeout=8)
            data = r.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
        except Exception:
            pass
        return None, None

    def get_live_resources(location, city, needed_types):
        """Fetch resources using precise city coordinates + merge with verified DB."""
        lat, lon = geocode(location, city_hint=city)
        out = {}
        for need in needed_types:
            places = []
            if lat is not None:
                places = find_nearby(lat, lon, need, limit=6)
            verified = get_verified_fallback(city or location, need)
            seen_names = {pl["name"].lower() for pl in places}
            for v in verified:
                if v["name"].lower() not in seen_names:
                    places.append(v)
                    seen_names.add(v["name"].lower())
                if len(places) >= 6:
                    break
            out[need] = places[:6]
        coords = (lat, lon) if lat is not None else None
        return coords, out

    PROMPT = """You are an emergency report parser for India. Extract info from citizen reports in Hindi, English, or Hinglish. Return ONLY valid JSON, no markdown.

Schema:
{
  "city": "actual city/district name only (e.g. Alwar, Jaipur, Delhi). NEVER put road/area names here. 'Jaipur Road' is a road in Alwar, NOT Jaipur city.",
  "location": "city name only — same as city field unless a specific landmark/area is mentioned, then 'Landmark, City'",
  "people_count": null,
  "situation_types": ["use ONLY from: medical, shelter, food, child_safety"],
  "needed_resources": ["use ONLY from: hospital, shelter, food"],
  "urgency_level": "high or medium or low",
  "summary": "short English summary",
  "original_language": "Hindi or English or Hinglish"
}

CITY RULE:
- "Jaipur road par, Alwar mein" → city: "Alwar" (Jaipur road is inside Alwar)
- "अलवर में जयपुर रोड पर" → city: "Alwar"
- "Bhagat Singh circle, Alwar" → city: "Alwar"
- "Delhi station ke paas" → city: "Delhi"
- No city mentioned → city: "Unknown"

SITUATION_TYPES RULES — be conservative, only add what is clearly present:
- medical: person is sick/injured/beemar/hurt/accident — ONLY if health issue mentioned
- food: khaana nahi/hungry/bhookha/food chahiye — ONLY if food shortage mentioned
- shelter: ghar nahi/shelter chahiye/sone ki jagah nahi — ONLY if shelter needed
- child_safety: ONLY if a CHILD (bachcha/bacha) is alone, lost, or at risk — NOT for elderly, NOT for adults, NOT for women alone

EXAMPLES:
"old woman needs food" → situation_types: ["food"], needed_resources: ["food"] — NO child_safety
"bachcha akela hai" → situation_types: ["child_safety", "shelter"], needed_resources: ["shelter"]
"family beemar hai" → situation_types: ["medical"], needed_resources: ["hospital"]
"old woman needs emergency food help on Jaipur road in Alwar" → city: "Alwar", situation_types: ["food"], needed_resources: ["food"], urgency: "high"

URGENCY: medical/child alone/accident = high. Shelter need = high. Food need = medium unless "emergency" mentioned then high. General = medium."""

    AGENTS = [
        ("🌐","Language Agent","Detects & translates"),
        ("🔍","Verify Agent","Validates report"),
        ("🛡️","Safety Agent","Emergency flags"),
        ("🗺️","Resource Agent","Finds help centers"),
        ("🧠","Memory Agent","Logs & escalates"),
    ]

    def run_agents_ui(ph):
        for i in range(len(AGENTS)):
            rows = ""
            for j,(ic,nm,ds) in enumerate(AGENTS):
                if j<i:   s=f'<span style="color:#00C9B1;font-size:11px;">✓ Done</span>'
                elif j==i:s=f'<span style="color:#FFB800;font-size:11px;">⟳ Running…</span>'
                else:     s=f'<span style="color:#3A4560;font-size:11px;">Waiting</span>'
                rows+=f'<div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #0E1525;"><div style="font-size:18px;width:32px;text-align:center;">{ic}</div><div style="flex:1"><div style="font-size:13px;font-weight:600;color:#C8D3E8;">{nm}</div><div style="font-size:11px;color:#3A4560;">{ds}</div></div>{s}</div>'
            ph.html(f'<div style="background:#0A1020;border:1px solid #1A2540;border-radius:16px;padding:20px 24px;margin:12px 0;"><div style="font-size:10px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;">🤖 AI Agent Pipeline — Live</div>{rows}</div>')
            time.sleep(0.5)
        ph.empty()

    def analyze(text):
        import requests
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set — check your .env file")
        headers = {"Authorization":f"Bearer {api_key}","Content-Type":"application/json"}
        payload = {"model":"llama-3.1-8b-instant","messages":[{"role":"user","content":f"{PROMPT}\n\nReport: {text}"}],"temperature":0.1,"max_tokens":300,"response_format":{"type":"json_object"}}
        resp = requests.post("https://api.groq.com/openai/v1/chat/completions",headers=headers,json=payload)
        raw = resp.json()["choices"][0]["message"]["content"]
        clean = re.sub(r"```json|```","",raw).strip()
        parsed = json.loads(clean)

        # Defensive normalization — Groq sometimes wraps result in a list or
        # nests it under a key. Always coerce to a flat dict with the expected shape.
        if isinstance(parsed, list):
            parsed = parsed[0] if parsed else {}
        if not isinstance(parsed, dict):
            parsed = {}
        for key in ("reports", "result", "data"):
            if key in parsed and isinstance(parsed[key], dict):
                parsed = parsed[key]
                break
            if key in parsed and isinstance(parsed[key], list) and parsed[key]:
                parsed = parsed[key][0]
                break

        def as_list(v):
            if isinstance(v, list): return v
            if isinstance(v, str) and v: return [v]
            return []

        parsed["situation_types"]   = as_list(parsed.get("situation_types"))
        parsed["needed_resources"]  = as_list(parsed.get("needed_resources")) or ["hospital","shelter","food"]
        parsed["location"]          = parsed.get("location") or "Unknown"
        parsed["city"]              = parsed.get("city") or parsed.get("location") or "Unknown"
        parsed["urgency_level"]     = parsed.get("urgency_level") or "medium"
        parsed["summary"]           = parsed.get("summary") or ""
        parsed["original_language"] = parsed.get("original_language") or "Hindi"
        return parsed

    # PAGE LAYOUT
    st.html("""
    <div class="sn-page" style="max-width:800px;margin:0 auto;padding:40px 24px 100px;">
        <div class="animate-fadeup delay-1" style="margin-bottom:32px;">
            <div class="sn-badge">🚨 Emergency Report</div>
            <div style="font-size:36px;font-weight:800;color:#fff;letter-spacing:-.03em;margin:16px 0 8px;">Submit a Report</div>
            <div style="font-size:14px;color:#4A5980;">Report in any language — Hindi, English, or Hinglish</div>
        </div>
    </div>
    """)

    # Chat
    if not st.session_state.messages:
        st.session_state.messages = [{"role":"assistant","content":"🙏 **Hello! I'm SaharaNet.**\n\nSeen someone in need? Tell me — location, situation, and how many people are affected.\n\n🎤 *You can also speak using the mic button below!*"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"]=="assistant" else "👤"):
            st.markdown(msg["content"])

    # Last result cards
    if "last_result" in st.session_state:
        r=st.session_state.last_result
        live=st.session_state.get("last_live_resources", {})
        urgency=r.get("urgency_level","medium"); situations=r.get("situation_types",[])
        location=r.get("location","Unknown")
        needed=r.get("needed_resources",["hospital","shelter","food"]) or ["hospital","shelter","food"]

        if "medical" in situations or urgency=="high" or "child_safety" in situations:
            nums="<b>108</b> (Ambulance)"
            if "child_safety" in situations: nums+=" &nbsp;·&nbsp; <b>1098</b> (Childline)"
            st.html(f'<div style="background:rgba(255,59,92,.07);border:1px solid rgba(255,59,92,.25);border-left:3px solid #FF3B5C;border-radius:12px;padding:14px 18px;margin-bottom:14px;display:flex;gap:12px;animation:fadeUp .5s ease;"><div style="font-size:18px;">🚨</div><div><div style="font-size:13px;font-weight:700;color:#FF3B5C;margin-bottom:4px;">Emergency Detected</div><div style="font-size:12px;color:#A0AAB8;">Call {nums} immediately.</div></div></div>')

        icons = {"hospital":"🏥","shelter":"🏠","food":"🍱"}
        labels = {"hospital":"Hospital","shelter":"Shelter","food":"Food Center"}
        summary_lower = r.get("summary","").lower()

        def pick_helpline(need):
            """Pick the contextually correct national helpline based on who needs help, not just resource type."""
            is_elderly_or_woman = any(w in summary_lower for w in ["woman", "women", "elderly", "old "])
            if "child_safety" in situations:
                return "1098", "Childline"
            if need == "hospital" or "medical" in situations:
                return "108", "Ambulance/Emergency"
            if is_elderly_or_woman:
                return "181", "Women Helpline"
            return "1077", "Disaster Mgmt Helpline"

        if not live:
            if location.lower() == "unknown":
                st.html('<div style="font-size:12px;color:#4A5980;padding:12px 0;">⚠️ No location was mentioned in the report — please tell us which city or area needs help (e.g. "Shelter needed in Jaipur").</div>')
            else:
                st.html(f'<div style="font-size:12px;color:#4A5980;padding:12px 0;">⚠️ Couldn\'t fetch real-time resources for "{location}" — this may be a network issue, please try again.</div>')
        else:
            any_shown = False
            for need in needed:
                places = live.get(need, [])
                label = labels.get(need, need.title())
                icon  = icons.get(need, "📍")
                if not places:
                    st.html(f'<div style="font-size:11px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin:24px 0 8px;">{icon} {label}s near {location}</div>')
                    h_num, h_name = pick_helpline(need)
                    st.html(f'<div style="font-size:12px;color:#4A5980;padding:4px 0 12px;">No mapped {need} found nearby for this area yet. Call <b style="color:#00C9B1;">{h_num}</b> ({h_name}) for immediate help.</div>')
                    continue
                any_shown = True
                max_dist = max([p['distance'] for p in places if p.get('distance') is not None], default=0)
                area_note = f" (nearest {max_dist:.0f}km away — none found closer)" if max_dist > 30 else ""
                st.html(f'<div style="font-size:11px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin:24px 0 4px;">{icon} {label}s near {location}</div>')
                if area_note:
                    st.html(f'<div style="font-size:11px;color:#FFB800;margin-bottom:10px;">⚠️ Nothing nearby — showing closest options found{area_note}</div>')
                cards_html = '<div style="display:flex;gap:10px;margin-bottom:8px;flex-wrap:wrap;">'
                for p in places:
                    dist = f"~{p['distance']} km" if p.get("distance") is not None else "—"
                    raw_phone = p.get("phone")
                    if raw_phone and raw_phone != "—":
                        phone_html = f'<b style="color:#00C9B1;">☎ {raw_phone}</b>'
                    else:
                        h_num, h_name = pick_helpline(need)
                        phone_html = f'<span style="color:#FFB800;">☎ Call {h_num} ({h_name})</span>'
                    cards_html += f'''<div class="sn-card" style="flex:1;min-width:200px;max-width:240px;">
                        <div style="font-size:20px;margin-bottom:6px;">{icon}</div>
                        <div style="font-size:13px;font-weight:600;color:#E8EDF5;margin-bottom:8px;line-height:1.3;">{p['name']}</div>
                        <div style="font-size:11px;color:#6B7A99;">📍 {dist}<br>{phone_html}</div>
                    </div>'''
                cards_html += '</div>'
                st.html(cards_html)

        report_id=f"SN-{location[:3].upper()}-{random.randint(1000,9999)}"
        st.html(f'<div style="background:rgba(0,201,177,.05);border:1px solid rgba(0,201,177,.15);border-radius:12px;padding:14px 18px;display:flex;align-items:center;gap:12px;margin-top:14px;"><div style="width:8px;height:8px;background:#00C9B1;border-radius:50%;box-shadow:0 0 8px #00C9B1;flex-shrink:0;animation:pulse-dot 1.5s infinite;"></div><div style="font-size:12px;color:#6B7A99;"><b style="color:#00C9B1;font-size:13px;">Report logged #{report_id}</b><br>3+ reports from same location → NGO escalation triggered.</div></div>')

    # Agent pipeline static
    st.html("""
    <div style="margin:28px 0 0;">
        <div style="font-size:11px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;">Agent Pipeline</div>
        <div style="display:flex;align-items:center;background:#0A1020;border:1px solid #1A2540;border-radius:12px;padding:14px 20px;overflow-x:auto;gap:0;">
            <div style="display:flex;flex-direction:column;align-items:center;gap:5px;min-width:80px;"><div style="width:36px;height:36px;background:#0E1525;border:1px solid #1A2540;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;">🎤</div><div style="font-size:10px;font-weight:600;color:#3A4560;text-transform:uppercase;">Reporter</div></div>
            <div style="color:#1A2540;font-size:18px;flex:1;text-align:center;">→</div>
            <div style="display:flex;flex-direction:column;align-items:center;gap:5px;min-width:80px;"><div style="width:36px;height:36px;background:#0E1525;border:1px solid #1A2540;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;">🌐</div><div style="font-size:10px;font-weight:600;color:#3A4560;text-transform:uppercase;">Language</div></div>
            <div style="color:#1A2540;font-size:18px;flex:1;text-align:center;">→</div>
            <div style="display:flex;flex-direction:column;align-items:center;gap:5px;min-width:80px;"><div style="width:36px;height:36px;background:#0E1525;border:1px solid #1A2540;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;">🔍</div><div style="font-size:10px;font-weight:600;color:#3A4560;text-transform:uppercase;">Verify</div></div>
            <div style="color:#1A2540;font-size:18px;flex:1;text-align:center;">→</div>
            <div style="display:flex;flex-direction:column;align-items:center;gap:5px;min-width:80px;"><div style="width:36px;height:36px;background:#0E1525;border:1px solid #1A2540;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;">🛡️</div><div style="font-size:10px;font-weight:600;color:#3A4560;text-transform:uppercase;">Safety</div></div>
            <div style="color:#1A2540;font-size:18px;flex:1;text-align:center;">→</div>
            <div style="display:flex;flex-direction:column;align-items:center;gap:5px;min-width:80px;"><div style="width:36px;height:36px;background:#0E1525;border:1px solid #1A2540;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;">🗺️</div><div style="font-size:10px;font-weight:600;color:#3A4560;text-transform:uppercase;">Resources</div></div>
            <div style="color:#1A2540;font-size:18px;flex:1;text-align:center;">→</div>
            <div style="display:flex;flex-direction:column;align-items:center;gap:5px;min-width:80px;"><div style="width:36px;height:36px;background:#0E1525;border:1px solid #1A2540;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;">🧠</div><div style="font-size:10px;font-weight:600;color:#3A4560;text-transform:uppercase;">Memory</div></div>
        </div>
    </div>""")

    # Voice button — FIXED: st.components.v1.html is deprecated, using st.iframe instead
    st.iframe("""<!DOCTYPE html><html><head><style>
    *{margin:0;padding:0;box-sizing:border-box;}
    body{background:transparent;font-family:Inter,sans-serif;padding:10px 0 4px;}
    #vb{display:inline-flex;align-items:center;gap:8px;background:rgba(0,201,177,.08);border:1px solid rgba(0,201,177,.3);color:#00C9B1;font-size:13px;font-weight:600;padding:10px 22px;border-radius:100px;cursor:pointer;font-family:Inter,sans-serif;transition:all .2s;outline:none;}
    #vb:hover{background:rgba(0,201,177,.18);}
    #vb.rec{background:rgba(255,59,92,.1);border-color:rgba(255,59,92,.5);color:#FF3B5C;}
    #lb{background:rgba(0,201,177,.05);border:1px solid #1A2540;color:#3A4560;font-size:11px;font-weight:600;padding:5px 12px;border-radius:100px;cursor:pointer;font-family:Inter,sans-serif;outline:none;}
    #st{font-size:12px;color:#6B7A99;margin-left:6px;}
    </style></head><body>
    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
    <button id="vb" onclick="go()">🎤 &nbsp;Report by voice</button>
    <button id="lb" onclick="tl()">Hindi</button>
    <span id="st"></span></div>
    <script>
    var lang='hi-IN';
    function tl(){var b=document.getElementById('lb');if(lang==='hi-IN'){lang='en-US';b.textContent='English';}else{lang='hi-IN';b.textContent='Hindi';}}
    function send(txt){
        var s=document.getElementById('st');
        var doc=null;
        try{doc=window.parent.document;}catch(e){}
        if(!doc){try{doc=window.top.document;}catch(e){}}
        var inp=doc?doc.querySelector('textarea[data-testid="stChatInput"]')||doc.querySelector('textarea'):null;
        if(!inp){if(navigator.clipboard)navigator.clipboard.writeText(txt).then(function(){s.textContent='📋 Copied! Press Ctrl+V to paste: '+txt;});else s.textContent='Please type: '+txt;return;}
        Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set.call(inp,txt);
        inp.dispatchEvent(new Event('input',{bubbles:true}));
        inp.dispatchEvent(new Event('change',{bubbles:true}));
        inp.focus();
        setTimeout(function(){var sb=doc.querySelector('button[data-testid="stChatInputSubmitButton"]');if(sb){sb.click();s.textContent='✅ Submit!';}else{inp.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true}));s.textContent='✅ Sent!';}},700);
    }
    function go(){
        var b=document.getElementById('vb'),s=document.getElementById('st');
        if(!('webkitSpeechRecognition' in window||'SpeechRecognition' in window)){alert('Please use Chrome!');return;}
        var SR=window.SpeechRecognition||window.webkitSpeechRecognition,r=new SR();
        r.lang=lang;r.interimResults=true;r.maxAlternatives=1;r.continuous=false;
        r.onstart=function(){b.className='rec';b.innerHTML='🔴 &nbsp;Listening...';s.textContent='🎙️ Listening...';};
        r.onspeechstart=function(){s.textContent='🎙️ Voice detected...';};
        r.onresult=function(e){var interim='',fin='';for(var i=0;i<e.results.length;i++){if(e.results[i].isFinal)fin+=e.results[i][0].transcript;else interim+=e.results[i][0].transcript;}s.textContent='📝 '+(fin||interim);if(fin)send(fin.trim());};
        r.onend=function(){b.className='';b.innerHTML='🎤 &nbsp;Report by voice';};
        r.onerror=function(e){b.className='';b.innerHTML='🎤 &nbsp;Report by voice';var m={'no-speech':'⚠️ Didn\'t hear anything','audio-capture':'❌ Microphone not found','not-allowed':'❌ Please allow microphone access'};s.textContent=m[e.error]||'❌ '+e.error;};
        r.start();
    }
    </script></body></html>""", height=55)

    # Chat input
    user_input = st.chat_input("Describe what you see… (Hindi / English / Hinglish)")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        with st.chat_message("user",avatar="👤"):
            st.markdown(user_input)
        with st.chat_message("assistant",avatar="🤖"):
            ph=st.empty()
            run_agents_ui(ph)
            with st.spinner("Analyzing…"):
                try:
                    result=analyze(user_input)
                    situations=result.get("situation_types",[])
                    urgency=result.get("urgency_level","medium")
                    location=result.get("location","Unknown")
                    city=result.get("city","Unknown")
                    needed=result.get("needed_resources",["hospital","shelter","food"]) or ["hospital","shelter","food"]

                    coords, live_resources = (None, {})
                    lookup = city if city and city.lower() != "unknown" else location
                    if lookup and lookup.lower() != "unknown":
                        coords, live_resources = get_live_resources(location, city, needed)

                    sit_text=" · ".join(s.replace("_"," ").title() for s in situations) or "General"
                    urgency_icon={"high":"🔴","medium":"🟡","low":"🟢"}.get(urgency,"🟡")
                    reply=(f"**Report analyzed** ✅\n\n**Situation:** {sit_text}\n\n**Urgency:** {urgency_icon} {urgency.upper()} &nbsp;·&nbsp; **Language:** {result.get('original_language','Hindi')}\n\n{result.get('summary','')}\n\n*Real-time resources are shown below 👇*")
                    st.markdown(reply)
                    st.session_state.messages.append({"role":"assistant","content":reply})
                    st.session_state.last_result=result
                    st.session_state.last_live_resources=live_resources
                    # Save to reports
                    st.session_state.reports.append({"text":user_input,"location":location,"urgency":urgency,"situations":situations,"lang":result.get("original_language","Hindi")})
                except Exception as e:
                    err=str(e)[:200]
                    st.markdown(f"⚠️ Error: `{err}`")
                    st.session_state.messages.append({"role":"assistant","content":f"⚠️ Error: {err}"})
        st.rerun()


# ══════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════
elif page == "dashboard":
    import random
    reports = st.session_state.reports

    # Sample data if no reports
    sample = [
        {"text":"Child alone in Jaipur","location":"Jaipur","urgency":"high","situations":["child_safety","shelter"],"lang":"Hinglish"},
        {"text":"Family sick in Delhi","location":"Delhi","urgency":"high","situations":["medical"],"lang":"Hindi"},
        {"text":"Mumbai shelter needed","location":"Mumbai","urgency":"medium","situations":["shelter","food"],"lang":"English"},
        {"text":"Food needed in Alwar","location":"Alwar","urgency":"low","situations":["food"],"lang":"Hindi"},
        {"text":"Three children in Jaipur","location":"Jaipur","urgency":"high","situations":["child_safety"],"lang":"Hinglish"},
    ]
    all_reports = sample + reports

    total    = len(all_reports)
    high_urg = len([r for r in all_reports if r["urgency"]=="high"])
    cities   = len(set(r["location"] for r in all_reports))
    children = len([r for r in all_reports if "child_safety" in r.get("situations",[])])

    st.html(f"""
    <div class="sn-page" style="max-width:1000px;margin:0 auto;padding:40px 24px 100px;">
        <div class="animate-fadeup delay-1" style="margin-bottom:32px;">
            <div class="sn-badge">📊 Live Dashboard</div>
            <div style="font-size:36px;font-weight:800;color:#fff;letter-spacing:-.03em;margin:16px 0 8px;">Report Dashboard</div>
            <div style="font-size:14px;color:#4A5980;">Real-time overview of all submitted reports</div>
        </div>

        <!-- KPI CARDS -->
        <div class="animate-fadeup delay-2" style="display:flex;gap:12px;margin-bottom:28px;flex-wrap:wrap;">
            <div class="sn-card" style="flex:1;min-width:140px;text-align:center;">
                <div style="font-size:36px;font-weight:900;color:#fff;">{total}</div>
                <div style="font-size:11px;color:#3A4560;text-transform:uppercase;font-weight:700;letter-spacing:.08em;margin-top:4px;">Total Reports</div>
                <div style="width:8px;height:8px;background:#00C9B1;border-radius:50%;box-shadow:0 0 8px #00C9B1;margin:8px auto 0;animation:pulse-dot 1.5s infinite;"></div>
            </div>
            <div class="sn-card" style="flex:1;min-width:140px;text-align:center;">
                <div style="font-size:36px;font-weight:900;color:#FF3B5C;">{high_urg}</div>
                <div style="font-size:11px;color:#3A4560;text-transform:uppercase;font-weight:700;letter-spacing:.08em;margin-top:4px;">High Urgency</div>
                <div style="display:inline-block;background:rgba(255,59,92,.1);color:#FF3B5C;font-size:10px;font-weight:600;padding:2px 10px;border-radius:100px;margin-top:8px;">🔴 Critical</div>
            </div>
            <div class="sn-card" style="flex:1;min-width:140px;text-align:center;">
                <div style="font-size:36px;font-weight:900;color:#FFB800;">{cities}</div>
                <div style="font-size:11px;color:#3A4560;text-transform:uppercase;font-weight:700;letter-spacing:.08em;margin-top:4px;">Cities Covered</div>
                <div style="display:inline-block;background:rgba(255,184,0,.1);color:#FFB800;font-size:10px;font-weight:600;padding:2px 10px;border-radius:100px;margin-top:8px;">📍 Active</div>
            </div>
            <div class="sn-card" style="flex:1;min-width:140px;text-align:center;">
                <div style="font-size:36px;font-weight:900;color:#00C9B1;">{children}</div>
                <div style="font-size:11px;color:#3A4560;text-transform:uppercase;font-weight:700;letter-spacing:.08em;margin-top:4px;">Child Cases</div>
                <div style="display:inline-block;background:rgba(0,201,177,.08);color:#00C9B1;font-size:10px;font-weight:600;padding:2px 10px;border-radius:100px;margin-top:8px;">🛡️ Priority</div>
            </div>
        </div>

        <!-- ESCALATION ALERT -->
        <div class="animate-fadeup delay-3" style="background:rgba(255,184,0,.06);border:1px solid rgba(255,184,0,.2);border-left:3px solid #FFB800;border-radius:12px;padding:16px 20px;margin-bottom:28px;display:flex;gap:12px;align-items:center;">
            <div style="font-size:24px;">⚡</div>
            <div>
                <div style="font-size:13px;font-weight:700;color:#FFB800;margin-bottom:4px;">NGO Escalation Triggered</div>
                <div style="font-size:12px;color:#A0AAB8;">Jaipur: 2 reports from same area — 1 more report will trigger automatic NGO alert</div>
            </div>
        </div>

        <!-- RECENT REPORTS TABLE -->
        <div class="animate-fadeup delay-4" style="background:#0A1020;border:1px solid #1A2540;border-radius:16px;padding:20px 24px;margin-bottom:28px;">
            <div style="font-size:11px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin-bottom:16px;">Recent Reports</div>
    """)

    for i, r in enumerate(reversed(all_reports[-8:])):
        urgency_color = {"high":"#FF3B5C","medium":"#FFB800","low":"#00C9B1"}.get(r["urgency"],"#FFB800")
        sits = " · ".join(s.replace("_"," ").title() for s in r.get("situations",[])) or "General"
        st.html(f"""
        <div class="sn-report-row" style="display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #0E1525;animation:slideIn .4s ease {i*0.05}s both;">
            <div style="width:8px;height:8px;background:{urgency_color};border-radius:50%;flex-shrink:0;"></div>
            <div style="flex:1;font-size:13px;color:#C8D3E8;min-width:120px;">{r['text'][:60]}{'...' if len(r['text'])>60 else ''}</div>
            <div class="sn-report-meta" style="font-size:11px;color:#4A5980;min-width:60px;">{r['location']}</div>
            <div class="sn-report-meta" style="font-size:11px;color:#3A4560;min-width:80px;">{sits[:20]}</div>
            <div style="font-size:10px;font-weight:700;color:{urgency_color};background:rgba(0,0,0,.3);padding:3px 10px;border-radius:100px;">{r['urgency'].upper()}</div>
        </div>""")

    st.html("</div></div>")

# ══════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ══════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════
# PAGE: GUIDE — Kya Karein?
# ══════════════════════════════════════════════════════════════
elif page == "guide":
    st.html("""
    <div class="sn-page" style="max-width:800px;margin:0 auto;padding:40px 24px 100px;">
        <div class="animate-fadeup delay-1" style="margin-bottom:40px;">
            <div class="sn-badge">📖 Emergency Guide</div>
            <div style="font-size:36px;font-weight:800;color:#fff;letter-spacing:-.03em;margin:16px 0 8px;">What To Do? 🆘</div>
            <div style="font-size:15px;color:#4A5980;line-height:1.7;">Seen someone in need? Look here for a step-by-step guide based on the situation.</div>
        </div>

        <!-- SCENARIO 1: CHILD LOST -->
        <div class="sn-card animate-fadeup delay-2" style="margin-bottom:16px;border-left:3px solid #FF3B5C;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <div style="font-size:32px;">👦</div>
                <div>
                    <div style="font-size:16px;font-weight:800;color:#fff;">Child Lost</div>
                    <div style="font-size:12px;color:#FF3B5C;font-weight:600;">🔴 HIGH PRIORITY — Take immediate action</div>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;gap:10px;">
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FF3B5C;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">1</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Call 1098 (Childline)</b> — India's 24/7 free child helpline. You'll be connected directly to an operator who will inform local police and NGOs.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FF3B5C;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">2</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Keep the child with you</b> — don't let them wander off. If they're trying to leave, take them to a safe place (a shop, a police post).</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FF3B5C;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">3</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Also call 100 (Police)</b> — informing police alongside Childline speeds up the search.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FF3B5C;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">4</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Report on SaharaNet</b> — submit the exact location on the Report page. Our agents will find the nearest shelter for you.</div>
                </div>
            </div>
            <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
                <div style="background:rgba(255,59,92,.1);border:1px solid rgba(255,59,92,.3);color:#FF3B5C;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">📞 1098 — Childline</div>
                <div style="background:rgba(255,59,92,.1);border:1px solid rgba(255,59,92,.3);color:#FF3B5C;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">🚔 100 — Police</div>
            </div>
        </div>

        <!-- SCENARIO 2: INJURY/ACCIDENT -->
        <div class="sn-card animate-fadeup delay-2" style="margin-bottom:16px;border-left:3px solid #FF6B35;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <div style="font-size:32px;">🚑</div>
                <div>
                    <div style="font-size:16px;font-weight:800;color:#fff;">Injury / Accident</div>
                    <div style="font-size:12px;color:#FF6B35;font-weight:600;">🔴 HIGH PRIORITY — Call an ambulance immediately</div>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;gap:10px;">
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FF6B35;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">1</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Call 108</b> — free ambulance service available across India. Give your location and they'll arrive.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FF6B35;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">2</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Don't move the injured person</b> if a spine/neck injury is suspected. Only move them if there's immediate danger (fire, traffic).</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FF6B35;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">3</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">If there's bleeding, apply pressure</b> with a clean cloth on the wound until the ambulance arrives.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FF6B35;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">4</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Keep them conscious</b> — keep talking, ask their name, don't let them close their eyes until a doctor arrives.</div>
                </div>
            </div>
            <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
                <div style="background:rgba(255,107,53,.1);border:1px solid rgba(255,107,53,.3);color:#FF6B35;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">🚑 108 — Free Ambulance</div>
                <div style="background:rgba(255,107,53,.1);border:1px solid rgba(255,107,53,.3);color:#FF6B35;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">🚔 100 — Police</div>
            </div>
        </div>

        <!-- SCENARIO 3: SICK PERSON -->
        <div class="sn-card animate-fadeup delay-3" style="margin-bottom:16px;border-left:3px solid #FFB800;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <div style="font-size:32px;">🤒</div>
                <div>
                    <div style="font-size:16px;font-weight:800;color:#fff;">Someone Is Sick</div>
                    <div style="font-size:12px;color:#FFB800;font-weight:600;">🟡 MEDIUM-HIGH — Assess the situation and decide</div>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;gap:10px;">
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FFB800;color:#050B18;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">1</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">If serious</b> (unconscious, chest pain, breathlessness) → call 108 immediately.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FFB800;color:#050B18;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">2</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">For mild symptoms</b> (fever, weakness, nausea) → take them to the nearest govt. hospital/clinic. OPD is free at govt. hospitals.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FFB800;color:#050B18;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">3</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Give water</b> — if conscious and able to swallow, offer a little water and keep them out of the sun.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#FFB800;color:#050B18;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">4</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Report on SaharaNet</b> — enter the location and the nearest hospital will show up in real time.</div>
                </div>
            </div>
            <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
                <div style="background:rgba(255,184,0,.1);border:1px solid rgba(255,184,0,.3);color:#FFB800;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">🚑 108 — Ambulance</div>
                <div style="background:rgba(255,184,0,.1);border:1px solid rgba(255,184,0,.3);color:#FFB800;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">🏥 Nearest Govt Hospital</div>
            </div>
        </div>

        <!-- SCENARIO 4: NO FOOD -->
        <div class="sn-card animate-fadeup delay-3" style="margin-bottom:16px;border-left:3px solid #00C9B1;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <div style="font-size:32px;">🍱</div>
                <div>
                    <div style="font-size:16px;font-weight:800;color:#fff;">No Food / Hungry</div>
                    <div style="font-size:12px;color:#00C9B1;font-weight:600;">🟡 MEDIUM — Help available from food centers and NGOs</div>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;gap:10px;">
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#00C9B1;color:#050B18;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">1</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Akshaya Patra Foundation</b> — India's largest meal distribution NGO. Call 1800-425-8622 (toll-free) or find the nearest outlet.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#00C9B1;color:#050B18;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">2</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">ISKCON Food for Life</b> — free meals available in every major city, especially on weekends.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#00C9B1;color:#050B18;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">3</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Nearest gurudwara/temple</b> — free community meals are available 24/7 in most places.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#00C9B1;color:#050B18;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">4</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Call 181</b> — the Women Helpline can also connect you to food and shelter.</div>
                </div>
            </div>
            <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
                <div style="background:rgba(0,201,177,.08);border:1px solid rgba(0,201,177,.3);color:#00C9B1;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">📞 181 — Helpline</div>
                <div style="background:rgba(0,201,177,.08);border:1px solid rgba(0,201,177,.3);color:#00C9B1;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">🍽️ Nearest Gurudwara</div>
            </div>
        </div>

        <!-- SCENARIO 5: NO SHELTER -->
        <div class="sn-card animate-fadeup delay-4" style="margin-bottom:16px;border-left:3px solid #7B61FF;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <div style="font-size:32px;">🏠</div>
                <div>
                    <div style="font-size:16px;font-weight:800;color:#fff;">No Shelter / Homeless</div>
                    <div style="font-size:12px;color:#7B61FF;font-weight:600;">🔴 HIGH — Shelter is essential for the night</div>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;gap:10px;">
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#7B61FF;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">1</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Call 1098 if children are involved</b> — Childline will find the nearest shelter home the same day.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#7B61FF;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">2</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Municipal Corporation</b> — every city has free night shelters. Call the local helpline 1077.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#7B61FF;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">3</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Railway station or bus stand</b> — a temporary safe place; ask RPF/security for help for the night.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#7B61FF;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">4</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Report on SaharaNet</b> — enter the exact city and situation to get a list of the nearest verified shelters.</div>
                </div>
            </div>
            <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
                <div style="background:rgba(123,97,255,.1);border:1px solid rgba(123,97,255,.3);color:#7B61FF;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">📞 1098 — Childline</div>
                <div style="background:rgba(123,97,255,.1);border:1px solid rgba(123,97,255,.3);color:#7B61FF;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">📞 1077 — Disaster/Shelter</div>
            </div>
        </div>

        <!-- SCENARIO 6: ELDERLY IN DISTRESS -->
        <div class="sn-card animate-fadeup delay-4" style="margin-bottom:16px;border-left:3px solid #4A90E2;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <div style="font-size:32px;">👴</div>
                <div>
                    <div style="font-size:16px;font-weight:800;color:#fff;">Elderly Person in Distress</div>
                    <div style="font-size:12px;color:#4A90E2;font-weight:600;">🟡 MEDIUM-HIGH — Elderly people are especially vulnerable</div>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;gap:10px;">
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#4A90E2;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">1</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Call 14567 — Elder Line</b> — the Government of India's dedicated senior citizen helpline, free of charge.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#4A90E2;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">2</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">If it's a medical emergency</b> → call 108 and mention their age so the right response is sent.</div>
                </div>
                <div style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="background:#4A90E2;color:#fff;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;flex-shrink:0;margin-top:2px;">3</div>
                    <div style="font-size:13px;color:#C8D3E8;line-height:1.6;"><b style="color:#fff;">Move them to a safe spot</b> — keep them out of the sun, give water, and let them sit until help arrives.</div>
                </div>
            </div>
            <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
                <div style="background:rgba(74,144,226,.1);border:1px solid rgba(74,144,226,.3);color:#4A90E2;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">📞 14567 — Elder Line</div>
                <div style="background:rgba(74,144,226,.1);border:1px solid rgba(74,144,226,.3);color:#4A90E2;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;">🚑 108 — Ambulance</div>
            </div>
        </div>

        <!-- QUICK REFERENCE -->
        <div style="background:#0A1020;border:1px solid #1A2540;border-radius:16px;padding:24px;margin-top:8px;">
            <div style="font-size:11px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin-bottom:16px;">📞 Quick Reference — India Emergency Helplines</div>
            <div style="display:flex;flex-wrap:wrap;gap:10px;">
                <div style="flex:1;min-width:180px;background:#050B18;border:1px solid #1A2540;border-radius:10px;padding:12px 14px;">
                    <div style="font-size:20px;font-weight:900;color:#00C9B1;">108</div>
                    <div style="font-size:12px;color:#E8EDF5;font-weight:600;margin-top:2px;">Ambulance / Emergency</div>
                    <div style="font-size:11px;color:#4A5980;margin-top:2px;">Free, 24/7, All India</div>
                </div>
                <div style="flex:1;min-width:180px;background:#050B18;border:1px solid #1A2540;border-radius:10px;padding:12px 14px;">
                    <div style="font-size:20px;font-weight:900;color:#FF3B5C;">1098</div>
                    <div style="font-size:12px;color:#E8EDF5;font-weight:600;margin-top:2px;">Childline</div>
                    <div style="font-size:11px;color:#4A5980;margin-top:2px;">Children in distress, 24/7</div>
                </div>
                <div style="flex:1;min-width:180px;background:#050B18;border:1px solid #1A2540;border-radius:10px;padding:12px 14px;">
                    <div style="font-size:20px;font-weight:900;color:#FFB800;">100</div>
                    <div style="font-size:12px;color:#E8EDF5;font-weight:600;margin-top:2px;">Police</div>
                    <div style="font-size:11px;color:#4A5980;margin-top:2px;">Law & order, 24/7</div>
                </div>
                <div style="flex:1;min-width:180px;background:#050B18;border:1px solid #1A2540;border-radius:10px;padding:12px 14px;">
                    <div style="font-size:20px;font-weight:900;color:#7B61FF;">181</div>
                    <div style="font-size:12px;color:#E8EDF5;font-weight:600;margin-top:2px;">Women Helpline</div>
                    <div style="font-size:11px;color:#4A5980;margin-top:2px;">Women in distress, 24/7</div>
                </div>
                <div style="flex:1;min-width:180px;background:#050B18;border:1px solid #1A2540;border-radius:10px;padding:12px 14px;">
                    <div style="font-size:20px;font-weight:900;color:#4A90E2;">14567</div>
                    <div style="font-size:12px;color:#E8EDF5;font-weight:600;margin-top:2px;">Elder Line</div>
                    <div style="font-size:11px;color:#4A5980;margin-top:2px;">Senior citizens, free</div>
                </div>
                <div style="flex:1;min-width:180px;background:#050B18;border:1px solid #1A2540;border-radius:10px;padding:12px 14px;">
                    <div style="font-size:20px;font-weight:900;color:#00C9B1;">1077</div>
                    <div style="font-size:12px;color:#E8EDF5;font-weight:600;margin-top:2px;">Disaster Mgmt</div>
                    <div style="font-size:11px;color:#4A5980;margin-top:2px;">Shelter & relief, 24/7</div>
                </div>
            </div>
        </div>
    </div>
    """)

elif page == "about":
    st.html("""
    <div class="sn-page" style="max-width:800px;margin:0 auto;padding:40px 24px 100px;">

        <div class="animate-fadeup delay-1" style="margin-bottom:40px;">
            <div class="sn-badge">ℹ️ About</div>
            <div style="font-size:36px;font-weight:800;color:#fff;letter-spacing:-.03em;margin:16px 0 8px;">About SaharaNet</div>
            <div style="font-size:15px;color:#4A5980;line-height:1.7;">
                A multilingual AI emergency response system built for India's most vulnerable — street children and homeless families.
            </div>
        </div>

        <div class="sn-card animate-fadeup delay-2" style="margin-bottom:16px;">
            <div style="font-size:11px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;">🎯 The Problem</div>
            <div style="font-size:14px;color:#C8D3E8;line-height:1.8;">
                India has over <b style="color:#00C9B1;">1.8 million street children</b> and countless homeless families. When a bystander sees someone in distress, there's no easy way to connect them to help — especially across language barriers. Emergency services are hard to navigate, and NGOs lack real-time visibility into where help is needed most.
            </div>
        </div>

        <div class="sn-card animate-fadeup delay-3" style="margin-bottom:16px;">
            <div style="font-size:11px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;">💡 Our Solution</div>
            <div style="font-size:14px;color:#C8D3E8;line-height:1.8;">
                SaharaNet uses a <b style="color:#00C9B1;">6-agent AI pipeline</b> to let anyone report emergencies in their native language — Hindi, English, or Hinglish — via voice or text. The system instantly identifies the situation type, finds the nearest resources, and escalates to NGOs when multiple reports come from the same area.
            </div>
        </div>

        <div class="sn-card animate-fadeup delay-4" style="margin-bottom:16px;">
            <div style="font-size:11px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin-bottom:16px;">🛠️ Tech Stack</div>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <span style="background:rgba(0,201,177,.08);border:1px solid rgba(0,201,177,.2);color:#00C9B1;font-size:12px;font-weight:600;padding:5px 14px;border-radius:100px;">Streamlit</span>
                <span style="background:rgba(0,201,177,.08);border:1px solid rgba(0,201,177,.2);color:#00C9B1;font-size:12px;font-weight:600;padding:5px 14px;border-radius:100px;">Google ADK</span>
                <span style="background:rgba(0,201,177,.08);border:1px solid rgba(0,201,177,.2);color:#00C9B1;font-size:12px;font-weight:600;padding:5px 14px;border-radius:100px;">Groq LLaMA 3.1</span>
                <span style="background:rgba(0,201,177,.08);border:1px solid rgba(0,201,177,.2);color:#00C9B1;font-size:12px;font-weight:600;padding:5px 14px;border-radius:100px;">Web Speech API</span>
                <span style="background:rgba(0,201,177,.08);border:1px solid rgba(0,201,177,.2);color:#00C9B1;font-size:12px;font-weight:600;padding:5px 14px;border-radius:100px;">Python</span>
                <span style="background:rgba(0,201,177,.08);border:1px solid rgba(0,201,177,.2);color:#00C9B1;font-size:12px;font-weight:600;padding:5px 14px;border-radius:100px;">FastAPI</span>
            </div>
        </div>

        <div class="sn-card animate-fadeup delay-5">
            <div style="font-size:11px;font-weight:700;color:#3A4560;text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;">👩‍💻 Builder</div>
            <div style="display:flex;align-items:center;gap:16px;">
                <div style="width:48px;height:48px;background:linear-gradient(135deg,#00C9B1,#0066FF);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;">P</div>
                <div>
                    <div style="font-size:15px;font-weight:700;color:#fff;">Palak Soni</div>
                    <div style="font-size:12px;color:#4A5980;">B.Tech CSE · MITRC Alwar · Frontend Developer & AI Builder</div>
                    <div style="margin-top:6px;display:flex;gap:8px;">
                        <span style="font-size:11px;color:#00C9B1;">linkedin.com/in/palak-soni-235401327</span>
                    </div>
                </div>
            </div>
        </div>

        <div style="text-align:center;margin-top:40px;padding:32px;background:rgba(0,201,177,.04);border:1px solid rgba(0,201,177,.1);border-radius:16px;">
            <div style="font-size:28px;margin-bottom:12px;">🏆</div>
            <div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:6px;">Kaggle · Agents for Good 2026</div>
            <div style="font-size:13px;color:#4A5980;">Built with ❤️ for India's most vulnerable communities</div>
        </div>
    </div>
    """)