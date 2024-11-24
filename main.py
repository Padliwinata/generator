import streamlit as st
import pandas as pd
import streamlit_nested_layout
import numpy as np


def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)


st.set_page_config(layout="wide", page_icon="🪑",
                   page_title="Generator")
st.title("🪑 Generator Ganjil 24/25")
right = st
left = st.sidebar

right.write("Hasil:")


left.write("Isi datanya:")

jenis = left.selectbox(
    "Matkul",
    ["ALPRO SE", "STD", "ALPRO IF", "PBO", "SISOP",
        "WEBPRO", "DPBO", "PPB", "CASLAB_PRAMAGANG_2526"],
    index=0,
)

if jenis == "ALPRO SE":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=1051006003")
elif jenis == "STD":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=1723414529")
elif jenis == "ALPRO IF":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=78512067")
elif jenis == "PBO":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=345368744")
elif jenis == "DPBO":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=165603706")
elif jenis == "PPB":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=1671897911")
elif jenis == "SISTER":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=1636199559")
elif jenis == "SISOP":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=1240343747")
elif jenis == "JARKOM":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=1854277346")
elif jenis == "BASDAT":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=882741712")
elif jenis == "ABP":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=38981871")
elif jenis == "KPL":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=955695029")
elif jenis == "WEBPRO":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=2084916089")
elif jenis == "CASLAB_PRAMAGANG_2526":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=1398007307")

if df.empty:
    right.write("Data kosong")
