import streamlit as st
from datetime import date

st.set_page_config(
    page_title="DSL JMP Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state ─────────────────────────────────────────────────────────────
def _def(key, val):
    if key not in st.session_state:
        st.session_state[key] = val

_def("page",          "Build my JMP")
_def("build_step",    1)
_def("param_tab",     "🗓️ Simulation")

_def("sim_results",  None)
_def("sim_error",    None)
_def("sim_seed_used", 42)
_def("mc_results",   None)
_def("roving_vessels", [
    {"name":"Laphroaig",  "true_cap":250000, "enabled":True},
    {"name":"MT Watson",  "true_cap":250000, "enabled":True},
    {"name":"Sherlock",   "true_cap":250000, "enabled":True},
    {"name":"Balham",     "true_cap":150000, "enabled":True},
    {"name":"Bedford",    "true_cap":150000, "enabled":False},
    {"name":"MT Berners", "true_cap":250000, "enabled":False},
    {"name":"Bagshot",    "true_cap":120000, "enabled":False},
    {"name":"Woodstock",  "true_cap":90000,  "enabled":False},
    {"name":"Rathbone",   "true_cap":80000,  "enabled":False},
])
_def("sts_start",    date(2026, 4, 1))
_def("sim_start",        date(2026, 3, 9))
_def("sim_end",          date(2026, 6, 30))
_def("start_inj_no",     138)
_def("pause_days",       3)
_def("whisky_trigger",   83000)
_def("sanjulian_cap",    450000)
_def("alk_stop",         date(2026, 3, 31))
_def("sanjulian_start",  date(2026, 4, 1))
_def("prescribed_end",   date(2026, 3, 12))
_def("whisky_win_start", date(2026, 3, 11))
_def("whisky_win_end",   date(2026, 6, 30))

_def("mother_vessels", [
    {"name":"Bryanston",   "cap":490000,"hard":560000,"stock":65017,  "retire":None},
    {"name":"Alkebulan",   "cap":440000,"hard":730000,"stock":0,      "retire":date(2026,3,31)},
    {"name":"Green Eagle", "cap":440000,"hard":730000,"stock":356672, "retire":None},
])

_def("shuttle_vessels", [
    {"name":"Bagshot",         "cap":45050, "lead":1,"start":date(2026,3,9), "active":True,"allowed":["Jasmine S_SOKU","Chapel_OML24","Westmore_Belema","Awoba_OML24"]},
    {"name":"Woodstock",       "cap":42024, "lead":1,"start":date(2026,3,9), "active":True,"allowed":["Chapel_OML24","Jasmine S_SOKU","Awoba_OML24"]},
    {"name":"Rathbone",        "cap":45005, "lead":1,"start":date(2026,3,5), "active":True,"allowed":["Dawes Island","Jasmine S_SOKU","Westmore_Belema","Soku Gas Plant","Chapel_OML24","Awoba_OML24"]},
    {"name":"Balham",          "cap":66446, "lead":1,"start":date(2026,3,9), "active":True,"allowed":["Jasmine S_SOKU","Chapel_OML24"]},
    {"name":"Laphroaig",       "cap":90751, "lead":1,"start":date(2026,3,9), "active":True,"allowed":["Jasmine S_SOKU","Westmore_Belema","Chapel_OML24"]},
    {"name":"Sherlock",        "cap":89287, "lead":1,"start":date(2026,3,15),"active":True,"allowed":["Chapel_OML24","Westmore_Belema","Jasmine S_SOKU"]},
    {"name":"Bedford",         "cap":65317, "lead":1,"start":date(2026,3,5), "active":True,"allowed":["Jasmine S_SOKU","Chapel_OML24"]},
    {"name":"MT Watson",       "cap":91056, "lead":1,"start":date(2026,3,4), "active":True,"allowed":["Chapel_OML24","Jasmine S_SOKU","Westmore_Belema"]},
    {"name":"MT Santa Monica", "cap":12000, "lead":1,"start":date(2026,4,12),"active":True,"allowed":["Dawes Island","Awoba_OML24","Soku Gas Plant","Chapel_OML24"]},
])

_def("storage_vessels", [
    {"name":"Chapel_OML24",     "stock":410040,"min_thr":70000, "cap":270000,"load_time":1.0, "start":date(2026,3,9)},
    {"name":"Jasmine S_SOKU",   "stock":233725,"min_thr":70000, "cap":270000,"load_time":1.0, "start":date(2026,3,9)},
    {"name":"Awoba_OML24",      "stock":85927, "min_thr":45000, "cap":270000,"load_time":2.0, "start":date(2026,3,9)},
    {"name":"Westmore_Belema",  "stock":277644,"min_thr":70000, "cap":270000,"load_time":1.0, "start":date(2026,2,25)},
    {"name":"Whisky Star XLV",  "stock":19002, "min_thr":80000, "cap":98000, "load_time":23.0,"start":date(2026,3,9)},
    {"name":"Dawes Island",     "stock":41946, "min_thr":35000, "cap":75000, "load_time":1.0, "start":date(2026,3,9)},
    {"name":"Soku Gas Plant",   "stock":0,     "min_thr":10000, "cap":75000, "load_time":2.0, "start":date(2026,1,1)},
    {"name":"Barge Starturn",   "stock":34678, "min_thr":45000, "cap":270000,"load_time":3.0, "start":date(2026,3,9)},
    {"name":"Asaramatoru",      "stock":8831,  "min_thr":10000, "cap":30000, "load_time":1.0, "start":date(2026,2,15)},
    {"name":"MT Sanbarth_OML24","stock":0,     "min_thr":70000, "cap":270000,"load_time":1.0, "start":date(2026,2,15)},
    {"name":"Chapel_SOKU",      "stock":0,     "min_thr":70000, "cap":270000,"load_time":1.0, "start":date(2026,5,15)},
])

_def("manual_events", [
    {"date":date(2026,3,12),"shuttle":"MT Watson","storage":"Chapel_OML24","volume":85629},
])

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
#MainMenu,footer,header{visibility:hidden;height:0;min-height:0;}
/* Hide the real Streamlit buttons used by HTML toggles */
div.hide-btn{visibility:hidden!important;height:0!important;overflow:hidden!important;
             position:absolute!important;width:0!important;pointer-events:none!important;}
div.hide-btn *{height:0!important;min-height:0!important;padding:0!important;margin:0!important;}
[data-testid="stMarkdownContainer"] button{pointer-events:auto!important;cursor:pointer!important;z-index:10!important;}
/* Hide Streamlit top toolbar and decoration completely */
[data-testid="stToolbar"]{display:none!important;}
[data-testid="stDecoration"]{display:none!important;}
[data-testid="stHeader"]{display:none!important;height:0!important;min-height:0!important;}
[data-testid="stStatusWidget"]{display:none!important;}
iframe[title="st_connection_status.iframe"]{display:none!important;}
div[class*="StatusWidget"]{display:none!important;}
header[data-testid="stHeader"]{display:none!important;height:0!important;min-height:0!important;}
/* Kill every possible top spacing source */
[data-testid="stAppViewContainer"]{margin-top:0!important;padding-top:0!important;}
[data-testid="stSidebar"] ~ section{margin-top:0!important;padding-top:0!important;}
.main .block-container{margin-top:0!important;}
div[class^="appview"]{padding-top:0!important;}
.block-container{padding:0 1.5rem 1rem!important;max-width:100%!important;}
/* Remove Streamlit's default large top gap on deployed apps */
div[data-testid="stMainBlockContainer"]{padding-top:0!important;margin-top:0!important;}
div[data-testid="stAppViewBlockContainer"]{padding-top:0!important;margin-top:0!important;}
div[data-testid="block-container"]{padding-top:0!important;margin-top:0!important;}
section.main > div:first-child{padding-top:0!important;margin-top:0!important;}
section.main .block-container{padding-top:0!important;margin-top:0!important;}
section.main{padding-top:0!important;}
.appview-container .main .block-container{padding-top:0!important;}
div[data-testid="stVerticalBlock"]{gap:0.75rem!important;}
div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="stMarkdownContainer"]:empty{display:none;}

