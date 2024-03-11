import streamlit as st
import pandas as pd
from deepdiff import DeepDiff

st.set_page_config(layout="wide")

# how-to-keep-widget-value-remembered-in-multi-page-app
for key, val in st.session_state.items():
    if not key.endswith('__do_not_persist'):
        st.session_state[key] = val

old_file = st.file_uploader("载入老文件")
new_file = st.file_uploader("载入新文件")
if (old_file is not None) & (new_file is not None):
    old_dict = pd.read_excel(old_file, sheet_name=None)
    new_dict = pd.read_excel(new_file, sheet_name=None)
    old_keys = old_dict.keys()
    new_keys = new_dict.keys()
    # new_view
    new_reduced = list(set(old_keys).difference(new_keys))
    new_added = list(set(new_keys).difference(old_keys))
    new_intersection = list(set(old_keys).intersection(new_keys))
    if len(new_reduced)>0:
        st.write("减少的表:",new_reduced)
    if len(new_added)>0:
        st.write("新增的表:",new_added)

########################general solution##################


    # for sheet_name in new_intersection:
    #     df1 = old_dict[sheet_name]
    #     df2 = new_dict[sheet_name]
    #     common_columns = set(df1.columns).intersection(df2.columns)
    #     merged_df = pd.merge(df1, df2, on=list(common_columns), suffixes=('_a', '_b'), how='outer', indicator=True)
    #     differences_df = merged_df[merged_df['_merge'] != 'both']
    #     rows = differences_df.shape[0]
    #     if rows >0 :
    #         new_reduced_rows = merged_df[merged_df['_merge'] == 'left_only']
    #         new_added_rows = merged_df[merged_df['_merge'] == 'right_only']
            
    #         st.write("🟠表[",sheet_name,"]共计",rows,"行不同")
    #         if new_reduced_rows.shape[0]>0:
    #             st.write("减少",new_reduced_rows.shape[0],"行:",new_reduced_rows)
    #         if new_added_rows.shape[0]>0:
    #             st.write("增加",new_added_rows.shape[0],"行:",new_added_rows)
########################domain solution##################
#是否可以认为5级地址没有变的modbus不需要，判断需要加上"名称","类型"吗？

    for sheet_name in new_intersection:
        if sheet_name == "控制器":
            on = ["名称","类型","系统地址","控制器地址"]
            df1 = old_dict[sheet_name].iloc[:, [0, 1, 2, 3]]
            df2 = new_dict[sheet_name].iloc[:, [0, 1, 2, 3]]
        elif sheet_name == "回路":
            on = ["名称","类型","系统地址","控制器地址","回路地址"]
            df1 = old_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4]]
            df2 = new_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4]]
        elif "点&通道" in sheet_name:
            on = ["名称","类型","系统地址","控制器地址","回路地址","点地址","通道地址"]
            df1 = old_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
            df2 = new_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
        merged_df = pd.merge(df1, df2, on=on, suffixes=('_old', '_new'), how='outer', indicator=True)
        differences_df = merged_df[merged_df['_merge'] != 'both']
        rows = differences_df.shape[0]
        if rows >0 :
            new_reduced_rows = merged_df[merged_df['_merge'] == 'left_only']
            new_added_rows = merged_df[merged_df['_merge'] == 'right_only']
            st.write("🟠表[",sheet_name,"]共计",rows,"行不同")
            if new_reduced_rows.shape[0]>0:
                st.write("减少",new_reduced_rows.shape[0],"行:",new_reduced_rows)
            if new_added_rows.shape[0]>0:
                st.write("增加",new_added_rows.shape[0],"行:",new_added_rows)
            if "点&通道" in sheet_name:
                on2 = ["系统地址","控制器地址","回路地址","点地址","通道地址"]
                merged_df2 = pd.merge(new_reduced_rows.iloc[:, [ 2, 3, 4, 5, 6]], new_added_rows.iloc[:, [2, 3, 4, 5, 6]], on=on2, suffixes=('_old', '_new'), how='outer', indicator=True)
                cols = st.columns(3)
                tmp = merged_df2[merged_df2['_merge'] == 'both']
                with cols[0]:
                    st.write("修改的",tmp.shape[0],tmp)
                tmp = merged_df2[merged_df2['_merge'] == 'left_only']
                with cols[1]:
                    st.write("删除的",tmp.shape[0],tmp)
                tmp = merged_df2[merged_df2['_merge'] == 'right_only']
                with cols[2]:
                    st.write("增加的",tmp.shape[0],tmp)
