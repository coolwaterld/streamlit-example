import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(layout="wide")

# how-to-keep-widget-value-remembered-in-multi-page-app
for key, val in st.session_state.items():
    if not key.endswith('_dataeditor_key'):
        st.session_state[key] = val

types_options = ['FC30i', 'P2_Object','V-Point','P2_Loop','ILOP','ILOP_Ch','FRT','Power','MB_IO','Comm_Port']

@st.cache_data
def load_sheet(filename, sheetname):
    df = pd.read_excel(filename, sheetname)
    return df

# @st.cache_data
# def merge_sheets(filename):
#     xls = pd.ExcelFile(filename)
#     sheet_list = xls.sheet_names
#     filtered_items = [item for item in sheet_list if '点&通道' in item]

#     dfs = [xls.parse(index)for index in filtered_items]
#     return pd.concat(dfs,ignore_index = True)





increment = 1

with st.sidebar:
    current_datetime = datetime.now()
    current_datetime_string = current_datetime.strftime("%Y%m%d%H%M")

    if st.session_state.get('uploaded_file'):
        st.download_button( label="导出工程",  
                            data=str(st.session_state.to_dict()).encode('utf-8'),
                            file_name=st.session_state['uploaded_file'].split(".")[0]+'_'+current_datetime_string+'.proj'
                            )
    
if st.session_state.get('export_configs') and st.session_state['export_configs'].get("hosts"):
    hosts_options = list(st.session_state['export_configs']["hosts"].keys())
else:
    hosts_options = []


# file_name = st.session_state['uploaded_file']
# panels_name = "FC726S-W火灾报警控制器_2"
# st.write(file_name)
# st.write(panels_name)
# st.divider()

# sheet_name = "控制器"
# df_panels = load_sheet(file_name,sheet_name)
# st.write("df_panels",df_panels)

# sheet_name = "回路"
# df_loops = load_sheet(file_name,sheet_name)
# # st.write("df_loops:",df_loops)


# index = df_panels[df_panels["名称"]==panels_name].index[0]
# panels_id = df_panels.at[index,"控制器地址"] 
# # st.write("panels_id",panels_id)

# sheet_name = "点&通道_1_"+str(panels_id)
# # st.write("point sheets:",sheet_name)
# df_points = load_sheet(file_name,sheet_name)
# # st.write("df_points:",df_points)

# ##############################################
# df_p2= df_points[(df_points['回路地址'] >= 1) & (df_points['回路地址'] <= 20) & (df_points['点地址'] >= 1)& (df_points['点地址'] <= 255)]
# st.write("df_p2:",df_p2)

# df_vpoint= df_points[(df_points['回路地址'] == 80) & (df_points['回路地址'] == 81) & (df_points['点地址'] >= 1)& (df_points['点地址'] <= 255)]
# st.write("df_vpoint:",df_vpoint)

# df_p2_loop = df_loops[(df_loops['回路地址'] >= 1) & (df_loops['回路地址'] <= 20) & (df_loops['控制器地址'] == panels_id)]
# st.write("df_p2_loop:",df_p2_loop)

# df_ilop =  df_points[(df_points['回路地址'] == 33) & (df_points['通道地址'] == 0)]
# st.write("df_ilop:",df_ilop)

# df_ilop_ch =  df_points[(df_points['回路地址'] == 33) & (df_points['通道地址'] > 0)]
# st.write("df_ilop_ch:",df_ilop_ch)

# df_frt =  df_points[(df_points['回路地址'] == 37)]
# st.write("df_frt:",df_frt)

# df_power =  df_points[(df_points['回路地址'] == 60)]
# st.write("df_power:",df_power)

# df_mb_io =  df_points[(df_points['回路地址'] == 61)]
# st.write("df_mb_io:",df_mb_io)

# df_comm_port =  df_points[(df_points['回路地址'] == 62)]
# st.write("df_comm_port:",df_comm_port)




