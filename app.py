import streamlit as st
import streamlit.components.v1 as static
import pandas as pd
import neattext.functions as nfx
import base64
import time

timestr = time.strftime("%Y%m%d-%H%M%S")


# Fxn to Download
def make_downloadable(data, task_type):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()  # B64 encoding
    st.markdown("### ** Download Results File ** ")
    new_filename = "extracted_{}_result_{}.csv".format(task_type, timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)


# Fxn to Download
def make_downloadable_df(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()  # B64 encoding
    st.markdown("### ** Download CSV File ** ")
    new_filename = "extracted_data_result_{}.csv".format(timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)


def main():
    st.title("Email Extractor")

    menu = ["Home", "Sigle Extractor", "Bulk Extractor", "About"]
    list_of_items = ["Emails", "URLS", "Phonenumbers"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Search & Extract")
    elif choice == "Sigle Extractor":
        st.subheader("Extract A Single Term")
        text = st.text_area("Paste Text Here")
        task_option = st.sidebar.selectbox("Task", list_of_items)

        if st.button("Extract"):
            if task_option == list_of_items[0]:
                results = nfx.extract_emails(text)
            elif task_option == list_of_items[1]:
                results = nfx.extract_urls(text)
            elif task_option == list_of_items[2]:
                results = nfx.extract_phone_numbers(text)

            st.write(results)

            with st.beta_expander("Results As DataFrame"):
                result_df = pd.DataFrame({"Results": results})
                st.dataframe(result_df)
                make_downloadable(result_df, task_option)

    elif choice == "Bulk Extractor":
        st.subheader("Bulk Extractor")
        text = st.text_area("Paste Text Here")
        task_option = st.sidebar.multiselect("Task", list_of_items, default="Emails")
        task_mapper = {list_of_items[0]: nfx.extract_emails(
            text), list_of_items[1]: nfx.extract_urls(text),
            list_of_items[2]: nfx.extract_phone_numbers(text)}

        all_result = []
        for task in task_option:
            result = task_mapper[task]
            # st.write(result)
            all_result.append(result)

        st.write(all_result)

        with st.beta_expander("Results As DataFrame"):
            result_df = pd.DataFrame(all_result).T
            result_df.columns = task_option
            st.dataframe(result_df)
            make_downloadable_df(result_df)
    else:
        st.subheader("About")


if __name__ == "__main__":
    main()
