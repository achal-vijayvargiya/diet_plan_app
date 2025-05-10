import streamlit as st

def render_modal(content_html, modal_id="modal1"):
    key = f"{modal_id}_visible"
    if st.session_state.get(key, False):
        st.markdown("""
            <style>
                .modal-background {
                    position: fixed;
                    top: 0; left: 0;
                    width: 100vw; height: 100vh;
                    background: rgba(0, 0, 0, 0.6);
                    z-index: 1000;
                }
                .modal-box {
                    position: fixed;
                    top: 50%; left: 50%;
                    transform: translate(-50%, -50%);
                    background: white;
                    padding: 2rem;
                    border-radius: 10px;
                    z-index: 1001;
                    width: 90%; max-width: 600px;
                    max-height: 80vh; overflow: auto;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="modal-background"></div>
            <div class="modal-box">
                <h3>LLM Output</h3>
                {content_html}
                <br>
                <form>
                    <button onclick="window.location.reload();">Close</button>
                </form>
            </div>
        """, unsafe_allow_html=True)

def toggle_modal(modal_id="modal1"):
    key = f"{modal_id}_visible"
    st.session_state[key] = not st.session_state.get(key, False)
