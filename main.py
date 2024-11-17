import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# --- App Setup ---
st.set_page_config(
    page_title="TMUA Guide",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- Initialize Session State ---
def init_session_state():
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'timer_start' not in st.session_state:
        st.session_state.timer_start = datetime.now()
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None


init_session_state()


# --- MathJax Setup Using HTML Component ---
def init_mathjax():
    components.html(
        """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        <script>
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                processEnvironments: true
            },
            displayAlign: 'center'
        });
        </script>
        """,
        height=0,
    )


# Call MathJax initialization
init_mathjax()


# --- Helper Functions ---
def render_latex(text):
    """Render text with LaTeX content using HTML component"""
    components.html(
        f"""
        <div style="font-size: 1rem; padding: 1rem;">
            {text}
        </div>
        """,
        height=None,
    )


def load_questions():
    try:
        df = pd.read_excel("questions.xlsx")
        return df
    except:
        return pd.DataFrame({
            'Serial No': ['1', '2', '3'],
            'Question': [
                'The expansion of $(a - bx)^c$ is $4 - px + 108x^2 + qx^3 + rx^4$ where $a$, $b$, $c$, $p$, $q$, and $r$ are positive real constants. Find the value of $p + q + r$.',
                'If $\\sqrt{x+5} + \\sqrt{x-5} = 4$, find the value of $x$.',
                'Solve the equation: $\\frac{x}{x-1} + \\frac{1}{x+1} = \\frac{3}{2}$'
            ],
            'Options': [
                'A@@81 + 132\\sqrt{2}, B@@81 - 84\\sqrt{2}, C@@132\\sqrt{2} - 81, D@@81 + 84\\sqrt{2}',
                'A@@10, B@@15, C@@20, D@@25',
                'A@@-2, B@@2, C@@3, D@@4'
            ],
            'Correct option': ['A', 'C', 'B'],
            'TAG': ['Algebra', 'Algebra', 'Calculus'],
            'Difficulty tag': ['Hard', 'Medium', 'Medium']
        })


def parse_options(options_str):
    """Parse options string into a clean format"""
    options = {}
    for opt in options_str.split(','):
        opt = opt.strip()
        key, value = opt.split('@@')
        # Clean up the LaTeX formatting
        value = value.strip()
        options[key.strip()] = value
    return options


def render_option_button(key, value, selected=False):
    """Render a single option button with proper LaTeX formatting"""
    button_style = """
        <div style="
            background-color: white;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 4px;
            border: 1px solid #eee;
            cursor: pointer;
            hover: background-color: #f5f5f5;
            {}
        ">
            <span style="font-weight: bold; margin-right: 1rem;">{}</span>
            <span>{}</span>
        </div>
    """.format(
        "background-color: #e3f2fd;" if selected else "",
        key,
        value
    )
    return button_style


# --- Main App ---
def main():
    # Sidebar setup remains the same...
    with st.sidebar:
        st.header("TMUA Guide")
        st.markdown("---")

        with st.expander("Filters", expanded=True):
            difficulty = st.selectbox(
                "Difficulty Level",
                ["All", "Easy", "Medium", "Hard"]
            )
            topic = st.selectbox(
                "Topic",
                ["All", "Algebra", "Calculus", "Geometry"]
            )

        st.markdown("---")
        if st.button("Reset Session", type="primary"):
            st.session_state.current_question_index = 0
            st.session_state.user_answers = {}
            st.session_state.timer_start = datetime.now()
            st.session_state.selected_option = None
            st.rerun()

    # Load and filter questions...
    df = load_questions()
    if difficulty != "All":
        df = df[df['Difficulty tag'] == difficulty]
    if topic != "All":
        df = df[df['TAG'] == topic]

    if len(df) > 0:
        current_q = df.iloc[st.session_state.current_question_index]

        left_col, right_col = st.columns([2, 1])

        with left_col:
            st.markdown("### Question Panel")

            # Render question with LaTeX
            render_latex(f"""
                <div style="background-color: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4>Question {current_q['Serial No']}</h4>
                    <p>{current_q['Question']}</p>
                </div>
            """)

            # Options
            st.markdown("### Select your answer")
            # st.markdown("""
            #     <style>
            #     .stButton button {
            #         width: 100%;
            #         text-align: left !important;
            #         padding: 1rem !important;
            #         margin: 0.5rem 0 !important;
            #         border: 1px solid #ddd !important;
            #         border-radius: 4px !important;
            #         background-color: white !important;
            #     }
            #
            #     .stButton button:hover {
            #         background-color: #f5f5f5 !important;
            #     }
            #
            #     .stButton button[data-selected="true"] {
            #         background-color: #e3f2fd !important;
            #         border-color: #2196f3 !important;
            #     }
            #
            #     .option-text {
            #         font-family: "Computer Modern", serif;
            #     }
            #     </style>
            # """, unsafe_allow_html=True)
            options = parse_options(current_q['Options'])

            # Create container for options
            options_container = st.container()

            # Render each option
            for key, value in options.items():
                is_selected = st.session_state.selected_option == key

                # Create clickable container
                col1, col2 = st.columns([9, 1])
                with col1:
                    if st.button(
                            f"{key}. {value}",
                            key=f"option_{key}",
                            use_container_width=True,
                    ):
                        st.session_state.selected_option = key
                        st.rerun()

            # Navigation buttons...
            st.markdown("---")
            nav_cols = st.columns([1, 1, 1])
            with nav_cols[0]:
                if st.button("← Previous", use_container_width=True,
                             disabled=st.session_state.current_question_index == 0):
                    st.session_state.current_question_index -= 1
                    st.session_state.selected_option = None
                    st.rerun()

            with nav_cols[1]:
                if st.button("Submit", type="primary", use_container_width=True):
                    if hasattr(st.session_state, 'selected_option') and st.session_state.selected_option:
                        st.session_state.user_answers[current_q['Serial No']] = {
                            'selected': st.session_state.selected_option,
                            'correct': current_q['Correct option'],
                            'is_correct': st.session_state.selected_option == current_q['Correct option']
                        }

            with nav_cols[2]:
                if st.button("Next →", use_container_width=True,
                             disabled=st.session_state.current_question_index == len(df) - 1):
                    st.session_state.current_question_index += 1
                    st.session_state.selected_option = None
                    st.rerun()

        # Right column (Progress panel) remains the same...
        with right_col:
            st.markdown("### Progress")
            total_attempted = len(st.session_state.user_answers)
            correct_answers = sum(1 for ans in st.session_state.user_answers.values() if ans['is_correct'])

            stats_cols = st.columns(2)
            with stats_cols[0]:
                st.metric(
                    "Questions Attempted",
                    f"{total_attempted}/{len(df)}"
                )
            with stats_cols[1]:
                if total_attempted > 0:
                    st.metric(
                        "Success Rate",
                        f"{(correct_answers / total_attempted) * 100:.1f}%"
                    )

            # Timer
            if st.session_state.timer_start:
                time_elapsed = datetime.now() - st.session_state.timer_start
                st.metric("Time Elapsed", str(time_elapsed).split('.')[0])

            # Answer History
            if st.session_state.user_answers:
                st.markdown("### Answer History")
                for q_no, ans in st.session_state.user_answers.items():
                    st.markdown(
                        f"""<div style="padding: 0.5rem; margin: 0.2rem 0; 
                            background-color: {'#e8f5e9' if ans['is_correct'] else '#ffebee'}; 
                            border-radius: 4px;">
                            Q{q_no}: {ans['selected']} 
                            {'✓' if ans['is_correct'] else '✗'}
                        </div>""",
                        unsafe_allow_html=True
                    )


if __name__ == "__main__":
    main()