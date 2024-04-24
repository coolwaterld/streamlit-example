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

current_text = st.session_state.current_text


old_file = st.file_uploader(current_text["UI_FUloadOldFile"])
new_file = st.file_uploader(current_text["UI_FUloadNewFile"])
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
        st.write(current_text["UI_WreducedTables"],new_reduced)
    if len(new_added)>0:
        st.write(current_text["UI_WaddedTables"],new_added)
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    on = []
    sheet_name = st.selectbox(current_text["UI_SBsheetForComparing"], new_intersection, index=None, )
    # st.write('You selected:', sheet_name)

    if sheet_name == current_text["K_panel"]:
        on = [current_text["K_systemID"],current_text["K_panelID"]]
        df1 = old_dict[sheet_name].iloc[:, [0, 1, 2, 3]]
        df2 = new_dict[sheet_name].iloc[:, [0, 1, 2, 3]]
    elif sheet_name == "回路":
        on = [current_text["K_systemID"],current_text["K_panelID"],current_text["K_loopID"]]
        df1 = old_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4]]
        df2 = new_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4]]
    elif sheet_name and (current_text["K_pointsChanels"] in sheet_name):
        on = [current_text["K_systemID"],current_text["K_panelID"],current_text["K_loopID"],current_text["K_pointID"],current_text["K_channelID"]]
        df1 = old_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
        df2 = new_dict[sheet_name].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
    # else:
    #     st.write('当前只关心[控制器],[回路],[点&通道]', sheet_name)
        

    merge_options = ['both','left_only','right_only','diff']
    merge_selected = st.multiselect( current_text["UI_MSshowComparedContent"],  merge_options, merge_options)

    if len(on)>0:
        merged_df = pd.merge(df1, df2, on=on, suffixes=('_old', '_new'), how='outer', indicator=True)
        merged_df['_merge'] = pd.Categorical(merged_df['_merge'], categories=merge_options)
        merged_df.loc[(((merged_df[current_text["K_type"]+'_new'] != merged_df[current_text["K_type"]+'_old'])|(merged_df[current_text["K_ID"]+'_new'] != merged_df[current_text["K_ID"]+'_old'])) & (merged_df['_merge'] == 'both')), '_merge'] = 'diff'

        merge_counts = merged_df['_merge'].value_counts()
        st.write("🟠[",sheet_name,"]",dict(merge_counts))

        merged_df = merged_df[merged_df['_merge'].isin(merge_selected)]
        styled_df = merged_df.style.apply(apply_row_colors, axis=1)
        st.table(styled_df)
        


            
