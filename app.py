import html
import streamlit as st
from logic import (
    calculate_stats,
    create_study_record,
    format_minutes_display,
)
from data_store import (
    add_record,
    clear_all_records,
    delete_record,
    load_records,
)

st.set_page_config(
    page_title="Study Time Tracker",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

APPLE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-canvas: #F5F5F7;
    --bg-card: #FFFFFF;
    --text-primary: #1D1D1F;
    --text-secondary: #86868B;
    --accent-blue: #0071E3;
    --accent-blue-hover: #0077ED;
    --border-subtle: rgba(0, 0, 0, 0.06);
    --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.04);
    --shadow-hover: 0 8px 28px rgba(0, 0, 0, 0.07);
}

/* Global Canvas & Typography */
html, body, [class*="css"], .stApp {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", "Sukhumvit Set", "Noto Sans Thai", sans-serif !important;
    background-color: var(--bg-canvas) !important;
    color: var(--text-primary) !important;
    -webkit-font-smoothing: antialiased;
}

/* ซ่อนแถบเมนูมาตรฐานของ Streamlit เพื่อให้ดูคลีนเหมือน Web App */
#MainMenu, footer, header {
    visibility: hidden;
    height: 0;
}

.block-container {
    max-width: 740px !important;
    padding-top: 2.8rem !important;
    padding-bottom: 4rem !important;
}

/* Smooth Entrance Animation */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.apple-hero {
    text-align: center;
    margin-bottom: 2rem;
    animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.apple-eyebrow {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent-blue);
    margin-bottom: 0.35rem;
}

.apple-title {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin: 0;
    line-height: 1.15;
}

.apple-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    font-weight: 400;
}

/* Form Container Card */
[data-testid="stForm"] {
    background-color: var(--bg-card);
    border: 1px solid var(--border-subtle) !important;
    border-radius: 22px !important;
    padding: 1.6rem 1.8rem !important;
    box-shadow: var(--shadow-card);
    transition: box-shadow 0.3s ease;
    animation: fadeInUp 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}

[data-testid="stForm"]:hover {
    box-shadow: var(--shadow-hover);
}

/* Inputs Styling */
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
    background-color: #F5F5F7 !important;
    border: 1.5px solid transparent !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 0.96rem !important;
    padding-top: 0.55rem !important;
    padding-bottom: 0.55rem !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus, .stNumberInput input:focus {
    background-color: #FFFFFF !important;
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.14) !important;
}

.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #424245 !important;
    margin-bottom: 0.25rem !important;
}

/* Primary Submit Button (Apple Blue Pill) */
[data-testid="stFormSubmitButton"] button {
    background-color: var(--accent-blue) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.65rem 1.4rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    transition: all 0.22s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    box-shadow: 0 4px 12px rgba(0, 113, 227, 0.22) !important;
}

[data-testid="stFormSubmitButton"] button:hover {
    background-color: var(--accent-blue-hover) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(0, 113, 227, 0.30) !important;
}

[data-testid="stFormSubmitButton"] button:active {
    transform: scale(0.985) !important;
}

/* Bento Stat Cards */
.bento-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.bento-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 1.25rem 1.4rem;
    box-shadow: var(--shadow-card);
}

.bento-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.3rem;
}

.bento-value {
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-primary);
}

/* iOS Storage-Style Breakdown Bar */
.breakdown-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 1.15rem 1.4rem;
    box-shadow: var(--shadow-card);
    margin-bottom: 1.8rem;
}

.seg-bar {
    display: flex;
    height: 10px;
    width: 100%;
    border-radius: 999px;
    overflow: hidden;
    background: #E8E8ED;
    gap: 2px;
    margin: 0.7rem 0 0.8rem 0;
}

.seg-short { background: #34C759; transition: width 0.5s ease; }
.seg-medium { background: #007AFF; transition: width 0.5s ease; }
.seg-long { background: #5856D6; transition: width 0.5s ease; }

.legend-row {
    display: flex;
    gap: 1.2rem;
    flex-wrap: wrap;
    font-size: 0.82rem;
    color: #424245;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
}

/* Record Card */
.record-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 1rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.025);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 0.55rem;
}

.record-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
}