else:
    if "cek_caslab" not in st.session_state:
        st.session_state["cek_caslab"] = False

    cek_caslab = False
    if jenis == "CASLAB_PRAMAGANG_2526" and not st.session_state["cek_caslab"]:
        user_input = st.text_input("Kode Program", type="password")

        if st.button("Submit"):
            if user_input == "caslabjaya2526":
                st.success("Kode benar!")
                st.session_state["cek_caslab"] = True
    
    if jenis != "CASLAB_PRAMAGANG_2526" or st.session_state["cek_caslab"]:
        kelas = left.selectbox(
            "Kelas",
            (df["Kelas"].drop_duplicates())
        )
        left.write('Pilih nomor meja yang tidak bisa digunakan:')
        columns = left.columns(5)
        options = []
        for i in range(5):
            for j in range(10):
                option = columns[i].checkbox(str(10 * i + j + 1))
                options.append(option)

        left.write('Pilih Nama yang tidak akan digunakan:')
        df_kelas = df[df["Kelas"] == kelas].reset_index(drop=True)
        k = 1
        A1, B1 = left.columns(2)
        for i, todo_text in df_kelas["NIM"].items():
            if k >= 1 and k <= np.ceil(len(df_kelas["NIM"])/2):
                A1.checkbox(f'{todo_text}',
                            key='optionNIM_'+str(k))
                k += 1
            elif k >= np.ceil(len(df_kelas["NIM"])/2)+1 and k <= len(df_kelas["NIM"]):
                B1.checkbox(f'{todo_text}', key='optionNIM_'+str(k))
                k += 1

        ATable, BTable, CTable, DTable, ETable = right.columns(5)
        d = []
        for x in range(1, 51):
            if (options[x-1] == True):
                d.append(x)

        def get_selected_checkboxes():
            return [i.replace('optionNIM_', '') for i in st.session_state.keys() if i.startswith('optionNIM_') and st.session_state[i]]

        NIMhapus = []
        res = [eval(i) for i in get_selected_checkboxes()]
        for x in range(1, 51):
            if (x in res):
                NIMhapus.append(df_kelas["NIM"][x-1])

        def highlight(x): return ['background: red'
                                if x.name in d
                                else '' for i in x]

        df_ATemplate = pd.DataFrame()
        df_BTemplate = pd.DataFrame()
        df_CTemplate = pd.DataFrame()
        df_DTemplate = pd.DataFrame()
        df_ETemplate = pd.DataFrame()

        df_ATemplate["NO"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        df_ATemplate["NIM"] = ["", "", "", "", "", "", "", "", "", ""]
        df_ATemplate["ASPRAK"] = ["", "", "", "", "", "", "", "", "", ""]

        df_BTemplate["NO"] = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        df_BTemplate["NIM"] = ["", "", "", "", "", "", "", "", "", ""]
        df_BTemplate["ASPRAK"] = ["", "", "", "", "", "", "", "", "", ""]

        df_CTemplate["NO"] = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        df_CTemplate["NIM"] = ["", "", "", "", "", "", "", "", "", ""]
        df_CTemplate["ASPRAK"] = ["", "", "", "", "", "", "", "", "", ""]

        df_DTemplate["NO"] = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
        df_DTemplate["NIM"] = ["", "", "", "", "", "", "", "", "", ""]
        df_DTemplate["ASPRAK"] = ["", "", "", "", "", "", "", "", "", ""]

        df_ETemplate["NO"] = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
        df_ETemplate["NIM"] = ["", "", "", "", "", "", "", "", "", ""]
        df_ETemplate["ASPRAK"] = ["", "", "", "", "", "", "", "", "", ""]

        if ("{}".format(kelas)) not in st.session_state:
            st.session_state["{}".format(kelas)] = df[df["Kelas"] ==
                                                    kelas].sample(frac=1).reset_index(drop=True)
        df_acak = st.session_state["{}".format(kelas)]
        for i in NIMhapus:
            df_acak = df_acak.drop(
                df_acak.index[(df_acak["NIM"] == i)], axis=0)
        df_acak = df_acak.reset_index(drop=True)

        i = 0
        for x in range(1, 51):
            if x >= 1 and x <= 10:
                if x not in d and i < len(df_acak):
                    df_ATemplate["NIM"][x-1] = df_acak["NIM"][i]
                    df_ATemplate["ASPRAK"][x-1] = df_acak["ASPRAK"][i]
                    i += 1
            elif x >= 11 and x <= 20:
                if x not in d and i < len(df_acak):
                    df_BTemplate["NIM"][x-11] = df_acak["NIM"][i]
                    df_BTemplate["ASPRAK"][x-11] = df_acak["ASPRAK"][i]
                    i += 1
            elif x >= 21 and x <= 30:
                if x not in d and i < len(df_acak):
                    df_CTemplate["NIM"][x-21] = df_acak["NIM"][i]
                    df_CTemplate["ASPRAK"][x-21] = df_acak["ASPRAK"][i]
                    i += 1
            elif x >= 31 and x <= 40:
                if x not in d and i < len(df_acak):
                    df_DTemplate["NIM"][x-31] = df_acak["NIM"][i]
                    df_DTemplate["ASPRAK"][x-31] = df_acak["ASPRAK"][i]
                    i += 1
            elif x >= 41 and x <= 50:
                if x not in d and i < len(df_acak):
                    df_ETemplate["NIM"][x-41] = df_acak["NIM"][i]
                    df_ETemplate["ASPRAK"][x-41] = df_acak["ASPRAK"][i]
                    i += 1

        df_ATemplate = df_ATemplate.astype(
            {"NO": int, "NIM": str, "ASPRAK": str})
        df_BTemplate = df_BTemplate.astype(
            {"NO": int, "NIM": str, "ASPRAK": str})
        df_CTemplate = df_CTemplate.astype(
            {"NO": int, "NIM": str, "ASPRAK": str})
        df_DTemplate = df_DTemplate.astype(
            {"NO": int, "NIM": str, "ASPRAK": str})
        df_ETemplate = df_ETemplate.astype(
            {"NO": int, "NIM": str, "ASPRAK": str})

        # CSS to inject contained in a string
        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """
        # Inject CSS with Markdown
        ATable.markdown(hide_table_row_index, unsafe_allow_html=True)
        BTable.markdown(hide_table_row_index, unsafe_allow_html=True)
        CTable.markdown(hide_table_row_index, unsafe_allow_html=True)
        DTable.markdown(hide_table_row_index, unsafe_allow_html=True)
        ETable.markdown(hide_table_row_index, unsafe_allow_html=True)

        df_AStyler = df_ATemplate.set_index(
            'NO', drop=False).style.apply(highlight, axis=1).hide()
        df_BStyler = df_BTemplate.set_index(
            'NO', drop=False).style.apply(highlight, axis=1).hide()
        df_CStyler = df_CTemplate.set_index(
            'NO', drop=False).style.apply(highlight, axis=1).hide()
        df_DStyler = df_DTemplate.set_index(
            'NO', drop=False).style.apply(highlight, axis=1).hide()
        df_EStyler = df_ETemplate.set_index(
            'NO', drop=False).style.apply(highlight, axis=1).hide()

        ATable.table(df_AStyler)

        BTable.table(df_BStyler)

        CTable.table(df_CStyler)

        DTable.table(df_DStyler)

        ETable.table(df_EStyler)