import streamlit as st
from app.pdf.generate_pdf import generate_pdf



st.set_page_config(page_title="Diet Plan Output")

if "user_data" not in st.session_state:
    st.error("No user data found. Please fill the form first.")
    st.switch_page("streamlit_app.py")
    
user = st.session_state.user_data


st.success("Your diet plan is ready!")

# Initialize session state for selected section
if "selected_section" not in st.session_state:
    st.session_state.selected_section = None

# Grid layout for buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Show Weekly Diet Plan"):
        st.session_state.selected_section = "weekly"
with col2:
    if st.button("Show Nutritional Requirement"):
        st.session_state.selected_section = "nutrition"

col3, col4 = st.columns(2)
with col3:
    if st.button("Show Interpretation Goals"):
        st.session_state.selected_section = "goals"
with col4:
    if st.button("Show Diet Summary"):
        st.session_state.selected_section = "summary"

if st.button("Generate PDF"):
    pdf_path = generate_pdf()
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, "report.pdf", "application/pdf")

# JavaScript for smooth scroll to result section
st.markdown("""
    <script>
    function scrollToMarkdown() {
        const el = document.getElementById("output-block");
        if (el) {
            el.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }
    setTimeout(scrollToMarkdown, 100);
    </script>
""", unsafe_allow_html=True)

# Display the markdown content with animation target
markdown_placeholder = st.empty()

# Wrap in a container with an ID for scrolling
markdown = ""

if st.session_state.selected_section == "weekly":
    markdown = st.session_state.weekly_meal_plan
elif st.session_state.selected_section == "nutrition":
    markdown = st.session_state.nutritional_req
elif st.session_state.selected_section == "goals":
    markdown = st.session_state.interpretation_goals
elif st.session_state.selected_section == "summary":
    markdown = st.session_state.diet_summary


if markdown:
    markdown_placeholder.markdown(
        f"<div id='output-block'>{markdown}</div>",
        unsafe_allow_html=True
    )

