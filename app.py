import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import neattext.functions as nfx
import base64
import time
import requests
import sqlite3

timestr = time.strftime("%Y%m%d-%H%M%S")
conn = sqlite3.connect('emails_data.db')


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


@st.cache
def fetch_query(query: str = 'devops'):
    base_url = "https://www.google.com/search?q={}".format(query)
    return requests.get(base_url).text


def main():
    countries_list = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Austrian Empire", "Azerbaijan", "Baden*", "Bahamas, The", "Bahrain", "Bangladesh", "Barbados", "Bavaria*", "Belarus", "Belgium", "Belize", "Benin (Dahomey)", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Brunswick and LÃ¼neburg", "Bulgaria", "Burkina Faso (Upper Volta)", "Burma", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Cayman Islands, The", "Central African Republic", "Central American Federation*", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo Free State, The", "Costa Rica", "Cote dâ€™Ivoire (Ivory Coast)", "Croatia", "Cuba", "Cyprus", "Czechia", "Czechoslovakia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Duchy of Parma, The*", "East Germany (German Democratic Republic)", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Federal Government of Germany (1848-49)*", "Fiji", "Finland", "France", "Gabon", "Gambia, The", "Georgia", "Germany", "Ghana", "Grand Duchy of Tuscany, The*", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Hanover*", "Hanseatic Republics*", "Hawaii*", "Hesse*", "Holy See", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kingdom of Serbia/Yugoslavia*", "Kiribati", "Korea", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Lew Chew (Loochoo)*",
                      "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mecklenburg-Schwerin*", "Mecklenburg-Strelitz*", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Namibia", "Nassau*", "Nauru", "Nepal", "Netherlands, The", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North German Confederation*", "North German Union*", "North Macedonia", "Norway", "Oldenburg*", "Oman", "Orange Free State*", "Pakistan", "Palau", "Panama", "Papal States*", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Piedmont-Sardinia*", "Poland", "Portugal", "Qatar", "Republic of Genoa*", "Republic of Korea (South Korea)", "Republic of the Congo", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Schaumburg-Lippe*", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands, The", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Texas*", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Two Sicilies*", "Uganda", "Ukraine", "Union of Soviet Socialist Republics*", "United Arab Emirates, The", "United Kingdom, The", "Uruguay", "Uzbekistan", "USA", "UK", "Vanuatu", "Venezuela", "Vietnam", "WÃ¼rttemberg*", "Yemen", "Zambia", "Zimbabwe"]
    email_extensions_list = ["gmail.com", "yahoo.com", "hotmail.com", "aol.com", "hotmail.co.uk", "hotmail.fr", "msn.com", "yahoo.fr", "wanadoo.fr", "orange.fr", "comcast.net", "yahoo.co.uk", "yahoo.com.br", "yahoo.co.in", "live.com", "rediffmail.com", "free.fr", "gmx.de", "web.de", "yandex.ru", "ymail.com", "libero.it", "outlook.com", "uol.com.br", "bol.com.br", "mail.ru", "cox.net", "hotmail.it", "sbcglobal.net", "sfr.fr", "live.fr", "verizon.net", "live.co.uk", "googlemail.com", "yahoo.es", "ig.com.br", "live.nl", "bigpond.com", "terra.com.br", "yahoo.it", "neuf.fr", "yahoo.de", "alice.it", "rocketmail.com", "att.net", "laposte.net", "facebook.com", "bellsouth.net", "yahoo.in", "hotmail.es",
                             "charter.net", "yahoo.ca", "yahoo.com.au", "rambler.ru", "hotmail.de", "tiscali.it", "shaw.ca", "yahoo.co.jp", "sky.com", "earthlink.net", "optonline.net", "freenet.de", "t-online.de", "aliceadsl.fr", "virgilio.it", "home.nl", "qq.com", "telenet.be", "me.com", "yahoo.com.ar", "tiscali.co.uk", "yahoo.com.mx", "voila.fr", "gmx.net", "mail.com", "planet.nl", "tin.it", "live.it", "ntlworld.com", "arcor.de", "yahoo.co.id", "frontiernet.net", "hetnet.nl", "live.com.au", "yahoo.com.sg", "zonnet.nl", "club-internet.fr", "juno.com", "optusnet.com.au", "blueyonder.co.uk", "bluewin.ch", "skynet.be", "sympatico.ca", "windstream.net", "mac.com", "centurytel.net", "chello.nl", "live.ca", "aim.com", "bigpond.net.au"]

    st.title("Email Extractor")
    custom_banner = """
    <div style="font-size:30px;font-weight:bolder;background-color:#fff;padding:10px;border-radius:10px;border:5px solid #464e5f;text-align:center;">


    <span style="color:blue">E</span>
    <span style="color:black">M</span>
    <span style="color:red">A</span>
    <span style="color:green">I</span>
    <span style="color:purple">L</span>

    <span style="color:blue">E</span>
    <span style="color:red">X</span>
    <span style="color:yellow">T</span>
    <span style="color:#464e5f">R</span>
    <span style="color:red">A</span>
    <span style="color:green">C</span>
    <span style="color:yellow">T</span>
    <span style="color:black">O</span>
    <span style="color:blue">R</span>
    </div>

    """
    stc.html(custom_banner)
    menu = ["Home", "Sigle Extractor", "Bulk Extractor", "DataStorage", "About"]
    list_of_items = ["Emails", "URLS", "Phonenumbers"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Search & Extract")

        country_name = st.sidebar.selectbox("Country", countries_list)
        email_type = st.sidebar.selectbox("Email Type", email_extensions_list)
        num_per_page = st.sidebar.number_input("Number of results Per Page", 10, 100, step=10)
        task_option = st.sidebar.multiselect("Task", list_of_items, default="Emails")
        search_text = st.text_input("Paste Term Here")
        generated_query = f'{search_text} + {country_name} + email@{email_type}&num={num_per_page}'
        # st.write(generated_query)
        st.info("Generated Query: {}".format(generated_query))

        if st.button("Search & Extract"):
            if generated_query is not None and search_text and int(num_per_page) > 9:
                st.success("Generated Query")
                text = fetch_query(generated_query)
                # st.write(text)
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
                    result_df['Emails']
                    # Save to DataBase as SQL with pandas
                    st.dataframe(result_df).to_sql(name='EmailsTable', con=conn, if_exists='append')
                    make_downloadable_df(result_df)
            else:
                st.warning("Paste Term...")

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
    elif choice == 'DataStorage':
        st.subheader("Data Storage of Emails")
        new_df = pd.read_sql('SELECT * FROM EmailsTable', con=conn)
        st.dataframe(new_df)
    else:
        st.subheader("About")


if __name__ == "__main__":
    main()
