import streamlit as st
import base64


def set_background(image_file):

    try:
        with open(image_file, "rb") as f:
            data = f.read()

        encoded = base64.b64encode(data).decode()

        st.markdown(
            f"""
            <style>

            .stApp {{
                background:
                    linear-gradient(
                        rgba(8,10,25,0.85),
                        rgba(8,10,25,0.85)
                    ),
                    url("data:image/jpg;base64,{encoded}");

                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except (FileNotFoundError, OSError) as e:

        # Fallback to plain dark background
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #080a19;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            f"Background image could not be loaded. "
            f"Using plain background instead. ({e})"
        )