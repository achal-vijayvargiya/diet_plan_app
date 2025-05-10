from xhtml2pdf import pisa
from pathlib import Path
import markdown
import streamlit as st
from main import BASE_DIR


def generate_pdf():

    markdown_blocks = [
        st.session_state.diet_summary,
        st.session_state.nutritional_req,
        st.session_state.interpretation_goals,
        st.session_state.weekly_meal_plan
    ]

    # Combine and convert to HTML
    combined_markdown = "\n\n".join(markdown_blocks)
    html = markdown.markdown(combined_markdown, extensions=['tables', 'fenced_code'])
    with open(BASE_DIR / "data" /"test_plan.pdf", "w+b") as result_file:
            pisa_status = pisa.CreatePDF(html, dest=result_file)
        
    if pisa_status.err:
            raise Exception("Failed to generate PDF")
        
    return BASE_DIR / "data" /"test_plan.pdf"