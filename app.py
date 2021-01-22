import streamlit as st
import streamlit.components.v1 as static
import pandas as pd
import neattext.functions as nfx


def main():
    st.title("Email Extractor")

    menu = ["Home", "Sigle Extractor", "Bulk Extractor", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Search & Extract")
    elif choice == "Sigle Extractor":
        st.subheader("Extract A Single Term")
    elif choice == "Bulk Extractor":
        st.subheader("Bulk Extractor")
    else:
        st.subheader("About")


if __name__ == "__main__":
    main()
