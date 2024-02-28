import streamlit as st
import pandas as pd
import os
st.set_page_config(layout="wide")

# how-to-keep-widget-value-remembered-in-multi-page-app
for key, val in st.session_state.items():
    if not key.endswith('__do_not_persist'):
        st.session_state[key] = val

# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)

# filename = file_selector()
# st.write('You selected `%s`' % filename)
        
def merge_sheets(filename):
    xls = pd.ExcelFile(filename)
    sheet_list = xls.sheet_names
    filtered_items = [item for item in sheet_list if '点&通道' in item]

    dfs = [xls.parse(index)for index in filtered_items]
    return pd.concat(dfs,ignore_index = True)

tmp_file = st.file_uploader("导入FS30i配置文件xlsx", type=["xlsx"])
if tmp_file is not None:
    st.write(tmp_file)
    df = pd.read_excel(tmp_file,'控制器')
    # st.write(type(tmp_file))
    st.write(df)
tmp_file = st.file_uploader("导入FS30i配置文件xlsx2", type=["xlsx"])
if tmp_file is not None:
    df =  merge_sheets(tmp_file)
    st.write(df)