"""
DSL JMP Simulation Engine
Refactored from notebook into a single callable function: run_simulation(params)

Returns a dict with:
  - df          : daily simulation DataFrame
  - inj_df      : injection/ullage events DataFrame
  - dis_df      : normalized discharge DataFrame
  - monthly_mother  : monthly volume by mother vessel
  - monthly_totals  : monthly totals
  - kpis        : dict with total_vol, nepl_vol, tp_vol, trips
  - summary_tables_html : HTML string of monthly injection summary tables
"""

import re
import json
import random
import warnings
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta, date as date_type

import pandas as pd

warnings.filterwarnings("ignore")

# ── Quality / site mappings ────────────────────────────────────────────────────
SITE_TO_ROW = {
    "Chapel_OML24":      "OML24",
    "Soku Gas Plant":    "Soku Gas Plant",
    "Jasmine S_SOKU":    "SOKU",
    "Chapel_SOKU":       "SOKU",
    "Awoba_OML24":       "AWOBA",
    "Whisky Star XLV":   "WHISKY STAR",
    "Dawes Island":      "DAWES ISLAND",
    "Westmore_Belema":   "BELEMA",
    "Asaramatoru":       "Asaramatoru",
    "Barge Starturn":    "DAWES ISLAND",
    "MT Duke":           "AWOBA",
    "MT Dean":           "OML24",
    "MT Sanbarth_OML24": "OML24",
}

API_BY_SITE = {
    "SOKU":           43.19,
    "OML24":          28.42,
    "BELEMA":         31.00,
    "AWOBA":          40.96,
    "WHISKY STAR":    32.03,
    "DAWES ISLAND":   39.58,
    "Soku Gas Plant": 43.00,
    "Asaramatoru":    30.00,
    "3rd Party Vessel": 41.00,
    "Unknown":        30.00,
}

THIRD_PARTY_API = {
    "ST Zeezee":           41.00,
    "OML18 - MT Holmes":   41.00,
    "OML18 - MT Halima":   41.00,
    "OML18 - MT Moriarty": 41.00,
}

STORAGE_ALIAS = {
    "MT Chapel":                             "Chapel_OML24",
    "MT Chapel - Soku":                      "Chapel_OML24",
    "MT Chapel(Direct from Soku)":           "Chapel_OML24",
    "MT Chapel(Direct from Soku/Starturn)":  "Chapel_OML24",
    "MT Chapel(Partially from Soku direct)": "Chapel_OML24",
    "MT Jasmine S":                          "Jasmine S_SOKU",
    "MT Woodstock - Awoba Storage":          "Awoba_OML24",
    "Whisky Star XLV - Ibom":               "Whisky Star XLV",
    "Barge Starturn-Dawes Island":           "Barge Starturn",
    "MT Westmore":                           "Westmore_Belema",
    "MT Westmore-Belema":                    "Westmore_Belema",
    "MT Westmore_Belema":                    "Westmore_Belema",
    "MT Duke":                               "MT Duke",
    "MT Dean":                               "MT Dean",
    "Asaramatoru":                           "Asaramatoru",
    "Chapel_SOKU":                           "Chapel_SOKU",
}

TARGET_LOAD_REF = {
    "Laphroaig": {"Westmore_Belema": 70000, "Chapel_OML24": 85000, "Jasmine S_SOKU": 90000},
    "Sherlock":  {"Westmore_Belema": 69000, "Chapel_OML24": 83000, "Jasmine S_SOKU": 90000},
    "MT Watson": {"Westmore_Belema": 69000, "Chapel_OML24": 83000, "Jasmine S_SOKU": 90000},
    "Bedford":   {"Whisky Star XLV": 80000, "Chapel_OML24": 63000, "Jasmine S_SOKU": 65000},
    "Balham":    {"Whisky Star XLV": 80000, "Chapel_OML24": 63000, "Jasmine S_SOKU": 65000},
    "Bagshot":   {"Westmore_Belema": 36000, "Awoba_OML24": 40000, "Chapel_OML24": 43000, "Jasmine S_SOKU": 45000},
    "Woodstock": {"Dawes Island": 42000, "Awoba_OML24": 40000, "Chapel_OML24": 42000, "Jasmine S_SOKU": 44000},
    "Rathbone":  {"Soku Gas Plant": 26000, "Dawes Island": 44000, "Westmore_Belema": 37000,
                  "Awoba_OML24": 41000, "Chapel_OML24": 44000, "Jasmine S_SOKU": 46000},
    "MT Santa Monica": {"Asaramatoru": 12000, "Soku Gas Plant": 15000, "Awoba_OML24": 24000,
                         "Chapel_OML24": 26000, "Jasmine S_SOKU": 27000},
}

LOAD_FACTOR_BY_STORAGE = {
    "Awoba_OML24":    0.70,
    "Soku Gas Plant": 0.30,
    "Asaramatoru":    0.20,
    "Dawes Island":   0.65,
    "Westmore_Belema": 0.80,
}

TRUE_CAP_BY_SHUTTLE = {
    "Bagshot":        120000,
    "Woodstock":       90000,
    "Rathbone":        80000,
    "Balham":         150000,
    "Laphroaig":      250000,
    "Sherlock":       250000,
    "Bedford":        150000,
    "MT Watson":      250000,
    "MT Berners":     250000,
    "MT Santa Monica": 40000,
}


# ── Stock sheet mapping (used when datahub_file uploaded) ──────────────────────
STOCK_SHEET_MAP = {
    "mothers": {
        "Green Eagle": {"sheet": "MT Green_Eagle Daily Stock",  "date_col": "DATE", "stock_col": "TOV"},
        "Alkebulan":   {"sheet": "MT Alkebulan Daily Stock",     "date_col": "DATE", "stock_col": "TOV"},
        "Bryanston":   {"sheet": "MT Bryanston Daily Stock",     "date_col": "DATE", "stock_col": "TOV"},
    },
    "storages": {
        "Westmore_Belema": {"sheet": "Belema Daily Stock",         "date_col": "Date", "stock_col": "Daily Stock Balance (TOV in bbls)"},
        "Barge Starturn":  {"sheet": "Petralon_54 Daily Stock",    "date_col": "Date", "stock_col": "Daily Stock Balance (TOV in bbls)"},
        "Whisky Star XLV": {"sheet": "Ibom Daily Stock",           "date_col": "Date", "stock_col": "Daily Stock Balance (TOV in bbls)"},
        "Awoba_OML24":     {"sheet": "Awoba Daily Stock",          "date_col": "Date", "stock_col": "Daily Stock Balance (TOV in bbls)"},
        "Chapel_OML24":    {"sheet": "OML24 Daily Stock Repo",     "date_col": "Date", "stock_col": "Daily Stock balance (TOV in bbl)"},
        "Jasmine S_SOKU":  {"sheet": "Sanbarth Daily Stock",       "date_col": "Date", "stock_col": "Daily Stock Balance (TOV in bbls)"},
    },
}

def _get_latest_stock(wb, sheet_name, date_col, stock_col, asof_date):
    """Read latest stock value from an Excel workbook for a given date."""
    try:
        import pandas as _pd
        import io as _io
        # BytesIO must be rewound before each read_excel call
        if hasattr(wb, "seek"):
            wb.seek(0)
        df = _pd.read_excel(wb, sheet_name=sheet_name)
        if date_col not in df.columns or stock_col not in df.columns:
            return None
        df[date_col] = _pd.to_datetime(df[date_col], errors="coerce").dt.normalize()
        df[stock_col] = _pd.to_numeric(
            df[stock_col].astype(str).str.replace(",", "", regex=False).str.strip(),
            errors="coerce"
        )
        df = df.dropna(subset=[date_col, stock_col]).sort_values(date_col)
        asof = _pd.to_datetime(asof_date).normalize()
        exact = df[df[date_col] == asof]
        if not exact.empty:
            return float(exact.iloc[-1][stock_col])
        prior = df[df[date_col] < asof]
        if not prior.empty:
            return float(prior.iloc[-1][stock_col])
        return None
    except Exception:
        return None

def initialize_stocks_from_datahub(datahub_file, asof_date, mothers_dict, storages_dict):
    """
    Update stock values in mothers_dict and storages_dict from the DSL Datahub Excel file.
    Reads each named sheet from STOCK_SHEET_MAP and overwrites stock where data is found.
    datahub_file must already be a BytesIO (pre-read bytes).
    """
    if datahub_file is None:
        return
    import pandas as _pd
    import io as _io

    # Accept BytesIO directly (pre-read by caller) or a raw file path
    if hasattr(datahub_file, "read"):
        raw = datahub_file.read()
        wb_bytes = raw
    else:
        with open(datahub_file, "rb") as _f:
            wb_bytes = _f.read()

    for mname, cfg in STOCK_SHEET_MAP["mothers"].items():
        if mname not in mothers_dict:
            continue
        val = _get_latest_stock(
            _io.BytesIO(wb_bytes), cfg["sheet"], cfg["date_col"], cfg["stock_col"], asof_date
        )
        if val is not None:
            mothers_dict[mname]["stock"] = float(val)

    for sname, cfg in STOCK_SHEET_MAP["storages"].items():
        if sname not in storages_dict:
            continue
        val = _get_latest_stock(
            _io.BytesIO(wb_bytes), cfg["sheet"], cfg["date_col"], cfg["stock_col"], asof_date
        )
        if val is not None:
            storages_dict[sname]["stock"] = float(val)

THIRD_PARTY_VESSELS_DEFAULT = [
    {"name": "ST Zeezee",          "cap": 92034, "freq": 20, "next_arrival": datetime(2026, 3, 23)},
    {"name": "OML18 - MT Holmes",  "cap": 79000, "freq": 7,  "next_arrival": datetime(2027, 2, 5),
     "end_date": datetime(2027, 3, 31)},
    {"name": "OML18 - MT Halima",  "cap": 82907, "freq": 7,  "next_arrival": datetime(2027, 2, 5)},
    {"name": "OML18 - MT Moriarty","cap": 81470, "freq": 7,  "next_arrival": datetime(2027, 2, 5),
     "end_date": datetime(2027, 3, 31)},
]

PRODUCTION_LINES = {
    "Soku":           {"target": "Jasmine S_SOKU",   "rate": 36900, "start_date": datetime(2026, 3, 9)},
    "Soku Gas Plant": {"target": "Soku Gas Plant",    "rate": 700,   "start_date": datetime(2026, 1, 1)},
    "OML24":          {"target": "Chapel_OML24",      "rate": 44800, "start_date": datetime(2026, 1, 1)},
    "Awoba":          {"target": "Awoba_OML24",       "rate": 6900,  "start_date": datetime(2026, 3, 9)},
    "Whisky Star XLV":{"target": "Whisky Star XLV",  "rate": 3800,  "start_date": datetime(2026, 3, 9)},
    "Dawes Island":   {"target": "Dawes Island",      "rate": 950,   "start_date": datetime(2026, 3, 9)},
    "Westmore_Belema":{"target": "Westmore_Belema",   "rate": 20615, "start_date": datetime(2026, 2, 26)},
    "Asaramatoru":    {"target": "Asaramatoru",       "rate": 1000,  "start_date": datetime(2026, 2, 21)},
}

WHISKY_SITE = "Whisky Star XLV"
WHISKY_STATION_SHUTTLES = {"Balham", "Bedford"}
STS_TRANSLOAD_START = datetime(2026, 4, 1)
DEFAULT_TRUE_CAP_FACTOR = 1.35


# ══════════════════════════════════════════════════════════════════════════════
# PURE HELPER FUNCTIONS (no global state)
# ══════════════════════════════════════════════════════════════════════════════

def _to_dt(val):
    if val is None:
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, date_type):
        return datetime(val.year, val.month, val.day)
    return pd.to_datetime(val).to_pydatetime()


def blend_quality(cur_stock, cur_api, in_vol, in_api):
    cur_stock = float(cur_stock or 0)
    in_vol = float(in_vol or 0)
    denom = cur_stock + in_vol
    if denom <= 0:
        return cur_api
    if in_api is None:
        return cur_api
    if cur_stock <= 0 or cur_api is None:
        return float(in_api)
    return (float(cur_api) * cur_stock + float(in_api) * in_vol) / denom


def get_incoming_api(source_storage, third_party_names):
    if source_storage in third_party_names:
        return float(THIRD_PARTY_API.get(source_storage, API_BY_SITE.get("3rd Party Vessel", 41.0)))
    site = SITE_TO_ROW.get(str(source_storage).strip() if source_storage else "", "Unknown")
    return API_BY_SITE.get(site, None)


def norm_storage_name(x):
    if x is None:
        return None
    x = str(x).strip().replace("\xa0", " ")
    return STORAGE_ALIAS.get(x, x)


def randomized_production(rate):
    variation = rate * 0.005
    return round(rate + random.uniform(-variation, variation))


def get_variable_load_volume(shuttle_name, stg_name, shuttles):
    sh = shuttles[shuttle_name]
    base = float(sh.get("eff_cap", sh["cap"]))
    ref = TARGET_LOAD_REF.get(shuttle_name, {}).get(stg_name)
    if ref is None:
        f = float(LOAD_FACTOR_BY_STORAGE.get(stg_name, 1.0))
        return base * f * random.uniform(0.97, 1.03)
    ratio = max(0.45, min(1.20, float(ref) / base if base > 0 else 1.0))
    vol = base * ratio * random.uniform(0.96, 1.04)
    lo, hi = 0.92 * ref, 1.08 * ref
    return max(lo, min(hi, vol))


def tide_adjust_eta(base_eta, load_complete, adj_map):
    sail_day = (_to_dt(load_complete) + timedelta(days=1)).date()
    tide_sum = int(adj_map.get(sail_day, 0))
    if tide_sum < 0:
        return _to_dt(base_eta)
    return _to_dt(base_eta) + timedelta(days=1)


def load_tide_adjustments(file_a, file_b, date_col="Date", cat_col="Category", default_year=None):
    def _read(path):
        df = pd.read_excel(path)
        if date_col not in df.columns or cat_col not in df.columns:
            return pd.DataFrame({"Date": [], "Category": []})
        df = df[[date_col, cat_col]].copy()
        s = df[date_col].astype(str).str.strip()
        dt = pd.to_datetime(s, errors="coerce", dayfirst=True)
        bad = dt.isna()
        if bad.any():
            dt2 = pd.to_datetime(s[bad], errors="coerce", format="%d-%b")
            dt.loc[bad] = dt2
        if default_year is not None:
            def fix_yr(x):
                if pd.isna(x):
                    return x
                if getattr(x, "year", None) == 1900:
                    return x.replace(year=default_year)
                return x
            dt = dt.map(fix_yr)
        out = pd.DataFrame({
            "Date": pd.to_datetime(dt, errors="coerce").dt.date,
            "Category": pd.to_numeric(df[cat_col], errors="coerce").fillna(0).astype(int),
        }).dropna(subset=["Date"])
        return out.groupby("Date", as_index=False)["Category"].sum()

    A = _read(file_a).rename(columns={"Category": "CatA"})
    B = _read(file_b).rename(columns={"Category": "CatB"})
    merged = A.merge(B, on="Date", how="outer")
    merged["CatA"] = merged["CatA"].fillna(0).astype(int)
    merged["CatB"] = merged["CatB"].fillna(0).astype(int)
    merged["Adj"] = (merged["CatA"] + merged["CatB"]).astype(int)
    return dict(zip(merged["Date"], merged["Adj"]))



def load_tide_lookup_from_pdf(pdf_path_or_file) -> dict:
    """
    Parse a Q2 tide PDF (San Barth format) into {date: [(hour, height), ...]}
    Accepts either a file path string or an uploaded file object (BytesIO / UploadedFile).
    """
    try:
        from PyPDF2 import PdfReader
        import re as _re
        from datetime import datetime as _dt
        reader = PdfReader(pdf_path_or_file)
        full_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        lines = [ln.strip() for ln in full_text.splitlines() if ln.strip()]
        tide_lookup = {}
        current_date = None
        date_pat = _re.compile(r"^(\d{2}/\d{2}/\d{4})$")
        tide_pat = _re.compile(r"^(\d{2}):\d{2}\s+([0-9.]+)\s*m$")
        for line in lines:
            dm = date_pat.match(line)
            if dm:
                current_date = _dt.strptime(dm.group(1), "%d/%m/%Y").date()
                tide_lookup.setdefault(current_date, [])
                continue
            tm = tide_pat.match(line)
            if tm and current_date is not None:
                tide_lookup[current_date].append((int(tm.group(1)), float(tm.group(2))))
        return tide_lookup
    except Exception:
        return {}

def apply_pdf_tide_delay(origin_storage, loading_complete_dt, eta_to_bonny_dt, tide_lookup: dict):
    """
    Delay ETA by 1 day if no high tide (>1.9m before 1pm) on the sailing day.
    Only applies to Jasmine S_SOKU and Chapel_OML24.
    """
    from datetime import timedelta as _td
    storage = str(origin_storage).strip()
    if storage not in {"Jasmine S_SOKU", "Chapel_OML24"}:
        return eta_to_bonny_dt
    try:
        load_dt = _to_dt(loading_complete_dt)
        eta_dt  = _to_dt(eta_to_bonny_dt)
        check_date = (load_dt + _td(days=1)).date()
        day_tides = tide_lookup.get(check_date, [])
        if any(hour < 13 and height > 1.9 for hour, height in day_tides):
            return eta_dt           # good tide — no delay
        return eta_dt + _td(days=1) # no good tide — add 1 day
    except Exception:
        return eta_to_bonny_dt


def load_tide_adjustments_pdf(pdf_file, default_year=None):
    """
    Parse tide adjustment data from a PDF file.
    Looks for table rows containing dates and tide categories (e.g. HW/LW, Neap/Spring).
    Returns same format as load_tide_adjustments: {date -> adjustment_sum}.
    """
    try:
        import pdfplumber
    except ImportError:
        return {}

    import io, re
    from datetime import date as _date

    tide_map = {}
    try:
        raw = pdf_file.read() if hasattr(pdf_file, 'read') else open(pdf_file, 'rb').read()
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            for page in pdf.pages:
                # Try table extraction first
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if not row:
                            continue
                        # Look for a date cell and a category cell
                        date_val = None
                        cat_val = None
                        for cell in row:
                            if not cell:
                                continue
                            cell_str = str(cell).strip()
                            # Try to parse as date
                            if date_val is None:
                                for fmt in ["%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%d-%b-%Y",
                                            "%d/%m", "%d-%b", "%d %b"]:
                                    try:
                                        dt = pd.to_datetime(cell_str, format=fmt, dayfirst=True)
                                        if default_year and dt.year == 1900:
                                            dt = dt.replace(year=default_year)
                                        date_val = dt.date()
                                        break
                                    except Exception:
                                        pass
                            # Look for tide category keywords
                            if cat_val is None and re.search(
                                    r'neap|spring|hw|lw|high|low|restrict|adverse', cell_str, re.I):
                                cat_val = cell_str.lower()
                        if date_val is not None and cat_val is not None:
                            # Adverse conditions add a delay (+1 day); favourable = 0
                            adj = -1 if re.search(r'neap|adverse|restrict|lw|low', cat_val) else 0
                            tide_map[date_val] = tide_map.get(date_val, 0) + adj

                # Fallback: plain text extraction
                if not tide_map:
                    text = page.extract_text() or ""
                    for line in text.split("\n"):
                        line = line.strip()
                        date_val = None
                        for fmt in ["%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%d-%b-%Y"]:
                            for tok in line.split():
                                try:
                                    dt = pd.to_datetime(tok, format=fmt, dayfirst=True)
                                    if default_year and dt.year == 1900:
                                        dt = dt.replace(year=default_year)
                                    date_val = dt.date()
                                    break
                                except Exception:
                                    pass
                            if date_val:
                                break
                        if date_val:
                            lower = line.lower()
                            adj = -1 if re.search(r'neap|adverse|restrict|lw|low', lower) else 0
                            tide_map[date_val] = tide_map.get(date_val, 0) + adj
    except Exception:
        pass

    return tide_map


def normalize_shuttle_name(x, shuttles_dict):
    if pd.isna(x):
        return None
    raw = str(x).strip().replace("\xa0", " ")
    if raw in shuttles_dict:
        return raw
    s = re.sub(r"^(MT|M/T)\s+", "", raw, flags=re.IGNORECASE).strip()
    s = s.split("-")[0].strip()
    if s in shuttles_dict:
        return s
    return s


def should_skip_discharge_mother(mother_name, mothers_dict):
    if pd.isna(mother_name):
        return True
    m = str(mother_name).strip().replace("\xa0", " ")
    if "bonny operations" in m.lower():
        return True
    if m not in mothers_dict:
        return True
    return False


def parse_discharge_label(dis_str):
    if not isinstance(dis_str, str) or "->" not in dis_str:
        return None, None, 0.0
    vessel, rest = dis_str.split("->", 1)
    vessel = vessel.strip()
    mother = rest.split("(")[0].strip()
    m = re.search(r"\(([\d,]+(?:\.\d+)?)\)", rest)
    vol = float(m.group(1).replace(",", "")) if m else 0.0
    return vessel, mother, vol


def ensure_is_third_party(dis_df):
    dis_df = dis_df.copy()
    ps = dis_df.get("production_site", pd.Series("", index=dis_df.index)).astype(str).str.strip().str.lower()
    src = dis_df.get("source", pd.Series("", index=dis_df.index)).astype(str).str.strip().str.lower()
    base = dis_df.get("is_third_party", pd.Series(False, index=dis_df.index)).fillna(False).astype(bool)
    base |= ps.isin(["3rd party", "third party", "3rdparty", "3rd party vessel"])
    base |= src.isin(["3rd party", "third party", "3rdparty"])
    dis_df["IsThirdParty"] = base
    return dis_df


