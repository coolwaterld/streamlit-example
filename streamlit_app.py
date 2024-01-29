import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import numpy as np
st.set_page_config(layout="wide")

pd_list_result = []
uploaded_file = st.file_uploader("选择需要转换的配置文件")

if uploaded_file is not None:
    print()
    df = pd.read_excel("30i_cfg.xlsx", sheet_name=None)
    sheet_list = list(df.keys())
    filtered_items = [item for item in sheet_list if '点&通道' in item]
    options = st.multiselect(
        '选择需要转换的类型',
        ['控制器节点', 'P2设备', '联动盘'])
    # print(options)
    df_controler = pd.read_excel("30i_cfg.xlsx", sheet_name='控制器')
    df_controler = df_controler.iloc[:, [0, 1, 2, 3, 4, 5, 6]]
    df_controler.rename(columns={'IP地址': '回路地址','子网掩码': '点地址','默认网关': '通道地址'}, inplace=True)
    controler_rows, columns = df_controler.shape

    increment = 2

    if '控制器节点' in options:
        st.header("控制器")
        controller_start_value = st.number_input(
            'Insert base address', value=10000)
        df_controler["Modbus"] = list(range(
            controller_start_value, controller_start_value + controler_rows * increment, increment))
        builder = GridOptionsBuilder.from_dataframe(df_controler)
        builder.configure_column("Modbus", editable=True)
        go = builder.build()
        # print(grid_options)
        controller_result = AgGrid(
            df_controler, fit_columns_on_grid_load=True, gridOptions=go)
        # print(controller_result.data)
        pd_list_result.append(controller_result.data)

    # st.header("回路")
    df_loop = pd.read_excel("30i_cfg.xlsx", sheet_name='回路')
    df_detect_loop = df_loop[df_loop['类型'].str.contains('探测总线')]
    # AgGrid(df_detect_loop)
    result_tuples = df_detect_loop.apply(lambda row: (
        row['系统地址'], row['控制器地址'], row['回路地址']), axis=1)
    # print(result_tuples)

    # st.header("点&通道")
    dfs = [pd.read_excel("30i_cfg.xlsx", sheet_name=index)
           for index in filtered_items]
    mergedf = pd.concat(dfs)
    # AgGrid(mergedf)

    df_p2 = mergedf[mergedf[['系统地址', '控制器地址', '回路地址']].apply(
        tuple, axis=1).isin(result_tuples)]
    df_p2 = df_p2.iloc[:, [0, 1, 2, 3, 4, 5, 6,]]
    p2_rows, columns = df_p2.shape
    if "P2设备" in options:
        st.header("P2设备")
        p2_start_value = st.number_input('Insert base address', value=20000)
        df_p2["Modbus"] = list(
            range(p2_start_value, p2_start_value + p2_rows * increment, increment))
        builder = GridOptionsBuilder.from_dataframe(df_p2)
        builder.configure_column("Modbus", editable=True)
        go = builder.build()
        p2_result = AgGrid(
            df_p2, fit_columns_on_grid_load=True, gridOptions=go)
        pd_list_result.append(p2_result.data)

    # st.header("P2设备_2")
    # AgGrid(mergedf[(mergedf["回路地址"]==2)])

    df_linkage = mergedf[(mergedf["回路地址"] == 33) & (
        mergedf['类型'].str.contains('联动盘'))]
    df_linkage = df_linkage.iloc[:, [0, 1, 2, 3, 4, 5, 6,]]
    linkage_rows, columns = df_linkage.shape
    if "联动盘" in options:
        st.header("联动盘")
        linkage_start_value = st.number_input(
            'Insert base address', value=30000)
        df_linkage["Modbus"] = list(range(
            linkage_start_value, linkage_start_value + linkage_rows * increment, increment))
        builder = GridOptionsBuilder.from_dataframe(df_linkage)
        builder.configure_column("Modbus", editable=True)
        go = builder.build()
        linkage_result = AgGrid(
            df_linkage, fit_columns_on_grid_load=True, gridOptions=go)
        pd_list_result.append(linkage_result.data)
    if len(pd_list_result)>0:
        appended_df = pd.concat(pd_list_result, ignore_index=True)
        csv_result = appended_df.to_csv().encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv_result,
            file_name=uploaded_file.name.split(".")[0]+'.csv',
            mime='text/csv',
        )