/* ── Main area background ── */
[data-testid="stAppViewContainer"]>section.main,
[data-testid="stAppViewBlockContainer"],
[data-testid="stMainBlockContainer"] { background-color:#f4f6fb!important; }

/* ── Sidebar: use Streamlit native, style with CSS ── */
[data-testid="stSidebarCollapseButton"] {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 50% !important;
    width: 28px !important;
    height: 28px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12) !important;
    color: #374151 !important;
}
[data-testid="stSidebarCollapseButton"]:hover {
    border-color: #1a3fc4 !important;
    color: #1a3fc4 !important;
    background: #eef2ff !important;
}
[data-testid="stSidebarCollapseButton"] svg { stroke: #374151 !important; }
[data-testid="stSidebarCollapseButton"]:hover svg { stroke: #1a3fc4 !important; }
[data-testid="collapsedControl"] {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 50% !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12) !important;
}
[data-testid="collapsedControl"] svg { stroke: #374151 !important; }

section[data-testid="stSidebar"] {
    background: linear-gradient(165deg,#0a1a6e 0%,#16042e 55%,#6b0a1a 100%) !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"]>div:first-child { padding:0!important; }
[data-testid="stSidebarContent"] { padding:0!important; }

/* every wrapper inside sidebar: transparent */
section[data-testid="stSidebar"] [data-testid="stSidebarContent"]>div,
section[data-testid="stSidebar"] [data-testid="stSidebarContent"]>div>div,
section[data-testid="stSidebar"] [data-testid="stSidebarContent"]>div>div>div {
    background: transparent !important;
}

/* nav buttons inside sidebar */
section[data-testid="stSidebar"] .stButton>button {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    color: rgba(255,255,255,0.65) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 9px 13px !important;
    width: 100% !important;
    text-align: left !important;
    box-shadow: none !important;
    transition: all 0.15s !important;
}
section[data-testid="stSidebar"] .stButton>button:hover {
    background: rgba(255,255,255,0.09) !important;
    color: #ffffff !important;
}
section[data-testid="stSidebar"] .nav-active .stButton>button {
    background: rgba(255,255,255,0.13) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-left: 3px solid #e84545 !important;
    padding-left: 10px !important;
}

/* ── Main area buttons ── */
.stButton>button {
    background: #ffffff !important;
    border: 1.5px solid #c8d3ee !important;
    border-radius: 9px !important;
    color: #1a3fc4 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
}
.stButton>button:hover {
    background: #1a3fc4 !important;
    color: #ffffff !important;
    border-color: #1a3fc4 !important;
}
.stButton>button:focus { box-shadow: none !important; }

/* Inactive segment */
.tab-inactive-wrap .stButton>button {
    background: transparent !important;
    color: #6b7a99 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    box-shadow: none !important;
    padding: 8px 14px !important;
}
.tab-inactive-wrap .stButton>button:hover {
    background: rgba(26,63,196,0.1) !important;
    color: #1a3fc4 !important;
}
/* Hide the real Streamlit buttons used as onclick targets */
.tab-active-wrap .stButton>button,
.tab-inactive-wrap .stButton>button {
    display: none !important;
}
/* Active segment */
.tab-active-wrap .stButton>button {
    background: #1a3fc4 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    box-shadow: 0 1px 6px rgba(26,63,196,0.28) !important;
    padding: 8px 14px !important;
}

/* add/remove/step-nav/run buttons */
.add-btn .stButton>button { border: 1.5px solid #1a3fc4 !important; }
.rm-btn .stButton>button  { background:#fff0f0!important;color:#e84545!important;border:1.5px solid #fecaca!important;width:auto!important; }
.rm-btn .stButton>button:hover { background:#e84545!important;color:#fff!important; }
.step-nav .stButton>button { border: 1.5px solid #1a3fc4 !important; }
.run-btn .stButton>button  {
    background: linear-gradient(90deg,#1a3fc4,#e84545) !important;
    color: #fff !important; font-weight: 700 !important; font-size: 14px !important;
    border-radius: 11px !important; border: none !important;
    box-shadow: 0 4px 18px rgba(26,63,196,0.3) !important;
}

/* inputs */
[data-testid="stDateInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    border-radius: 8px !important;
    border: 1.5px solid #c8d3ee !important;
    font-size: 12.5px !important;
    color: #0d1b6e !important;
    font-weight: 600 !important;
    background: #ffffff !important;
}
[data-testid="stNumberInput"] button {
    background: #1a3fc4 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
}
[data-testid="stNumberInput"] button svg { fill: #ffffff !important; }

/* multiselect */
[data-baseweb="tag"]     { background: #eef2ff !important; color: #1a3fc4 !important; }
[data-baseweb="option"]  { background: #ffffff !important; color: #111827 !important; }
[data-baseweb="option"]:hover { background: #f0f4ff !important; }
[data-baseweb="popover"],[data-baseweb="menu"] { background: #ffffff !important; }

/* page text */
.page-title    { font-size:32px;font-weight:800;color:#0d1b6e;letter-spacing:-0.7px;margin-bottom:3px;margin-top:0!important;padding-top:0!important; }
.page-subtitle { font-size:13.5px;color:#6b7a99;margin-bottom:22px; }
.sec-title     { font-size:10.5px;font-weight:800;letter-spacing:1.1px;color:#1a3fc4;
                 text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:7px; }
.sec-title span{ display:inline-flex;align-items:center;justify-content:center;
                 width:20px;height:20px;border-radius:5px;background:#1a3fc4;color:#fff;font-size:10px; }
.plabel { font-size:13px;font-weight:600;color:#1a3fc4;margin-bottom:4px;margin-top:14px;display:block; }
.phint  { font-size:12px;color:#6b7a99;margin-top:2px;margin-bottom:6px;display:block; }
.col-hdr{ font-size:10px;font-weight:700;color:#1a3fc4;text-transform:uppercase;
          letter-spacing:0.6px;padding:3px 0 8px; }
.file-pill    { display:flex;align-items:center;gap:8px;padding:9px 12px;border-radius:9px;
                margin-bottom:6px;font-size:12.5px;font-weight:600; }
.file-pill.ok { background:#f0fdf6;border:1.5px solid #a7f3d0;color:#065f46; }
/* Force progress bar text dark */
div[data-testid="stProgressBar"] > div > p,
div[data-testid="stProgressBar"] p,
div[class*="stProgress"] p {
    color: #111827 !important;
}
/* Force all form labels dark */
div[data-testid="stForm"] label,
div[data-testid="column"] label,
label[data-testid="stWidgetLabel"],
label[data-testid="stWidgetLabel"] p,
.stSelectbox label, .stSelectbox label p,
.stTextInput label, .stNumberInput label,
div[class*="stSelectbox"] label p,
div[class*="stSelectbox"] > label {
    color: #111827 !important;
    font-weight: 600 !important;
}
/* Selectbox itself */
div[data-testid="stSelectbox"] > label,
div[data-testid="stSelectbox"] > label > p {
    color: #111827 !important;
    font-weight: 600 !important;
}
/* Force expander to white in all environments */
div[data-testid="stExpander"] {
    background:#ffffff !important;
    border:1.5px solid #e8edf8 !important;
    border-radius:10px !important;
}
div[data-testid="stExpander"] summary {
    color:#111827 !important;
    background:#ffffff !important;
}
div[data-testid="stExpander"] summary:hover {
    background:#f8faff !important;
}
div[data-testid="stExpander"] summary span {
    color:#111827 !important;
}
div[data-testid="stExpander"] > div {
    background:#ffffff !important;
}
.file-pill.pending { background:#f8faff;border:1.5px solid #dde4f5;color:#6b7a99; }
.kpi-card  { background:#fff;border:1.5px solid #e8edf8;border-radius:13px;padding:16px 18px; }
.kpi-label { font-size:10.5px;color:#a0abbe;font-weight:700;margin-bottom:7px;
             text-transform:uppercase;letter-spacing:0.5px; }
.kpi-value { font-size:24px;font-weight:800;color:#0d1b6e;letter-spacing:-0.4px; }
.kpi-sub   { font-size:11px;color:#a0abbe;margin-top:2px; }
.sum-row   { display:flex;justify-content:space-between;align-items:center;
             padding:8px 0;border-bottom:1px solid #f2f5fb;font-size:13px; }
.sum-row:last-child { border-bottom:none; }
.sum-key { color:#6b7a99;font-weight:500; }
.sum-val { color:#0d1b6e;font-weight:700; }

/* How it works banner */
.hiw-banner { background:linear-gradient(135deg,#f0f4ff 0%,#fdf0f0 100%);
    border:1.5px solid #dde4f8;border-radius:16px;padding:22px 28px 20px;margin-bottom:22px; }
.hiw-label  { font-size:10px;font-weight:800;letter-spacing:1.4px;color:#1a3fc4;
    text-transform:uppercase;margin-bottom:20px; }
.hiw-steps  { display:flex;align-items:flex-start; }
.hiw-step   { flex:1;text-align:center; }
.hiw-connector { flex:0 0 50px;height:2px;background:linear-gradient(90deg,#c8d3ee,#e8c8c8);margin-top:24px; }
.hiw-circle { width:48px;height:48px;border-radius:50%;display:flex;align-items:center;
    justify-content:center;margin:0 auto 12px;font-size:18px;
    border:2px solid #dde4f8;background:#fff;box-shadow:0 2px 8px rgba(26,63,196,0.07); }
.hiw-circle.active { background:linear-gradient(135deg,#1a3fc4,#2952e3);border-color:#1a3fc4;
    box-shadow:0 4px 14px rgba(26,63,196,0.28); }
.hiw-circle.done { background:linear-gradient(135deg,#0d9e6e,#12b87e);border-color:#0d9e6e; }
.hiw-step-title { font-size:13.5px;font-weight:700;color:#0d1b6e;margin-bottom:3px; }
.hiw-step-desc  { font-size:11.5px;color:#6b7a99;line-height:1.5; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar open/close state — always open on first load
if "sb_open" not in st.session_state:
    st.session_state.sb_open = True
# Safety: if somehow stuck closed and on a fresh page, reset
_def("sb_open", True)

# ── Sidebar width via CSS injection
_w = "260px" if st.session_state.sb_open else "64px"
st.markdown(f"""
<style>
/* Force sidebar width — overrides Streamlit default resize */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"][aria-expanded="true"],
section[data-testid="stSidebar"][aria-expanded="false"] {{
    width: {_w} !important;
    min-width: {_w} !important;
    max-width: {_w} !important;
    flex-shrink: 0 !important;
    transform: translateX(0) !important;
    visibility: visible !important;
    display: flex !important;
    position: relative !important;
    transition: width 0.22s ease !important;
}}
/* Hide Streamlit's own collapse button entirely */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
button[kind="header"] {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    _open = st.session_state.sb_open

    if _open:
        # ── Full panel ──────────────────────────────────────────────────
        st.markdown("""
<div style="padding:22px 18px 14px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:6px;">
  <div style="display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;
       background:linear-gradient(135deg,#1a3fc4,#e84545);border-radius:10px;font-size:17px;
       margin-bottom:10px;">⛵</div>
  <div style="font-size:19px;font-weight:800;color:#ffffff;line-height:1.2;">DSL JMP</div>
  <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-top:3px;line-height:1.5;">
    Build, simulate and review your JMP</div>
</div>
<div style="font-size:9.5px;font-weight:700;letter-spacing:1.4px;
     color:rgba(255,255,255,0.28);text-transform:uppercase;padding:12px 18px 4px;">
  Navigation
</div>""", unsafe_allow_html=True)

        for icon, label in [("🏗️","Build my JMP"),("📊","Dashboard"),("📋","Simulation Table"),("📄","Summary"),("🎲","Monte Carlo"),("🎬","3D Simulation")]:
            active = st.session_state.page == label
            st.markdown(f'<div class="{"nav-active" if active else ""}">', unsafe_allow_html=True)
            if st.button(f"{icon}  {label}", key=f"nav_{label}"):
                st.session_state.page = label; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div style="height:1px;background:rgba(255,255,255,0.07);margin:10px 14px;"></div>
<div style="padding:10px 18px;font-size:11px;color:rgba(255,255,255,0.22);">
  DSL JMP Simulator · v1.0
</div>""", unsafe_allow_html=True)

        # collapse button at the bottom
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
<div style="padding:0 10px 14px;">
  <style>
    .collapse-btn .stButton>button {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 8px !important;
        color: rgba(255,255,255,0.7) !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        padding: 6px 12px !important;
        width: 100% !important;
        text-align: center !important;
    }
    .collapse-btn .stButton>button:hover {
        background: rgba(255,255,255,0.18) !important;
        color: #fff !important;
    }
  </style>
</div>""", unsafe_allow_html=True)
        st.markdown('<div class="collapse-btn">', unsafe_allow_html=True)
        if st.button("‹  Collapse", key="sb_toggle"):
            st.session_state.sb_open = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # ── Icon-only strip ─────────────────────────────────────────────
        st.markdown("""
<style>
  .icon-btn .stButton>button {
      background: transparent !important;
      border: none !important;
      border-radius: 10px !important;
      color: rgba(255,255,255,0.7) !important;
      font-size: 20px !important;
      padding: 8px 0 !important;
      width: 44px !important;
      min-width: 44px !important;
      text-align: center !important;
      margin: 2px auto !important;
      display: block !important;
  }
  .icon-btn .stButton>button:hover {
      background: rgba(255,255,255,0.1) !important;
      color: #fff !important;
  }
  .icon-btn-active .stButton>button {
      background: rgba(255,255,255,0.15) !important;
      border-left: 3px solid #e84545 !important;
      color: #fff !important;
  }
</style>
""", unsafe_allow_html=True)

        # expand button at the top
        st.markdown('<div style="padding:14px 10px 6px;display:flex;justify-content:center;">', unsafe_allow_html=True)
        if st.button("›", key="sb_toggle"):
            st.session_state.sb_open = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div style="height:1px;background:rgba(255,255,255,0.08);margin:0 8px 8px;"></div>', unsafe_allow_html=True)

        for icon, label in [("🏗️","Build my JMP"),("📊","Dashboard"),("📋","Simulation Table"),("📄","Summary"),("🎲","Monte Carlo"),("🎬","3D Simulation")]:
            active = st.session_state.page == label
            cls = "icon-btn-active" if active else "icon-btn"
            st.markdown(f'<div class="{cls}" style="display:flex;justify-content:center;">', unsafe_allow_html=True)
            if st.button(icon, key=f"nav_{label}"):
                st.session_state.page = label; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ── MAIN ───────────────────────────────────────────────────────────────────────
# Handle tab navigation via query params
_qp = st.query_params
if "build_step" in _qp:
    try: st.session_state.build_step = int(_qp["build_step"])
    except: pass
    st.query_params.clear(); st.rerun()
if "param_tab" in _qp:
    import urllib.parse
    _pt = urllib.parse.unquote(_qp["param_tab"])
    if _pt in ["🗓️ Simulation","🚢 Mother Vessels","🛥️ Shuttle Vessels","🏭 Storages","🔄 Roving Storage","📋 Prescribed Events"]:
        st.session_state.param_tab = _pt
    st.query_params.clear(); st.rerun()

page = st.session_state.page
st.markdown('<div style="padding:0.3rem 2.0rem 2rem;">', unsafe_allow_html=True)

# Handle tab navigation via query params
import urllib.parse as _ulp
_qp = st.query_params
if "build_step" in _qp:
    try: st.session_state.build_step = int(_qp["build_step"])
    except: pass
    st.query_params.clear(); st.rerun()
if "param_tab" in _qp:
    _pt = _ulp.unquote(_qp["param_tab"])
    _valid_tabs = ["🗓️ Simulation","🚢 Mother Vessels","🛥️ Shuttle Vessels","🏭 Storages","🔄 Roving Storage","📋 Prescribed Events"]
    if _pt in _valid_tabs:
        st.session_state.param_tab = _pt
    st.query_params.clear(); st.rerun()

page = st.session_state.page
st.markdown('<div style="padding:0.3rem 2.0rem 2rem;">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# BUILD MY JMP
# ════════════════════════════════════════════════════════════════════════
if page == "Build my JMP":
    st.markdown('<div class="page-title">Build my JMP</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Define simulation parameters, upload data files, then run</div>', unsafe_allow_html=True)

    step = st.session_state.build_step
    def cc(n): return "done" if n<step else ("active" if n==step else "")
    def ci(n): return "✓" if n<step else {1:"⚙️",2:"📂",3:"▶"}[n]

    st.markdown(f"""
    <div class="hiw-banner">
        <div class="hiw-label">✦ &nbsp; How it Works</div>
        <div class="hiw-steps">
            <div class="hiw-step"><div class="hiw-circle {cc(1)}">{ci(1)}</div>
                <div class="hiw-step-title">1. Define Parameters</div>
                <div class="hiw-step-desc">Set simulation window, vessel caps, storage stocks and engine rules</div></div>
            <div class="hiw-connector"></div>
            <div class="hiw-step"><div class="hiw-circle {cc(2)}">{ci(2)}</div>
                <div class="hiw-step-title">2. Upload Files</div>
                <div class="hiw-step-desc">Upload DSL Datahub and two tidal window summary files</div></div>
            <div class="hiw-connector"></div>
            <div class="hiw-step"><div class="hiw-circle {cc(3)}">{ci(3)}</div>
                <div class="hiw-step-title">3. Run Simulation</div>
                <div class="hiw-step-desc">Execute the daily loop and review outputs across all views</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Step segmented control ───────────────────────────────────────────────
    _step_labels = {1:"⚙️  Parameters", 2:"📂  Upload Files", 3:"▶  Run Simulation"}
    _step_css = "<style>"
    for _sv in [1,2,3]:
        _nth = _sv
        if step == _sv:
            _step_css += f"""
            div[data-testid="stHorizontalBlock"]:nth-of-type(1) > div:nth-child({_nth}) button {{
                background:#1a3fc4!important;color:#fff!important;font-weight:700!important;
                border:none!important;border-radius:10px!important;box-shadow:0 1px 6px rgba(26,63,196,0.3)!important;}}"""
        else:
            _step_css += f"""
            div[data-testid="stHorizontalBlock"]:nth-of-type(1) > div:nth-child({_nth}) button {{
                background:transparent!important;color:#6b7a99!important;font-weight:500!important;
                border:none!important;border-radius:10px!important;}}"""
    _step_css += """
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) {{
        background:#eef2ff!important;border:1.5px solid #c8d3ee!important;
        border-radius:14px!important;padding:4px!important;gap:3px!important;
        max-width:660px!important;
    }}
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) button:hover {{
        background:#dde4f5!important;color:#1a3fc4!important;
    }}
    </style>"""
    st.markdown(_step_css, unsafe_allow_html=True)
    _sc1, _sc2, _sc3 = st.columns(3, gap="small")
    for _sval, _scol in zip([1,2,3], [_sc1,_sc2,_sc3]):
        with _scol:
            if st.button(_step_labels[_sval], key=f"_sbtn{_sval}", use_container_width=True):
                st.session_state.build_step = _sval; st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    # ── STEP 1: PARAMETERS ───────────────────────────────────────────────────
    if step == 1:
        # Sub-tab segmented control (pure HTML <a> links)
        PTABS = ["🗓️ Simulation","🚢 Mother Vessels","🛥️ Shuttle Vessels","🏭 Storages","🔄 Roving Storage","📋 Prescribed Events"]
        cur_pt = st.session_state.param_tab
        _ptab_css = "<style>"
        for _pti, _ptl in enumerate(PTABS):
            _nth = _pti + 1
            if cur_pt == _ptl:
                _ptab_css += f"""
                div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child({_nth}) button {{
                    background:#1a3fc4!important;color:#fff!important;font-weight:700!important;
                    border:none!important;border-radius:8px!important;
                    box-shadow:0 1px 4px rgba(26,63,196,0.2)!important;}}"""
            else:
                _ptab_css += f"""
                div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child({_nth}) button {{
                    background:transparent!important;color:#6b7a99!important;font-weight:500!important;
                    border:none!important;border-radius:8px!important;}}"""
        _ptab_css += """
        div[data-testid="stHorizontalBlock"]:nth-of-type(2) {{
            background:#eef2ff!important;border:1.5px solid #c8d3ee!important;
            border-radius:12px!important;padding:4px!important;gap:2px!important;
        }}
        div[data-testid="stHorizontalBlock"]:nth-of-type(2) button {{
            font-size:12px!important;padding:8px 4px!important;transition:all 0.15s!important;}}
        div[data-testid="stHorizontalBlock"]:nth-of-type(2) button:hover {{
            background:#dde4f5!important;color:#1a3fc4!important;}}
        </style>"""
        st.markdown(_ptab_css, unsafe_allow_html=True)
        _pt_cols = st.columns(len(PTABS), gap="small")
        for _pti, (_ptc, _ptl) in enumerate(zip(_pt_cols, PTABS)):
            with _ptc:
                if st.button(_ptl, key=f"ptbtn_{_pti}", use_container_width=True):
                    st.session_state.param_tab = _ptl; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        pt = st.session_state.param_tab

        # ── Simulation ──────────────────────────────────────────────────────
        if pt == "🗓️ Simulation":
            L,R = st.columns(2, gap="large")
            with L:
                st.markdown('<div class="sec-title"><span>1</span> Simulation Window</div>', unsafe_allow_html=True)
                c1,c2 = st.columns(2)
                with c1:
                    st.markdown('<div class="plabel">Start Date</div>', unsafe_allow_html=True)
                    st.session_state.sim_start = st.date_input("_ss", value=st.session_state.sim_start, label_visibility="collapsed", key="inp_ss")
                with c2:
                    st.markdown('<div class="plabel">End Date</div>', unsafe_allow_html=True)
                    st.session_state.sim_end = st.date_input("_se", value=st.session_state.sim_end, label_visibility="collapsed", key="inp_se")
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="sec-title"><span>2</span> Engine Settings</div>', unsafe_allow_html=True)
                c1,c2 = st.columns(2)
                with c1:
                    st.markdown('<div class="plabel">Starting Injection No.</div>', unsafe_allow_html=True)
                    st.session_state.start_inj_no = st.number_input("_inj", value=st.session_state.start_inj_no, min_value=1, step=1, label_visibility="collapsed", key="inp_inj")
                    st.markdown('<div class="plabel">Mother Pause Days</div>', unsafe_allow_html=True)
                    st.markdown('<div class="phint">Clear days mother waits after ullage before reset</div>', unsafe_allow_html=True)
                    st.session_state.pause_days = st.number_input("_pd", value=st.session_state.pause_days, min_value=1, max_value=14, step=1, label_visibility="collapsed", key="inp_pd")
                with c2:
                    st.markdown('<div class="plabel">Whisky Trigger (bbls)</div>', unsafe_allow_html=True)
                    st.markdown('<div class="phint">Stock level that triggers Whisky station loading</div>', unsafe_allow_html=True)
                    st.session_state.whisky_trigger = st.number_input("_wt", value=st.session_state.whisky_trigger, min_value=0, step=1000, label_visibility="collapsed", key="inp_wt")
                    st.markdown('<div class="plabel">SanJulian Cap (bbls)</div>', unsafe_allow_html=True)
                    st.session_state.sanjulian_cap = st.number_input("_sjc", value=st.session_state.sanjulian_cap, min_value=0, step=10000, label_visibility="collapsed", key="inp_sjc")
            with R:
                st.markdown('<div class="sec-title"><span>3</span> Key Vessel Dates</div>', unsafe_allow_html=True)
                c1,c2 = st.columns(2)
                with c1:
                    st.markdown('<div class="plabel">Alkebulan Retirement</div>', unsafe_allow_html=True)
                    st.markdown('<div class="phint">Last active day for Alkebulan</div>', unsafe_allow_html=True)
                    st.session_state.alk_stop = st.date_input("_as", value=st.session_state.alk_stop, label_visibility="collapsed", key="inp_as")
                with c2:
                    st.markdown('<div class="plabel">SanJulian Active From</div>', unsafe_allow_html=True)
                    st.markdown('<div class="phint">Date SanJulian buffer becomes available</div>', unsafe_allow_html=True)
                    st.session_state.sanjulian_start = st.date_input("_sjs", value=st.session_state.sanjulian_start, label_visibility="collapsed", key="inp_sjs")
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="sec-title"><span>4</span> Prescribed Events Window</div>', unsafe_allow_html=True)
                st.markdown('<div class="phint">Events from Excel up to this date override simulation.</div>', unsafe_allow_html=True)
                st.session_state.prescribed_end = st.date_input("_pe", value=st.session_state.prescribed_end, label_visibility="collapsed", key="inp_pe")
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown('<div class="step-nav">', unsafe_allow_html=True)
                if st.button("Next: Upload Files →", key="go2", use_container_width=True): st.session_state.build_step=2; st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        elif pt == "🚢 Mother Vessels":
            st.markdown('<div class="sec-title"><span>M</span> Mother Vessel Configuration</div>', unsafe_allow_html=True)
            hcols = st.columns([1.2,0.8,0.8,0.9,0.9,0.5])
            for col,lbl in zip(hcols,["Vessel Name","Soft Cap","Hard Cap","Opening Stock","Retire Date","Fill %"]):
                with col: st.markdown(f'<div class="col-hdr">{lbl}</div>', unsafe_allow_html=True)
            updated = []
            for i,mv in enumerate(st.session_state.mother_vessels):
                cols = st.columns([1.2,0.8,0.8,0.9,0.9,0.4,0.15])
                with cols[0]: name  = st.text_input("n",  value=mv["name"],        key=f"mv_n_{i}", label_visibility="collapsed")
                with cols[1]: cap   = st.number_input("c", value=int(mv["cap"]),   key=f"mv_c_{i}", label_visibility="collapsed", min_value=0, step=10000)
                with cols[2]: hard  = st.number_input("h", value=int(mv["hard"]),  key=f"mv_h_{i}", label_visibility="collapsed", min_value=0, step=10000)
                with cols[3]: stock = st.number_input("s", value=int(mv["stock"]), key=f"mv_s_{i}", label_visibility="collapsed", min_value=0, step=1000)
                with cols[4]: retire= st.date_input("r",   value=mv["retire"] if mv["retire"] else date(2099,12,31), key=f"mv_r_{i}", label_visibility="collapsed")
                with cols[5]:
                    pct = round(100*stock/cap,1) if cap else 0
                    color = "#e84545" if pct>=90 else ("#f59e0b" if pct>=60 else "#1a3fc4")
                    st.markdown(f'<div style="padding-top:8px;font-size:16px;font-weight:800;color:{color};">{pct}%</div>', unsafe_allow_html=True)
                with cols[6]:
                    st.markdown('<div class="rm-btn">', unsafe_allow_html=True)
                    if st.button("✕", key=f"rm_mv_{i}"): st.session_state.mother_vessels.pop(i); st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                updated.append({"name":name,"cap":cap,"hard":hard,"stock":stock,"retire":retire if retire!=date(2099,12,31) else None})
            st.session_state.mother_vessels = updated
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="add-btn">', unsafe_allow_html=True)
            if st.button("＋ Add Mother Vessel", key="add_mv"): st.session_state.mother_vessels.append({"name":"New Vessel","cap":440000,"hard":730000,"stock":0,"retire":None}); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif pt == "🛥️ Shuttle Vessels":
            st.markdown('<div class="sec-title"><span>S</span> Shuttle Vessel Configuration</div>', unsafe_allow_html=True)
            all_stg = [s["name"] for s in st.session_state.storage_vessels]
            updated = []
            for i,sh in enumerate(st.session_state.shuttle_vessels):
                st.markdown('<div style="background:#fff;border:1.5px solid #e8edf8;border-radius:12px;padding:14px 18px;margin-bottom:10px;">', unsafe_allow_html=True)
                r1 = st.columns([1.2,0.7,0.4,0.8,0.35,0.18])
                with r1[0]:
                    st.markdown('<div class="col-hdr">Vessel Name</div>', unsafe_allow_html=True)
                    name = st.text_input("n", value=sh["name"], key=f"sh_n_{i}", label_visibility="collapsed")
                with r1[1]:
                    st.markdown('<div class="col-hdr">Cap (bbls)</div>', unsafe_allow_html=True)
                    cap = st.number_input("c", value=int(sh["cap"]), min_value=0, step=1000, key=f"sh_c_{i}", label_visibility="collapsed")
                with r1[2]:
                    st.markdown('<div class="col-hdr">Lead</div>', unsafe_allow_html=True)
                    lead = st.number_input("l", value=int(sh["lead"]), min_value=0, max_value=10, step=1, key=f"sh_l_{i}", label_visibility="collapsed")
                with r1[3]:
                    st.markdown('<div class="col-hdr">Commission Date</div>', unsafe_allow_html=True)
                    start = st.date_input("s", value=sh["start"], key=f"sh_s_{i}", label_visibility="collapsed")
                with r1[4]:
                    st.markdown('<div class="col-hdr">Active</div>', unsafe_allow_html=True)
                    active = st.checkbox("A", value=sh["active"], key=f"sh_a_{i}", label_visibility="collapsed")
                with r1[5]:
                    st.markdown('<div style="margin-top:22px;"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="rm-btn">', unsafe_allow_html=True)
                    if st.button("✕", key=f"rm_sh_{i}"): st.session_state.shuttle_vessels.pop(i); st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                st.markdown('<div class="col-hdr" style="margin-top:10px;">Allowed Load Points</div>', unsafe_allow_html=True)
                valid = [a for a in sh.get("allowed",[]) if a in all_stg]
                allowed = st.multiselect("ap", options=all_stg, default=valid, key=f"sh_ap_{i}", label_visibility="collapsed", placeholder="Select allowed storages…")
                st.markdown("</div>", unsafe_allow_html=True)
                updated.append({"name":name,"cap":cap,"lead":lead,"start":start,"active":active,"allowed":allowed})
            st.session_state.shuttle_vessels = updated
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="add-btn">', unsafe_allow_html=True)
            if st.button("＋ Add Shuttle", key="add_sh"): st.session_state.shuttle_vessels.append({"name":"New Shuttle","cap":80000,"lead":1,"start":date(2026,3,9),"active":True,"allowed":[]}); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif pt == "🏭 Storages":
            st.markdown('<div class="sec-title"><span>T</span> Storage Configuration</div>', unsafe_allow_html=True)
            hcols = st.columns([1.2,0.75,0.7,0.7,0.55,0.85,0.15])
            for col,lbl in zip(hcols,["Storage Name","Open Stock","Min Threshold","Cap (bbls)","Load Days","Start Date",""]):
                with col: st.markdown(f'<div class="col-hdr">{lbl}</div>', unsafe_allow_html=True)
            updated = []
            for i,stg in enumerate(st.session_state.storage_vessels):
                cols = st.columns([1.2,0.75,0.7,0.7,0.55,0.85,0.15])
                with cols[0]: name    = st.text_input("n",  value=stg["name"],             key=f"stg_n_{i}", label_visibility="collapsed")
                with cols[1]: stock   = st.number_input("s", value=int(stg["stock"]),       key=f"stg_s_{i}", label_visibility="collapsed", min_value=0, step=1000)
                with cols[2]: min_thr = st.number_input("m", value=int(stg["min_thr"]),    key=f"stg_m_{i}", label_visibility="collapsed", min_value=0, step=1000)
                with cols[3]: cap     = st.number_input("c", value=int(stg["cap"]),         key=f"stg_c_{i}", label_visibility="collapsed", min_value=0, step=10000)
                with cols[4]: lt      = st.number_input("l", value=float(stg["load_time"]),key=f"stg_l_{i}", label_visibility="collapsed", min_value=0.0, step=0.5, format="%.1f")
                with cols[5]: start   = st.date_input("d",   value=stg["start"],            key=f"stg_d_{i}", label_visibility="collapsed")
                with cols[6]:
                    st.markdown('<div class="rm-btn" style="padding-top:2px;">', unsafe_allow_html=True)
                    if st.button("✕", key=f"rm_stg_{i}"): st.session_state.storage_vessels.pop(i); st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                updated.append({"name":name,"stock":stock,"min_thr":min_thr,"cap":cap,"load_time":lt,"start":start})
            st.session_state.storage_vessels = updated
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="add-btn">', unsafe_allow_html=True)
            if st.button("＋ Add Storage", key="add_stg"): st.session_state.storage_vessels.append({"name":"New Storage","stock":0,"min_thr":50000,"cap":270000,"load_time":1.0,"start":date(2026,3,9)}); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif pt == "🔄 Roving Storage":
            st.markdown('''<div class="sec-title"><span>R</span> Roving Storage Configuration</div>''', unsafe_allow_html=True)
            st.markdown('''<div class="phint" style="margin-bottom:16px;">
Roving storage allows shuttle vessels with large true-capacity to consolidate
smaller shuttle cargo at Bonny before discharging to a mother vessel.
This reduces mother vessel wait time and increases throughput.<br><br>
<strong>SanJulian</strong> is always active as a roving buffer at Bonny Anchorage (overflow when no mother is free).<br>
<strong>Shuttle-to-shuttle transloading</strong> starts from the STS Active Date below.
</div>''', unsafe_allow_html=True)

            # STS start date
            r1, r2 = st.columns(2, gap="large")
            with r1:
                st.markdown('<div class="sec-title"><span>1</span> STS Transload Settings</div>', unsafe_allow_html=True)
                st.markdown('<div class="plabel">STS Active From</div>', unsafe_allow_html=True)
                st.markdown('<div class="phint">Date shuttle-to-shuttle transloading begins at Bonny</div>', unsafe_allow_html=True)
                st.session_state.sts_start = st.date_input("_sts", value=st.session_state.sts_start,
                    label_visibility="collapsed", key="inp_sts")

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('''<div style="background:#f0f4ff;border:1.5px solid #c8d3ee;border-radius:12px;padding:14px 16px;">
<div style="font-size:11px;font-weight:700;color:#1a3fc4;margin-bottom:6px;">🔒 SanJulian (Always Active)</div>
<div style="font-size:12px;color:#374151;line-height:1.6;">
Stationed at <strong>Bonny Anchorage</strong> as overflow roving storage.<br>
Capacity: <strong>450,000 bbls</strong><br>
When no mother is free, shuttles discharge into SanJulian.<br>
SanJulian transloads to next available mother (1-day lead).
</div></div>''', unsafe_allow_html=True)

            with r2:
                st.markdown('<div class="sec-title"><span>2</span> Shuttle Vessels as Roving Storage</div>', unsafe_allow_html=True)
                st.markdown('<div class="phint">Enable large-capacity shuttles to receive cargo from smaller shuttles at Bonny before discharging to mother.</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                _rv = st.session_state.roving_vessels
                for i, rv in enumerate(_rv):
                    c1, c2, c3 = st.columns([2.5, 2, 0.8])
                    with c1:
                        st.markdown(f'<div style="padding:6px 0;font-size:13px;font-weight:600;color:#111827;">{rv["name"]}</div>', unsafe_allow_html=True)
                    with c2:
                        new_cap = st.number_input(
                            "True Cap (bbls)", value=int(rv["true_cap"]),
                            min_value=10000, max_value=500000, step=5000,
                            key=f"rv_cap_{i}", label_visibility="collapsed"
                        )
                        st.markdown(f'<div style="font-size:10px;color:#9aa3bc;margin-top:-8px;">true cap: {new_cap:,} bbls</div>', unsafe_allow_html=True)
                        _rv[i]["true_cap"] = new_cap
                    with c3:
                        enabled = st.checkbox("", value=rv["enabled"], key=f"rv_en_{i}")
                        _rv[i]["enabled"] = enabled
                    st.markdown("---" if i < len(_rv)-1 else "", unsafe_allow_html=True)
                st.session_state.roving_vessels = _rv

        elif pt == "📋 Prescribed Events":
            L,R = st.columns([1.4,1], gap="large")
            with L:
                st.markdown('<div class="sec-title"><span>P</span> Prescribed Events Window</div>', unsafe_allow_html=True)
                st.markdown("""<div style="background:#f0f4ff;border:1.5px solid #dde4f8;border-radius:12px;
                    padding:14px 16px;margin-bottom:14px;font-size:12.5px;color:#374151;line-height:1.7;">
                    <b>What are prescribed events?</b><br>Rows in the DSL Datahub Excel that have actual
                    historical discharge dates. The simulation replays these exactly as they happened,
                    up to the <b>Prescribed End Date</b>. After that date the engine simulates freely.</div>""", unsafe_allow_html=True)
                st.markdown('<div class="plabel">Prescribed Events End Date</div>', unsafe_allow_html=True)
                st.session_state.prescribed_end = st.date_input("_pe2", value=st.session_state.prescribed_end, label_visibility="collapsed", key="inp_pe2")
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="sec-title"><span>W</span> Whisky Station Interchange Window</div>', unsafe_allow_html=True)
                wc1,wc2 = st.columns(2)
                with wc1:
                    st.markdown('<div class="plabel">Interchange Start</div>', unsafe_allow_html=True)
                    st.session_state.whisky_win_start = st.date_input("_wws", value=st.session_state.whisky_win_start, label_visibility="collapsed", key="inp_wws")
                with wc2:
                    st.markdown('<div class="plabel">Interchange End</div>', unsafe_allow_html=True)
                    st.session_state.whisky_win_end = st.date_input("_wwe", value=st.session_state.whisky_win_end, label_visibility="collapsed", key="inp_wwe")
            with R:
                st.markdown('<div class="sec-title"><span>M</span> Manual Override Events</div>', unsafe_allow_html=True)
                sh_names  = [s["name"] for s in st.session_state.shuttle_vessels]
                stg_names = [s["name"] for s in st.session_state.storage_vessels]
                updated_ev = []
                for i,ev in enumerate(st.session_state.manual_events):
                    st.markdown(f'<div style="font-size:10.5px;font-weight:700;color:#a0abbe;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:4px;">Event {i+1}</div>', unsafe_allow_html=True)
                    mc1,mc2 = st.columns(2)
                    with mc1:
                        d  = st.date_input("Date", value=ev["date"], key=f"mev_d_{i}")
                        si = sh_names.index(ev["shuttle"]) if ev["shuttle"] in sh_names else 0
                        sh = st.selectbox("Shuttle", sh_names, index=si, key=f"mev_sh_{i}", label_visibility="collapsed")
                    with mc2:
                        gi = stg_names.index(ev["storage"]) if ev["storage"] in stg_names else 0
                        sg = st.selectbox("Storage", stg_names, index=gi, key=f"mev_stg_{i}", label_visibility="collapsed")
                        vl = st.number_input("Vol", value=int(ev["volume"]), min_value=0, step=1000, key=f"mev_v_{i}", label_visibility="collapsed")
                    updated_ev.append({"date":d,"shuttle":sh,"storage":sg,"volume":vl})
                    rc,_ = st.columns([1,3])
                    with rc:
                        st.markdown('<div class="rm-btn">', unsafe_allow_html=True)
                        if st.button("🗑 Remove", key=f"rm_ev_{i}"): st.session_state.manual_events.pop(i); st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown('<hr style="border:none;border-top:1px solid #f0f3fb;margin:8px 0;">', unsafe_allow_html=True)
                st.session_state.manual_events = updated_ev
                st.markdown('<div class="add-btn">', unsafe_allow_html=True)
                if st.button("＋ Add Manual Event", key="add_ev"):
                    st.session_state.manual_events.append({"date":date(2026,3,13),"shuttle":sh_names[0] if sh_names else "Sherlock","storage":stg_names[0] if stg_names else "Chapel_OML24","volume":85000}); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    elif step == 2:
        L,R = st.columns([1.4,1], gap="large")
        with L:
            st.markdown('<div class="sec-title"><span>1</span> DSL Datahub</div>', unsafe_allow_html=True)
            st.markdown('<div class="phint" style="margin-bottom:8px;">Excel file with shuttle vessel schedule, storage loads and historical discharge data. Initial stock levels will be read from this file.</div>', unsafe_allow_html=True)
            st.file_uploader("DSL Datahub (.xlsx)", type=["xlsx"], key="datahub_upload", label_visibility="collapsed")

            # ── Auto-read stock levels from datahub as soon as file is uploaded ──
            _dh_up = st.session_state.get("datahub_upload")
            if _dh_up is not None:
                import io as _io, pandas as _pd
                from engine import STOCK_SHEET_MAP as _SSM
                try:
                    _dh_up.seek(0)
                    _wb_bytes = _dh_up.read()
                    _dh_up.seek(0)
                    _asof = _pd.to_datetime(st.session_state.sim_start).normalize()

                    # Update mother vessel stocks
                    _mv_updated = {m["name"]: m.copy() for m in st.session_state.mother_vessels}
                    for _mname, _cfg in _SSM["mothers"].items():
                        try:
                            _df = _pd.read_excel(_io.BytesIO(_wb_bytes), sheet_name=_cfg["sheet"])
                            _df[_cfg["date_col"]] = _pd.to_datetime(_df[_cfg["date_col"]], errors="coerce").dt.normalize()
                            _df[_cfg["stock_col"]] = _pd.to_numeric(_df[_cfg["stock_col"]].astype(str).str.replace(",","",regex=False).str.strip(), errors="coerce")
                            _df = _df.dropna(subset=[_cfg["date_col"], _cfg["stock_col"]]).sort_values(_cfg["date_col"])
                            _row = _df[_df[_cfg["date_col"]] == _asof]
                            if _row.empty:
                                _row = _df[_df[_cfg["date_col"]] < _asof]
                            if not _row.empty and _mname in _mv_updated:
                                _mv_updated[_mname]["stock"] = int(_row.iloc[-1][_cfg["stock_col"]])
                        except Exception:
                            pass
                    st.session_state.mother_vessels = list(_mv_updated.values())

                    # Update storage vessel stocks
                    _sv_updated = {s["name"]: s.copy() for s in st.session_state.storage_vessels}
                    for _sname, _cfg in _SSM["storages"].items():
                        try:
                            _df = _pd.read_excel(_io.BytesIO(_wb_bytes), sheet_name=_cfg["sheet"])
                            _df[_cfg["date_col"]] = _pd.to_datetime(_df[_cfg["date_col"]], errors="coerce").dt.normalize()
                            _df[_cfg["stock_col"]] = _pd.to_numeric(_df[_cfg["stock_col"]].astype(str).str.replace(",","",regex=False).str.strip(), errors="coerce")
                            _df = _df.dropna(subset=[_cfg["date_col"], _cfg["stock_col"]]).sort_values(_cfg["date_col"])
                            _row = _df[_df[_cfg["date_col"]] == _asof]
                            if _row.empty:
                                _row = _df[_df[_cfg["date_col"]] < _asof]
                            if not _row.empty and _sname in _sv_updated:
                                _sv_updated[_sname]["stock"] = int(_row.iloc[-1][_cfg["stock_col"]])
                        except Exception:
                            pass
                    st.session_state.storage_vessels = list(_sv_updated.values())

                except Exception:
                    pass

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="sec-title"><span>2</span> Tidal Window File</div>', unsafe_allow_html=True)
            st.markdown('<div class="phint" style="margin-bottom:8px;">San Barth Entrance predicted tides PDF (e.g. "San Barth Entrance Q2 2026 Predicted Tides.pdf").</div>', unsafe_allow_html=True)
            st.file_uploader("Tide PDF", type=["pdf"], key="tide_pdf_upload", label_visibility="collapsed")
        with R:
            st.markdown('<div class="sec-title"><span>✓</span> File Status</div>', unsafe_allow_html=True)
            files = {"DSL Datahub":st.session_state.get("datahub_upload"),"Tide PDF":st.session_state.get("tide_pdf_upload")}
            for name,f in files.items():
                if f:  st.markdown(f'<div class="file-pill ok">✅ &nbsp; {name} &nbsp;<span style="font-weight:400;font-size:11px;">— {f.name}</span></div>', unsafe_allow_html=True)
                else:  st.markdown(f'<div class="file-pill pending">⬜ &nbsp; {name} — awaiting upload</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            n1,n2 = st.columns(2)
            with n1:
                st.markdown('<div class="step-nav">', unsafe_allow_html=True)
                if st.button("← Parameters", key="back1", use_container_width=True): st.session_state.build_step=1; st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with n2:
                st.markdown('<div class="step-nav">', unsafe_allow_html=True)
                if st.button("Next: Run →", key="go3", use_container_width=True): st.session_state.build_step=3; st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    elif step == 3:
        import sys, os, traceback
        # ── Ensure engine is importable ────────────────────────────────────────
        _cwd = os.getcwd()
        try:    _script_dir = os.path.dirname(os.path.abspath(__file__))
        except: _script_dir = _cwd
        for _p in [_cwd, _script_dir]:
            if _p not in sys.path: sys.path.insert(0, _p)

        # ── Helper: build params dict from session state ───────────────────────
        def _build_params(seed=None):
            import io as _io
            # Read uploaded file bytes immediately — Streamlit UploadedFile
            # can only be read once; convert to BytesIO so engine always gets fresh data
            _dh = st.session_state.get("datahub_upload")
            if _dh is not None:
                try:
                    _dh.seek(0)
                    _dh_bytes = _io.BytesIO(_dh.read())
                    _dh.seek(0)
                except Exception:
                    _dh_bytes = None
            else:
                _dh_bytes = None

            _tp = st.session_state.get("tide_pdf_upload")
            if _tp is not None:
                try:
                    _tp.seek(0)
                    _tp_bytes = _io.BytesIO(_tp.read())
                    _tp.seek(0)
                except Exception:
                    _tp_bytes = None
            else:
                _tp_bytes = None

            return {
                "sim_start":       st.session_state.sim_start,
                "sim_end":         st.session_state.sim_end,
                "start_inj_no":    st.session_state.start_inj_no,
                "pause_days":      st.session_state.pause_days,
                "whisky_trigger":  st.session_state.whisky_trigger,
                "sanjulian_cap":   st.session_state.sanjulian_cap,
                "alk_stop":        st.session_state.alk_stop,
                "sanjulian_start": st.session_state.sanjulian_start,
                "prescribed_end":  st.session_state.prescribed_end,
                "whisky_win_start":st.session_state.whisky_win_start,
                "whisky_win_end":  st.session_state.whisky_win_end,
                "mother_vessels":  st.session_state.mother_vessels,
                "shuttle_vessels": st.session_state.shuttle_vessels,
                "storage_vessels": st.session_state.storage_vessels,
                "manual_events":   st.session_state.get("manual_events", []),
                "datahub_file":    _dh_bytes,
                "tide_pdf_file":   _tp_bytes,
                "seed":            seed,
                "roving_vessels":  st.session_state.get("roving_vessels", []),
                "sts_start":       st.session_state.get("sts_start", date(2026, 4, 1)),
            }

        # ── Layout ─────────────────────────────────────────────────────────────
        L, R = st.columns([1.6, 1], gap="large")

        with L:
            # Simulation summary panel
            st.markdown('<div class="sec-title"><span>✓</span> Simulation Summary</div>', unsafe_allow_html=True)
            active_sh = sum(1 for s in st.session_state.shuttle_vessels if s.get("active", True))
            summary = [
                ("Simulation Period",       f"{st.session_state.sim_start.strftime('%d %b %Y')} → {st.session_state.sim_end.strftime('%d %b %Y')}"),
                ("Prescribed Events Up To", st.session_state.prescribed_end.strftime('%d %b %Y')),
                ("Starting Injection No.",  str(st.session_state.start_inj_no)),
                ("Mother Pause Days",       f"{st.session_state.pause_days} days after ullage"),
                ("Whisky Trigger",          f"{st.session_state.whisky_trigger:,} bbls"),
                ("SanJulian Buffer",        f"Active {st.session_state.sanjulian_start.strftime('%d %b %Y')} · Cap {st.session_state.sanjulian_cap:,}"),
                ("Alkebulan Retirement",    st.session_state.alk_stop.strftime('%d %b %Y')),
                ("Active Shuttle Vessels",  f"{active_sh} of {len(st.session_state.shuttle_vessels)}"),
            ]
            html = '<div style="background:#fff;border:1.5px solid #e8edf8;border-radius:13px;padding:18px 24px;">'
            for k, v in summary:
                html += f'<div class="sum-row"><span class="sum-key">{k}</span><span class="sum-val">{v}</span></div>'
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

        with R:
            # File status
            files = {
                "DSL Datahub": st.session_state.get("datahub_upload"),
                "Tide PDF":     st.session_state.get("tide_pdf_upload"),
            }
            files_uploaded = sum(1 for v in files.values() if v is not None)
            st.markdown('<div class="sec-title"><span>✓</span> File Status</div>', unsafe_allow_html=True)
            for name, f in files.items():
                if f:   st.markdown(f'<div class="file-pill ok">✅ &nbsp; {name} — {f.name}</div>', unsafe_allow_html=True)
                else:   st.markdown(f'<div class="file-pill pending">⬜ &nbsp; {name} — optional</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if files_uploaded == 0:
                st.info("No files — runs on parameters only.", icon="ℹ️")
            elif files_uploaded < 3:
                st.warning(f"Only {files_uploaded}/3 files uploaded.", icon="⚠️")
            else:
                st.success("All files uploaded.", icon="✅")

        # ── Persistent error display ───────────────────────────────────────────
        if st.session_state.get("sim_error"):
            st.error("Last run failed — see error below.")
            st.code(st.session_state.sim_error, language="python")
            if st.button("Clear error", key="clear_err"):
                st.session_state.sim_error = None; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<hr style="border:none;border-top:1.5px solid #e8edf8;margin-bottom:20px;">', unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════════
        # DETERMINISTIC MODE
        # ══════════════════════════════════════════════════════════════════════
        det_col, mc_col = st.columns(2, gap="large")

        with det_col:
            st.markdown('''<div style="background:#f0f4ff;border:1.5px solid #c8d3ee;border-radius:14px;padding:18px 20px;">
<div style="font-size:11px;font-weight:800;letter-spacing:1px;color:#1a3fc4;text-transform:uppercase;margin-bottom:8px;">
⚙️ Deterministic Run</div>
<div style="font-size:13px;color:#374151;line-height:1.6;">
Fix a random seed so you get the <strong>same output every time</strong> with the same parameters.
Good for debugging and comparing parameter changes fairly.</div></div>''', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            d1, d2 = st.columns([2, 1])
            with d1:
                det_seed = st.number_input("Random seed", min_value=0, max_value=9999,
                                           value=42, step=1, key="det_seed")
            with d2:
                st.markdown("<br>", unsafe_allow_html=True)
                use_seed = st.toggle("Use seed", value=True, key="use_seed_toggle")

            st.markdown('<div class="run-btn">', unsafe_allow_html=True)
            if st.button("▶  Run Deterministic", key="run_det", use_container_width=True):
                from engine import run_simulation as _rse
                _prog = st.progress(0, text="Initialising…")
                try:
                    _prog.progress(15, text="Loading engine…")
                    _seed_val = int(det_seed) if use_seed else None
                    _prog.progress(35, text=f"Running with seed={_seed_val}…")
                    _res = _rse(_build_params(seed=_seed_val))
                    _prog.progress(90, text="Building tables…")
                    st.session_state.sim_results  = _res
                    st.session_state.sim_seed_used = _seed_val
                    st.session_state.sim_error    = None
                    st.session_state.mc_results   = None   # clear any MC results
                    # Capture stock init error so user can see what went wrong
                    _sierr = _res.get("stock_init_error") if _res else None
                    st.session_state["stock_init_error"] = _sierr
                    _prog.progress(100, text="Done!")
                except Exception:
                    st.session_state.sim_error = traceback.format_exc()
                    st.session_state.sim_results = None
                    _prog.empty()
                if st.session_state.get("sim_results"):
                    if st.session_state.get("stock_init_error"):
                        st.warning(f"⚠️ Stock levels from datahub could not be read — using UI defaults instead.\n\n**Error:** `{st.session_state['stock_init_error']}`", icon="⚠️")
                        import time; time.sleep(4)
                    st.session_state.page = "Dashboard"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════════
        # MONTE CARLO MODE
        # ══════════════════════════════════════════════════════════════════════
        with mc_col:
            st.markdown('''<div style="background:#fff8f0;border:1.5px solid #fcd9a8;border-radius:14px;padding:18px 20px;">
<div style="font-size:11px;font-weight:800;letter-spacing:1px;color:#c65911;text-transform:uppercase;margin-bottom:8px;">
🎲 Monte Carlo — Top 5 Finder</div>
<div style="font-size:13px;color:#374151;line-height:1.6;">
Run the simulation N times with different seeds, score each run against your criteria,
and surface the <strong>top 5 best outcomes</strong>.</div></div>''', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            mc_n = st.slider("Number of runs", min_value=10, max_value=500,
                             value=300, step=10, key="mc_n_runs")

            st.markdown('<div style="font-size:11px;font-weight:700;color:#6b7a99;text-transform:uppercase;letter-spacing:0.8px;margin:12px 0 6px;">Ranking Criteria Weights</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:11px;color:#9aa3bc;margin-bottom:10px;">Set to 0 to exclude a criterion</div>', unsafe_allow_html=True)

            w_trips   = st.slider("SBM Trips (most injections)",        0, 10, 8, key="w_trips")
            w_nepl    = st.slider("NEPL Volume (least 3rd party)",       0, 10, 9, key="w_nepl")
            w_vol     = st.slider("Total Discharge Volume",              0, 10, 6, key="w_vol")
            w_mother  = st.slider("Mother Vessel Balance",               0, 10, 4, key="w_mother")
            w_shuttle = st.slider("Shuttle Utilisation (total vol)",     0, 10, 5, key="w_shuttle")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="run-btn">', unsafe_allow_html=True)
            if st.button(f"🎲  Run {mc_n} Simulations", key="run_mc", use_container_width=True):
                from engine import run_simulation as _rse
                import pandas as _pd

                _weights = {
                    "trips":          w_trips,
                    "nepl_vol":       w_nepl,
                    "total_vol":      w_vol,
                    "mother_balance": w_mother,
                    "shuttle_vol":    w_shuttle,
                }
                _total_w = sum(_weights.values()) or 1

                _all_kpis = []
                _prog = st.progress(0, text="Starting Monte Carlo runs…")
                _errors = 0

                for _i in range(mc_n):
                    _prog.progress(int((_i / mc_n) * 95),
                                   text=f"Run {_i+1} / {mc_n}  ({_errors} errors)")
                    try:
                        _r = _rse(_build_params(seed=_i))
                        _k = _r["kpis"].copy()
                        _k["seed"]    = _i
                        _k["run_no"]  = _i + 1
                        # keep lightweight refs for top-5
                        _k["_results"] = _r
                        _all_kpis.append(_k)
                    except Exception:
                        _errors += 1

                _prog.progress(97, text="Scoring and ranking…")

                if _all_kpis:
                    # normalise each metric 0→1 across all runs
                    _metrics = ["trips","nepl_vol","total_vol","mother_balance","shuttle_vol"]
                    _df_kpi = _pd.DataFrame([{m: r[m] for m in _metrics} | {"seed": r["seed"], "run_no": r["run_no"]} for r in _all_kpis])

                    for _m in _metrics:
                        _lo, _hi = _df_kpi[_m].min(), _df_kpi[_m].max()
                        _rng = _hi - _lo
                        _df_kpi[f"_n_{_m}"] = (_df_kpi[_m] - _lo) / _rng if _rng > 0 else 0.5

                    _df_kpi["score"] = sum(
                        _weights[_m] * _df_kpi[f"_n_{_m}"] for _m in _metrics
                    ) / _total_w

                    _df_kpi = _df_kpi.sort_values("score", ascending=False).reset_index(drop=True)
                    _top5_seeds = _df_kpi["seed"].iloc[:5].tolist()
                    _top5_results = [next(r["_results"] for r in _all_kpis if r["seed"] == s) for s in _top5_seeds]

                    st.session_state.mc_results     = {
                        "df_kpi":       _df_kpi,
                        "top5_seeds":   _top5_seeds,
                        "top5_results": _top5_results,
                        "n_runs":       mc_n,
                        "n_errors":     _errors,
                        "weights":      _weights,
                    }
                    # Default sim_results = rank #1
                    st.session_state.sim_results  = _top5_results[0]
                    st.session_state.sim_seed_used = _top5_seeds[0]
                    st.session_state.sim_error    = None
                    _prog.progress(100, text=f"Done! Best seed = {_top5_seeds[0]}")

                    st.session_state.page = "Monte Carlo"
                    st.rerun()
                else:
                    st.error(f"All {mc_n} runs failed. Check your parameters.")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="step-nav">', unsafe_allow_html=True)
        if st.button("← Back to Upload Files", key="back2", use_container_width=True):
            st.session_state.build_step = 2; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Dashboard":
    import pandas as pd
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Shuttle vessel behaviour — simulation overview</div>', unsafe_allow_html=True)

    results = st.session_state.get("sim_results")

    # ── KPI cards ─────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    if results:
        kpis = results["kpis"]
        kpi_data = [
            ("Total Volume",     f"{kpis['total_vol']:,}", "bbls discharged"),
            ("NEPL Volume",      f"{kpis['nepl_vol']:,}", "NEPL contribution"),
            ("3rd Party Volume", f"{kpis['tp_vol']:,}",   "External contribution"),
            ("SBM Trips",        str(kpis['trips']),       "Injections completed"),
        ]
    else:
        kpi_data = [("Total Volume","—","Run simulation"),("NEPL Volume","—","Run simulation"),
                    ("3rd Party Volume","—","Run simulation"),("SBM Trips","—","Run simulation")]
    for col, (lbl, val, sub) in zip([k1, k2, k3, k4], kpi_data):
        with col:
            st.markdown(f'<div class="kpi-card"><div class="kpi-label">{lbl}</div>'                        f'<div class="kpi-value">{val}</div><div class="kpi-sub">{sub}</div></div>',
                        unsafe_allow_html=True)

    if not results:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("Run the simulation from **Build my JMP → Step 3** to populate the dashboard.", icon="📊")
    else:
        monthly_mother = results.get("monthly_mother")
        inj_df = results.get("inj_df")
        dis_df = results.get("dis_df")

        # ── Row 1: Monthly volume chart + shuttle chart ────────────────────────
        ch1, ch2 = st.columns(2, gap="medium")

        with ch1:
            if monthly_mother is not None and not monthly_mother.empty:
                try:
                    import plotly.express as px
                    fig = px.bar(
                        monthly_mother.sort_values("MonthStart"),
                        x="MonthLabel", y="Total_Volume", color="Vessel",
                        title="Monthly Discharge Volume by Mother Vessel",
                        color_discrete_map={"Bryanston":"#111827","Alkebulan":"#EF553B","Green Eagle":"#636EFA"},
                    )
                    fig.update_layout(barmode="stack", height=360,
                        margin=dict(l=10,r=10,t=40,b=40),
                        xaxis_title="", yaxis_title="Volume (bbls)",
                        legend=dict(orientation="h", y=-0.25,
                            font=dict(color="#111827"), bgcolor="#ffffff",
                            title=dict(font=dict(color="#111827"))),
                        paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                        font=dict(color="#111827"),
                        title_font=dict(color="#111827", size=14),
                        xaxis=dict(color="#111827",gridcolor="#e2e8f0",linecolor="#cbd5e1",tickfont=dict(color="#111827")),
                        yaxis=dict(color="#111827",gridcolor="#e2e8f0",linecolor="#cbd5e1",tickfont=dict(color="#111827")))
                    st.plotly_chart(fig, use_container_width=True)
                except ImportError:
                    st.warning("Run: pip install plotly")

        with ch2:
            if dis_df is not None and not dis_df.empty:
                try:
                    import plotly.express as px
                    shuttle_agg = (dis_df[~dis_df["IsThirdParty"]]
                        .groupby("vessel", as_index=False)["volume"].sum()
                        .sort_values("volume", ascending=False))
                    fig2 = px.bar(shuttle_agg, x="vessel", y="volume",
                        title="Total Volume Discharged by Shuttle Vessel",
                        color_discrete_sequence=["#111827"])
                    fig2.update_layout(height=360, margin=dict(l=10,r=10,t=40,b=80),
                        xaxis_title="", yaxis_title="Volume (bbls)",
                        xaxis_tickangle=-30,
                        paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                        font=dict(color="#111827"),
                        title_font=dict(color="#111827", size=14),
                        xaxis=dict(color="#111827",gridcolor="#e2e8f0",linecolor="#cbd5e1",tickfont=dict(color="#111827")),
                        yaxis=dict(color="#111827",gridcolor="#e2e8f0",linecolor="#cbd5e1",tickfont=dict(color="#111827")))
                    st.plotly_chart(fig2, use_container_width=True)
                except ImportError:
                    pass

        # ── Mother stock chart ─────────────────────────────────────────────────
        df_main = results.get("df")
        if df_main is not None and not df_main.empty:
            try:
                import plotly.graph_objects as go
                fig3 = go.Figure()
                COLORS = {"Bryanston":"#111827", "Alkebulan":"#EF553B", "Green Eagle":"#636EFA"}
                for mname, col in COLORS.items():
                    scol = f"{mname} Stock"
                    if scol in df_main.columns:
                        cap = next((m["cap"] for m in st.session_state.mother_vessels if m["name"] == mname), None)
                        fig3.add_trace(go.Scatter(
                            x=df_main["Date"], y=df_main[scol],
                            name=mname, line=dict(color=col, width=2)))
                        if cap:
                            fig3.add_hline(y=cap, line_dash="dot", line_color=col,
                                           annotation_text=f"{mname} cap", annotation_position="right",
                                           line_width=1, opacity=0.5)
                fig3.update_layout(title="Mother Vessel Stock Over Time", title_font=dict(color="#111827", size=14),
                    height=320, margin=dict(l=10,r=10,t=40,b=20),
                    xaxis_title="", yaxis_title="Stock (bbls)",
                    legend=dict(orientation="h", y=-0.2,
                        font=dict(color="#111827"), bgcolor="#ffffff",
                        title=dict(font=dict(color="#111827"))),
                    paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                    font=dict(color="#111827"),
                    xaxis=dict(color="#111827",gridcolor="#e2e8f0",linecolor="#cbd5e1",tickfont=dict(color="#111827")),
                    yaxis=dict(color="#111827",gridcolor="#e2e8f0",linecolor="#cbd5e1",tickfont=dict(color="#111827")))
                st.plotly_chart(fig3, use_container_width=True)
            except ImportError:
                pass

        # ── Injection summary table ────────────────────────────────────────────
        if inj_df is not None and not inj_df.empty:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="sec-title"><span>I</span> Injection Log</div>', unsafe_allow_html=True)
            show = [c for c in ["Injection No","Vessel","MonthLabel","Total Quantity",
                                 "NEPL","Third Party","Final Ullage",
                                 "SBM Discharge Day 2","SBM Discharge Day 3"] if c in inj_df.columns]
            _inj_disp = inj_df[show].copy()
            # Format date columns — remove 00:00:00 timestamp
            for _dc in ["Final Ullage","SBM Discharge Day 2","SBM Discharge Day 3"]:
                if _dc in _inj_disp.columns:
                    _inj_disp[_dc] = _inj_disp[_dc].apply(
                        lambda x: str(x)[:10] if pd.notna(x) else "")
            _inj_html = _inj_disp.reset_index(drop=True).to_html(index=False, border=0, classes="inj-log-tbl")
            st.markdown(
                """<style>
                .inj-log-tbl{border-collapse:collapse;width:100%;font-size:13px;color:#111827;}
                .inj-log-tbl th{background:#1a3fc4;color:#fff;padding:9px 14px;text-align:left;
                    font-weight:600;white-space:nowrap;}
                .inj-log-tbl td{padding:8px 14px;border-bottom:1px solid #e8edf8;
                    color:#111827;background:#fff;white-space:nowrap;}
                .inj-log-tbl tr:nth-child(even) td{background:#f8faff;}
                .inj-log-tbl tr:hover td{background:#eef2ff;}
                </style>""" + f'<div style="overflow-x:auto;max-height:320px;overflow-y:auto;border-radius:10px;border:1.5px solid #e8edf8;">{_inj_html}</div>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIMULATION TABLE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Simulation Table":
    import pandas as pd
    st.markdown('<div class="page-title">Simulation Table</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Daily output — vessel movements, stock levels and discharge events</div>', unsafe_allow_html=True)

    results = st.session_state.get("sim_results")
    if not results:
        st.info("Run the simulation from **Build my JMP → Step 3** to view the simulation table.", icon="📋")
    else:
        df = results["df"].copy()

        # ── Filter bar ─────────────────────────────────────────────────────────
        f1, f2, f3 = st.columns([1, 1, 2])
        with f1:
            months = ["All"] + sorted(df["Month"].dropna().unique().tolist())
            sel_month = st.selectbox("Month", months, key="tbl_month")
        with f2:
            mother_names = [m["name"] for m in st.session_state.mother_vessels]
            sel_vessel = st.selectbox("Discharge includes", ["All"] + mother_names, key="tbl_vessel")

        if sel_month != "All":
            df = df[df["Month"] == sel_month]
        if sel_vessel != "All":
            # filter rows where that mother appears in any discharge column
            dis_cols = [c for c in df.columns if c.startswith("Discharge")]
            mask = df[dis_cols].apply(lambda col: col.astype(str).str.contains(sel_vessel, na=False)).any(axis=1)
            df = df[mask]

        # ── Drop noisy columns for display ─────────────────────────────────────
        drop = [c for c in df.columns if c.endswith(" Prod")] + ["Month",
                "Shuttles In Transit Names"]
        display_df = df.drop(columns=[c for c in drop if c in df.columns])

        # ── Colour styling matching Jupyter output ─────────────────────────────
        mother_caps = {m["name"]: m["cap"] for m in st.session_state.mother_vessels}
        storage_info = {s["name"]: {"min_thr": s["min_thr"], "cap": s["cap"]}
                        for s in st.session_state.storage_vessels}

        VESSEL_COLORS = {
            "Rathbone":     "#f4b183","Woodstock":    "#a9d18e","Laphroaig":    "#9dc3e6",
            "Bagshot":      "#bdd7ee","Bedford":      "#ffe699","Sherlock":     "#e6ccff",
            "Balham":       "#c6e0b4","MT Watson":    "#C65911","MT Santa Monica":"#1F6F78",
            "SanJulian":    "#0F4C5C",
        }

        def _style_cell(val, col_name):
            if col_name.endswith(" Stock") and col_name.replace(" Stock","") in mother_caps:
                mname = col_name.replace(" Stock","")
                cap = mother_caps.get(mname, 1)
                v = float(val) if val else 0
                if v >= cap:   return "background-color:#e84545;color:white;font-weight:600"
                if v >= 0.7*cap: return "background-color:#ffd966;color:black"
                return ""
            if col_name.endswith(" Stock") and col_name.replace(" Stock","") in storage_info:
                sname = col_name.replace(" Stock","")
                si = storage_info[sname]
                v = float(val) if val else 0
                if v <= si["min_thr"]: return "background-color:#00B95F;color:white;font-weight:600"
                if v >= si["cap"]:     return "background-color:#e84545;color:white;font-weight:600"
                return "background-color:#ffd966;color:black"
            if col_name.startswith("Shuttle ") or col_name.startswith("Discharge "):
                s = str(val or "")
                vessel = s.split("->")[0].strip() if "->" in s else s
                c = VESSEL_COLORS.get(vessel, "")
                return f"background-color:{c};color:black;font-weight:600" if c else ""
            return ""

        def _apply_styles(df_s):
            styles = pd.DataFrame("", index=df_s.index, columns=df_s.columns)
            for col in df_s.columns:
                styles[col] = df_s[col].apply(lambda v: _style_cell(v, col))
            return styles

        styled = (display_df.style
                  .apply(_apply_styles, axis=None)
                  .format(na_rep="")
                  .hide(axis="index"))

        _sim_html = styled.to_html()
        sim_table_css = (
            "<style>"
            ".sim-tbl-wrap{background:#fff;}"
            ".sim-tbl-wrap table{border-collapse:collapse;width:max-content;font-size:12px;background:#fff;}"
            ".sim-tbl-wrap th{background:#1a3fc4!important;color:#fff!important;padding:7px 10px;"
            "text-align:center;font-weight:600;white-space:nowrap;position:sticky;top:0;z-index:2;}"
            ".sim-tbl-wrap td{padding:6px 10px;text-align:center;border:1px solid #e2e8f0;"
            "white-space:nowrap;color:#111827!important;background:#ffffff;}"
            ".sim-tbl-wrap td:first-child{color:#111827!important;font-weight:600;"
            "background:#f0f4ff!important;position:sticky;left:0;z-index:1;}"
            ".sim-tbl-wrap tr:nth-child(even) td{background:#f8faff;}"
            "</style>"
        )
        st.markdown(
            sim_table_css +
            '<div class="sim-tbl-wrap" style="overflow-x:auto;border-radius:12px;' +
            'border:1.5px solid #e8edf8;background:#fff;">' +
            _sim_html +
            '</div>',
            unsafe_allow_html=True)

        # ── Download ───────────────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download CSV", data=csv,
                           file_name="simulation_table.csv", mime="text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Summary":
    import pandas as pd
    st.markdown('<div class="page-title">Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Monthly injection tables, totals by mother vessel and SBM discharge schedule</div>', unsafe_allow_html=True)

    results = st.session_state.get("sim_results")
    if not results:
        st.info("Run the simulation from **Build my JMP → Step 3** to view summary tables.", icon="📄")
    else:
        monthly_totals = results.get("monthly_totals")
        monthly_mother = results.get("monthly_mother")
        inj_df         = results.get("inj_df")
        summary_html   = results.get("summary_tables_html", "")

        # ── Monthly totals ─────────────────────────────────────────────────────
        if monthly_totals is not None and not monthly_totals.empty:
            st.markdown('<div class="sec-title"><span>T</span> Monthly Totals</div>', unsafe_allow_html=True)
            disp = monthly_totals[["MonthLabel","Total_Volume","NEPL_Volume","ThirdParty_Volume","Trips"]].copy()
            disp.columns = ["Month","Total Volume (bbls)","NEPL (bbls)","3rd Party (bbls)","Trips"]
            for c in ["Total Volume (bbls)","NEPL (bbls)","3rd Party (bbls)"]:
                disp[c] = disp[c].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "")
            _h = disp.to_html(index=False, border=0, classes="sum-tbl")
            _sum_css = (
                "<style>.sum-tbl{border-collapse:collapse;width:100%;font-size:13px;color:#111827;}"
                ".sum-tbl th{background:#1a3fc4;color:#fff;padding:9px 14px;text-align:left;"
                "font-weight:600;white-space:nowrap;}"
                ".sum-tbl td{padding:8px 14px;border-bottom:1px solid #e8edf8;"
                "color:#111827;background:#fff;white-space:nowrap;}"
                ".sum-tbl tr:nth-child(even) td{background:#f8faff;}"
                ".sum-tbl tr:hover td{background:#eef2ff;}</style>"
            )
            st.markdown(
                _sum_css + f'<div style="overflow-x:auto;border-radius:10px;border:1.5px solid #e8edf8;">{_h}</div>',
                unsafe_allow_html=True)

        # ── By mother vessel ───────────────────────────────────────────────────
        if monthly_mother is not None and not monthly_mother.empty:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="sec-title"><span>M</span> Volume by Mother Vessel</div>', unsafe_allow_html=True)
            disp2 = monthly_mother[["MonthLabel","Vessel","Total_Volume","NEPL_Volume","ThirdParty_Volume","Trips"]].copy()
            disp2.columns = ["Month","Vessel","Total Volume","NEPL","3rd Party","Trips"]
            for c in ["Total Volume","NEPL","3rd Party"]:
                disp2[c] = disp2[c].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "")
            _h2 = disp2.to_html(index=False, border=0, classes="sum-tbl")
            st.markdown(f'<div style="overflow-x:auto;border-radius:10px;border:1.5px solid #e8edf8;">{_h2}</div>', unsafe_allow_html=True)

        # ── Injection tables HTML ──────────────────────────────────────────────
        if summary_html:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="sec-title"><span>I</span> Injection Tables by Month</div>', unsafe_allow_html=True)
            inj_css = """<style>
                .inj-wrap table{border-collapse:collapse;width:max-content;font-size:13px;color:#111827;}
                .inj-wrap th{background:#1a3fc4;color:#fff;padding:8px 14px;text-align:center;font-weight:600;white-space:nowrap;}
                .inj-wrap td{padding:7px 14px;text-align:center;border:1px solid #e2e8f0;color:#111827;white-space:nowrap;background:#fff;}
                .inj-wrap tr:nth-child(even) td{background:#f8faff;}
                .inj-wrap h3{font-size:17px;font-weight:700;color:#1a3fc4;margin:20px 0 10px;}
                </style>"""
            st.markdown(
                inj_css + f'<div class="inj-wrap" style="background:#fff;border:1.5px solid #e8edf8;border-radius:14px;padding:20px 24px;overflow-x:auto;">{summary_html}</div>',
                unsafe_allow_html=True)

        # ── Downloads ──────────────────────────────────────────────────────────
        if inj_df is not None and not inj_df.empty:
            st.markdown("<br>", unsafe_allow_html=True)
            dl_cols = [c for c in inj_df.columns if c not in ["Month","MonthStart"]]
            c1, c2 = st.columns(2)
            with c1:
                csv_inj = inj_df[dl_cols].to_csv(index=False).encode("utf-8")
                st.download_button("⬇ Download Injection Table",
                                   data=csv_inj, file_name="injection_summary.csv", mime="text/csv")
            if monthly_totals is not None and not monthly_totals.empty:
                with c2:
                    csv_tot = monthly_totals.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇ Download Monthly Totals",
                                       data=csv_tot, file_name="monthly_totals.csv", mime="text/csv")

# ══════════════════════════════════════════════════════════════════════════════
# MONTE CARLO RESULTS PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Monte Carlo":
    import pandas as pd
    st.markdown('<div class="page-title">Monte Carlo Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Top 5 best simulation outcomes ranked by your criteria</div>', unsafe_allow_html=True)

    mc = st.session_state.get("mc_results")
    if not mc:
        st.info("Run the Monte Carlo simulation from **Build my JMP → Step 3** first.", icon="🎲")
    else:
        df_kpi    = mc["df_kpi"]
        top5      = mc["top5_results"]
        top5seeds = mc["top5_seeds"]
        weights   = mc["weights"]
        n_runs    = mc["n_runs"]
        n_err     = mc["n_errors"]

        # ── Run stats banner ──────────────────────────────────────────────────
        s1, s2, s3, s4 = st.columns(4, gap="medium")
        for col, (lbl, val, sub) in zip([s1, s2, s3, s4], [
            ("Runs Completed",  f"{n_runs - n_err:,}",  f"{n_err} failed"),
            ("Best Score",      f"{df_kpi['score'].iloc[0]:.3f}", "weighted rank"),
            ("Score Range",     f"{df_kpi['score'].min():.3f} – {df_kpi['score'].max():.3f}", "min → max"),
            ("Best Seed",       str(top5seeds[0]),       "use for deterministic"),
        ]):
            with col:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">{lbl}</div>'                            f'<div class="kpi-value">{val}</div><div class="kpi-sub">{sub}</div></div>',
                            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Top 5 rank cards ──────────────────────────────────────────────────
        st.markdown('<div class="sec-title"><span>★</span> Top 5 Ranked Outcomes</div>', unsafe_allow_html=True)

        RANK_COLORS = ["#1a3fc4","#2952e3","#4a6fe8","#7a96ef","#a8b8f5"]
        MEDAL = ["🥇","🥈","🥉","4th","5th"]

        for rank_i, (seed, res) in enumerate(zip(top5seeds, top5)):
            k = res["kpis"]
            row_score = df_kpi[df_kpi["seed"] == seed]["score"].iloc[0]
            bar_pct = int(row_score * 100)
            col_hex = RANK_COLORS[rank_i]

            st.markdown(f'''
<div style="background:#fff;border:1.5px solid #e8edf8;border-radius:14px;
     padding:16px 20px;margin-bottom:12px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;height:100%;width:{bar_pct}%;
       background:linear-gradient(90deg,{col_hex}12,{col_hex}05);
       border-right:3px solid {col_hex}33;z-index:0;"></div>
  <div style="position:relative;z-index:1;display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
    <div style="font-size:22px;">{MEDAL[rank_i]}</div>
    <div style="flex:1;min-width:120px;">
      <div style="font-size:16px;font-weight:800;color:#0d1b6e;">
        Rank {rank_i+1} &nbsp;·&nbsp; Seed {seed}
      </div>
      <div style="font-size:12px;color:#9aa3bc;">Score: {row_score:.4f}</div>
    </div>
    <div style="display:flex;gap:24px;flex-wrap:wrap;">
      <div style="text-align:center;">
        <div style="font-size:18px;font-weight:800;color:{col_hex};">{k["trips"]}</div>
        <div style="font-size:10px;color:#9aa3bc;text-transform:uppercase;">Trips</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:18px;font-weight:800;color:{col_hex};">{k["nepl_vol"]:,}</div>
        <div style="font-size:10px;color:#9aa3bc;text-transform:uppercase;">NEPL bbls</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:18px;font-weight:800;color:{col_hex};">{k["total_vol"]:,}</div>
        <div style="font-size:10px;color:#9aa3bc;text-transform:uppercase;">Total bbls</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:18px;font-weight:800;color:{col_hex};">{k["tp_vol"]:,}</div>
        <div style="font-size:10px;color:#9aa3bc;text-transform:uppercase;">3rd Party</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:18px;font-weight:800;color:{col_hex};">{k["mother_balance"]:.2f}</div>
        <div style="font-size:10px;color:#9aa3bc;text-transform:uppercase;">Mother Balance</div>
      </div>
    </div>
  </div>
</div>''', unsafe_allow_html=True)

        # ── Use rank buttons ───────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px;color:#6b7a99;margin-bottom:8px;">Load a ranked run into Dashboard / Simulation Table:</div>', unsafe_allow_html=True)
        btn_cols = st.columns(5)
        for bi, (seed, res) in enumerate(zip(top5seeds, top5)):
            with btn_cols[bi]:
                if st.button(f"{MEDAL[bi]} Use Rank {bi+1}", key=f"use_rank_{bi}", use_container_width=True):
                    st.session_state.sim_results   = res
                    st.session_state.sim_seed_used = seed
                    st.session_state.page = "Dashboard"
                    st.rerun()

        # ── Score distribution chart ───────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        try:
            import plotly.express as px
            fig_dist = px.histogram(df_kpi, x="score", nbins=30,
                color_discrete_sequence=["#1a3fc4"])
            # mark top 5
            for i, seed in enumerate(top5seeds):
                sc = df_kpi[df_kpi["seed"] == seed]["score"].iloc[0]
                fig_dist.add_vline(x=sc, line_dash="dot",
                    line_color=RANK_COLORS[i], line_width=2,
                    annotation_text=f"#{i+1}", annotation_position="top")
            fig_dist.update_layout(height=280, margin=dict(l=10,r=10,t=40,b=20),
                title_font=dict(color="#111827", size=14),
                xaxis_title="Weighted Score", yaxis_title="Count",
                showlegend=False,
                paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                font=dict(color="#111827"),
                xaxis=dict(color="#111827", gridcolor="#e2e8f0", linecolor="#cbd5e1",
                           title_font=dict(color="#111827"), tickfont=dict(color="#111827")),
                yaxis=dict(color="#111827", gridcolor="#e2e8f0", linecolor="#cbd5e1",
                           title_font=dict(color="#111827"), tickfont=dict(color="#111827")))
            st.plotly_chart(fig_dist, use_container_width=True)
        except ImportError:
            pass

        # ── Top 5 comparison table ─────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sec-title"><span>C</span> Top 5 Comparison</div>', unsafe_allow_html=True)
        _cmp_rows = []
        for rank_i, (seed, res) in enumerate(zip(top5seeds, top5)):
            k = res["kpis"]
            sc = df_kpi[df_kpi["seed"] == seed]["score"].iloc[0]
            _cmp_rows.append({
                "Rank":             f"{MEDAL[rank_i]} {rank_i+1}",
                "Seed":             seed,
                "Score":            f"{sc:.4f}",
                "SBM Trips":        k["trips"],
                "NEPL (bbls)":      f"{k['nepl_vol']:,}",
                "Total Vol (bbls)": f"{k['total_vol']:,}",
                "3rd Party (bbls)": f"{k['tp_vol']:,}",
                "Mother Balance":   f"{k['mother_balance']:.3f}",
                "Shuttle Vol":      f"{k['shuttle_vol']:,}",
            })
        _cmp_df = pd.DataFrame(_cmp_rows)
        _cmp_html = _cmp_df.to_html(index=False, border=0, classes="cmp-tbl")
        st.markdown("""<style>
            .cmp-tbl{border-collapse:collapse;width:100%;font-size:13px;color:#111827;}
            .cmp-tbl th{background:#1a3fc4;color:#fff;padding:9px 14px;text-align:left;
                font-weight:600;white-space:nowrap;}
            .cmp-tbl td{padding:8px 14px;border-bottom:1px solid #e8edf8;
                color:#111827;background:#fff;white-space:nowrap;}
            .cmp-tbl tr:nth-child(even) td{background:#f8faff;}
            .cmp-tbl tr:hover td{background:#eef2ff;}
            </style>""" + f'<div style="overflow-x:auto;border-radius:10px;border:1.5px solid #e8edf8;">{_cmp_html}</div>',
            unsafe_allow_html=True)

        # ── Overlay chart: NEPL per run, top 5 highlighted ────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        try:
            import plotly.graph_objects as go
            _sorted = df_kpi.sort_values("run_no")
            fig_ov = go.Figure()
            fig_ov.add_trace(go.Scatter(
                x=_sorted["run_no"], y=_sorted["nepl_vol"],
                mode="markers", name="All runs",
                marker=dict(color="#c8d3ee", size=5), opacity=0.6))
            for ri, seed in enumerate(top5seeds):
                row = df_kpi[df_kpi["seed"] == seed].iloc[0]
                fig_ov.add_trace(go.Scatter(
                    x=[row["run_no"]], y=[row["nepl_vol"]],
                    mode="markers+text", name=f"Rank {ri+1}",
                    marker=dict(color=RANK_COLORS[ri], size=12, symbol="star"),
                    text=[f"#{ri+1}"], textposition="top center"))
            fig_ov.update_layout(
                title="NEPL Volume across all runs (top 5 highlighted)",
                title_font=dict(color="#111827", size=14),
                height=300, margin=dict(l=10,r=10,t=40,b=20),
                xaxis_title="Run #", yaxis_title="NEPL Volume (bbls)",
                paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                font=dict(color="#111827"),
                xaxis=dict(color="#111827", gridcolor="#e2e8f0", linecolor="#cbd5e1",
                           title_font=dict(color="#111827"), tickfont=dict(color="#111827")),
                yaxis=dict(color="#111827", gridcolor="#e2e8f0", linecolor="#cbd5e1",
                           title_font=dict(color="#111827"), tickfont=dict(color="#111827")),
                legend=dict(font=dict(color="#111827"), bgcolor="#ffffff",
                            bordercolor="#e2e8f0", borderwidth=1))
            st.plotly_chart(fig_ov, use_container_width=True)
        except ImportError:
            pass

        # ── Criteria weights used ─────────────────────────────────────────────
        with st.expander("Weights used for this run"):
            _wdf = pd.DataFrame([
                {"Criterion": k.replace("_"," ").title(), "Weight": v,
                 "% of Total": f"{100*v/sum(weights.values()):.0f}%" if sum(weights.values()) > 0 else "0%"}
                for k, v in weights.items()
            ])
            _w_html = _wdf.to_html(index=False, border=0, classes="wgt-tbl")
            st.markdown("""<style>
                .wgt-tbl{border-collapse:collapse;width:100%;font-size:13px;color:#111827;}
                .wgt-tbl th{background:#1a3fc4;color:#fff;padding:8px 14px;text-align:left;font-weight:600;}
                .wgt-tbl td{padding:7px 14px;border-bottom:1px solid #e8edf8;color:#111827;background:#fff;}
                .wgt-tbl tr:nth-child(even) td{background:#f8faff;}
                </style>""" + f'<div style="overflow-x:auto;">{_w_html}</div>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 3D SIMULATION PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "3D Simulation":
    import json, pandas as pd
    import streamlit.components.v1 as components

    st.markdown('<div class="page-title">3D Simulation</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Animated vessel movements, tank fills and Gantt timeline</div>', unsafe_allow_html=True)

    results = st.session_state.get("sim_results")
    if not results:
        st.info("Run a simulation from **Build my JMP → Step 3** first, then return here.", icon="🎬")
    else:
        df     = results["df"].copy()
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

        mother_names  = [m["name"] for m in st.session_state.mother_vessels]
        mother_caps   = {m["name"]: m["cap"]            for m in st.session_state.mother_vessels}
        mother_hards  = {m["name"]: m.get("hard",m["cap"]) for m in st.session_state.mother_vessels}
        storage_names = [s["name"] for s in st.session_state.storage_vessels]
        storage_caps  = {s["name"]: s["cap"]      for s in st.session_state.storage_vessels}
        storage_thrs  = {s["name"]: s["min_thr"]  for s in st.session_state.storage_vessels}

        shuttle_cols = [c for c in df.columns if c.startswith("Shuttle ")]
        lp_cols      = [c for c in df.columns if c.startswith("Load Point ")]
        dis_cols_all = [c for c in df.columns if c.startswith("Discharge ")]

        daily_records = []
        for _, row in df.iterrows():
            rec = {"date": row["Date"]}
            rec["mothers"] = {
                m: {"stock": int(row.get(f"{m} Stock", 0) or 0),
                    "cap":   mother_caps.get(m, 490000),
                    "hard":  mother_hards.get(m, 560000)}
                for m in mother_names
            }
            # Include SanJulian as a special roving storage at Bonny
            sj_stock = int(row.get("SanJulian Stock", 0) or 0)
            rec["mothers"]["SanJulian"] = {"stock": sj_stock, "cap": 450000, "hard": 450000}
            rec["storages"] = {
                s: {"stock": int(row.get(f"{s} Stock", 0) or 0),
                    "cap":   storage_caps.get(s, 270000),
                    "thr":   storage_thrs.get(s, 70000)}
                for s in storage_names if f"{s} Stock" in df.columns
            }
            rec["loads"] = []
            for sc, lc in zip(shuttle_cols, lp_cols):
                sv, lv = row.get(sc), row.get(lc)
                if pd.notna(sv) and sv:
                    rec["loads"].append({"shuttle": str(sv), "storage": str(lv) if pd.notna(lv) else ""})
            rec["discharges"] = []
            rec["sj_receives"] = []    # shuttle→SanJulian events
            rec["sj_transfers"] = []   # SanJulian→mother events
            rec["sts_events"] = []     # STS consolidation events
            for dc in dis_cols_all:
                dv = row.get(dc)
                if pd.notna(dv) and dv and "->  " not in str(dv) and "->" in str(dv):
                    raw = str(dv)
                    parts = raw.split("->")
                    sn = parts[0].strip()
                    rest = parts[1].strip()
                    mn = rest.split("(")[0].strip()
                    try:    vol = float(rest.split("(")[1].split(")")[0].replace(",",""))
                    except: vol = 0
                    # Check for STS consolidation marker
                    is_sts = "[rcvd" in raw.lower()
                    if sn == "SanJulian":
                        # SanJulian transloads to mother
                        rec["sj_transfers"].append({"mother": mn, "vol": vol})
                        rec["discharges"].append({"shuttle": "SanJulian", "mother": mn, "vol": vol, "is_sj": True})
                    elif mn == "SanJulian":
                        # Shuttle discharges into SanJulian (overflow)
                        rec["sj_receives"].append({"shuttle": sn, "vol": vol})
                        rec["discharges"].append({"shuttle": sn, "mother": "SanJulian", "vol": vol, "is_sj_recv": True})
                    elif is_sts:
                        # STS consolidated discharge — mark as special
                        rec["discharges"].append({"shuttle": sn, "mother": mn, "vol": vol, "is_sts": True})
                        rec["sts_events"].append({"shuttle": sn, "mother": mn, "vol": vol})
                    else:
                        rec["discharges"].append({"shuttle": sn, "mother": mn, "vol": vol})
            rec["in_transit"]    = int(row.get("Shuttles In Transit", 0) or 0)
            rec["transit_names"] = str(row.get("Shuttles In Transit Names", "") or "")
            daily_records.append(rec)

        import json as _json

        # ── Shuttle state timeline ──────────────────────────────────────────
        # For each shuttle, build: {date -> {state, storage, mother, load_days}}
        # state: "loading" | "transit" | "discharging" | "idle"
        storage_load_times_map = {s["name"]: float(s.get("load_time", 1))
                                   for s in st.session_state.storage_vessels}
        eta_cols = [c for c in df.columns if c.startswith("ETA ")]

        shuttle_timeline = {}  # shuttle_name -> {date_str -> state_dict}
        active_shuttles = [s["name"] for s in st.session_state.shuttle_vessels if s.get("active", True)]
        for shuttle in active_shuttles:
            shuttle_timeline[shuttle] = {}

        # Pass 1 — loading windows, forward transit (loaded), discharge
        for _, row in df.iterrows():
            date_str = row["Date"]
            for sc, lc, vc, ec in zip(shuttle_cols, lp_cols,
                                       [c for c in df.columns if c.startswith("Volume ")],
                                       eta_cols):
                sv = row.get(sc); lv = row.get(lc); ev = row.get(ec)
                if pd.notna(sv) and sv and str(sv).strip() in shuttle_timeline:
                    sname = str(sv).strip()
                    storage = str(lv).strip() if pd.notna(lv) else ""
                    load_days = int(storage_load_times_map.get(storage, 1))
                    load_date = pd.to_datetime(date_str)
                    # Loading window
                    for d_offset in range(load_days):
                        ld = (load_date + pd.Timedelta(days=d_offset)).strftime("%Y-%m-%d")
                        shuttle_timeline[sname][ld] = {
                            "state": "loading", "storage": storage, "load_days": load_days
                        }
                    # Forward transit (loaded → Bonny)
                    if pd.notna(ev):
                        eta_date = pd.to_datetime(ev)
                        td = load_date + pd.Timedelta(days=load_days)
                        while td < eta_date:
                            shuttle_timeline[sname][td.strftime("%Y-%m-%d")] = {
                                "state": "transit_loaded", "storage": storage
                            }
                            td += pd.Timedelta(days=1)

            for dc in dis_cols_all:
                dv = row.get(dc)
                if pd.notna(dv) and dv and "->" in str(dv):
                    parts = str(dv).split("->")
                    sname = parts[0].strip()
                    if sname in shuttle_timeline:
                        rest = parts[1].strip()
                        mn = rest.split("(")[0].strip()
                        try:    vol = float(rest.split("(")[1].rstrip(")").replace(",",""))
                        except: vol = 0
                        shuttle_timeline[sname][date_str] = {
                            "state": "discharging", "mother": mn, "vol": vol
                        }

        # Pass 2 — fill return trip (empty, Bonny → storage)
        # Between discharge day and next load day, the vessel is returning empty
        for sname, tl in shuttle_timeline.items():
            sorted_dates = sorted(tl.keys())
            for i, d in enumerate(sorted_dates):
                if tl[d]["state"] == "discharging":
                    discharge_storage = None
                    # Look ahead for next load event to know which storage to return to
                    for j in range(i+1, len(sorted_dates)):
                        nd = sorted_dates[j]
                        if tl[nd]["state"] == "loading":
                            discharge_storage = tl[nd].get("storage","")
                            # Fill gap days as "returning"
                            disch_dt = pd.to_datetime(d)
                            load_dt  = pd.to_datetime(nd)
                            td = disch_dt + pd.Timedelta(days=1)
                            while td < load_dt:
                                ds = td.strftime("%Y-%m-%d")
                                if ds not in tl:   # don't overwrite existing states
                                    tl[ds] = {"state": "returning", "storage": discharge_storage}
                                td += pd.Timedelta(days=1)
                            break

        # ── Mother SBM injection cycle events ───────────────────────────────
        inj_df_raw = results.get("inj_df")
        sbm_events = []  # list of {mother, ullage, trip_day, discharge_day, return_day}
        if inj_df_raw is not None and not inj_df_raw.empty:
            for _, inj_row in inj_df_raw.iterrows():
                ullage   = pd.to_datetime(inj_row["Final Ullage"]).strftime("%Y-%m-%d")
                trip_day = pd.to_datetime(inj_row["SBM Discharge Day 2"]).strftime("%Y-%m-%d")
                disc_day = pd.to_datetime(inj_row["SBM Discharge Day 3"]).strftime("%Y-%m-%d")
                # Return day = one after disc_day
                ret_day  = (pd.to_datetime(disc_day) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
                sbm_events.append({
                    "mother":    inj_row["Vessel"],
                    "inj_no":    int(inj_row["Injection No"]),
                    "ullage":    ullage,    # Full — departs Bonny toward SBM3
                    "trip":      trip_day,  # Travelling to / arriving SBM3
                    "discharge": disc_day,  # Discharging at SBM3
                    "ret":       ret_day,   # Returning to Bonny, stock reset
                })

        D   = _json.dumps(daily_records)
        M   = _json.dumps(mother_names)
        MC  = _json.dumps(mother_caps)
        SH  = _json.dumps(active_shuttles)
        STL = _json.dumps(shuttle_timeline)   # new: shuttle state timeline
        SBM = _json.dumps(sbm_events)         # new: SBM injection cycle events
        SLT = _json.dumps(storage_load_times_map)  # new: load times per storage

        # Load the HTML template and inject data
        import os as _os

        # Try multiple candidate paths to find sim3d.html
        _candidates = []
        try:    _candidates.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "sim3d.html"))
        except: pass
        _candidates.append(_os.path.join(_os.getcwd(), "sim3d.html"))
        # Also check same dir as the running script
        import sys as _sys
        if _sys.argv and _sys.argv[0]:
            _candidates.append(_os.path.join(_os.path.dirname(_os.path.abspath(_sys.argv[0])), "sim3d.html"))

        _tpl_path = next((_p for _p in _candidates if _os.path.exists(_p)), None)

        if _tpl_path:
            with open(_tpl_path, "r", encoding="utf-8") as _fh:
                _html = _fh.read()
            _html = (_html
                .replace("__DAILY__",    D)
                .replace("__MOTHERS__",  M)
                .replace("__MCAPS__",    MC)
                .replace("__SHUTTLES__", SH)
                .replace("__STL__",      STL)
                .replace("__SBM__",      SBM)
                .replace("__SLT__",      SLT)
            )
        else:
            _searched = "\n".join(_candidates)
            _html = f"""<div style='color:#f85149;background:#161b22;padding:20px;border-radius:8px;font-family:monospace;'>
            <b>⚠ sim3d.html not found</b><br><br>
            Please make sure <code>sim3d.html</code> is in the <b>same folder</b> as <code>app.py</code>.<br><br>
            Searched in:<br><pre>{_searched}</pre>
            Current working directory: <code>{_os.getcwd()}</code>
            </div>"""

        components.html(_html, height=780, scrolling=False)

st.markdown("</div>", unsafe_allow_html=True)
