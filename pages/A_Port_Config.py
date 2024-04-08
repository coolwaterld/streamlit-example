import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(layout="wide")

# how-to-keep-widget-value-remembered-in-multi-page-app
for key, val in st.session_state.items():
    if not key.endswith('__do_not_persist'):
        st.session_state[key] = val


@st.cache_data
def load_sheet(file, sheetname):
    df = pd.read_excel(file, sheetname)
    return df

if 'name_list' not in st.session_state:
    st.session_state['name_list'] = []
if 'export_configs' not in st.session_state:
    st.session_state['export_configs'] = {}
    st.session_state['export_configs']["hosts"] = {}


########################


hosts_options = ["ETH1", "ETH2", "COM1", "COM2"]
for host in hosts_options:
    if host not in st.session_state:
        st.session_state[host]={}
        st.session_state[host]['panels'] = {}
        st.session_state[host]['indexs'] = set()
          

def get_next_salve_index(host):
    # print(st.session_state[host])
    if len(st.session_state[host]['indexs'])==0:
        return 0
    else:
        end = max(st.session_state[host]['indexs'])+1
        full_set = set(range(0,end))
        other_set = full_set - st.session_state[host]['indexs']
        if len(other_set)>0:
            return min(other_set)
        else:
            return end

def add_slave(host):
    next = get_next_salve_index(host)
    st.session_state[host]['indexs'].add(next)

def delete_slave(index,host):
    st.session_state[host]['indexs'].discard(index)
    del st.session_state[host]['panels'][index]

def sort_slave(host):
    st.session_state[host]['indexs'] = set(sorted(st.session_state[host]['indexs'] ))

def display_input_slave_row(i,panels,host):
    c1, c2,c3 = st.columns([1,4,1])
    with c1:
        st.write(f"Salve{i}:")
    with c2:
        st.session_state[host]['panels'][i] = st.selectbox(f"Slave {i}", panels,key=host+f"selectbox{i}",label_visibility="collapsed")

    with c3:
        st.button("🗑️", key=host+f"delete{i}__do_not_persist", on_click=delete_slave, args=(i,host))
def display_slave_button(host):
    c1, c2,c3 = st.columns([1,1,4])
    with c1:
        st.button("Add Slave", on_click=add_slave,key=host+'add_salve_button__do_not_persist', args=(host,))
    with c2:
        st.button("Sort Slaves", on_click=sort_slave,key=host+'sort_salve_button__do_not_persist', args=(host,))
    ########################

tab1,tab2= st.tabs(["加载FS30i配置文件","加载已有工程文件"])
with tab1:
    tmp_file = st.file_uploader("导入FS30i配置文件xlsx")
    if tmp_file is not None:
        if st.session_state.get("uploaded_file") and st.session_state.get("uploaded_file") != tmp_file:#tmp_file.name:
            st.session_state.clear()
            st.session_state["hosts_multiselect_key"]=[]
        st.session_state["uploaded_file"] = tmp_file #tmp_file.name
with tab2:
    project_file = st.file_uploader("导入工程文件")
    if project_file is not None:
        st.session_state.clear()
        content = project_file.read().decode('utf-8')
        dict_session_state = eval(content)
        for key, val in dict_session_state.items():
            if not key.endswith('__do_not_persist'):
                st.session_state[key] = val
            else:
                new_key = key.replace('__do_not_persist', '__changed')
                if not st.session_state.get(new_key):
                    st.session_state[new_key] = {}
                st.session_state[new_key].update(val)
                # st.session_state["ETH1slave0FC30i_dataeditor_key___changed"]["edited_rows"][0]["Modbus_Offset"] = 13
                # st.write(new_key,st.session_state[new_key])



if st.session_state.get("uploaded_file"):
    st.write("当前加载的文件：",st.session_state.get("uploaded_file").name)
    df_controler = load_sheet(st.session_state.uploaded_file, '控制器')
    panels = list(df_controler['名称'])

    
    st.multiselect('选择在MODBUS中要使用的硬件端口', hosts_options, key="hosts_multiselect_key")
    options = st.session_state.hosts_multiselect_key
    for host in options:
        st.header(host)
        if "COM" in host:
            baudrate_options = ['9600', '38400', '115200']
            transfmt_options = ['1-8-E-1', '1-8-O-1']
            st.selectbox("baudrate:", baudrate_options,
                         key=host+"_baudrate_selectbox_key")
            st.selectbox("transfmt:", transfmt_options,
                         key=host+"_baudrate_transfmt_key")

            st.write("选择Salve对应的Panel")
            if st.session_state[host].get('indexs'):
                for i in st.session_state[host]['indexs'] :
                    display_input_slave_row(i,panels,host)
            display_slave_button(host)
            if st.session_state['export_configs']["hosts"].get(host):
                st.session_state['export_configs']["hosts"][host].update({
                    "properties": {
                        "baudrate": st.session_state[host+"_baudrate_selectbox_key"],
                        "transfmt": st.session_state[host+"_baudrate_transfmt_key"]
                    },
                    "panels": st.session_state[host]["panels"]
                })
            else:
                st.session_state['export_configs']["hosts"][host]= {
                    "properties": {
                        "baudrate": st.session_state[host+"_baudrate_selectbox_key"],
                        "transfmt": st.session_state[host+"_baudrate_transfmt_key"]
                    },
                    "panels": st.session_state[host]["panels"]
                }


        else:
            st.text_input("IP:", key=host+"_ip_text_input_key",
                          value="192.168.1.1")
            st.number_input("Port:", key=host +
                            "_port_number_input_key", value=9000)

            st.write("选择Salve对应的Panel")
            if st.session_state[host].get('indexs'):
                for i in st.session_state[host]['indexs'] :
                    display_input_slave_row(i,panels,host)

            display_slave_button(host)

            if st.session_state['export_configs']["hosts"].get(host):
                st.session_state['export_configs']["hosts"][host].update({
                    "properties": {
                        "IP": st.session_state[host+"_ip_text_input_key"],
                        "Port": st.session_state[host+"_port_number_input_key"]
                    },
                    "panels": st.session_state[host]["panels"]
                })
            else:
                st.session_state['export_configs']["hosts"][host] = {
                    "properties": {
                        "IP": st.session_state[host+"_ip_text_input_key"],
                        "Port": st.session_state[host+"_port_number_input_key"]
                    },
                    "panels": st.session_state[host]["panels"]
                }

    
        


if st.session_state.get("uploaded_file") and st.session_state.get("export_configs"):
    current_datetime = datetime.now()
    current_datetime_string = current_datetime.strftime("%Y%m%d%H%M")
    hostsstr = json.dumps(st.session_state['export_configs'],indent=2,ensure_ascii=False)
    st.download_button( label="导出Hosts配置文件",  
                        data=hostsstr.encode('utf-8'),
                        file_name=st.session_state['uploaded_file'].name.split(".")[0]+'_hosts_'+current_datetime_string+'.json'#st.session_state['uploaded_file'].split(".")[0]+'_hosts_'+current_datetime_string+'.json'
                        )

if st.session_state.get("export_configs") and st.sidebar.checkbox('More Informaton'):
    st.sidebar.write(st.session_state["export_configs"]) 