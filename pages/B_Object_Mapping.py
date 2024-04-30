import streamlit as st
import pandas as pd
# import json
from datetime import datetime

st.set_page_config(layout="wide")

# how-to-keep-widget-value-remembered-in-multi-page-app
for key, val in st.session_state.items():
    if not key.endswith('__do_not_persist'):
        st.session_state[key] = val

# st.write(st.session_state.current_text["greet"])
current_text = st.session_state.current_text

###########################data ############################

modbus_base_address = {
    'FC30i':100,
    'P2_Object':1000,
    'V-Point':7000,
    'P2_Loop':10000,
    'ILOP':10100,
    'ILOP_Ch':11000,
    'FRT':12000,
    'Power':12100,
    'MB_IO':12200,
    'Comm_Port':12300
}
types_options = list(modbus_base_address.keys())
st.session_state["export_configs"]["types"] = types_options

###########################General ############################
def find_duplicates_and_indices(lst):
    seen = {}  # Dictionary to store indices of each element
    duplicates = {}

    for i, value in enumerate(lst):
        # If the value is not in the dictionary, add it with its index
        if value not in seen:
            seen[value] = i
        else:
            # If the value is already in the dictionary, it's a duplicate
            if value not in duplicates:
                duplicates[value] = [seen[value], i]
            else:
                duplicates[value].append(i)

    return duplicates

@st.cache_data
def load_sheet(file, sheetname):
    df = pd.read_excel(file, sheetname)
    return df

#################file level###################

@st.cache_data
def domain_load_panels_loops(file):
    sheet_name = current_text["K_panel"]
    df_panels = load_sheet(file,sheet_name)
    # st.write("df_panels",df_panels)

    sheet_name = current_text["K_loop"]
    df_loops = load_sheet(file,sheet_name)
    # st.write("df_loops:",df_loops)

    return df_panels,df_loops

#################panel level###################
@st.cache_data
def domain_load_points(file,panel_id):
    sheet_name = current_text["K_pointsChanels"]+str(panel_id)
    df_points = load_sheet(file,sheet_name)
    return df_points
