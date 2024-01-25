import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
st.set_page_config(layout="wide")


uploaded_file = st.file_uploader("选择需要转换的配置文件")
if uploaded_file is not None:
    df = pd.read_excel("30i_cfg.xlsx", sheet_name=None)
    sheet_list = list(df.keys())
    filtered_items = [item for item in sheet_list if '点&通道' in item]
    options = st.multiselect(
    '选择需要转换的类型',
    ['控制器节点', 'P2设备', '联动盘'])
    # sheet = st.selectbox(
    #     "Choose a sheet?",
    #     list(df.keys()),
    #     index=None,
    #     placeholder="sheet...",
    # )

    st.header("控制器")
    df_controler = pd.read_excel("30i_cfg.xlsx",sheet_name='控制器')
    AgGrid(df_controler)
    st.header("点&通道")
    dfs = [pd.read_excel("30i_cfg.xlsx",sheet_name=index) for index in filtered_items]
    mergedf = pd.concat(dfs)
    AgGrid(mergedf)

# df = pd.read_excel("30i_cfg.xlsx",sheet_name='回路')
# st.write(df)
# st.dataframe(df)
# AgGrid(df)



