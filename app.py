import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Marine Propulsion Configurator",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: linear-gradient(160deg, #0a1628 0%, #0d2240 40%, #0a3d5c 100%); min-height: 100vh; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 2rem 2rem 4rem 2rem; max-width: 960px; }
  .section-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(100,180,255,0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
  }
  .section-title {
    color: #7ec8e3;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
  }
  .pill {
    display: inline-block;
    background: rgba(61,181,230,0.15);
    border: 1px solid rgba(61,181,230,0.35);
    border-radius: 20px;
    padding: 4px 14px;
    color: #b8e4f5;
    font-size: 0.82rem;
    margin: 4px;
  }
  .bom-table { width: 100%; border-collapse: collapse; }
  .bom-table th {
    color: #7ec8e3;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(100,180,255,0.2);
    padding: 6px 10px;
    text-align: left;
  }
  .bom-table td {
    color: #e8f4f8;
    font-size: 0.88rem;
    padding: 9px 10px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }
  .bom-table td.pn { font-family: monospace; color: #7ec8e3; font-size: 0.8rem; }
  .bom-table td.qty { text-align: center; font-weight: 600; }
  .bom-table td.cat { color: #a0c4d8; font-size: 0.8rem; }
  .page-title { color: #e8f4f8; font-size: 1.8rem; font-weight: 600; margin-bottom: 0.2rem; }
  .page-sub { color: #7ec8e3; font-size: 0.92rem; margin-bottom: 1.75rem; }
  .stTextInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(100,180,255,0.3) !important;
    border-radius: 8px !important;
    color: #e8f4f8 !important;
  }
  .stButton > button {
    background: rgba(14,90,160,0.5) !important;
    border: 1px solid #3db5e6 !important;
    color: #e8f4f8 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
  }
  .stButton > button:hover { background: rgba(14,90,160,0.8) !important; }
  div[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(100,180,255,0.3) !important;
    border-radius: 8px !important;
    color: #e8f4f8 !important;
  }
</style>
""", unsafe_allow_html=True)


def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align:center;color:#7ec8e3;font-size:2.5rem;margin-bottom:0.5rem;">⚓</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;color:#e8f4f8;font-size:1.4rem;font-weight:600;margin-bottom:0.25rem;">Marine Propulsion Configurator</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;color:#7ec8e3;font-size:0.9rem;margin-bottom:1.5rem;">Enter your access password to continue</div>', unsafe_allow_html=True)
        pwd = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password...")
        if st.button("Access Configurator", use_container_width=True):
            correct = st.secrets.get("APP_PASSWORD", "marine2024")
            if pwd == correct:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
    return False


@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv("data/configurator.csv", comment="#")
        df.columns = df.columns.str.strip()
        df = df.dropna(how="all")
        return df
    except Exception as e:
        st.error(f"Could not load configurator.csv: {e}")
        return pd.DataFrame()


def get_section(df, section_name):
    return df[df["section"].str.strip() == section_name].copy()


def main():
    df = load_data()
    if df.empty:
        st.warning("No data loaded. Check that data/configurator.csv exists.")
        return

    st.markdown('<div class="page-title">⚓ Marine Propulsion Configurator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Select your powertrain options to generate the top-level Bill of Materials.</div>', unsafe_allow_html=True)

    bom_rows = []

    # Section 1: Drive System
    drive_df = get_section(df, "drive_system")
    drive_options = drive_df["label"].tolist()
    drive_pns = dict(zip(drive_df["label"], drive_df["part_number"]))
    drive_display = st.session_state.get("drive_radio", drive_options[0])
    st.markdown(f'<div class="section-card"><div class="section-title">1 — Drive system: {drive_display}</div>', unsafe_allow_html=True)
    drive_sel = st.radio("Drive system", drive_options, label_visibility="collapsed", key="drive_radio", horizontal=True)
    if drive_sel:
        bom_rows.append({"Part Number": drive_pns[drive_sel], "Description": drive_sel, "Qty": 1, "Category": "Drive System"})
    st.markdown("</div>", unsafe_allow_html=True)

    # Section 2: Battery Pack
    batt_df = get_section(df, "battery_pack")
    batt_options = batt_df["label"].tolist()
    batt_pns = dict(zip(batt_df["label"], batt_df["part_number"]))
    batt_qtys = dict(zip(batt_df["label"], batt_df["qty"].astype(int)))
    batt_display = st.session_state.get("batt_radio", batt_options[0])
    st.markdown(f'<div class="section-card"><div class="section-title">2 — HV battery pack: {batt_display}</div>', unsafe_allow_html=True)
    batt_sel = st.radio("Battery pack", batt_options, label_visibility="collapsed", key="batt_radio", horizontal=True)
    if batt_sel:
        bom_rows.append({"Part Number": batt_pns[batt_sel], "Description": batt_sel, "Qty": batt_qtys[batt_sel], "Category": "HV Battery"})
    st.markdown("</div>", unsafe_allow_html=True)

    # Section 3: Included Items
    st.markdown('<div class="section-card"><div class="section-title">3 — Included customer-facing items (always included)</div>', unsafe_allow_html=True)
    inc_df = get_section(df, "included_items")
    pills_html = "".join([f'<span class="pill">{row["label"]}</span>' for _, row in inc_df.iterrows()])
    st.markdown(f"<div>{pills_html}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    for _, row in inc_df.iterrows():
        bom_rows.append({"Part Number": row["part_number"], "Description": row["label"], "Qty": int(row["qty"]), "Category": "Included Item"})

    # Section 4: Harness Lengths
    st.markdown('<div class="section-card"><div class="section-title">4 — Harness lengths</div>', unsafe_allow_html=True)
    harn_df = get_section(df, "harness")
    pn_lookup = get_section(df, "harness_pn_lookup")
    for _, hrow in harn_df.iterrows():
        lengths = [l.strip() for l in str(hrow["harness_lengths"]).split("|")]
        default = str(hrow.get("default_length", lengths[0])).strip()
        default_idx = lengths.index(default) if default in lengths else 0
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f'<div style="color:#e8f4f8;font-size:0.9rem;font-weight:500;padding-top:8px;">{hrow["label"]}</div>', unsafe_allow_html=True)
        with col2:
            chosen_len = st.selectbox(hrow["label"], lengths, index=default_idx, label_visibility="collapsed", key=f"harn_{hrow['option_id']}")
        match = pn_lookup[
            (pn_lookup["harness_id"].str.strip() == str(hrow["option_id"]).strip()) &
            (pn_lookup["label"].str.strip() == chosen_len.strip())
        ]
        resolved_pn = match["part_number"].values[0] if not match.empty else str(hrow["pn_pattern"]).replace("{LENGTH}", chosen_len)
        st.markdown(f'<div style="color:#7ec8e3;font-size:0.75rem;font-family:monospace;margin-bottom:10px;margin-top:2px;">{resolved_pn}</div>', unsafe_allow_html=True)
        bom_rows.append({"Part Number": resolved_pn, "Description": f"{hrow['label']} ({chosen_len})", "Qty": 1, "Category": "Harness"})
    st.markdown("</div>", unsafe_allow_html=True)

    # Section 5: BoM Summary
    st.markdown('<div class="section-card"><div class="section-title">5 — Top-level BoM summary</div>', unsafe_allow_html=True)
    if bom_rows:
        bom_df = pd.DataFrame(bom_rows)
        table_html = '<table class="bom-table"><thead><tr>'
        for col in ["Part Number", "Description", "Qty", "Category"]:
            table_html += f"<th>{col}</th>"
        table_html += "</tr></thead><tbody>"
        for _, r in bom_df.iterrows():
            table_html += f'<tr><td class="pn">{r["Part Number"]}</td><td>{r["Description"]}</td><td class="qty">{r["Qty"]}</td><td class="cat">{r["Category"]}</td></tr>'
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        csv_out = bom_df.to_csv(index=False)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        st.download_button(label="⬇  Export BoM as CSV", data=csv_out, file_name=f"BoM_{timestamp}.csv", mime="text/csv")
    else:
        st.markdown('<div style="color:#7ec8e3;font-size:0.9rem;">Make selections above to populate the BoM.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


if check_password():
    main()