#################type level###################
@st.cache_data
def domain_load_type(df_panels,df_loops,df_points,panels_id,type):
    if type == "FC30i":
        df_tmp = df_panels[df_panels[current_text["K_panelID"]] == panel_id].iloc[:, [0, 1, 2, 3, 4, 5, 6]].reset_index(drop=True)
        df_tmp.rename(columns={current_text["K_IP"]: current_text["K_loopID"], current_text["K_subnetMask"]: current_text["K_pointID"], current_text["K_gateway"]: current_text["K_channelID"]}, inplace=True)
        df_tmp[current_text["K_loopID"]] = 0
        df_tmp[current_text["K_pointID"]] = 0
        df_tmp[current_text["K_channelID"]] = 0
    elif type == 'P2_Object':
        df_tmp = df_points[(df_points[current_text["K_loopID"]] >= 1) & (df_points[current_text["K_loopID"]] <= 20) & (df_points[current_text["K_pointID"]] >= 1)& (df_points[current_text["K_pointID"]] <= 255)].iloc[:, [0, 1, 2, 3, 4, 5, 6]].reset_index(drop=True)
    elif type == 'V-Point':
        df_tmp = df_points[(df_points[current_text["K_loopID"]] >= 80) & (df_points[current_text["K_loopID"]] <= 81) & (df_points[current_text["K_pointID"]] >= 1)& (df_points[current_text["K_pointID"]] <= 255)].iloc[:, [0, 1, 2, 3, 4, 5, 6]].reset_index(drop=True)
    elif type == 'P2_Loop':
        df_tmp = df_loops[(df_loops[current_text["K_loopID"]] >= 1) & (df_loops[current_text["K_loopID"]] <= 20) & (df_loops[current_text["K_panelID"]] == panels_id)].iloc[:, [0, 1, 2, 3, 4, 5, 6]].reset_index(drop=True)
        df_tmp.rename(columns={current_text["K_topologyType"]: current_text["K_pointID"], current_text["K_groundDetection"]: current_text["K_channelID"]}, inplace=True)
        df_tmp[current_text["K_pointID"]] = 0
        df_tmp[current_text["K_channelID"]] = 0
    elif type == 'ILOP':
        df_tmp = df_points[(df_points[current_text["K_loopID"]] == 33) & (df_points[current_text["K_channelID"]] == 0)].iloc[:, [0, 1, 2, 3, 4, 5, 6]].reset_index(drop=True)
    elif type == 'ILOP_Ch':
        df_tmp = df_points[(df_points[current_text["K_loopID"]] == 33) & (df_points[current_text["K_channelID"]] > 0)].iloc[:, [0, 1, 2, 3, 4, 5, 6]].reset_index(drop=True)
    elif type == 'FRT':
        df_tmp = df_points[(df_points[current_text["K_loopID"]] == 37)].iloc[:, [0, 1, 2, 3, 4, 5, 6]].reset_index(drop=True)
    elif type == 'Power':
        df_tmp = df_points[(df_points[current_text["K_loopID"]] == 60)].iloc[:, [0, 1, 2, 3, 4, 5, 6]].reset_index(drop=True)
    elif type == 'MB_IO':
        df_tmp = df_points[(df_points[current_text["K_loopID"]] == 61)].iloc[:, [0, 1, 2, 3, 4, 5, 6]].reset_index(drop=True)
    elif type == 'Comm_Port':
        df_tmp = df_points[(df_points[current_text["K_loopID"]] == 62)].iloc[:, [0, 1, 2, 3, 4, 5, 6]].reset_index(drop=True)
    else:
        st.write(type,"is wrong")
        df_tmp = pd.DataFrame()
    return df_tmp


###########################UI ##########################

def modbus_editor(df,host,slave,type):
    rows, columns = df.shape
    df["type"] = types_options.index(type)
    df["Modbus_Offset"] = range(0,rows)
    st.caption("🟠"+type)
    base_address = st.number_input(current_text["UI_NIModbusBaseAddr"], value=modbus_base_address[type],key=host+slave+type+"_numberinput_key")
    key = host+slave+type+"_dataeditor_key_"+"__do_not_persist"
    # key_changed = host+slave+type+"_dataeditor_key_"+"__changed"
    # if st.session_state.get(key_changed):
    #     for k,v in st.session_state[key_changed]["edited_rows"].items():
    #         st.write(v)
    #         df.at[k,"Modbus_Offset"]=1

    df_result = st.data_editor(df,use_container_width=True,
                                key=key,
                                hide_index = True,
                                num_rows='dynamic')
    # st.write("当前的结果：",df_result)
    return base_address,df_result

def find_duplicates_UI(lst):
    duplicates_info = find_duplicates_and_indices(lst)
    if duplicates_info:
        for value, indices in duplicates_info.items():
            st.error(f"Value {value} is duplicated at indices: {indices}")

def dispay_tab(type,type_option,pd_dict_result): 
    if type in type_option:
        df_temp = domain_load_type(df_panels,df_loops,df_points,panel_id,type)
        base_address,df_result = modbus_editor(df_temp,host,slave,type)
        pd_dict_result[type]=df_result
        find_duplicates_UI(df_result["Modbus_Offset"])
    else:
        if type in pd_dict_result:
            del pd_dict_result[type]

with st.sidebar:
    current_datetime = datetime.now()
    current_datetime_string = current_datetime.strftime("%Y%m%d%H%M")

    if st.session_state.get('uploaded_file'):
        st.download_button( label=current_text["UI_DBTExportProject"],  
                            data=str(st.session_state.to_dict()).encode('utf-8'),
                            file_name=st.session_state['uploaded_file'].name.split(".")[0]+'_'+current_datetime_string+'.proj' #st.session_state['uploaded_file'].split(".")[0]+'_'+current_datetime_string+'.proj'
                            )
    