def build_prescribed_events_from_excel(filepath, sheet_name, sim_start, sim_end, shuttles_dict, mothers_dict, third_party_names):
    c_vessel     = "Vessel Name"
    c_load_date  = "SanBarth/Awoba Arrival Date (Moored to Main Storage)"
    c_load_stg   = "Main Storage Vessel"
    c_load_qty   = "Received Qty. (GOV in bbls) from Main Storage Vessel"
    c_mother     = "Storage @ Bonny Terminal"
    c_disch_date = "Actual Date for completing discharge to Storage @ Bonny Terminal"
    c_disch_qty_primary  = "Discharged Qty (GOV in bbls) to Storage @ Bonny Terminal"
    c_disch_qty_fallback = "Received Qty (GOV in bbls) by Storage @ Bonny Terminal"

    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
    except Exception as e:
        raise ValueError(f"Could not read Excel file: {e}")

    missing = [c for c in [c_vessel, c_load_date, c_load_stg, c_load_qty, c_mother, c_disch_date] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    c_disch_qty = c_disch_qty_primary if c_disch_qty_primary in df.columns else c_disch_qty_fallback
    if c_disch_qty not in df.columns:
        raise ValueError("Missing discharge quantity column.")

    df = df.rename(columns={
        c_vessel: "vessel", c_load_date: "load_date", c_load_stg: "load_storage",
        c_load_qty: "load_qty", c_mother: "mother", c_disch_date: "disch_date", c_disch_qty: "disch_qty",
    })

    for col in ["vessel", "load_storage", "mother"]:
        df[col] = df[col].astype(str).str.strip().replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})

    df["load_qty"]  = pd.to_numeric(df["load_qty"], errors="coerce")
    df["disch_qty"] = pd.to_numeric(df["disch_qty"], errors="coerce")
    df["load_date"]  = pd.to_datetime(df["load_date"], errors="coerce").dt.normalize()
    df["disch_date"] = pd.to_datetime(df["disch_date"], errors="coerce").dt.normalize()

    sim_start = pd.to_datetime(sim_start).normalize()
    sim_end   = pd.to_datetime(sim_end).normalize()

    in_window = (
        df["load_date"].between(sim_start, sim_end, inclusive="both")
        | df["disch_date"].between(sim_start, sim_end, inclusive="both")
    )
    df = df.loc[in_window].copy()

    def normalize_vessel_any(v):
        v = str(v).strip().replace("\xa0", " ")
        if v in shuttles_dict or v in third_party_names:
            return v
        return normalize_shuttle_name(v, shuttles_dict)

    df["vessel"] = df["vessel"].map(normalize_vessel_any)
    allowed = set(shuttles_dict.keys()) | set(third_party_names)
    df = df[df["vessel"].isin(allowed)].copy()

    def map_storage(x):
        if pd.isna(x):
            return pd.NA
        x = str(x).strip()
        return STORAGE_ALIAS.get(x, x)

    df["load_storage"] = df["load_storage"].map(map_storage)

    events = []
    for _, r in df.iterrows():
        vessel = r["vessel"]
        if not vessel or pd.isna(vessel):
            continue

        load_dt  = r.get("load_date")
        disch_dt = r.get("disch_date")
        load_storage = r.get("load_storage")
        load_qty  = r.get("load_qty")
        disch_qty = r.get("disch_qty")

        discharge_mother = None
        if pd.notna(r.get("mother")):
            m = str(r["mother"]).strip().replace("\xa0", " ")
            if not should_skip_discharge_mother(m, mothers_dict):
                discharge_mother = m

        if (pd.notna(load_dt) and sim_start <= load_dt <= sim_end
                and pd.notna(load_storage) and pd.notna(load_qty) and float(load_qty) > 0):
            events.append({
                "date": load_dt.to_pydatetime(),
                "shuttle": vessel,
                "action": "load",
                "storage": load_storage,
                "load_qty": float(load_qty),
                "mother": discharge_mother,
                "source": load_storage,
                "disch_date": disch_dt.to_pydatetime() if pd.notna(disch_dt) else None,
                "disch_qty": float(disch_qty) if pd.notna(disch_qty) else None,
                "prescribed": True,
            })

        if (pd.notna(disch_dt) and sim_start <= disch_dt <= sim_end
                and pd.notna(disch_qty) and float(disch_qty) > 0):
            events.append({
                "date": disch_dt.to_pydatetime(),
                "disch_date": disch_dt.to_pydatetime(),
                "shuttle": vessel,
                "action": "discharge",
                "mother": discharge_mother,
                "volume": float(disch_qty),
                "source": load_storage,
                "prescribed": True,
            })

    events.sort(key=lambda e: (e["date"], e["shuttle"], e["action"]))
    return events


# ══════════════════════════════════════════════════════════════════════════════
# MAIN SIMULATION FUNCTION
# ══════════════════════════════════════════════════════════════════════════════


