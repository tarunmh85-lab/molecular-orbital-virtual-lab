
import streamlit as st
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Molecular Orbital Virtual Lab",
    page_icon="⚛️",
    layout="wide"
)

# ==================================================
# MOLECULE DATABASE
# Electron counts refer to the curated MO model.
# ==================================================

molecules = {
    "H2": {
        "name": "Hydrogen",
        "bonding": 2,
        "antibonding": 0,
        "magnetic": "Diamagnetic",
        "configuration": "sigma 1s^2",
        "orbitals": [
            ("sigma 1s", "up down"),
            ("sigma* 1s", "empty")
        ],
        "explanation": "Two electrons occupy the bonding 1s orbital."
    },

    "He2": {
        "name": "Helium",
        "bonding": 2,
        "antibonding": 2,
        "magnetic": "Diamagnetic",
        "configuration": "sigma 1s^2 sigma* 1s^2",
        "orbitals": [
            ("sigma 1s", "up down"),
            ("sigma* 1s", "up down")
        ],
        "explanation": "Bonding and antibonding electrons cancel the bond order."
    },

    "Li2": {
        "name": "Lithium",
        "bonding": 2,
        "antibonding": 0,
        "magnetic": "Diamagnetic",
        "configuration": "sigma 2s^2",
        "orbitals": [
            ("sigma 2s", "up down"),
            ("sigma* 2s", "empty")
        ],
        "explanation": "The two valence electrons occupy the bonding 2s orbital."
    },

    "Be2": {
        "name": "Beryllium",
        "bonding": 2,
        "antibonding": 2,
        "magnetic": "Diamagnetic",
        "configuration": "sigma 2s^2 sigma* 2s^2",
        "orbitals": [
            ("sigma 2s", "up down"),
            ("sigma* 2s", "up down")
        ],
        "explanation": "The simple MO model predicts zero bond order."
    },

    "B2": {
        "name": "Boron",
        "bonding": 4,
        "antibonding": 2,
        "magnetic": "Paramagnetic",
        "configuration": "sigma 2s^2 sigma* 2s^2 pi 2px^1 pi 2py^1",
        "orbitals": [
            ("sigma 2s", "up down"),
            ("sigma* 2s", "up down"),
            ("pi 2px", "up"),
            ("pi 2py", "up"),
            ("sigma 2pz", "empty")
        ],
        "explanation": "Two unpaired electrons occupy separate pi orbitals."
    },

    "C2": {
        "name": "Carbon",
        "bonding": 6,
        "antibonding": 2,
        "magnetic": "Diamagnetic",
        "configuration": "sigma 2s^2 sigma* 2s^2 pi 2px^2 pi 2py^2",
        "orbitals": [
            ("sigma 2s", "up down"),
            ("sigma* 2s", "up down"),
            ("pi 2px", "up down"),
            ("pi 2py", "up down"),
            ("sigma 2pz", "empty")
        ],
        "explanation": "All occupied orbitals contain paired electrons."
    },

    "N2": {
        "name": "Nitrogen",
        "bonding": 8,
        "antibonding": 2,
        "magnetic": "Diamagnetic",
        "configuration": "sigma 2s^2 sigma* 2s^2 pi 2px^2 pi 2py^2 sigma 2pz^2",
        "orbitals": [
            ("sigma 2s", "up down"),
            ("sigma* 2s", "up down"),
            ("pi 2px", "up down"),
            ("pi 2py", "up down"),
            ("sigma 2pz", "up down"),
            ("pi* 2px", "empty"),
            ("pi* 2py", "empty")
        ],
        "explanation": "All occupied molecular orbitals have paired electrons."
    },

    "O2": {
        "name": "Oxygen",
        "bonding": 8,
        "antibonding": 4,
        "magnetic": "Paramagnetic",
        "configuration": "sigma 2s^2 sigma* 2s^2 sigma 2pz^2 pi 2px^2 pi 2py^2 pi* 2px^1 pi* 2py^1",
        "orbitals": [
            ("sigma 2s", "up down"),
            ("sigma* 2s", "up down"),
            ("sigma 2pz", "up down"),
            ("pi 2px", "up down"),
            ("pi 2py", "up down"),
            ("pi* 2px", "up"),
            ("pi* 2py", "up")
        ],
        "explanation": "Two unpaired electrons occupy separate antibonding pi orbitals."
    },

    "F2": {
        "name": "Fluorine",
        "bonding": 8,
        "antibonding": 6,
        "magnetic": "Diamagnetic",
        "configuration": "sigma 2s^2 sigma* 2s^2 sigma 2pz^2 pi 2px^2 pi 2py^2 pi* 2px^2 pi* 2py^2",
        "orbitals": [
            ("sigma 2s", "up down"),
            ("sigma* 2s", "up down"),
            ("sigma 2pz", "up down"),
            ("pi 2px", "up down"),
            ("pi 2py", "up down"),
            ("pi* 2px", "up down"),
            ("pi* 2py", "up down")
        ],
        "explanation": "All occupied orbitals contain paired electrons."
    },

    "Ne2": {
        "name": "Neon",
        "bonding": 8,
        "antibonding": 8,
        "magnetic": "Diamagnetic",
        "configuration": "sigma 2s^2 sigma* 2s^2 sigma 2pz^2 pi 2px^2 pi 2py^2 pi* 2px^2 pi* 2py^2 sigma* 2pz^2",
        "orbitals": [
            ("sigma 2s", "up down"),
            ("sigma* 2s", "up down"),
            ("sigma 2pz", "up down"),
            ("pi 2px", "up down"),
            ("pi 2py", "up down"),
            ("pi* 2px", "up down"),
            ("pi* 2py", "up down"),
            ("sigma* 2pz", "up down")
        ],
        "explanation": "The simple MO model predicts zero bond order."
    }
}

