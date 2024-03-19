import streamlit as st
import pandas as pd
from deepdiff import DeepDiff

st.set_page_config(layout="wide")

row_colors = {
    'right_only': 'lightgreen',
    'left_only': 'lightcoral',
    'both':'white',
    'diff':'lightyellow'
}
def apply_row_colors(row):
    return [f'background-color: {row_colors[row["_merge"]]}']*len(row)

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
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    on = []
    sheet_name = st.selectbox("Choose sheet for comparing ", new_intersection, index=None, )
    # st.write('You selected:', sheet_name)

    if sheet_name == "控制器":
        on = ["系统地址","控制器地址"]
        df1 = old_dict[sheet_name].iloc[:, [0, 1, 2, 3]]
        df2 = new_dict[sheet_name].iloc[:, [0, 1, 2, 3]]
    elif sheet_name == "回路":
        on = ["系统地址","控制器地址","回路地址"]
        df1 = old_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4]]
        df2 = new_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4]]
    elif sheet_name and ("点&通道" in sheet_name):
        on = ["系统地址","控制器地址","回路地址","点地址","通道地址"]
        df1 = old_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
        df2 = new_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
    else:
        st.write('当前只关心[控制器],[回路],[点&通道]', sheet_name)
        

    merge_options = ['both','left_only','right_only','diff']
    merge_selected = st.multiselect( 'What types do you want to ',  merge_options, merge_options)

    if len(on)>0:
        merged_df = pd.merge(df1, df2, on=on, suffixes=('_old', '_new'), how='outer', indicator=True)
        # st.table(merged_df)
        merged_df['_merge'] = pd.Categorical(merged_df['_merge'], categories=merge_options)
        merged_df.loc[(((merged_df['类型_new'] != merged_df['类型_old'])|(merged_df['名称_new'] != merged_df['名称_old'])) & (merged_df['_merge'] == 'both')), '_merge'] = 'diff'

        merge_counts = merged_df['_merge'].value_counts()
        st.write("🟠表[",sheet_name,"]共计",dict(merge_counts))

        merged_df = merged_df[merged_df['_merge'].isin(merge_selected)]
        styled_df = merged_df.style.apply(apply_row_colors, axis=1)
        st.table(styled_df)
        


            
