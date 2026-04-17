import streamlit as st
from parser import QueryParser
from analyzer import QueryAnalyzer

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SmartQueryLab",
    layout="wide"
)

# =========================
# CUSTOM CSS (IDENTIDADE VISUAL)
# =========================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+Chettan+2:wght@400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Baloo Chettan 2', cursive;
    }

    .title {
        color: #1a4683;
        font-size: 36px;
        font-weight: 600;
    }

    .score {
        font-size: 28px;
        font-weight: bold;
    }

    .good { color: #2ccf63; }
    .medium { color: #2581c4; }
    .bad { color: #de6a73; }

    .box {
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
    }

    .issues {
        background-color: #fdecec;
        color: #de6a73;
    }

    .suggestions {
        background-color: #eaf6ff;
        color: #1a4683;
    }

    </style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown('<div class="title">SmartQueryLab</div>', unsafe_allow_html=True)
st.write("SQL Performance Risk Analyzer")

# =========================
# SESSION STATE
# =========================
if "query" not in st.session_state:
    st.session_state.query = ""

# =========================
# FUNÇÃO CLEAR
# =========================
def clear_query():
    st.session_state.query = ""

# =========================
# INPUT
# =========================
query = st.text_area(
    "Paste your SQL query here:",
    height=250,
    key="query"
)

# =========================
# BUTTONS
# =========================
col1, col2 = st.columns([2,1])

with col1:
    analyze_clicked = st.button("Analyze Query")

with col2:
    st.button("Clear", on_click=clear_query)

# =========================
# ANALYSIS EXECUTION
# =========================
if analyze_clicked:

    if query.strip() == "":
        st.warning("Please enter a query.")
    else:
        parser = QueryParser(query)
        analyzer = QueryAnalyzer(parser)

        issues, suggestions, score, classification = analyzer.analyze()

        # =========================
        # SCORE DISPLAY
        # =========================
        if score >= 70:
            color_class = "good"
        elif score >= 50:
            color_class = "medium"
        else:
            color_class = "bad"

        st.markdown(
            f'<div class="score {color_class}">Score: {score}/100 ({classification})</div>',
            unsafe_allow_html=True
        )

        # =========================
        # ISSUES
        # =========================
        st.markdown('<div class="box issues"><b>Issues:</b></div>', unsafe_allow_html=True)
        for issue in issues:
            st.write(f"- {issue}")

        # =========================
        # SUGGESTIONS
        # =========================
        st.markdown('<div class="box suggestions"><b>Suggestions:</b></div>', unsafe_allow_html=True)
        for suggestion in suggestions:
            st.write(f"- {suggestion}")