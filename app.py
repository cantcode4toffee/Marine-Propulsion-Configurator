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
  .summary-strip {
    background: rgba(61,181,230,0.08);
    border: 1px solid rgba(61,181,230,0.25);
    border-radius: 10px;
    padding: 0.75rem 1.25rem;
    margin-bottom: 1.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    align-items: center;
  }
  .summary-item { display: inline-flex; align-items: center; gap: 5px; }
  .summary-label { color: #7ec8e3; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }
  .summary-pill {
    background: rgba(61,181,230,0.18);
    border: 1px solid rgba(61,181,230,0.35);
    border-radius: 14px;
    padding: 2px 10px;
    color: #b8e4f5;
    font-size: 0.78rem;
  }
  .badge {
    display: inline-block;
    border-radius: 4px;
    padding: 1px 7px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }
  .badge-included { background: rgba(40,180,100,0.18); color: #6de8a8; border: 1px solid rgba(40,180,100,0.3); }
  .badge-derived  { background: rgba(100,140,255,0.18); color: #a0b8ff; border: 1px solid rgba(100,140,255,0.3); }
  .badge-customer { background: rgba(255,180,60,0.18);  color: #ffd080; border: 1px solid rgba(255,180,60,0.3);  }
  .badge-harness  { background: rgba(180,100,255,0.18); color: #d0a0ff; border: 1px solid rgba(180,100,255,0.3); }
  .badge-sel      { background: rgba(61,181,230,0.18);  color: #7ec8e3; border: 1px solid rgba(61,181,230,0.3);  }
  .bom-table { width: 100%; border-collapse: collapse; }
  .bom-table th {
    color: #7ec8e3; font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.06em; text-transform: uppercase;
    border-bottom: 1px solid rgba(100,180,255,0.2);
    padding: 6px 10px; text-align: left;
  }
  .bom-table th.right { text-align: right; }
  .bom-table td {
    color: #e8f4f8; font-size: 0.86rem;
    padding: 9px 10px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    vertical-align: top;
  }
  .bom-table tr:nth-child(even) td { background: rgba(255,255,255,0.025); }
  .bom-table td.pn  { font-family: monospace; color: #7ec8e3; font-size: 0.8rem; }
  .bom-table td.qty { text-align: right; font-weight: 600; }
  .bom-table td.cat { color: #a0c4d8; font-size: 0.8rem; }
  .bom-table td.note { color: #6a8ea0; font-size: 0.76rem; }
  .harness-note { color: #7a9eb0; font-size: 0.77rem; margin: 2px 0 8px 0; }
  .warn-box {
    background: rgba(255,160,60,0.1);
    border: 1px solid rgba(255,160,60,0.35);
    border-radius: 8px;
    padding: 0.55rem 1rem;
    color: #ffd080; font-size: 0.84rem;
    margin-bottom: 0.6rem;
  }
  .page-title { color: #e8f4f8; font-size: 1.8rem; font-weight: 600; margin-bottom: 0.2rem; }
  .page-sub   { color: #7ec8e3; font-size: 0.92rem; margin-bottom: 1.75rem; }
  .stTextInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(100,180,255,0.3) !important;
    border-radius: 8px !important; color: #e8f4f8 !important;
  }
  .stButton > button {
    background: rgba(14,90,160,0.5) !important;
    border: 1px solid #3db5e6 !important;
    color: #e8f4f8 !important; border-radius: 8px !important; font-weight: 500 !important;
  }
  .stButton > button:hover { background: rgba(14,90,160,0.8) !important; }
  div[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(100,180,255,0.3) !important;
    border-radius: 8px !important; color: #e8f4f8 !important;
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
        df["sort_order"] = pd.to_numeric(df.get("sort_order", 0), errors="coerce").fillna(999)
        df = df.sort_values("sort_order").reset_index(drop=True)
        for col in ["conditions", "harness_id", "notes", "source_type", "category",
                    "label", "part_number", "pn_pattern", "section", "group_id", "option_id"]:
            if col in df.columns:
                df[col] = df[col].fillna("").astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Could not load configurator.csv: {e}")
        return pd.DataFrame()


def get_effective_conditions(row):
    """Return condition string, falling back to harness_id when it looks like a condition."""
    cond = row.get("conditions", "")
    if not cond:
        hid = row.get("harness_id", "")
        if "=" in str(hid):
            return hid
    return cond


def parse_conditions(cond_str):
    """Parse 'key=v1|v2;key2=v3' into list of (key, [values]) tuples."""
    if not cond_str:
        return []
    result = []
    for part in str(cond_str).split(";"):
        part = part.strip()
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        result.append((k.strip(), [x.strip() for x in v.split("|")]))
    return result


def row_is_active(row, selections):
    """Return True if all conditions in a row are satisfied by current selections."""
    for key, values in parse_conditions(get_effective_conditions(row)):
        if selections.get(key) not in values:
            return False
    return True


def get_selectable_groups(df):
    """Return ordered list of (group_id, group_df) for source_type==selectable rows."""
    sel_df = df[df["source_type"] == "selectable"].copy()
    seen, groups = [], []
    for _, row in sel_df.iterrows():
        gid = row["group_id"]
        if gid not in seen:
            seen.append(gid)
            groups.append((gid, sel_df[sel_df["group_id"] == gid].copy()))
    return groups


def resolve_harness_pn(hrow, chosen_len, lookup_df):
    """Return (part_number, warning_or_None) for a harness row at the chosen length."""
    hid = hrow.get("harness_id", "")
    if not hid or "=" in hid:
        return None, f"No harness_id set for '{hrow['label']}'"
    matches = lookup_df[
        (lookup_df["harness_id"] == hid) &
        (lookup_df["label"] == chosen_len)
    ]
    if not matches.empty:
        return matches["part_number"].values[0], None
    pn_pat = hrow.get("pn_pattern", "")
    if pn_pat and pn_pat != "lookup":
        return pn_pat.replace("{LENGTH}", chosen_len), None
    return None, f"No part number found for '{hrow['label']}' at {chosen_len}"


def safe_qty(v):
    try:
        return int(float(str(v)))
    except (ValueError, TypeError):
        return 1


SECTION_LABELS = {
    "market": "Market",
    "drive_system": "Drive System",
    "battery_pack": "HV Battery Pack",
    "display_screen": "Display Screen",
    "throttle": "Throttle",
    "drive_interface": "Drive Interface",
}

SUMMARY_ORDER = ["market", "drive_system", "battery_pack", "display_screen", "throttle", "drive_interface"]


def main():
    df = load_data()
    if df.empty:
        st.warning("No data loaded. Check that data/configurator.csv exists.")
        return

    lookup_df = df[df["section"] == "harness_pn_lookup"].copy()
    main_df   = df[df["section"] != "harness_pn_lookup"].copy()

    selectable_groups = get_selectable_groups(main_df)

    # Initialise session state defaults for all selectable groups
    for gid, gdf in selectable_groups:
        key = f"sel_{gid}"
        if key not in st.session_state or st.session_state[key] not in gdf["label"].tolist():
            st.session_state[key] = gdf["label"].iloc[0]

    def current_selections():
        sels = {}
        for gid, gdf in selectable_groups:
            sel_label = st.session_state.get(f"sel_{gid}", gdf["label"].iloc[0])
            lbl_map = dict(zip(gdf["label"], gdf["option_id"]))
            oid = lbl_map.get(sel_label)
            if oid:
                sels[gid] = oid
        return sels

    selections = current_selections()

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown('<div class="page-title">⚓ Marine Propulsion Configurator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Select your powertrain options to generate the top-level Bill of Materials.</div>', unsafe_allow_html=True)

    # ── Summary strip ─────────────────────────────────────────────────────────
    summary_items = []
    oid_to_label = {}
    for gid, gdf in selectable_groups:
        oid_to_label.update(dict(zip(gdf["option_id"], gdf["label"])))

    for gid in SUMMARY_ORDER:
        oid = selections.get(gid)
        if not oid:
            continue
        lbl = oid_to_label.get(oid, "")
        if not lbl:
            continue
        disp = SECTION_LABELS.get(gid, gid.replace("_", " ").title())
        summary_items.append(
            f'<span class="summary-item">'
            f'<span class="summary-label">{disp}</span>'
            f'<span class="summary-pill">{lbl}</span>'
            f'</span>'
        )
    if summary_items:
        st.markdown(
            f'<div class="summary-strip">{"&nbsp;·&nbsp;".join(summary_items)}</div>',
            unsafe_allow_html=True,
        )

    # ── Input sections ────────────────────────────────────────────────────────
    sec_num = 1
    for gid, gdf in selectable_groups:
        # Filter options that pass their own row-level conditions
        active_opts = gdf[gdf.apply(lambda r: row_is_active(r, selections), axis=1)]

        # Hide section if ALL options carry conditions and none are active
        if all(get_effective_conditions(r) for _, r in gdf.iterrows()) and active_opts.empty:
            continue

        labels = (active_opts if not active_opts.empty else gdf)["label"].tolist()
        key    = f"sel_{gid}"

        if st.session_state.get(key) not in labels:
            st.session_state[key] = labels[0]

        current_lbl = st.session_state[key]
        sec_name    = SECTION_LABELS.get(gid, gid.replace("_", " ").title())

        st.markdown(
            f'<div class="section-card">'
            f'<div class="section-title">{sec_num} — {sec_name}: {current_lbl}</div>',
            unsafe_allow_html=True,
        )
        st.radio(sec_name, labels, label_visibility="collapsed", key=key, horizontal=True)
        st.markdown("</div>", unsafe_allow_html=True)
        sec_num += 1

    # Re-read selections after widgets have rendered
    selections = current_selections()

    # ── Included / Derived / Info items ───────────────────────────────────────
    non_sel_df   = main_df[main_df["source_type"].isin(["included", "derived", "info"])].copy()
    active_items = non_sel_df[non_sel_df.apply(lambda r: row_is_active(r, selections), axis=1)]

    if not active_items.empty:
        st.markdown(
            f'<div class="section-card">'
            f'<div class="section-title">{sec_num} — Included / Derived Items</div>',
            unsafe_allow_html=True,
        )
        for _, row in active_items.iterrows():
            st_type = row.get("source_type", "")
            if st_type == "included":
                badge = '<span class="badge badge-included">Included</span>'
            elif st_type == "derived":
                badge = '<span class="badge badge-derived">Derived</span>'
            else:
                badge = '<span class="badge badge-customer">Customer Supplied</span>'
            pn = row.get("part_number", "")
            pn_html = (
                f' <span style="font-family:monospace;color:#7ec8e3;font-size:0.78rem;">({pn})</span>'
                if pn and pn not in ("N/A", "") else ""
            )
            st.markdown(
                f'<div style="padding:4px 0;color:#e8f4f8;font-size:0.86rem;">'
                f'{badge} {row["label"]}{pn_html}'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
        sec_num += 1

    # ── Harness section ───────────────────────────────────────────────────────
    harness_df     = main_df[main_df["source_type"] == "harness"].copy()
    active_harness = harness_df[harness_df.apply(lambda r: row_is_active(r, selections), axis=1)]

    harness_resolved = {}   # option_id → (hrow, chosen_len, resolved_pn, warning)
    harness_warnings = []

    if not active_harness.empty:
        st.markdown(
            f'<div class="section-card">'
            f'<div class="section-title">{sec_num} — Harness Lengths ({len(active_harness)} runs)</div>',
            unsafe_allow_html=True,
        )
        for _, hrow in active_harness.iterrows():
            lengths     = [l.strip() for l in str(hrow["harness_lengths"]).split("|") if l.strip()]
            default     = str(hrow.get("default_length", lengths[0])).strip()
            default_idx = lengths.index(default) if default in lengths else 0

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f'<div style="color:#e8f4f8;font-size:0.9rem;font-weight:500;padding-top:8px;">'
                    f'{hrow["label"]}</div>',
                    unsafe_allow_html=True,
                )
                if hrow.get("notes"):
                    st.markdown(f'<div class="harness-note">{hrow["notes"]}</div>', unsafe_allow_html=True)
            with col2:
                chosen_len = st.selectbox(
                    hrow["label"], lengths,
                    index=default_idx,
                    label_visibility="collapsed",
                    key=f"harn_{hrow['option_id']}",
                )

            resolved_pn, warn = resolve_harness_pn(hrow, chosen_len, lookup_df)
            if warn:
                harness_warnings.append(warn)
                st.markdown(f'<div style="color:#ffd080;font-size:0.75rem;margin-bottom:10px;">⚠ {warn}</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div style="color:#7ec8e3;font-size:0.75rem;font-family:monospace;margin-bottom:10px;margin-top:2px;">'
                    f'{resolved_pn}</div>',
                    unsafe_allow_html=True,
                )
            harness_resolved[hrow["option_id"]] = (hrow, chosen_len, resolved_pn, warn)

        st.markdown("</div>", unsafe_allow_html=True)
        sec_num += 1

    # ── Validation warnings ───────────────────────────────────────────────────
    warnings = []
    if not selections.get("market"):
        warnings.append("No market selected.")
    if not selections.get("drive_system"):
        warnings.append("No drive system selected.")
    warnings.extend(harness_warnings)

    # ── Build BOM ─────────────────────────────────────────────────────────────
    bom_rows     = []
    traceability = []

    def add_row(pn, desc, qty, cat, src_type, length="", notes="", trace_reason="", trace_meta=None):
        if pn in ("UPON-REQUEST",):
            warnings.append(f"'{desc}' is available upon request only (PN: {pn}).")
        bom_rows.append({
            "Part Number":     pn,
            "Description":     desc,
            "Qty":             qty,
            "Category":        cat,
            "Source Type":     src_type,
            "Selected Length": length,
            "Notes":           notes,
        })
        traceability.append({
            "label":       desc,
            "source_type": src_type,
            "reason":      trace_reason,
            **(trace_meta or {}),
        })

    # Selectable
    for gid, gdf in selectable_groups:
        oid = selections.get(gid)
        if not oid:
            continue
        for _, r in gdf[gdf["option_id"] == oid].iterrows():
            pn = r.get("part_number", "")
            if not pn:
                continue
            add_row(
                pn, r["label"], safe_qty(r.get("qty", 1)),
                r.get("category", ""), "Selectable",
                notes=r.get("notes", ""),
                trace_reason=f"Selected in '{SECTION_LABELS.get(gid, gid)}'",
            )

    # Included / Derived / Info
    for _, r in active_items.iterrows():
        pn = r.get("part_number", "")
        if pn == "N/A":
            warnings.append(f"'{r['label']}' has no part number (N/A) — customer-supplied item.")
            continue
        if not pn:
            continue
        cond = get_effective_conditions(r)
        add_row(
            pn, r["label"], safe_qty(r.get("qty", 1)),
            r.get("category", ""), r.get("source_type", "included").capitalize(),
            notes=r.get("notes", ""),
            trace_reason=f"Conditions met: {cond}" if cond else "Always included",
            trace_meta={"section": r.get("section", ""), "group_id": r.get("group_id", ""), "conditions": cond},
        )

    # Harness
    for oid, (hrow, chosen_len, resolved_pn, warn) in harness_resolved.items():
        if warn or not resolved_pn:
            continue
        add_row(
            resolved_pn, f"{hrow['label']} ({chosen_len})",
            safe_qty(hrow.get("qty", 1)),
            hrow.get("category", "Harness"), "Harness",
            length=chosen_len, notes=hrow.get("notes", ""),
            trace_reason=f"Harness length selected: {chosen_len}",
            trace_meta={"harness_id": hrow.get("harness_id", ""), "conditions": get_effective_conditions(hrow)},
        )

    # ── Warnings display ──────────────────────────────────────────────────────
    for w in warnings:
        st.markdown(f'<div class="warn-box">⚠ {w}</div>', unsafe_allow_html=True)

    # ── BOM table ─────────────────────────────────────────────────────────────
    bom_count    = len(bom_rows)
    harness_count = sum(1 for r in bom_rows if r["Source Type"] == "Harness")

    st.markdown(
        f'<div class="section-card">'
        f'<div class="section-title">'
        f'{sec_num} — Top-level BoM summary &nbsp;·&nbsp; {bom_count} lines &nbsp;·&nbsp; {harness_count} harness runs'
        f'</div>',
        unsafe_allow_html=True,
    )

    BADGE_MAP = {
        "harness":    '<span class="badge badge-harness">Harness</span>',
        "included":   '<span class="badge badge-included">Included</span>',
        "derived":    '<span class="badge badge-derived">Derived</span>',
        "selectable": '<span class="badge badge-sel">Selected</span>',
        "info":       '<span class="badge badge-customer">Info</span>',
    }

    if bom_rows:
        bom_df = pd.DataFrame(bom_rows)

        table_html = (
            '<table class="bom-table"><thead><tr>'
            '<th>Part Number</th><th>Description</th>'
            '<th class="right">Qty</th><th>Category</th>'
            '<th>Type</th><th>Notes</th>'
            '</tr></thead><tbody>'
        )
        for _, r in bom_df.iterrows():
            src_key  = str(r["Source Type"]).lower()
            src_badge = BADGE_MAP.get(src_key, f'<span style="color:#a0c4d8;font-size:0.78rem;">{r["Source Type"]}</span>')
            table_html += (
                f'<tr>'
                f'<td class="pn">{r["Part Number"]}</td>'
                f'<td>{r["Description"]}</td>'
                f'<td class="qty">{r["Qty"]}</td>'
                f'<td class="cat">{r["Category"]}</td>'
                f'<td>{src_badge}</td>'
                f'<td class="note">{r["Notes"]}</td>'
                f'</tr>'
            )
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Export
        export_df = bom_df[["Part Number", "Description", "Qty", "Category", "Source Type", "Selected Length", "Notes"]].copy()
        export_df.columns = ["part_number", "description", "qty", "category", "source_type", "selected_length", "notes"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        st.download_button(
            label="⬇  Export BoM as CSV",
            data=export_df.to_csv(index=False),
            file_name=f"BoM_{timestamp}.csv",
            mime="text/csv",
        )

        # Traceability
        with st.expander("Why included? — Traceability"):
            for item in traceability:
                cond_hint = f' <span style="color:#6a8ea0;font-size:0.74rem;">({item.get("conditions","")})</span>' if item.get("conditions") else ""
                st.markdown(
                    f'<div style="padding:3px 0;color:#b0cfe0;font-size:0.81rem;">'
                    f'<span style="color:#e8f4f8;font-weight:500;">{item["label"]}</span>'
                    f' — {item["reason"]}{cond_hint}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
    else:
        st.markdown(
            '<div style="color:#7ec8e3;font-size:0.9rem;">Make selections above to populate the BoM.</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


if check_password():
    main()