if len(hosts_options):
    tabs= st.tabs(hosts_options)
    for i, tab in enumerate(tabs):
        with tab:#Host
            host = hosts_options[i]
            panels_dict = st.session_state['export_configs']["hosts"][host]["panels"]
            panels = ["slave"+str(item) for item in sorted(list(panels_dict.keys()))]
            if len(panels)>0:
                panels_tabs= st.tabs(panels)
            # for panel_index, panel_tab in enumerate(panels_tabs):
                for panel_index,panel_tab in enumerate(panels_tabs):
                    with panel_tab:#Panel
                        pd_list_result = [] # used for get result from data_editor to generate final csv
                        panel = panels[panel_index] # it for identify widget
                        panel_value = panels_dict[int(panel[5:])]# it for filter dataframe
                        st.write(panel_value)

                        file_name = st.session_state['uploaded_file']

                        panels_name = panel_value
                        # st.write(file_name)
                        # st.write(panels_name)
                        # st.divider()

                        sheet_name = "控制器"
                        df_panels = load_sheet(file_name,sheet_name)
                        # st.write("df_panels",df_panels)

                        sheet_name = "回路"
                        df_loops = load_sheet(file_name,sheet_name)
                        # st.write("df_loops:",df_loops)


                        index = df_panels[df_panels["名称"]==panels_name].index[0]
                        panels_id = df_panels.at[index,"控制器地址"] 
                        # st.write("panels_id",panels_id)

                        sheet_name = "点&通道_1_"+str(panels_id)
                        # st.write("point sheets:",sheet_name)
                        df_points = load_sheet(file_name,sheet_name)
                        # st.write("df_points:",df_points)

                        type_option = st.multiselect('选择需要转换的类型',types_options,key=host+panel+"_type_key")

                        ##############################################
                        if "FC30i" in type_option:
                            df_panel = df_panels[df_panels['控制器地址'] == panels_id].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                            df_panel.rename(columns={'IP地址': '回路地址', '子网掩码': '点地址', '默认网关': '通道地址'}, inplace=True)
                            df_panel['回路地址'] = 0
                            df_panel['点地址'] = 0
                            df_panel['通道地址'] = 0
                            st.write("FC30i:",df_panel)

                        if "P2_Object" in type_option:
                            df_p2= df_points[(df_points['回路地址'] >= 1) & (df_points['回路地址'] <= 20) & (df_points['点地址'] >= 1)& (df_points['点地址'] <= 255)].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                            st.write("P2_Object:",df_p2)

                        if 'V-Point' in type_option:
                            df_vpoint= df_points[(df_points['回路地址'] >= 80) & (df_points['回路地址'] <= 81) & (df_points['点地址'] >= 1)& (df_points['点地址'] <= 255)].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                            st.write("V-Point:",df_vpoint)
                        
                        if 'P2_Loop' in type_option:
                            df_p2_loop = df_loops[(df_loops['回路地址'] >= 1) & (df_loops['回路地址'] <= 20) & (df_loops['控制器地址'] == panels_id)].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                            df_p2_loop.rename(columns={'拓扑类型': '点地址', '接地检测': '通道地址'}, inplace=True)
                            df_p2_loop['点地址'] = 0
                            df_p2_loop['通道地址'] = 0
                            st.write("P2_Loop:",df_p2_loop)

                        if 'ILOP' in type_option:
                            df_ilop =  df_points[(df_points['回路地址'] == 33) & (df_points['通道地址'] == 0)].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                            st.write("ILOP:",df_ilop)

                        if 'ILOP_Ch' in type_option:
                            df_ilop_ch =  df_points[(df_points['回路地址'] == 33) & (df_points['通道地址'] > 0)].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                            st.write("ILOP_Ch:",df_ilop_ch)

                        if 'FRT' in type_option:
                            df_frt =  df_points[(df_points['回路地址'] == 37)].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                            st.write("FRT:",df_frt)

                        if 'Power' in type_option:   
                            df_power =  df_points[(df_points['回路地址'] == 60)].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                            st.write("Power:",df_power)

                        if 'MB_IO' in type_option:
                            df_mb_io =  df_points[(df_points['回路地址'] == 61)].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                            st.write("MB_IO:",df_mb_io)

                        if 'Comm_Port' in type_option:       
                            df_comm_port =  df_points[(df_points['回路地址'] == 62)].iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                            st.write("Comm_Port:",df_comm_port) 
else:
    st.warning("请先选择硬件接口")
