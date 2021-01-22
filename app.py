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
        text = st.text_area("Paste Text Here")
        list_of_items = ["Emails", "URLS", "Phonenumbers"]
        task_option = st.sidebar.selectbox("Task", list_of_items)

        if st.button("Extract"):
            if task_option == list_of_items[0]:
                results = nfx.extract_emails(text)
            elif task_option == list_of_items[1]:
                results = nfx.extract_urls(text)
            elif task_option == list_of_items[2]:
                results = nfx.extract_phone_numbers(text)

            st.write(results)

            with st.beta_expander("Results As Dataframe"):
                result_df = pd.DataFrame({"Results": results})
                st.dataframe(result_df)

    elif choice == "Bulk Extractor":
        st.subheader("Bulk Extractor")
    else:
        st.subheader("About")


if __name__ == "__main__":
    main()