# ==================================================
# SESSION STATE
# ==================================================

if "selected_molecule" not in st.session_state:
    st.session_state.selected_molecule = "O2"

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

st.sidebar.title("⚛️ MO Virtual Lab")
st.sidebar.caption("Chemistry Learning Platform")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Home",
        "🔬 Molecular Analysis",
        "🧠 Quiz",
        "📄 Download Report"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Molecular Orbital Theory Project")

# ==================================================
# HOME PAGE
# ==================================================

if page == "🏠 Home":

    st.title("⚛️ Molecular Orbital Theory Virtual Lab")

    st.subheader("Welcome to your virtual chemistry laboratory!")

    st.write(
        "Learn molecular orbital theory through concepts, "
        "interactive molecular analysis and quizzes."
    )

    st.divider()

    st.header("📚 Fundamental Concepts")

    with st.expander("1. What is Molecular Orbital Theory?"):
        st.write(
            "Molecular Orbital Theory explains how atomic orbitals "
            "combine to form molecular orbitals spread across a molecule."
        )

    with st.expander("2. What are Bonding Orbitals?"):
        st.write(
            "Bonding molecular orbitals are formed by constructive "
            "combination of atomic orbitals. They generally lower "
            "the energy and support bonding."
        )

    with st.expander("3. What are Antibonding Orbitals?"):
        st.write(
            "Antibonding molecular orbitals are formed by destructive "
            "combination of atomic orbitals. They are represented "
            "using an asterisk (*)."
        )

    with st.expander("4. What is Bond Order?"):
        st.write(
            "Bond order measures the net bonding effect of electrons "
            "in a molecule."
        )
        st.latex(r"BO = \frac{N_b-N_a}{2}")
        st.write(
            "Nb = Bonding electrons; Na = Antibonding electrons."
        )

    with st.expander("5. What is Paramagnetism?"):
        st.write(
            "Paramagnetic substances contain unpaired electrons "
            "and are attracted to a magnetic field."
        )

    with st.expander("6. What is Diamagnetism?"):
        st.write(
            "Diamagnetic substances have all electrons paired "
            "and are weakly repelled by a magnetic field."
        )

    with st.expander("7. Bond Order and Stability"):
        st.write(
            "A positive bond order generally indicates a stable "
            "bond in the elementary MO model. Zero bond order "
            "indicates no net bond in this model."
        )

    st.divider()

    st.header("🧪 What can you do here?")

    col1, col2 = st.columns(2)

    with col1:
        st.info("Analyse 10 selected diatomic molecules.")

    with col2:
        st.info("Learn concepts and test your knowledge.")

    st.caption(
        "Use the navigation menu on the left to explore the laboratory."
    )

# ==================================================
# MOLECULAR ANALYSIS PAGE
# ==================================================