###########################main################################

# 1.load file
if st.session_state.get('uploaded_file'):
    df_panels,df_loops = domain_load_panels_loops(st.session_state['uploaded_file'])
else:
    df_panels = pd.DataFrame()
    df_loops = pd.DataFrame()


if st.session_state.get('export_configs') and st.session_state['export_configs'].get("hosts"):
    hosts_options = list(st.session_state['export_configs']["hosts"].keys())
else:
    hosts_options = []

if len(hosts_options)==0:
    st.write("Please select hosts first")
else:
# 2.select hosts
    tabs= st.tabs(hosts_options)
    for i, tab in enumerate(tabs):
        with tab:#Host
            host = hosts_options[i]
            if st.session_state['export_configs']["hosts"].get(host) and st.session_state['export_configs']["hosts"][host].get("panels"):
                slaves_dict = st.session_state['export_configs']["hosts"][host]["panels"]
                st.write(slaves_dict)
                slaves = ["slave"+str(item) for item in sorted(list(slaves_dict.keys()))]
            else:
                slaves = []
            if len(slaves)==0:
                st.write("Please add Modbus Slave first")
            else:
# 3. select slave
                slaves_tabs= st.tabs(slaves)
                for slave_index,slave_tab in enumerate(slaves_tabs):
                    with slave_tab:#Panel
                        pd_dict_result = {} # used for get result from data_editor to generate final csv
                        slave = slaves[slave_index] # it for identify widget
                        panel_name = slaves_dict[int(slave[5:])]# it for filter dataframe
                        index = df_panels[df_panels["名称"]==panel_name].index[0]
                        panel_id = df_panels.at[index,"控制器地址"] 
                        # st.write("slave:",slave,",slave_value:",panel_name,",panel_id:",panel_id)
                        df_points = domain_load_points(st.session_state['uploaded_file'],panel_id)
# 4. select objects types and show
                        type_option = st.multiselect(current_text["UI_MSObjectTypes"],types_options,key=host+slave+"_type_key")
                        for type in types_options:
                            dispay_tab(type,type_option,pd_dict_result)

# 5. concat and map dataframe              
                        if len(pd_dict_result) > 0:
                            for key in pd_dict_result.keys():
                                pd_dict_result[key]["Modbus_Offset"] += st.session_state[host+slave+key+"_numberinput_key"]
                                pd_dict_result[key].rename(columns={'Modbus_Offset': 'Modbus'}, inplace=True)                          
                                    
                            appended_df = pd.concat(list(pd_dict_result.values()), ignore_index=True)
                            st.divider()
                            st.write(slave,current_text["UI_WMappingResults"],appended_df)
                            find_duplicates_UI(appended_df["Modbus"])
                            csv_result = appended_df.drop(appended_df.columns[[0, 1]], axis=1).to_csv(index=False).encode('utf-8')
                            download_file_name = st.session_state["uploaded_file"].name.split(".")[0]+'_'+host+'_'+slave+'.csv'#st.session_state["uploaded_file"].split(".")[0]+'_'+host+'_'+slave+'.csv'
                            ret = st.download_button(
                                label=current_text["UI_DBTExportCSV"],
                                data=csv_result,
                                file_name=download_file_name,
                                mime='text/csv',
                            )
                            if ret:
                                if not st.session_state["export_configs"]["hosts"][host].get("files"):
                                    st.session_state["export_configs"]["hosts"][host]["files"] = {}
                                st.session_state["export_configs"]["hosts"][host]["files"][slave] =download_file_name
                               
if st.session_state.get("export_configs") and st.sidebar.checkbox(current_text["UI_CBMoreInformation"]):
    st.sidebar.write(st.session_state["export_configs"])                                    