def run_simulation(params):
    """
    params keys (all from st.session_state):
      sim_start, sim_end, start_inj_no, pause_days, whisky_trigger,
      sanjulian_cap, alk_stop, sanjulian_start, prescribed_end,
      whisky_win_start, whisky_win_end,
      mother_vessels   : list of dicts {name, cap, hard, stock, retire}
      shuttle_vessels  : list of dicts {name, cap, lead, start, active, allowed}
      storage_vessels  : list of dicts {name, stock, min_thr, cap, load_time, start}
      manual_events    : list of dicts {date, shuttle, storage, volume}
      datahub_file     : uploaded file object or None
      tide_a_file      : uploaded file object or None
      tide_b_file      : uploaded file object or None
      seed             : int or None — if set, fixes random seed for deterministic output
    """

    # ── 0. Set random seed if provided ────────────────────────────────────────
    _seed = params.get("seed", None)
    if _seed is not None:
        random.seed(int(_seed))
    else:
        random.seed(None)   # truly random

    # ── 1. Parse params ────────────────────────────────────────────────────────
    sim_start      = _to_dt(params["sim_start"])
    sim_end        = _to_dt(params["sim_end"])
    START_INJ_NO   = int(params.get("start_inj_no", 138))
    MOTHER_PAUSE_DAYS = int(params.get("pause_days", 3))
    WHISKY_TRIGGER = float(params.get("whisky_trigger", 83000))
    SANJULIAN_CAP  = float(params.get("sanjulian_cap", 450000))
    ALK_STOP_DATE  = _to_dt(params.get("alk_stop", datetime(2026, 3, 31))).date()
    SANJULIAN_START = _to_dt(params.get("sanjulian_start", datetime(2026, 4, 1)))
    PRESCRIBED_END  = _to_dt(params.get("prescribed_end", datetime(2026, 3, 12))).date()
    WHISKY_WIN_START = _to_dt(params.get("whisky_win_start", datetime(2026, 3, 11))).date()
    WHISKY_WIN_END   = _to_dt(params.get("whisky_win_end", datetime(2026, 6, 30))).date()
    SANJULIAN_LEAD_TO_MOTHER = 1
    STS_TRANSLOAD_START_DT = _to_dt(params.get("sts_start", datetime(2026, 4, 1)))

    # ── 2. Build mothers dict ──────────────────────────────────────────────────
    mothers = {}
    for m in params["mother_vessels"]:
        retire_dt = _to_dt(m.get("retire")) if m.get("retire") else None
        mothers[m["name"]] = {
            "cap":          float(m["cap"]),
            "hard_cap":     float(m.get("hard", m["cap"])),
            "stock":        float(m["stock"]),
            "api":          32.0,
            "is_full":      False,
            "stock_at_full": None,
            "available_on": sim_start,
            "end_date":     retire_dt,
            "pause_counter": 0,
        }

    MOTHER_CAPS = {n: float(d["cap"]) for n, d in mothers.items()}
    MOTHER_STOCK_COL = {n: f"{n} Stock" for n in mothers}

    # ── 3. Build shuttles dict ─────────────────────────────────────────────────
    shuttles = {}
    for s in params["shuttle_vessels"]:
        if not s.get("active", True):
            continue
        name = s["name"]
        cap = float(s["cap"])
        eff = round(cap * 1.07, 0)
        # Check roving_vessels override for true_cap and participation
        _rv_cfg = {rv["name"]: rv for rv in params.get("roving_vessels", []) if rv.get("enabled", True)}
        _default_true_cap = float(TRUE_CAP_BY_SHUTTLE.get(name, round(eff * DEFAULT_TRUE_CAP_FACTOR, 0)))
        _true_cap = float(_rv_cfg[name]["true_cap"]) if name in _rv_cfg else _default_true_cap
        shuttles[name] = {
            "cap":          cap,
            "eff_cap":      eff,
            "lead":         int(s.get("lead", 1)),
            "start_date":   _to_dt(s.get("start", sim_start)),
            "allowed_storages": list(s.get("allowed", [])),
            "available_on": sim_start,
            "cargo_info":   None,
            "waiting_for_mother": False,
            "on_station":   None,
            "station_until": None,
            "station_locked_until": None,
            "true_cap":     _true_cap,
            "roving_enabled": name in _rv_cfg,  # only enabled vessels participate in STS
        }

    THIRD_PARTY_NAMES = {v["name"] for v in THIRD_PARTY_VESSELS_DEFAULT}

    # ── 4. Build storages dict ─────────────────────────────────────────────────
    storages = {}
    storage_load_times = {}
    for stg in params["storage_vessels"]:
        name = stg["name"]
        storages[name] = {
            "stock":         float(stg["stock"]),
            "min_threshold": float(stg.get("min_thr", 0)),
            "cap":           float(stg["cap"]),
            "start_date":    _to_dt(stg.get("start", sim_start)),
        }
        storage_load_times[name] = float(stg.get("load_time", 1))

    # ── 5. SanJulian ──────────────────────────────────────────────────────────
    sanjulian = {
        "name": "SanJulian",
        "cap":  SANJULIAN_CAP,
        "hard_cap": SANJULIAN_CAP,
        "stock": 0.0,
        "api":  None,
        "available_on": SANJULIAN_START,
        "waiting_for_mother": False,
        "target_mother": None,
        "transfer_eta": None,
        "received_today_on": None,
        "received_today_from": None,
    }

    # ── 6. Tide PDF (San Barth format — single file) ─────────────────────────
    PDF_TIDE_LOOKUP = {}
    tide_pdf = params.get("tide_pdf_file")
    if tide_pdf is not None:
        try:
            if hasattr(tide_pdf, "seek"):
                tide_pdf.seek(0)
            PDF_TIDE_LOOKUP = load_tide_lookup_from_pdf(tide_pdf)
        except Exception:
            pass
    # ── 7. Prescribed events ───────────────────────────────────────────────────
    pre_scheduled_events = []
    datahub = params.get("datahub_file")
    _stock_init_error = None
    if datahub is not None:
        import io as _io
        # datahub is a BytesIO pre-read by app.py — get raw bytes once
        try:
            datahub.seek(0)
            _datahub_bytes = datahub.read()
        except Exception as _e:
            _datahub_bytes = None
            _stock_init_error = f"Could not read datahub bytes: {_e}"

        if _datahub_bytes:
            # ── Prescribed events ────────────────────────────────────────────
            try:
                pre_scheduled_events = build_prescribed_events_from_excel(
                    _io.BytesIO(_datahub_bytes), "Shuttle Vessel ",
                    sim_start, sim_end, shuttles, mothers, THIRD_PARTY_NAMES
                )
            except Exception:
                pass
            # ── Stock init (STOCK_SHEET_MAP) — overwrites UI param defaults ──
            try:
                initialize_stocks_from_datahub(
                    _io.BytesIO(_datahub_bytes), sim_start, mothers, storages
                )
            except Exception as _e:
                _stock_init_error = str(_e)

    # ── 8. Whisky interchange windows ─────────────────────────────────────────
    WHISKY_INTERCHANGE_WINDOWS = [{
        "start":     WHISKY_WIN_START,
        "end":       WHISKY_WIN_END,
        "stationed": "Bedford",
        "shuttling": "Balham",
    }]

    # ── 9. Manual override events from session state ───────────────────────────
    MANUAL_EVENTS = []
    for ev in params.get("manual_events", []):
        _ev_action  = str(ev.get("action", "load")).strip().lower()
        _ev_storage = ev.get("storage")
        _ev_mother  = ev.get("mother")
        _ev_shuttle = ev.get("shuttle", "")
        _ev_tag     = f"manual_{_ev_shuttle}_{_ev_storage or _ev_mother or _ev_action}"
        MANUAL_EVENTS.append({
            "date":    _to_dt(ev["date"]),
            "action":  _ev_action,
            "shuttle": _ev_shuttle,
            "storage": _ev_storage,
            "volume":  float(ev["volume"]) if ev.get("volume") else None,
            "mother":  _ev_mother,
            "tag":     _ev_tag,
        })

    # ── 10. Third-party vessels (deep copy so next_arrival advances per run) ───
    import copy
    third_party_vessels = copy.deepcopy(THIRD_PARTY_VESSELS_DEFAULT)
    for tv in third_party_vessels:
        tv["next_arrival"] = _to_dt(tv["next_arrival"])

    # ══════════════════════════════════════════════════════════════════════════
    # CLOSURE-STYLE HELPERS (access mutable state via enclosing scope)
    # ══════════════════════════════════════════════════════════════════════════

    # mutable state
    active_pause_mother = [None]   # wrap in list so closures can mutate
    active_pause_until  = [None]
    waiting_full = []
    shuttle_arrivals_pending = []
    loading_paused_until = {stg: None for stg in storages}
    mother_busy_until = {n: sim_start for n in mothers}
    normalized_discharges = []
    WHISKY_DAILY_BLOCK = set()

    def _apm():   return active_pause_mother[0]
    def _apu():   return active_pause_until[0]

    def mother_return_day(filled_on_date):
        return filled_on_date + timedelta(days=MOTHER_PAUSE_DAYS)

    def mother_is_active(mname, current_day):
        if mname not in mothers:
            return False
        m = mothers[mname]
        day = _to_dt(current_day)
        avail = _to_dt(m.get("available_on", sim_start))
        if day < avail:
            return False
        end = m.get("end_date")
        if end is not None and day > _to_dt(end):
            return False
        return True

    def storage_is_active(stg_name, current_day):
        stg = storages.get(stg_name)
        if stg is None:
            return False
        day = _to_dt(current_day)
        if day < _to_dt(stg.get("start_date", sim_start)):
            return False
        if stg.get("end_date") and day > _to_dt(stg["end_date"]):
            return False
        return True

    def storage_fullness(stg_name):
        stg = storages[stg_name]
        cap = float(stg.get("cap", 1) or 1)
        return float(stg.get("stock", 0.0)) / cap

    def apply_mother_discharge(mname, volume, current_day, prescribed=False, incoming_api=None):
        if not mother_is_active(mname, current_day):
            return False
        m = mothers[mname]
        vol = float(volume)
        apm = _apm()
        if (mname == apm
                or any(x["mother"] == mname for x in waiting_full)
                or m.get("is_full", False)):
            return False
        soft_cap = float(m.get("cap", 0))
        hard_cap = float(m.get("hard_cap", soft_cap))
        if (m["stock"] + vol) > hard_cap:
            return False
        cur_stock = float(m.get("stock", 0.0))
        cur_api   = m.get("api")
        m["stock"] = cur_stock + vol
        m["api"] = blend_quality(cur_stock, cur_api, vol, incoming_api)
        if m["stock"] >= soft_cap:
            m["is_full"] = True
            if m.get("stock_at_full") is None:
                m["stock_at_full"] = m["stock"]
            filled_on = pd.to_datetime(current_day).date()
            if active_pause_mother[0] is None:
                active_pause_mother[0] = mname
                active_pause_until[0]  = mother_return_day(filled_on)
            else:
                waiting_full.append({"mother": mname, "filled_on": filled_on})
        return True

    def pick_available_mother(current_day, mothers_loaded_today, volume=None):
        wf_set = {x["mother"] for x in waiting_full}
        eligible = []
        for mname, m in mothers.items():
            if not mother_is_active(mname, current_day):
                continue
            if mname == _apm():
                continue
            if mname in wf_set:
                continue
            if m.get("is_full", False):
                continue
            if _to_dt(current_day) < mother_busy_until.get(mname, sim_start):
                continue
            if mname in mothers_loaded_today:
                continue
            if volume is not None:
                hard_cap = float(m.get("hard_cap", m["cap"]))
                if (m["stock"] + float(volume)) > hard_cap:
                    continue
            eligible.append((mname, m))
        if not eligible:
            return None
        eligible.sort(key=lambda x: x[1]["stock"], reverse=True)
        return eligible[0][0]

    def pick_best_mother_for_sanjulian(current_day, mothers_loaded_today):
        wf_set = {x["mother"] for x in waiting_full}
        eligible = []
        for mname, m in mothers.items():
            if not mother_is_active(mname, current_day):
                continue
            if mname == _apm():
                continue
            if mname in wf_set:
                continue
            if m.get("is_full", False):
                continue
            if _to_dt(current_day) < mother_busy_until.get(mname, sim_start):
                continue
            if mname in mothers_loaded_today:
                continue
            hard_cap = float(m.get("hard_cap", m["cap"]))
            free = hard_cap - float(m["stock"])
            if free <= 0:
                continue
            soft_cap = float(m.get("cap", 1))
            stock = float(m["stock"])
            eligible.append((mname, stock, free, soft_cap))
        if not eligible:
            return None
        eligible.sort(key=lambda x: x[1] / x[3], reverse=True)
        return eligible[0][0]

    def sanjulian_has_received_today(current_day):
        d = sanjulian.get("received_today_on")
        if d is None:
            return False
        return pd.to_datetime(d).date() == pd.to_datetime(current_day).date()

    def apply_sanjulian_receipt(volume, current_day, incoming_api=None, vessel_name=None):
        vol = float(volume)
        if vol <= 0:
            return False
        if sanjulian_has_received_today(current_day):
            return False
        hard_cap = float(sanjulian["hard_cap"])
        if (float(sanjulian["stock"]) + vol) > hard_cap:
            return False
        cur_stock = float(sanjulian.get("stock", 0.0))
        cur_api   = sanjulian.get("api")
        sanjulian["stock"] = cur_stock + vol
        sanjulian["api"] = blend_quality(cur_stock, cur_api, vol, incoming_api)
        sanjulian["received_today_on"]   = pd.to_datetime(current_day).date()
        sanjulian["received_today_from"] = vessel_name
        return True

    def schedule_sanjulian_transfer(current_day, mothers_loaded_today):
        if _to_dt(current_day) < SANJULIAN_START:
            return
        if sanjulian.get("waiting_for_mother", False):
            return
        if float(sanjulian["stock"]) <= 0:
            return
        tm = pick_best_mother_for_sanjulian(current_day, mothers_loaded_today)
        if not tm:
            return
        sanjulian["waiting_for_mother"] = True
        sanjulian["target_mother"]  = tm
        sanjulian["transfer_eta"]   = _to_dt(current_day) + timedelta(days=SANJULIAN_LEAD_TO_MOTHER)

    def process_sanjulian_transfer(current_day, daily_record, sim_discharge_today, mothers_loaded_today):
        if not sanjulian.get("waiting_for_mother", False):
            return
        eta = sanjulian.get("transfer_eta")
        if eta is None or pd.to_datetime(eta).date() > _to_dt(current_day).date():
            return
        mname = sanjulian.get("target_mother")
        wf_set = {x["mother"] for x in waiting_full}
        if (not mname or not mother_is_active(mname, current_day)
                or mname == _apm() or mname in wf_set
                or mothers.get(mname, {}).get("is_full", False)
                or _to_dt(current_day) < mother_busy_until.get(mname, sim_start)
                or mname in mothers_loaded_today):
            mname = pick_best_mother_for_sanjulian(current_day, mothers_loaded_today)
        if not mname:
            sanjulian["transfer_eta"] = _to_dt(current_day) + timedelta(days=1)
            return
        sj_stock = float(sanjulian["stock"])
        if sj_stock <= 0:
            sanjulian.update({"waiting_for_mother": False, "target_mother": None, "transfer_eta": None, "api": None})
            return
        hard_cap = float(mothers[mname].get("hard_cap", mothers[mname]["cap"]))
        free = hard_cap - float(mothers[mname]["stock"])
        vol = min(sj_stock, free)
        if vol <= 0:
            return
        accepted = apply_mother_discharge(mname, vol, current_day, incoming_api=sanjulian.get("api"))
        if not accepted:
            sanjulian["transfer_eta"] = _to_dt(current_day) + timedelta(days=1)
            return
        sanjulian["stock"] -= vol
        if float(sanjulian["stock"]) <= 0:
            sanjulian["stock"] = 0.0
            sanjulian["api"]   = None
        sanjulian.update({"waiting_for_mother": False, "target_mother": None, "transfer_eta": None})
        label = f"SanJulian -> {mname} ({vol:,.2f})"
        for slot in range(1, 5):
            key = f"Discharge {slot}"
            if daily_record.get(key) in (None, "", " "):
                daily_record[key] = label
                break
        mothers_loaded_today.add(mname)
        sim_discharge_today.append({
            "date": pd.to_datetime(current_day).normalize(),
            "mother": mname, "vessel": "SanJulian", "source": "SanJulian",
            "production_site": "POINT B", "is_third_party": False, "volume": float(vol),
        })

    # ── Whisky helpers ─────────────────────────────────────────────────────────
    def get_whisky_override(current_day):
        d = pd.to_datetime(current_day).date()
        for w in WHISKY_INTERCHANGE_WINDOWS:
            if w["start"] <= d <= w["end"]:
                return w
        return None

    def get_whisky_active():
        on = [n for n in WHISKY_STATION_SHUTTLES if n in shuttles and shuttles[n].get("on_station") == WHISKY_SITE]
        return on[0] if on else None

    def whisky_partner(shuttle_name):
        if shuttle_name == "Balham":
            return "Bedford"
        if shuttle_name == "Bedford":
            return "Balham"
        return None

    def is_whisky_stationed_today(shuttle_name, current_day):
        if shuttle_name not in WHISKY_STATION_SHUTTLES:
            return False
        active = get_whisky_active()
        if active is not None:
            return shuttle_name == active
        ov = get_whisky_override(current_day)
        if ov:
            return shuttle_name == ov["stationed"]
        return False

    def is_whisky_shuttle_blocked_today(shuttle_name, current_day):
        return is_whisky_stationed_today(shuttle_name, current_day)

    def process_whisky_station(current_day, daily_record):
        nonlocal WHISKY_DAILY_BLOCK
        whisky_stock = float(storages.get(WHISKY_SITE, {}).get("stock", 0))
        ov = get_whisky_override(current_day)
        active = get_whisky_active()

        if ov:
            default_stationed = ov["stationed"]
            default_relief    = ov["shuttling"]
            if active is not None:
                active_free = (
                    _to_dt(current_day) >= shuttles.get(active, {}).get("available_on", sim_start)
                    and not shuttles.get(active, {}).get("waiting_for_mother", False)
                )
                if not active_free:
                    active = whisky_partner(active)
            if active is None:
                def_free = (
                    default_stationed in shuttles
                    and _to_dt(current_day) >= shuttles[default_stationed].get("available_on", sim_start)
                    and not shuttles[default_stationed].get("waiting_for_mother", False)
                )
                active = default_stationed if def_free else default_relief
            if active is None or active not in shuttles:
                return
            for n in WHISKY_STATION_SHUTTLES:
                if n in shuttles:
                    shuttles[n]["on_station"] = None
            shuttles[active]["on_station"] = WHISKY_SITE
            WHISKY_DAILY_BLOCK.add(active)
        else:
            if active is not None:
                active_free = (
                    _to_dt(current_day) >= shuttles.get(active, {}).get("available_on", sim_start)
                    and not shuttles.get(active, {}).get("waiting_for_mother", False)
                )
                if not active_free:
                    if active in shuttles:
                        shuttles[active]["on_station"] = None
                    active = whisky_partner(active)
            if active is None or active not in shuttles:
                return
            for n in WHISKY_STATION_SHUTTLES:
                if n in shuttles:
                    shuttles[n]["on_station"] = None
            shuttles[active]["on_station"] = WHISKY_SITE
            WHISKY_DAILY_BLOCK.add(active)

        if whisky_stock < WHISKY_TRIGGER:
            return
        if active not in shuttles:
            return

        load_vol = float(storages[WHISKY_SITE]["stock"])
        if load_vol <= 0:
            return

        storages[WHISKY_SITE]["stock"] = 0.0
        sh = shuttles[active]

        for slot in range(1, 5):
            if daily_record[f"Shuttle {slot}"] is None:
                daily_record[f"Shuttle {slot}"] = active
                daily_record[f"Load Point {slot}"] = WHISKY_SITE
                daily_record[f"Volume {slot}"] = int(round(load_vol))
                site = SITE_TO_ROW.get(WHISKY_SITE, "Unknown")
                daily_record[f"ETA {slot}"] = (_to_dt(current_day) + timedelta(days=sh["lead"])).date()
                daily_record[f"API {slot}"] = API_BY_SITE.get(site)
                break

        load_complete = _to_dt(current_day)
        base_eta = load_complete + timedelta(days=sh["lead"])
        eta = apply_pdf_tide_delay(WHISKY_SITE, load_complete, base_eta, PDF_TIDE_LOOKUP)
        sh["on_station"] = None
        sh["available_on"] = eta
        shuttle_arrivals_pending.append({
            "shuttle": active, "mother": None, "volume": load_vol,
            "arrival_date": eta, "load_complete": load_complete,
            "source": WHISKY_SITE,
            "incoming_api": get_incoming_api(WHISKY_SITE, THIRD_PARTY_NAMES),
            "next_attempt": eta.date(), "prescribed": False,
        })
        sh["waiting_for_mother"] = True
        sh["cargo_info"] = {"source": WHISKY_SITE, "volume": load_vol}

        partner = whisky_partner(active)
        if active in shuttles:
            shuttles[active]["on_station"] = None
        if partner and partner in shuttles:
            shuttles[partner]["on_station"] = WHISKY_SITE
            WHISKY_DAILY_BLOCK.add(partner)

    # ── STS consolidation ──────────────────────────────────────────────────────
    def can_receive(receiver_arr, donor_arr):
        r_name, d_name = receiver_arr["shuttle"], donor_arr["shuttle"]
        if r_name == d_name or r_name not in shuttles or d_name not in shuttles:
            return False
        # Receiver must be roving-enabled to accept consolidated cargo
        if not shuttles[r_name].get("roving_enabled", True):
            return False
        r_true = float(shuttles[r_name].get("true_cap", shuttles[r_name].get("eff_cap", shuttles[r_name]["cap"])))
        d_true = float(shuttles[d_name].get("true_cap", shuttles[d_name].get("eff_cap", shuttles[d_name]["cap"])))
        if r_true <= d_true:
            return False
        r_vol = float(receiver_arr.get("volume", 0) or 0)
        d_vol = float(donor_arr.get("volume", 0) or 0)
        if r_vol <= 0 or d_vol <= 0:
            return False
        return (r_vol + d_vol) <= r_true

    def try_sts_consolidation(current_day):
        if _to_dt(current_day) < STS_TRANSLOAD_START_DT:
            return
        today = pd.to_datetime(current_day).date()
        used_r, used_d = set(), set()
        eligible = [
            arr for arr in shuttle_arrivals_pending
            if arr.get("shuttle") in shuttles
            and arr.get("shuttle") not in THIRD_PARTY_NAMES
            and not arr.get("prescribed", False)
            and not arr.get("sts_donated_out", False)
            and not is_whisky_shuttle_blocked_today(arr["shuttle"], current_day)
            and pd.to_datetime(arr["arrival_date"]).date() == today
            and today >= arr.get("next_attempt", today)
            # Only receivers need roving_enabled; donors can be any shuttle
        ]
        eligible.sort(key=lambda a: float(shuttles[a["shuttle"]].get("true_cap", 0)), reverse=True)
        for receiver in eligible:
            r_name = receiver["shuttle"]
            if r_name in used_r or r_name in used_d:
                continue
            donors = [d for d in eligible
                      if d["shuttle"] != r_name
                      and d["shuttle"] not in used_d
                      and d["shuttle"] not in used_r
                      and can_receive(receiver, d)]
            if not donors:
                continue
            donor = donors[0]
            d_name = donor["shuttle"]
            r_vol = float(receiver.get("volume", 0) or 0)
            d_vol = float(donor.get("volume", 0) or 0)
            receiver["volume"] = r_vol + d_vol
            receiver["incoming_api"] = blend_quality(r_vol, receiver.get("incoming_api"), d_vol, donor.get("incoming_api"))
            receiver.setdefault("received_from", []).append({"from_shuttle": d_name, "volume": d_vol, "source": donor.get("source")})
            receiver["next_attempt"] = (pd.to_datetime(current_day) + timedelta(days=1)).date()
            donor["sts_donated_out"] = True
            donor["volume"] = 0.0
            sh_d = shuttles[d_name]
            sh_d["waiting_for_mother"] = False
            sh_d["cargo_info"] = None
            sh_d["available_on"] = pd.to_datetime(current_day).to_pydatetime() + timedelta(days=1)
            used_r.add(r_name)
            used_d.add(d_name)

    # ══════════════════════════════════════════════════════════════════════════
    # INITIALIZE pre-simulation state (mothers that start full)
    # ══════════════════════════════════════════════════════════════════════════
    for mname, m in sorted(mothers.items()):
        if m["stock"] >= m["cap"]:
            m["is_full"] = True
            m["stock_at_full"] = m["stock"]
            filled_on = sim_start.date()
            if active_pause_mother[0] is None:
                active_pause_mother[0] = mname
                active_pause_until[0]  = mother_return_day(filled_on)
            else:
                waiting_full.append({"mother": mname, "filled_on": filled_on})

    # ══════════════════════════════════════════════════════════════════════════
    # DAILY LOOP
    # ══════════════════════════════════════════════════════════════════════════
    records = []
    prescribed_start = datetime(2026, 2, 1)
    prescribed_end_dt = datetime.combine(PRESCRIBED_END, datetime.min.time())
    ALK_WARN_DATE = (datetime(ALK_STOP_DATE.year, ALK_STOP_DATE.month, ALK_STOP_DATE.day) - timedelta(days=3)).date()
    alk_eol_triggered = [False]
    tp_loaded_mothers = set()

    for current_day in pd.date_range(sim_start, sim_end):
        current_day = current_day.to_pydatetime()

        # storage zeroing before start_date
        for stg_name, stg in storages.items():
            stg_start = stg.get("start_date", sim_start)
            if current_day < _to_dt(stg_start):
                stg["stock"] = 0

        # ── Mother pause release ──────────────────────────────────────────────
        apm = active_pause_mother[0]
        apu = active_pause_until[0]
        if apm is not None and apu is not None:
            if current_day.date() >= apu:
                mothers[apm]["stock"]        = 0
                mothers[apm]["api"]          = None
                mothers[apm]["is_full"]      = False
                mothers[apm]["stock_at_full"] = None
                if waiting_full:
                    nxt = waiting_full.pop(0)
                    active_pause_mother[0] = nxt["mother"]
                    active_pause_until[0]  = mother_return_day(current_day.date())
                else:
                    active_pause_mother[0] = None
                    active_pause_until[0]  = None

        # ── Alkebulan EOL ─────────────────────────────────────────────────────
        alk = mothers.get("Alkebulan")
        if alk is not None:
            if current_day.date() == ALK_WARN_DATE and not alk_eol_triggered[0]:
                alk_stock = float(alk.get("stock", 0))
                if not alk.get("is_full", False) and alk_stock > 0:
                    candidates = []
                    wf_set = {x["mother"] for x in waiting_full}
                    for mname, m in mothers.items():
                        if mname == "Alkebulan":
                            continue
                        if not mother_is_active(mname, current_day):
                            continue
                        if mname == _apm() or mname in wf_set or m.get("is_full", False):
                            continue
                        hard_cap = float(m.get("hard_cap", m["cap"]))
                        if (float(m["stock"]) + alk_stock) <= hard_cap:
                            candidates.append((float(m["stock"]), mname))
                    if candidates:
                        candidates.sort(reverse=True)
                        tgt = candidates[0][1]
                        accepted = apply_mother_discharge(tgt, alk_stock, current_day, incoming_api=alk.get("api"))
                        if accepted:
                            alk["stock"] = 0.0
                            alk["api"]   = None
                alk["alk_eol_triggered"] = True
                alk["is_full"] = True
                alk["stock_at_full"] = float(alk.get("stock", 0))
                filled_on = current_day.date()
                if active_pause_mother[0] is None:
                    active_pause_mother[0] = "Alkebulan"
                    active_pause_until[0]  = mother_return_day(filled_on)
                elif active_pause_mother[0] != "Alkebulan":
                    waiting_full[:] = [x for x in waiting_full if x["mother"] != "Alkebulan"]
                    waiting_full.insert(0, {"mother": "Alkebulan", "filled_on": filled_on})
                alk_eol_triggered[0] = True

            if current_day.date() >= ALK_STOP_DATE:
                if float(alk.get("stock", 0)) > 0:
                    alk["stock"] = 0.0
                    alk["api"]   = None
                if active_pause_mother[0] == "Alkebulan":
                    active_pause_mother[0] = None
                    active_pause_until[0]  = None
                    if waiting_full:
                        nxt = waiting_full.pop(0)
                        active_pause_mother[0] = nxt["mother"]
                        active_pause_until[0]  = mother_return_day(current_day.date())
                waiting_full[:] = [x for x in waiting_full if x["mother"] != "Alkebulan"]
                alk["is_full"] = False

        # ── Build daily record ────────────────────────────────────────────────
        daily_record = {"Date": current_day.date()}
        for stg_name in storages:
            daily_record[f"{stg_name} Stock"] = storages[stg_name]["stock"]
        for slot in range(1, 5):
            daily_record[f"Shuttle {slot}"]    = None
            daily_record[f"Load Point {slot}"] = None
            daily_record[f"Volume {slot}"]     = None
            daily_record[f"ETA {slot}"]        = None
            daily_record[f"API {slot}"]        = None
        for line in PRODUCTION_LINES:
            daily_record[f"{line} Prod"] = None
        daily_record["Shuttles In Transit"]       = None
        daily_record["Shuttles In Transit Names"] = None
        for mname in mothers:
            daily_record[f"{mname} Stock"] = mothers[mname]["stock"]
            daily_record[f"{mname} API"]   = mothers[mname].get("api")
        daily_record["SanJulian Stock"] = sanjulian["stock"]
        daily_record["SanJulian API"]   = sanjulian.get("api")
        for slot in range(1, 5):
            daily_record[f"Discharge {slot}"] = None

        prescribed_discharge_today = []
        sim_discharge_today        = []
        mothers_loaded_today       = set()
        discharged_shuttles_today  = set()
        storages_loaded_today      = set()

        # ── Manual events ─────────────────────────────────────────────────────
        manual_shuttles_used_today = set()
        for ev in MANUAL_EVENTS:
            if _to_dt(ev["date"]).date() != current_day.date():
                continue
            shuttle_name = ev.get("shuttle")
            ev_action    = str(ev.get("action","load")).strip().lower()

            if is_whisky_shuttle_blocked_today(shuttle_name, current_day):
                continue
            if shuttle_name not in shuttles:
                continue

            # ── DISCHARGE event ───────────────────────────────────────────────
            if ev_action == "discharge":
                mother_name = ev.get("mother")
                if not mother_name or mother_name not in mothers:
                    continue
                if not mother_is_active(mother_name, current_day):
                    continue
                if mother_name in mothers_loaded_today:
                    continue
                if shuttle_name in discharged_shuttles_today:
                    continue
                sh = shuttles[shuttle_name]
                eff_cap = float(sh.get("eff_cap", sh["cap"]))
                vol = float(ev["volume"]) if ev.get("volume") else eff_cap
                if vol <= 0:
                    continue
                src = ev.get("storage")
                inc_api = get_incoming_api(src, THIRD_PARTY_NAMES) if src else None
                accepted = apply_mother_discharge(
                    mother_name, vol, current_day,
                    prescribed=False, incoming_api=inc_api,
                )
                if not accepted:
                    continue
                label = f"{shuttle_name} -> {mother_name} ({vol:,.2f})"
                for slot in range(1, 5):
                    if daily_record.get(f"Discharge {slot}") in (None, "", " "):
                        daily_record[f"Discharge {slot}"] = label
                        break
                sim_discharge_today.append({
                    "date": pd.to_datetime(current_day).normalize(),
                    "mother": mother_name, "vessel": shuttle_name,
                    "source": src, "production_site": SITE_TO_ROW.get(str(src or "").strip(), "Unknown"),
                    "is_third_party": False, "volume": float(vol), "label": label,
                })
                mothers_loaded_today.add(mother_name)
                discharged_shuttles_today.add(shuttle_name)
                sh["available_on"] = current_day + timedelta(days=1)
                sh["waiting_for_mother"] = False
                sh["cargo_info"] = None
                manual_shuttles_used_today.add(shuttle_name)
                continue

            # ── LOAD event ────────────────────────────────────────────────────
            stg_name = norm_storage_name(ev.get("storage"))
            if stg_name not in storages:
                continue
            sh = shuttles[shuttle_name]
            if not (current_day >= sh.get("available_on", sim_start)
                    and current_day >= sh.get("start_date", sim_start)
                    and sh.get("on_station") is None
                    and not sh.get("waiting_for_mother", False)):
                continue
            if not storage_is_active(stg_name, current_day):
                continue
            paused_until = loading_paused_until.get(stg_name)
            if paused_until and current_day.date() < paused_until:
                continue
            eff_cap = float(sh.get("eff_cap", sh["cap"]))
            vol = float(ev["volume"]) if ev.get("volume") else eff_cap
            if float(storages[stg_name]["stock"]) < vol:
                continue
            storages[stg_name]["stock"] -= vol
            load_days = storage_load_times.get(stg_name, 1)
            load_complete = current_day + timedelta(days=load_days)
            loading_paused_until[stg_name] = load_complete.date()
            base_eta = load_complete + timedelta(days=sh["lead"])
            eta = apply_pdf_tide_delay(stg_name, load_complete, base_eta, PDF_TIDE_LOOKUP)
            shuttle_arrivals_pending.append({
                "shuttle": shuttle_name, "mother": None, "volume": float(vol),
                "arrival_date": eta, "load_complete": load_complete,
                "source": stg_name,
                "incoming_api": get_incoming_api(stg_name, THIRD_PARTY_NAMES),
                "prescribed": False, "next_attempt": eta.date(), "manual_tag": ev.get("tag"),
            })
            sh["waiting_for_mother"] = True
            sh["cargo_info"] = {"source": stg_name, "volume": float(vol)}
            sh["available_on"] = eta
            for slot in range(1, 5):
                if daily_record[f"Shuttle {slot}"] is None:
                    daily_record[f"Shuttle {slot}"] = shuttle_name
                    daily_record[f"Load Point {slot}"] = stg_name
                    daily_record[f"Volume {slot}"] = int(round(vol))
                    daily_record[f"ETA {slot}"] = eta.date()
                    site = SITE_TO_ROW.get(stg_name, "Unknown")
                    daily_record[f"API {slot}"] = API_BY_SITE.get(site)
                    break
            manual_shuttles_used_today.add(shuttle_name)
            storages_loaded_today.add(stg_name)

        # ── Prescribed events ─────────────────────────────────────────────────
        daily_record_pre_events = []
        for event in pre_scheduled_events:
            if event["action"] == "load":
                event_day = pd.to_datetime(event.get("date"), errors="coerce")
            elif event["action"] == "discharge":
                event_day = pd.to_datetime(event.get("disch_date") or event.get("date"), errors="coerce")
            else:
                continue
            if pd.isna(event_day):
                continue
            event_day = event_day.date()
            if event_day > PRESCRIBED_END:
                continue
            if event_day != current_day.date():
                continue

            vessel_name = event["shuttle"]
            is_tp = event.get("is_third_party", False)

            if is_tp:
                disch_dt = event.get("disch_date") or event["date"]
                if _to_dt(disch_dt).date() != current_day.date():
                    continue
                mname = event.get("mother")
                if mname and mname in mothers:
                    vol = float(event.get("disch_qty") or event.get("load_qty") or 0)
                    if vol > 0:
                        inc_api = float(THIRD_PARTY_API.get(vessel_name, 41.0))
                        accepted = apply_mother_discharge(mname, vol, current_day, prescribed=True, incoming_api=inc_api)
                        if accepted:
                            r = {"date": pd.to_datetime(current_day).normalize(), "mother": mname,
                                 "vessel": vessel_name, "source": "Third Party",
                                 "production_site": "3rd Party Vessel", "is_third_party": True, "volume": float(vol)}
                            normalized_discharges.append(r)
                continue

            if event["action"] == "discharge":
                vol = float(event.get("volume") or event.get("disch_qty") or 0)
                if vol <= 0:
                    continue
                mname = event.get("mother")
                if mname and mname not in mothers:
                    mname = None
                if not mname:
                    mname = pick_available_mother(current_day, mothers_loaded_today, volume=vol)
                if not mname:
                    continue
                src = event.get("source")
                inc_api = get_incoming_api(src, THIRD_PARTY_NAMES)
                accepted = apply_mother_discharge(mname, vol, current_day, prescribed=True, incoming_api=inc_api)
                if not accepted:
                    continue
                row = {"date": current_day.date(), "mother": mname, "vessel": vessel_name,
                       "source": src,
                       "production_site": SITE_TO_ROW.get(str(src).strip(), "Unknown") if src else "Unknown",
                       "is_third_party": False, "volume": float(vol)}
                prescribed_discharge_today.append(row)
                label = f"{vessel_name} -> {mname} ({vol:,.2f})"
                for slot in range(1, 5):
                    key = f"Discharge {slot}"
                    if daily_record.get(key) in (None, "", " "):
                        daily_record[key] = label
                        break
                mothers_loaded_today.add(mname)
                discharged_shuttles_today.add(vessel_name)
                continue

            if vessel_name in daily_record_pre_events:
                continue
            if event["action"] == "load":
                stg_name = STORAGE_ALIAS.get(event["storage"], event["storage"])
                if stg_name == WHISKY_SITE and str(event["storage"]).strip() != WHISKY_SITE:
                    continue
                if stg_name not in storages:
                    continue
                stg = storages[stg_name]
                volume_loaded = float(event.get("load_qty") or event.get("volume") or shuttles.get(vessel_name, {}).get("eff_cap", 0))
                preloaded = event.get("preloaded", False)
                if not preloaded:
                    stg["stock"] = max(0, stg["stock"] - volume_loaded)
                    load_days = storage_load_times.get(stg_name, 1)
                    load_complete = current_day + timedelta(days=load_days)
                    loading_paused_until[stg_name] = load_complete.date()
                else:
                    load_complete = current_day

                eta_calc = load_complete + timedelta(days=shuttles.get(vessel_name, {}).get("lead", 1))
                if event.get("prescribed") and event.get("disch_date"):
                    eta = _to_dt(event["disch_date"])
                else:
                    eta = apply_pdf_tide_delay(stg_name, load_complete, eta_calc, PDF_TIDE_LOOKUP)

                trip_volume = float(event.get("disch_qty") or volume_loaded)
                eta_date = eta.date()
                if vessel_name in shuttles:
                    shuttles[vessel_name]["available_on"] = eta
                    shuttle_arrivals_pending.append({
                        "shuttle": vessel_name, "mother": event.get("mother"),
                        "volume": trip_volume, "arrival_date": eta,
                        "load_complete": load_complete, "source": stg_name,
                        "incoming_api": get_incoming_api(stg_name, THIRD_PARTY_NAMES),
                        "prescribed": True, "next_attempt": eta_date,
                    })
                    shuttles[vessel_name]["waiting_for_mother"] = True
                    shuttles[vessel_name]["cargo_info"] = {"source": stg_name, "volume": trip_volume}

                if stg_name == WHISKY_SITE and vessel_name in WHISKY_STATION_SHUTTLES:
                    if vessel_name in shuttles:
                        shuttles[vessel_name]["on_station"] = None
                    partner = whisky_partner(vessel_name)
                    if partner and partner in shuttles:
                        shuttles[partner]["on_station"] = WHISKY_SITE

                for slot in range(1, 5):
                    if daily_record[f"Shuttle {slot}"] is None:
                        daily_record[f"Shuttle {slot}"] = vessel_name
                        daily_record[f"Load Point {slot}"] = stg_name
                        daily_record[f"Volume {slot}"] = int(round(volume_loaded))
                        daily_record[f"ETA {slot}"] = eta.date()
                        site = SITE_TO_ROW.get(stg_name, "Unknown")
                        daily_record[f"API {slot}"] = API_BY_SITE.get(site)
                        break

        # ── Production ────────────────────────────────────────────────────────
        for line, info in PRODUCTION_LINES.items():
            line_start = _to_dt(info.get("start_date", sim_start))
            if current_day < line_start:
                prod = 0
            else:
                rate = float(info.get("rate", 0))
                prod = randomized_production(rate)
            daily_record[f"{line} Prod"] = prod
            tgt = info.get("target")
            if tgt and tgt in storages and prod > 0:
                if current_day >= _to_dt(storages[tgt].get("start_date", sim_start)):
                    storages[tgt]["stock"] += prod

        # ── STS consolidation ─────────────────────────────────────────────────
        try_sts_consolidation(current_day)

        # ── Process shuttle arrivals ──────────────────────────────────────────
        shuttle_arrivals_pending.sort(key=lambda a: a["arrival_date"])
        new_pending = []

        for arr in shuttle_arrivals_pending:
            shuttle_name = arr["shuttle"]
            if arr.get("sts_donated_out", False):
                continue
            if arr["arrival_date"].date() > current_day.date():
                new_pending.append(arr)
                continue
            if shuttle_name in discharged_shuttles_today:
                new_pending.append(arr)
                continue
            if current_day.date() < arr.get("next_attempt", arr["arrival_date"].date()):
                new_pending.append(arr)
                continue

            vol = float(arr["volume"])
            src = arr.get("source")
            inc_api = arr.get("incoming_api") or get_incoming_api(src, THIRD_PARTY_NAMES)

            if _to_dt(current_day) >= SANJULIAN_START:
                mname = pick_available_mother(current_day, mothers_loaded_today, volume=vol)
                if mname:
                    accepted = apply_mother_discharge(mname, vol, current_day, incoming_api=inc_api)
                    if not accepted:
                        arr["next_attempt"] = (current_day + timedelta(days=1)).date()
                        new_pending.append(arr)
                        continue
                    # Include STS donor info if this shuttle received cargo from another
                    _rcvd = arr.get("received_from", [])
                    if _rcvd:
                        _donors = ", ".join(f"{r['from_shuttle']} ({float(r['volume']):,.0f})" for r in _rcvd)
                        label = f"{shuttle_name} -> {mname} ({vol:,.2f}) [rcvd. {_donors}]"
                    else:
                        label = f"{shuttle_name} -> {mname} ({vol:,.2f})"
                    destination = mname
                else:
                    if sanjulian_has_received_today(current_day):
                        arr["next_attempt"] = (current_day + timedelta(days=1)).date()
                        new_pending.append(arr)
                        continue
                    accepted = apply_sanjulian_receipt(vol, current_day, incoming_api=inc_api, vessel_name=shuttle_name)
                    if not accepted:
                        arr["next_attempt"] = (current_day + timedelta(days=1)).date()
                        new_pending.append(arr)
                        continue
                    label = f"{shuttle_name} -> SanJulian ({vol:,.2f})"
                    destination = "SanJulian"
            else:
                mname = arr.get("mother")
                if mname and mname not in mothers:
                    mname = None
                if not mname:
                    mname = pick_available_mother(current_day, mothers_loaded_today, volume=vol)
                if not mname:
                    arr["next_attempt"] = (current_day + timedelta(days=1)).date()
                    new_pending.append(arr)
                    continue
                accepted = apply_mother_discharge(mname, vol, current_day, incoming_api=inc_api)
                if not accepted:
                    arr["next_attempt"] = (current_day + timedelta(days=1)).date()
                    new_pending.append(arr)
                    continue
                _rcvd = arr.get("received_from", [])
                if _rcvd:
                    _donors = ", ".join(f"{r['from_shuttle']} ({float(r['volume']):,.0f})" for r in _rcvd)
                    label = f"{shuttle_name} -> {mname} ({vol:,.2f}) [rcvd. {_donors}]"
                else:
                    label = f"{shuttle_name} -> {mname} ({vol:,.2f})"
                destination = mname

            for slot in range(1, 5):
                key = f"Discharge {slot}"
                if daily_record.get(key) in (None, "", " "):
                    daily_record[key] = label
                    break

            production_site = SITE_TO_ROW.get(str(src).strip(), "Unknown") if src else "Unknown"
            row = {
                "date": pd.to_datetime(current_day).normalize(), "mother": destination,
                "vessel": shuttle_name, "source": src,
                "production_site": production_site,
                "is_third_party": shuttle_name in THIRD_PARTY_NAMES, "volume": float(vol), "label": label,
            }
            sim_discharge_today.append(row)
            if destination != "SanJulian":
                normalized_discharges.append(row)
            discharged_shuttles_today.add(shuttle_name)
            if destination != "SanJulian":
                mothers_loaded_today.add(destination)
            if shuttle_name in shuttles:
                shuttles[shuttle_name]["available_on"] = current_day + timedelta(days=1)
                shuttles[shuttle_name]["waiting_for_mother"] = False
                shuttles[shuttle_name]["cargo_info"] = None

        shuttle_arrivals_pending[:] = new_pending

        schedule_sanjulian_transfer(current_day, mothers_loaded_today)
        process_sanjulian_transfer(current_day, daily_record, sim_discharge_today, mothers_loaded_today)

        # ── Asaramatoru / Santa Monica priority ───────────────────────────────
        SANTA = "MT Santa Monica"
        ASARAM_SITE = "Asaramatoru"
        ASARAM_TRIGGER = 10000
        if SANTA in shuttles:
            santa = shuttles[SANTA]
            santa_free = (
                current_day >= santa.get("start_date", sim_start)
                and current_day >= santa.get("available_on", sim_start)
                and santa.get("on_station") is None
                and not santa.get("waiting_for_mother", False)
            )
            if santa_free and not (prescribed_start <= current_day <= prescribed_end_dt):
                if ASARAM_SITE in storages and storages[ASARAM_SITE]["stock"] >= ASARAM_TRIGGER:
                    paused_until = loading_paused_until.get(ASARAM_SITE)
                    if not (paused_until and current_day.date() < paused_until):
                        load_vol = min(float(santa.get("eff_cap", santa["cap"])), float(storages[ASARAM_SITE]["stock"]))
                        if load_vol > 0:
                            storages[ASARAM_SITE]["stock"] -= load_vol
                            load_days = storage_load_times.get(ASARAM_SITE, 1)
                            load_complete = current_day + timedelta(days=load_days)
                            loading_paused_until[ASARAM_SITE] = load_complete.date()
                            base_eta = load_complete + timedelta(days=santa["lead"])
                            eta = apply_pdf_tide_delay(ASARAM_SITE, load_complete, base_eta, PDF_TIDE_LOOKUP)
                            shuttle_arrivals_pending.append({
                                "shuttle": SANTA, "mother": None, "volume": float(load_vol),
                                "arrival_date": eta, "load_complete": load_complete,
                                "source": ASARAM_SITE,
                                "incoming_api": get_incoming_api(ASARAM_SITE, THIRD_PARTY_NAMES),
                                "prescribed": False, "next_attempt": eta.date(),
                            })
                            santa["waiting_for_mother"] = True
                            santa["cargo_info"] = {"source": ASARAM_SITE, "volume": float(load_vol)}
                            santa["available_on"] = eta
                            for slot in range(1, 5):
                                if daily_record[f"Shuttle {slot}"] is None:
                                    daily_record[f"Shuttle {slot}"] = SANTA
                                    daily_record[f"Load Point {slot}"] = ASARAM_SITE
                                    daily_record[f"Volume {slot}"] = int(round(load_vol))
                                    daily_record[f"ETA {slot}"] = eta.date()
                                    break
                            storages_loaded_today.add(ASARAM_SITE)

        # ── Whisky station & normal shuttle loading ───────────────────────────
        WHISKY_DAILY_BLOCK = set()
        process_whisky_station(current_day, daily_record)

        available_shuttles = [
            (name, s) for name, s in shuttles.items()
            if current_day >= s.get("available_on", sim_start)
            and current_day >= s.get("start_date", sim_start)
            and not s.get("waiting_for_mother", False)
            and name not in WHISKY_DAILY_BLOCK
            and not is_whisky_shuttle_blocked_today(name, current_day)
            and s.get("on_station") is None
            and name not in manual_shuttles_used_today
        ]
        available_shuttles.sort(key=lambda x: float(x[1].get("eff_cap", x[1]["cap"])), reverse=True)

        loads_today = 0
        for shuttle_name, shuttle in available_shuttles:
            if prescribed_start <= current_day <= prescribed_end_dt:
                continue
            if loads_today >= 7:
                break

            eff_cap = float(shuttle.get("eff_cap", shuttle["cap"]))
            allowed = [norm_storage_name(a) for a in shuttle.get("allowed_storages", [])]
            candidates = []
            for actual in allowed:
                if actual is None or actual not in storages:
                    continue
                if actual == WHISKY_SITE:
                    continue
                if actual in storages_loaded_today:
                    continue
                if not storage_is_active(actual, current_day):
                    continue
                paused_until = loading_paused_until.get(actual)
                if paused_until and current_day.date() < paused_until:
                    continue
                stg = storages[actual]
                stock = float(stg.get("stock", 0.0))
                min_thr = float(stg.get("min_threshold", 0.0))
                if stock <= min_thr:
                    continue
                if stock < eff_cap:
                    continue
                candidates.append((storage_fullness(actual), actual))

            if not candidates:
                continue
            candidates.sort(key=lambda x: x[0], reverse=True)
            stg_name = candidates[0][1]

            load_volume = float(get_variable_load_volume(shuttle_name, stg_name, shuttles))
            if float(storages[stg_name]["stock"]) < load_volume:
                load_volume = float(storages[stg_name]["stock"])
            if load_volume <= 0:
                continue

            storages[stg_name]["stock"] -= load_volume
            load_days = storage_load_times.get(stg_name, 1)
            load_complete = current_day + timedelta(days=load_days)
            loading_paused_until[stg_name] = load_complete.date()
            base_eta = load_complete + timedelta(days=shuttle["lead"])
            eta = apply_pdf_tide_delay(stg_name, load_complete, base_eta, PDF_TIDE_LOOKUP)

            shuttle_arrivals_pending.append({
                "shuttle": shuttle_name, "mother": None, "volume": float(load_volume),
                "arrival_date": eta, "load_complete": load_complete, "source": stg_name,
                "incoming_api": get_incoming_api(stg_name, THIRD_PARTY_NAMES),
                "prescribed": False, "next_attempt": eta.date(),
            })
            shuttle["waiting_for_mother"] = True
            shuttle["cargo_info"] = {"source": stg_name, "volume": float(load_volume)}
            shuttle["available_on"] = eta

            for slot in range(1, 5):
                if daily_record.get(f"Shuttle {slot}") is None:
                    daily_record[f"Shuttle {slot}"] = shuttle_name
                    daily_record[f"Load Point {slot}"] = stg_name
                    daily_record[f"Volume {slot}"] = int(round(load_volume))
                    daily_record[f"ETA {slot}"] = eta.date()
                    site = SITE_TO_ROW.get(stg_name, "Unknown")
                    daily_record[f"API {slot}"] = API_BY_SITE.get(site)
                    break

            loads_today += 1
            storages_loaded_today.add(stg_name)

        # ── Third-party discharges ────────────────────────────────────────────
        wf_set = {x["mother"] for x in waiting_full}
        for vessel in third_party_vessels:
            vname = str(vessel.get("name", "")).strip()
            if not vname:
                continue
            if vessel.get("end_date") and current_day.date() > pd.to_datetime(vessel["end_date"]).date():
                continue
            if current_day.date() < pd.to_datetime(vessel["next_arrival"]).date():
                continue
            cands = [
                (n, m) for n, m in mothers.items()
                if n != _apm() and n not in wf_set
                and n not in tp_loaded_mothers and n not in mothers_loaded_today
                and _to_dt(current_day) >= mother_busy_until[n]
                and (m["stock"] + vessel["cap"]) <= float(m.get("hard_cap", m["cap"]))
            ]
            if not cands:
                continue
            cands.sort(key=lambda x: x[1]["stock"], reverse=True)
            mname, _ = cands[0]
            if vname == "ST Zeezee":
                mother_busy_until[mname] = current_day + timedelta(days=2)
            inc_api = float(THIRD_PARTY_API.get(vname, 41.0))
            accepted = apply_mother_discharge(mname, vessel["cap"], current_day, prescribed=True, incoming_api=inc_api)
            if not accepted:
                continue
            row = {"date": pd.to_datetime(current_day).normalize(), "mother": mname,
                   "vessel": vname, "source": "Third Party",
                   "production_site": "3rd Party Vessel", "is_third_party": True, "volume": float(vessel["cap"])}
            normalized_discharges.append(row)
            mothers_loaded_today.add(mname)
            tp_loaded_mothers.add(mname)
            vessel["next_arrival"] = current_day + timedelta(days=int(vessel["freq"]))

        # ── Discharge labels ──────────────────────────────────────────────────
        all_discharge = prescribed_discharge_today + sim_discharge_today
        for idx, d in enumerate(all_discharge[:4]):
            daily_record[f"Discharge {idx+1}"] = d.get("label", f"{d['vessel']} -> {d['mother']} ({d['volume']:,.2f})")

        # ── In transit ────────────────────────────────────────────────────────
        loading_today = {daily_record[f"Shuttle {i}"] for i in range(1, 5) if daily_record[f"Shuttle {i}"]}
        discharging_today = set()
        for i in range(1, 5):
            entry = daily_record.get(f"Discharge {i}")
            if entry and "->" in str(entry):
                discharging_today.add(str(entry).split("->")[0].strip())
        busy_today = loading_today | discharging_today
        in_transit_list = [
            arr["shuttle"] for arr in shuttle_arrivals_pending
            if arr["arrival_date"].date() > current_day.date()
            and current_day >= arr.get("load_complete", sim_start)
            and arr["shuttle"] not in busy_today
        ]
        daily_record["Shuttles In Transit"]       = len(in_transit_list)
        daily_record["Shuttles In Transit Names"] = ", ".join(in_transit_list)

        # ── End-of-day mother stock refresh ───────────────────────────────────
        for mname in mothers:
            daily_record[f"{mname} Stock"] = mothers[mname]["stock"]
            daily_record[f"{mname} API"]   = mothers[mname].get("api")
        daily_record["SanJulian Stock"] = sanjulian["stock"]
        daily_record["SanJulian API"]   = sanjulian.get("api")

        records.append(daily_record)

    # ══════════════════════════════════════════════════════════════════════════
    # POST-PROCESSING
    # ══════════════════════════════════════════════════════════════════════════
    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError("Simulation produced no records.")

    df.sort_values("Date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime("%b")

    stock_cols = [c for c in df.columns if "Stock" in c]
    vol_cols   = [c for c in df.columns if c.startswith("Volume ")]
    for c in stock_cols + vol_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).round(0).astype(int)
    api_cols = [c for c in df.columns if c.startswith("API ") or c.endswith(" API")]
    for c in api_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").round(2)

    # ── Build discharge DataFrame ──────────────────────────────────────────────
    # Also collect from daily table (catch anything missed above)
    shuttle_cols   = [c for c in df.columns if c.startswith("Shuttle")]
    discharge_cols = [c for c in df.columns if c.startswith("Discharge")]
    for _, row in df.iterrows():
        day = pd.to_datetime(row["Date"]).normalize()
        for sh_col, dis_col in zip(shuttle_cols, discharge_cols):
            dis_str = row.get(dis_col)
            if pd.isna(dis_str):
                continue
            vessel, mother, volume = parse_discharge_label(dis_str)
            if not mother or volume <= 0:
                continue
            lp = row.get(sh_col.replace("Shuttle", "Load Point"))
            if str(vessel).strip() in THIRD_PARTY_NAMES:
                ps = "3rd Party"
                src = "3rd Party"
                is_tp = True
            else:
                lp_s = None if pd.isna(lp) else str(lp).strip()
                ps = SITE_TO_ROW.get(lp_s, "Unknown")
                src = lp_s if lp_s else "Unknown"
                is_tp = False
            # avoid duplicates by checking normalized_discharges doesn't already have this exact row
            normalized_discharges.append({
                "date": day, "mother": mother, "vessel": str(vessel).strip(),
                "production_site": ps, "source": src, "is_third_party": is_tp, "volume": float(volume),
            })

    dis_df = pd.DataFrame(normalized_discharges,
                          columns=["date","mother","vessel","production_site","source","is_third_party","volume"])
    if not dis_df.empty:
        dis_df["date"]   = pd.to_datetime(dis_df["date"]).dt.normalize()
        dis_df["volume"] = pd.to_numeric(dis_df["volume"], errors="coerce").fillna(0.0)
        dis_df = ensure_is_third_party(dis_df)
        # deduplicate
        dis_df = dis_df.drop_duplicates(subset=["date","mother","vessel","volume"]).reset_index(drop=True)
    else:
        dis_df = pd.DataFrame(columns=["date","mother","vessel","production_site","source","is_third_party","volume","IsThirdParty"])

    # ── Injection detection ────────────────────────────────────────────────────
    df_sorted = df.sort_values("Date").copy()
    df_sorted["Date"] = pd.to_datetime(df_sorted["Date"]).dt.normalize()

    prev_stock = {m: 0 for m in MOTHER_CAPS}
    cycle_start_dt = {m: None for m in MOTHER_CAPS}
    events = []
    inj_no = START_INJ_NO

    if not dis_df.empty:
        for _, r in df_sorted.iterrows():
            day = r["Date"]
            for mother_name, cap in MOTHER_CAPS.items():
                stock_col = f"{mother_name} Stock"
                if stock_col not in df_sorted.columns:
                    continue
                today_stock = r[stock_col]
                yesterday_stock = prev_stock[mother_name]
                if yesterday_stock < cap and today_stock >= cap:
                    total_qty = int(today_stock)
                    mask = (dis_df["mother"] == mother_name) & (dis_df["date"] <= day)
                    if cycle_start_dt[mother_name] is not None:
                        mask &= (dis_df["date"] > cycle_start_dt[mother_name])
                    tp_vol = int(dis_df.loc[mask & (dis_df["IsThirdParty"] == True), "volume"].sum())
                    nepl_vol = total_qty - tp_vol
                    events.append({
                        "Injection No": inj_no,
                        "Vessel":        mother_name,
                        "Final Ullage":  day,
                        "Total Quantity": total_qty,
                        "Third Party":   tp_vol,
                        "NEPL":          nepl_vol,
                        "SBM Discharge Day 2": day + pd.Timedelta(days=1),
                        "SBM Discharge Day 3": day + pd.Timedelta(days=2),
                        "Month":         day.to_period("M"),
                    })
                    inj_no += 1
                    cycle_start_dt[mother_name] = day
                prev_stock[mother_name] = today_stock

    events.sort(key=lambda x: (x["Final Ullage"], x["Vessel"]))
    inj_df = pd.DataFrame(events).reset_index(drop=True) if events else pd.DataFrame()
    if not inj_df.empty:
        inj_df["MonthStart"] = inj_df["Final Ullage"].dt.to_period("M").dt.to_timestamp()
        inj_df["MonthLabel"] = inj_df["Final Ullage"].dt.strftime("%b %Y")

    # ── KPIs ──────────────────────────────────────────────────────────────────
    if not inj_df.empty:
        total_vol = int(inj_df["Total Quantity"].sum())
        tp_vol    = int(inj_df["Third Party"].sum())
        nepl_vol  = int(inj_df["NEPL"].sum())
        trips     = len(inj_df)
    else:
        total_vol = tp_vol = nepl_vol = trips = 0

    # ── Shuttle utilisation ────────────────────────────────────────────────────
    # Count distinct discharge days per shuttle (proxy for utilisation)
    shuttle_names_active = [s["name"] for s in params.get("shuttle_vessels", []) if s.get("active", True)]
    shuttle_util = {}
    if not dis_df.empty:
        sh_dis = dis_df[dis_df["vessel"].isin(shuttle_names_active)]
        shuttle_util = sh_dis.groupby("vessel")["volume"].sum().to_dict()
    total_shuttle_vol = sum(shuttle_util.values())
    # Balance score: 1 - coefficient of variation (lower spread = higher score)
    if len(shuttle_util) > 1:
        import statistics
        sv = [float(x) for x in shuttle_util.values()]
        shuttle_balance = 1.0 - (statistics.stdev(sv) / max(statistics.mean(sv), 1))
    else:
        shuttle_balance = 1.0

    # Mother balance: spread of total volumes across mothers
    if not inj_df.empty:
        mother_vols = inj_df.groupby("Vessel")["Total Quantity"].sum()
        if len(mother_vols) > 1:
            mv = [float(x) for x in mother_vols.values]
            import statistics as _st
            mother_balance = 1.0 - (_st.stdev(mv) / max(_st.mean(mv), 1))
        else:
            mother_balance = 1.0
    else:
        mother_balance = 0.0

    # ── Risk metrics ──────────────────────────────────────────────────────────
    _tank_top_dates   = []   # dates where any storage hit cap
    _backlog_dates    = []   # dates where shuttles waiting > 1
    _idle_dates       = []   # dates where mother free but shuttle waiting

    for _, _row in df.iterrows():
        _day = _row["Date"]
        # Tank top: any storage at or above cap
        for _stg_name, _stg_cfg in storages.items():
            _scol = f"{_stg_name} Stock"
            if _scol in _row and float(_row[_scol] or 0) >= float(_stg_cfg.get("cap", 1)):
                _tank_top_dates.append(_day)
                break
        # Backlog: shuttles in transit > avg (proxy: transit count above 5)
        _transit = int(_row.get("Shuttles In Transit", 0) or 0)
        if _transit > 5:
            _backlog_dates.append(_day)
        # Idle mother: no discharge recorded but mother below cap and shuttles in transit
        _no_discharge = all(
            pd.isna(_row.get(f"Discharge {_s}")) or str(_row.get(f"Discharge {_s}", "")).strip() == ""
            for _s in range(1, 5)
        )
        if _no_discharge and _transit > 0:
            for _mn in mothers:
                _mcol = f"{_mn} Stock"
                if _mcol in _row:
                    _mstock = float(_row[_mcol] or 0)
                    _mcap   = float(mothers[_mn].get("cap", 1))
                    if _mstock < _mcap * 0.95:  # mother not full but no discharge
                        _idle_dates.append(_day)
                        break

    _has_tank_top   = len(_tank_top_dates) > 0
    _first_tank_top = str(min(_tank_top_dates))[:10] if _tank_top_dates else None
    _has_backlog    = len(_backlog_dates) > 0
    _first_backlog  = str(min(_backlog_dates))[:10] if _backlog_dates else None
    _idle_days      = len(set(str(d)[:10] for d in _idle_dates))

    kpis = {
        "total_vol":       total_vol,
        "nepl_vol":        nepl_vol,
        "tp_vol":          tp_vol,
        "trips":           trips,
        "shuttle_vol":     int(total_shuttle_vol),
        "shuttle_balance": float(shuttle_balance),
        "mother_balance":  float(mother_balance),
        # Risk metrics
        "has_tank_top":    _has_tank_top,
        "first_tank_top":  _first_tank_top,
        "has_backlog":     _has_backlog,
        "first_backlog":   _first_backlog,
        "idle_days":       _idle_days,
    }

    # ── Monthly aggregates ─────────────────────────────────────────────────────
    monthly_mother = pd.DataFrame()
    monthly_totals = pd.DataFrame()
    if not inj_df.empty:
        monthly_mother = (
            inj_df.groupby(["MonthStart", "MonthLabel", "Vessel"], as_index=False)
                  .agg(Total_Volume=("Total Quantity","sum"), NEPL_Volume=("NEPL","sum"),
                       ThirdParty_Volume=("Third Party","sum"), Trips=("Injection No","count"))
        )
        monthly_totals = (
            inj_df.groupby(["MonthStart", "MonthLabel"], as_index=False)
                  .agg(Total_Volume=("Total Quantity","sum"), NEPL_Volume=("NEPL","sum"),
                       ThirdParty_Volume=("Third Party","sum"), Trips=("Injection No","count"))
        )

    # ── Monthly summary tables HTML ────────────────────────────────────────────
    SUMMARY_ROWS = ["Vessel","Month","NEPL/SOKU/SANBARTH/AWOBA/BELAMA (Qty)",
                    "Third Party","Total Quantity","Final Ullage","SBM Discharge Day 2","SBM Discharge Day 3"]
    summary_tables_html = ""
    if not inj_df.empty:
        monthly_tables = OrderedDict()
        for month, g in inj_df.groupby("Month", sort=False):
            g = g.sort_values(["Final Ullage","Injection No"])
            cols = [f"Injection {int(i)}" for i in g["Injection No"]]
            table = pd.DataFrame(index=SUMMARY_ROWS, columns=cols)
            for _, r in g.iterrows():
                col = f"Injection {int(r['Injection No'])}"
                table.loc["Vessel", col]    = r["Vessel"]
                table.loc["Month", col]     = r["Final Ullage"].strftime("%B %Y")
                table.loc["NEPL/SOKU/SANBARTH/AWOBA/BELAMA (Qty)", col] = f"{int(r['NEPL']):,}"
                table.loc["Third Party", col]    = f"{int(r['Third Party']):,}"
                table.loc["Total Quantity", col]  = f"{int(r['Total Quantity']):,}"
                table.loc["Final Ullage", col]    = r["Final Ullage"].strftime("%Y-%m-%d")
                table.loc["SBM Discharge Day 2", col] = pd.to_datetime(r["SBM Discharge Day 2"]).strftime("%Y-%m-%d")
                table.loc["SBM Discharge Day 3", col] = pd.to_datetime(r["SBM Discharge Day 3"]).strftime("%Y-%m-%d")

            mc = "Monthly Total"
            table[mc] = ""
            table.loc["NEPL/SOKU/SANBARTH/AWOBA/BELAMA (Qty)", mc] = f"{int(g['NEPL'].sum()):,}"
            table.loc["Third Party", mc]   = f"{int(g['Third Party'].sum()):,}"
            table.loc["Total Quantity", mc] = f"{int(g['Total Quantity'].sum()):,}"
            monthly_tables[month] = table

        for month, table in monthly_tables.items():
            summary_tables_html += f"<h3 style='font-family:sans-serif;'>{month.strftime('%B %Y')}</h3>"
            summary_tables_html += table.to_html(border=1)

    return {
        "stock_init_error": _stock_init_error if "_stock_init_error" in dir() else None,
        "df":                  df,
        "inj_df":              inj_df,
        "dis_df":              dis_df,
        "monthly_mother":      monthly_mother,
        "monthly_totals":      monthly_totals,
        "kpis":                kpis,
        "summary_tables_html": summary_tables_html,
    }