elif page == "🔬 Molecular Analysis":

    st.title("🔬 Molecular Analysis Laboratory")

    st.write(
        "Select a molecule and explore its molecular orbital properties."
    )

    selected = st.selectbox(
        "Search or select a molecule:",
        list(molecules.keys()),
        format_func=lambda x: f"{x} — {molecules[x]['name']}"
    )

    data = molecules[selected]

    st.session_state.selected_molecule = selected

    st.info(data["explanation"])

    if st.button("Analyse Molecule", type="primary"):

        st.session_state.analysis_done = True

    if st.session_state.analysis_done:

        bond_order = (
            data["bonding"] - data["antibonding"]
        ) / 2

        st.divider()

        st.subheader(f"Results: {selected} — {data['name']}")

        col1, col2, col3 = st.columns(3)

        col1.metric("Bond Order", bond_order)
        col2.metric("Magnetic Nature", data["magnetic"])
        col3.metric("Total Electrons in Model", data["bonding"] + data["antibonding"])

        st.header("Electron Configuration")
        st.code(data["configuration"])

        st.header("Electron Distribution")

        col4, col5 = st.columns(2)

        with col4:
            st.metric("Bonding Electrons", data["bonding"])
            st.progress(data["bonding"] / 8)

        with col5:
            st.metric("Antibonding Electrons", data["antibonding"])
            st.progress(data["antibonding"] / 8)

        st.header("Bond Order Calculation")

        st.latex(r"BO = \frac{N_b-N_a}{2}")

        st.write(
            f"BO = ({data['bonding']} - "
            f"{data['antibonding']}) / 2 = {bond_order}"
        )

        st.header("Orbital Electron Arrangement")

        for orbital, electrons in data["orbitals"]:

            if electrons == "up down":
                symbol = "[ ↑↓ ]"
            elif electrons == "up":
                symbol = "[ ↑ ]"
            else:
                symbol = "[   ]"

            st.write(f"**{orbital}**     {symbol}")

        st.header("Stability Prediction")

        if bond_order > 0:
            st.success(
                "Positive bond order: a stable bond is predicted "
                "in this simplified MO model."
            )
        else:
            st.warning(
                "Zero bond order: no stable bound molecule is "
                "predicted in this simplified MO model."
            )

        st.header("Magnetic Explanation")

        if data["magnetic"] == "Paramagnetic":
            st.info(
                "Unpaired electrons are present. "
                "The molecule is paramagnetic."
            )
        else:
            st.info(
                "All occupied orbitals have paired electrons. "
                "The molecule is diamagnetic."
            )

        st.caption(
            "Note: This is a curated educational MO model, "
            "not a general-purpose quantum chemistry calculator."
        )

# ==================================================
# QUIZ PAGE
# ==================================================

elif page == "🧠 Quiz":

    st.title("🧠 Molecular Orbital Theory Quiz")

    st.write("Test your knowledge with 10 multiple-choice questions.")

    questions = [
        (
            "What is the formula for bond order?",
            [
                "(Nb + Na) / 2",
                "(Nb - Na) / 2",
                "Nb - Na",
                "Nb / Na"
            ],
            "(Nb - Na) / 2"
        ),
        (
            "What is the bond order of H2?",
            ["0", "1", "2", "3"],
            "1"
        ),
        (
            "Why is O2 paramagnetic?",
            [
                "It has no electrons",
                "It has two unpaired electrons",
                "All electrons are paired",
                "It has zero bond order"
            ],
            "It has two unpaired electrons"
        ),
        (
            "What is the bond order of N2?",
            ["1", "2", "3", "4"],
            "3"
        ),
        (
            "Which symbol represents an antibonding orbital?",
            ["sigma", "pi", "*", "delta"],
            "*"
        ),
        (
            "What is the magnetic nature of N2?",
            [
                "Paramagnetic",
                "Diamagnetic",
                "Both",
                "Neither"
            ],
            "Diamagnetic"
        ),
        (
            "What is the bond order of He2 in the simple MO model?",
            ["0", "1", "2", "3"],
            "0"
        ),
        (
            "Which electrons determine paramagnetism?",
            [
                "Paired electrons",
                "Unpaired electrons",
                "Protons",
                "Neutrons"
            ],
            "Unpaired electrons"
        ),
        (
            "What is the bond order of O2?",
            ["1", "2", "3", "4"],
            "2"
        ),
        (
            "What happens when bond order is zero in the simple MO model?",
            [
                "A strong bond forms",
                "A triple bond forms",
                "No net stable bond is predicted",
                "The molecule becomes paramagnetic"
            ],
            "No net stable bond is predicted"
        )
    ]

    with st.form("molecular_quiz"):

        answers = []

        for index, (question, options, correct) in enumerate(questions):

            answer = st.radio(
                f"Question {index + 1}: {question}",
                options,
                key=f"question_{index}"
            )

            answers.append(answer)

            st.divider()

        submitted = st.form_submit_button(
            "Submit Quiz",
            type="primary"
        )

    if submitted:

        score = 0

        for index, question_data in enumerate(questions):

            if answers[index] == question_data[2]:
                score += 1

        st.session_state.quiz_submitted = True
        st.session_state.quiz_score = score

    if st.session_state.quiz_submitted:

        score = st.session_state.quiz_score

        st.subheader("🏆 Your Quiz Results")

        st.metric("Your Score", f"{score}/10")

        if score >= 9:
            st.success("Excellent! You have mastered the basics.")
        elif score >= 7:
            st.success("Very good! Keep practising.")
        elif score >= 5:
            st.warning("Good attempt. Revise a few concepts.")
        else:
            st.error("Revise the concepts on the Home page and try again.")

        if st.button("Retake Quiz"):
            st.session_state.quiz_submitted = False
            st.rerun()

