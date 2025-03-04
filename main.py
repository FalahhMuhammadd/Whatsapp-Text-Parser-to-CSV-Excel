import streamlit as st
import pandas as pd
from io import BytesIO
from utils import read_rtf, parse_whatsapp_chat

# Title of the program
st.title("Whatsapp Parser to CSV/Excel")

# Upload RTF File
uploaded_file = st.file_uploader("Upload RTF File", type=["rtf"])

if uploaded_file is not None:
    with open("temp.rtf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read RTF File
    rtf_text = read_rtf("temp.rtf")

    if rtf_text:
        # Inisialisasi df_chat sebagai variabel global
        df_chat = parse_whatsapp_chat(rtf_text)

        # Tampilkan DataFrame
        st.write("### Result")
        st.dataframe(df_chat)

        # Option to download the parsing result as CSV or XLSX in download button
        st.write("#### Download The Data")
        csv = df_chat.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="whatsapp_chat_parsed.csv",
            mime="text/csv",
        )
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df_chat.to_excel(writer, index=False, sheet_name="Chat WhatsApp")
        
        # Atur pointer ke awal buffer
        excel_buffer.seek(0)

        st.download_button(
            label="Download Excel",
            data=excel_buffer,
            file_name="whatsapp_chat_parsed.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )