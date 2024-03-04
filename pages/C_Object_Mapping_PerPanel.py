import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(layout="wide")

# how-to-keep-widget-value-remembered-in-multi-page-app
for key, val in st.session_state.items():
    if not key.endswith('_dataeditor_key'):
        st.session_state[key] = val

types_options = ['控制器节点', 'P2设备', '联动盘']

@st.cache_data
def load_sheet(filename, sheetname):
    df = pd.read_excel(filename, sheetname)
    return df

@st.cache_data
def merge_sheets(filename):
    xls = pd.ExcelFile(filename)
    sheet_list = xls.sheet_names
    filtered_items = [item for item in sheet_list if '点&通道' in item]

    dfs = [xls.parse(index)for index in filtered_items]
    return pd.concat(dfs,ignore_index = True)

def onChange(key):
    if not st.session_state.get(key+"_changed"):
        st.session_state[key+"_changed"] = {}

    st.session_state[key+"_changed"].update(st.session_state[key]["edited_rows"])

def validateUnique(serie,value,index):
        indexlist = serie[serie == value].index.tolist()
        if index is not None:
            indexlist.remove(index)
        return indexlist

def validateAll(key,value,whichResult):
    if not controller_result.empty:
        ret = validateUnique(controller_result["Modbus"],val,key if whichResult == 'controller_result'else None)
        if len(ret)>0:
            st.error(whichResult+"["+str(key)+"],conflict with controller_result" +str(ret))
    if not p2_result.empty:
        ret = validateUnique(p2_result["Modbus"],val,key if whichResult == 'p2_result'else None)
        if len(ret)>0:
            st.error(whichResult+"["+str(key)+"],conflict with p2_result" +str(ret))
    if not linkage_result.empty:
        ret = validateUnique(linkage_result["Modbus"],val,key if whichResult == 'linkage_result'else None)
        if len(ret)>0:
            st.error(whichResult+"["+str(key)+"],conflict with linkage_result" +str(ret))

increment = 1

with st.sidebar:
    current_datetime = datetime.now()
    current_datetime_string = current_datetime.strftime("%Y%m%d%H%M")

    if st.session_state.get('uploaded_file'):
        st.download_button( label="导出工程",  
                            data=str(st.session_state.to_dict()).encode('utf-8'),
                            file_name=st.session_state['uploaded_file'].split(".")[0]+'_'+current_datetime_string+'.proj'
                            )
    

hosts_options = list(st.session_state['export_configs']["hosts"].keys())
if len(hosts_options):
    tabs= st.tabs(hosts_options)
    for i, tab in enumerate(tabs):
        with tab:
            host = hosts_options[i]
            panels_dict = st.session_state['export_configs']["hosts"][host]["panels"]
            panels = ["slave"+str(item) for item in sorted(list(panels_dict.keys()))]
            if len(panels)>0:
                panels_tabs= st.tabs(panels)
            # for panel_index, panel_tab in enumerate(panels_tabs):
                for panel_index,panel_tab in enumerate(panels_tabs):
                    with panel_tab:
                        pd_list_result = [] # used for get result from data_editor to generate final csv
                        panel = panels[panel_index] # it for identify widget
                        panel_value = panels_dict[int(panel[5:])]# it for filter dataframe
                        st.write(panel_value)
                        st.multiselect('选择需要转换的类型',types_options,key=host+panel+"_type_key")

                        df_controler = load_sheet(st.session_state["uploaded_file"], '控制器')
                        df_controler = df_controler[df_controler['名称']==panel_value]
                        panels_tuples = df_controler.apply(lambda row: (row['系统地址'], row['控制器地址']), axis=1)
                        df_controler = df_controler.iloc[:, [0, 1, 2, 3, 4, 5, 6]]
                        df_controler.rename(columns={'IP地址': '回路地址', '子网掩码': '点地址', '默认网关': '通道地址'}, inplace=True)
                        df_controler['回路地址'] = 0
                        df_controler['点地址'] = 0
                        df_controler['通道地址'] = 0
                        df_controler = df_controler.reset_index(drop=True) # make sure index is unique
                        controler_rows, columns = df_controler.shape

                        df_loop = load_sheet(st.session_state["uploaded_file"], '回路')
                        df_detect_loop = df_loop[df_loop['类型'].str.contains('探测总线')]
                        df_detect_loop = df_detect_loop[df_detect_loop[['系统地址', '控制器地址']].apply(tuple, axis=1).isin(panels_tuples)]

                        
                        mergedf = merge_sheets(st.session_state["uploaded_file"])
                        result_tuples = df_detect_loop.apply(lambda row: (row['系统地址'], row['控制器地址'], row['回路地址']), axis=1)
                        df_p2 = mergedf[mergedf[['系统地址', '控制器地址', '回路地址']].apply(tuple, axis=1).isin(result_tuples)]
                        df_p2 = df_p2.reset_index(drop=True) # make sure index is unique
                        df_p2 = df_p2.iloc[:, [0,1, 2, 3, 4, 5, 6,]]
                        p2_rows, columns = df_p2.shape

                        df_linkage = mergedf[(mergedf["回路地址"] == 33) & (mergedf['类型'].str.contains('联动盘'))]
                        df_linkage = df_linkage[df_linkage[['系统地址', '控制器地址']].apply(tuple, axis=1).isin(panels_tuples)] # filter: only keep rows whose panel in [panels]
                        df_linkage = df_linkage.reset_index(drop=True) # make sure index is unique
                        df_linkage = df_linkage.iloc[:, [0, 1, 2, 3, 4, 5, 6,]]
                        linkage_rows, columns = df_linkage.shape

                        if "控制器节点" in st.session_state[host+panel+"_type_key"]:
                            st.header("控制器节点")
                            st.number_input('Insert base address', value=10000,key=host+panel+"_controller_numberinput_key")

                            df_controler["Modbus"] = list(range(st.session_state[host+panel+"_controller_numberinput_key"], st.session_state[host+panel+"_controller_numberinput_key"] + controler_rows * increment, increment))
                            tmp= host+panel+"_controller_dataeditor_key"+"_changed"
                            if st.session_state.get(tmp):
                                for key in st.session_state[tmp]:
                                    df_controler.loc[key, "Modbus"] = st.session_state[tmp][key]["Modbus"]
                            
                            controller_result = st.data_editor(df_controler, use_container_width=True, key=host+panel+"_controller_dataeditor_key", disabled=[0, 1, 2, 3, 4, 5, 6],on_change=onChange,args=[host+panel+"_controller_dataeditor_key"])
                            pd_list_result.append(controller_result)
                        else:
                            controller_result = pd.DataFrame()
                            st.session_state[host+panel+"_controller_dataeditor_key"+"_changed"] = {}


                        if "P2设备" in st.session_state[host+panel+"_type_key"]:
                            st.header("P2设备")
                            st.number_input('Insert base address', value=20000,key=host+panel+"_P2_numberinput_key")

                            df_p2["Modbus"] = list(range(st.session_state[host+panel+"_P2_numberinput_key"], st.session_state[host+panel+"_P2_numberinput_key"] + p2_rows * increment, increment))
                            
                            tmp= host+panel+"_p2_dataeditor_key"+"_changed"
                            if st.session_state.get(tmp):
                                for key in st.session_state[tmp]:
                                    df_p2.loc[key, "Modbus"] = st.session_state[tmp][key]["Modbus"]
                            
                            p2_result = st.data_editor(df_p2, use_container_width=True,key=host+panel+"_p2_dataeditor_key",disabled=[0, 1, 2, 3, 4, 5, 6],on_change=onChange,args=[host+panel+"_p2_dataeditor_key"])
                            pd_list_result.append(p2_result)
                        else:
                            p2_result = pd.DataFrame()
                            st.session_state[host+panel+"_p2_dataeditor_key"+"_changed"] = {}

                        if "联动盘" in st.session_state[host+panel+"_type_key"]:
                            st.header("联动盘")
                            st.number_input('Insert base address', value=30000,key=host+panel+"_linkage_numberinput_key")
                            df_linkage["Modbus"] = list(range(st.session_state[host+panel+"_linkage_numberinput_key"], st.session_state[host+panel+"_linkage_numberinput_key"] + linkage_rows * increment, increment))
                            
                            tmp= host+panel+"_linkage_dataeditor_key"+"_changed"
                            if st.session_state.get(tmp):
                                for key in st.session_state[tmp]:
                                    df_linkage.loc[key, "Modbus"] = st.session_state[tmp][key]["Modbus"]
                            
                            linkage_result = st.data_editor(df_linkage, use_container_width=True,key=host+panel+"_linkage_dataeditor_key",disabled=[0, 1, 2, 3, 4, 5, 6],on_change=onChange,args=[host+panel+"_linkage_dataeditor_key"])
                            pd_list_result.append(linkage_result)
                        else:
                            linkage_result = pd.DataFrame()
                            st.session_state[host+panel+"_linkage_dataeditor_key"+"_changed"] = {}
                
                        ################################################
                        st.write("Modbus 设置冲突:")
                        for key in st.session_state[host+panel+"_controller_dataeditor_key"+"_changed"]:
                            val = st.session_state[host+panel+"_controller_dataeditor_key"+"_changed"][key]["Modbus"]
                            validateAll(key,val,'controller_result')
                        for key in st.session_state[host+panel+"_p2_dataeditor_key"+"_changed"]:
                            val = st.session_state[host+panel+"_p2_dataeditor_key"+"_changed"][key]["Modbus"]
                            validateAll(key,val,'p2_result')
                        for key in st.session_state[host+panel+"_linkage_dataeditor_key"+"_changed"]:
                            val = st.session_state[host+panel+"_linkage_dataeditor_key"+"_changed"][key]["Modbus"]
                            validateAll(key,val,'linkage_result')

                        if len(pd_list_result) > 0:
                            appended_df = pd.concat(pd_list_result, ignore_index=True)       
                            csv_result = appended_df.to_csv().encode('utf-8')
                            st.download_button(
                                label="导出CSV文件",
                                data=csv_result,
                                file_name=st.session_state["uploaded_file"].split(".")[0]+'_'+host+'_'+panel+'.csv',
                                mime='text/csv',
                            )
else:
    st.warning("请先选择硬件接口")