# ==================================================
# REPORT DOWNLOAD PAGE
# ==================================================

elif page == "📄 Download Report":

    st.title("📄 Generate Experiment Report")

    st.write(
        "Generate a PDF report containing the results "
        "of your molecular analysis."
    )

    selected = st.session_state.selected_molecule
    data = molecules[selected]

    bond_order = (
        data["bonding"] - data["antibonding"]
    ) / 2

    st.subheader("Selected Molecule")

    st.write(f"Formula: **{selected}**")
    st.write(f"Name: **{data['name']}**")

    st.write(
        "The report will contain electron configuration, "
        "bond order, magnetic nature and stability prediction."
    )

    def create_pdf():

        buffer = io.BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "Molecular Orbital Theory Virtual Lab",
                styles["Title"]
            )
        )

        content.append(Spacer(1, 20))

        content.append(
            Paragraph("Molecular Experiment Report", styles["Heading2"])
        )

        content.append(Spacer(1, 15))

        report_data = [
            ["Property", "Result"],
            ["Molecule", selected],
            ["Name", data["name"]],
            ["Bonding electrons", str(data["bonding"])],
            ["Antibonding electrons", str(data["antibonding"])],
            ["Bond order", str(bond_order)],
            ["Magnetic nature", data["magnetic"]],
            ["Electron configuration", data["configuration"]],
            [
                "Stability prediction",
                "Positive bond order" if bond_order > 0
                else "Zero bond order"
            ]
        ]

        table = Table(report_data, colWidths=[6 * cm, 10 * cm])

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173D65")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP")
            ])
        )

        content.append(table)

        content.append(Spacer(1, 20))

        content.append(
            Paragraph(
                "Orbital Electron Arrangement",
                styles["Heading2"]
            )
        )

        for orbital, electrons in data["orbitals"]:

            content.append(
                Paragraph(
                    f"{orbital}: {electrons}",
                    styles["Normal"]
                )
            )

        content.append(Spacer(1, 20))

        content.append(
            Paragraph(
                "Educational note: This report uses a curated "
                "simplified molecular orbital model. It is not "
                "a quantum chemistry calculation.",
                styles["Italic"]
            )
        )

        document.build(content)

        buffer.seek(0)

        return buffer.getvalue()

    if st.button("Generate PDF Report", type="primary"):

        pdf_data = create_pdf()

        st.download_button(
            "⬇️ Download Your Report",
            data=pdf_data,
            file_name=f"{selected}_MO_Report.pdf",
            mime="application/pdf"
        )

# ==================================================
# FOOTER
# ==================================================

st.sidebar.divider()

st.sidebar.markdown("### 👨‍💻 Developed By")

st.sidebar.markdown(
    """
    **M H TARUN KUMAR**

    Student  
    **SRM Institute of Science and Technology**

    Department: Computer Science and Engineering

    ---
    *Molecular Orbital Theory Virtual Lab*
    """
)

st.sidebar.caption("Built with Python and Streamlit")