.record-subject {
    font-size: 1.02rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.15rem;
}

.record-time {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.record-right {
    display: flex;
    align-items: center;
    gap: 10px;
}

.duration-text {
    font-size: 0.98rem;
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
}

/* Soft Apple Pill Badges */
.badge {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 11px;
    border-radius: 999px;
    letter-spacing: 0.01em;
}

.badge-Short { background: rgba(52, 199, 89, 0.14); color: #1E8E3E; }
.badge-Medium { background: rgba(0, 122, 255, 0.12); color: #0066CC; }
.badge-Long { background: rgba(88, 86, 214, 0.14); color: #4B49C8; }

/* Subtle Secondary / Delete Buttons */
.stButton button {
    background: transparent !important;
    color: #86868B !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    border-radius: 12px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.stButton button:hover {
    background: rgba(255, 59, 48, 0.08) !important;
    color: #FF3B30 !important;
    border-color: rgba(255, 59, 48, 0.25) !important;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 3rem 1.5rem;
    background: var(--bg-card);
    border: 1px dashed rgba(0, 0, 0, 0.12);
    border-radius: 22px;
    color: var(--text-secondary);
}

.section-header {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-primary);
    margin: 0.5rem 0 0.8rem 0;
}

.helper-hint {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin-top: -0.35rem;
    margin-bottom: 0.8rem;
}
</style>
"""
st.markdown(APPLE_CSS, unsafe_allow_html=True)

# --- 3. Hero Header ---
st.markdown(
    """
    <div class="apple-hero">
        <div class="apple-eyebrow">Focus · Minimal · Persistent</div>
        <h1 class="apple-title">Study Time Tracker</h1>
        <p class="apple-subtitle">บันทึกและติดตามเวลาเรียนรู้ในแต่ละวันอย่างเป็นระบบ</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 4. Input Form Card (UI -> Logic -> Data) ---
with st.form("study_entry_form", clear_on_submit=True):
    col1, col2 = st.columns([1.8, 1])
    with col1:
        subject_input = st.text_input(
            "ชื่อวิชา (Subject)",
            placeholder="เช่น คณิตศาสตร์, Python, ฟิสิกส์...",
        )
    with col2:
        # ไม่จำกัด min_value/max_value เพื่อให้ทดสอบค่า 0 และ 241 ผ่าน Logic Layer ได้จริง
        duration_input = st.number_input(
            "เวลาเรียน (นาที)",
            value=30,
            step=1,
            format="%d",
        )

    st.markdown(
        '<div class="helper-hint">'
        "เกณฑ์เวลา: <b>Short</b> (&lt; 30 นาที) · "
        "<b>Medium</b> (30–59 นาที) · "
        "<b>Long</b> (60–240 นาที)"
        "</div>",
        unsafe_allow_html=True,
    )

    submitted = st.form_submit_button("บันทึกเวลาเรียน", use_container_width=True)

    if submitted:
        # ส่งต่อไปตรวจสอบและจำแนกใน Logic Layer
        new_record, error_msg = create_study_record(
            subject_input, int(duration_input)
        )
        if error_msg:
            st.error(error_msg, icon="⚠️")
        else:
            # ส่งต่อไปบันทึกถาวรใน Data Layer
            add_record(new_record)
            st.toast(
                f"บันทึก {new_record['subject']} ({new_record['duration']} นาที · {new_record['category']}) เรียบร้อย",
                icon="✅",
            )
            st.rerun()

# --- 5. Load Persisted Data ---
records = load_records()
stats = calculate_stats(records)

# --- 6. Dashboard Overview (Bento Cards + Segmented Bar) ---
if records:
    total_str = format_minutes_display(stats["total_minutes"])
    avg_str = f"{stats['avg_minutes']} นาที"

    st.markdown(
        f"""
        <div class="bento-grid">
            <div class="bento-card">
                <div class="bento-label">เวลาเรียนรู้รวมทั้งหมด</div>
                <div class="bento-value">{total_str}</div>
            </div>
            <div class="bento-card">
                <div class="bento-label">เวลาเฉลี่ยต่อครั้ง</div>
                <div class="bento-value">{avg_str}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_items = len(records)
    c_short = stats["counts"]["Short"]
    c_med = stats["counts"]["Medium"]
    c_long = stats["counts"]["Long"]

    p_short = (c_short / total_items) * 100
    p_med = (c_med / total_items) * 100
    p_long = (c_long / total_items) * 100

    st.markdown(
        f"""
        <div class="breakdown-card">
            <div class="bento-label">สัดส่วนระยะเวลาการเรียนรู้</div>
            <div class="seg-bar">
                <div class="seg-short" style="width: {p_short:.1f}%;"></div>
                <div class="seg-medium" style="width: {p_med:.1f}%;"></div>
                <div class="seg-long" style="width: {p_long:.1f}%;"></div>
            </div>
            <div class="legend-row">
                <span class="legend-item"><span class="dot" style="background:#34C759;"></span>Short: {p_short:.0f}%</span>
                <span class="legend-item"><span class="dot" style="background:#007AFF;"></span>Medium: {p_med:.0f}%</span>
                <span class="legend-item"><span class="dot" style="background:#5856D6;"></span>Long: {p_long:.0f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- 7. History Section with Search & Filter ---
header_col, action_col = st.columns([3, 1])
with header_col:
    st.markdown('<div class="section-header">ประวัติการเรียน</div>', unsafe_allow_html=True)
with action_col:
    if records:
        if st.button("ล้างทั้งหมด", use_container_width=True):
            clear_all_records()
            st.rerun()

if not records:
    st.markdown(
        """
        <div class="empty-state">
            <div style="font-size: 2rem; margin-bottom: 0.4rem;">📖</div>
            <div style="font-weight: 600; color: #1D1D1F; margin-bottom: 0.2rem;">ยังไม่มีประวัติการเรียน</div>
            <div style="font-size: 0.88rem;">เริ่มบันทึกวิชาแรกของคุณด้านบนได้เลย ข้อมูลจะถูกจัดเก็บไว้ในไฟล์ JSON อัตโนมัติ</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    f_col1, f_col2 = st.columns([1.6, 1])
    with f_col1:
        search_query = st.text_input(
            "ค้นหาวิชา",
            placeholder="พิมพ์ชื่อวิชาเพื่อค้นหา...",
            label_visibility="collapsed",
        )
    with f_col2:
        category_filter = st.selectbox(
            "กรองระดับเวลา",
            ["ทั้งหมด", "Short", "Medium", "Long"],
            label_visibility="collapsed",
        )

    filtered_records = [
        r
        for r in records
        if (category_filter == "ทั้งหมด" or r.get("category") == category_filter)
        and (search_query.strip().lower() in r.get("subject", "").lower())
    ]

    if not filtered_records:
        st.info("ไม่พบรายการที่ตรงกับเงื่อนไขการค้นหา")
    else:
        for rec in filtered_records:
            safe_subject = html.escape(str(rec.get("subject", "")))
            safe_time = html.escape(str(rec.get("timestamp", "")))
            duration_val = rec.get("duration", 0)
            category_val = rec.get("category", "Short")
            rec_id = rec.get("id", "")

            card_col, del_col = st.columns([9, 1], vertical_alignment="center")
            with card_col:
                st.markdown(
                    f"""
                    <div class="record-card">
                        <div>
                            <div class="record-subject">{safe_subject}</div>
                            <div class="record-time">{safe_time}</div>
                        </div>
                        <div class="record-right">
                            <span class="duration-text">{duration_val} นาที</span>
                            <span class="badge badge-{category_val}">{category_val}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with del_col:
                if st.button("✕", key=f"del_{rec_id}", help="ลบรายการนี้"):
                    delete_record(rec_id)
                    st.rerun()