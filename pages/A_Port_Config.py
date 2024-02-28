import streamlit as st
import pandas as pd
import json
st.set_page_config(layout="wide")

# how-to-keep-widget-value-remembered-in-multi-page-app
for key, val in st.session_state.items():
    if not key.endswith('__do_not_persist'):
        st.session_state[key] = val


@st.cache_data
def load_sheet(filename, sheetname):
    df = pd.read_excel(filename, sheetname)
    return df

tab1,tab2= st.tabs(["加载FS30i配置文件","加载已有工程文件"])
with tab1:
    tmp_file = st.file_uploader("导入FS30i配置文件xlsx")
    if tmp_file is not None:
        if st.session_state.get("uploaded_file") and st.session_state.get("uploaded_file") != tmp_file.name:
            st.session_state.clear()
            st.session_state["hosts_multiselect_key"]=[]
        st.session_state["uploaded_file"] = tmp_file.name
with tab2:
    project_file = st.file_uploader("导入工程文件")
    if project_file is not None:
        st.session_state.clear()
        content = project_file.read().decode('utf-8')
        dict_session_state = eval(content)
        for key, val in dict_session_state.items():
            st.session_state[key] = val


if 'name_list' not in st.session_state:
    st.session_state['name_list'] = []
if 'export_configs' not in st.session_state:
    st.session_state['export_configs'] = {}
    st.session_state['export_configs']["hosts"] = {}


if st.session_state.get("uploaded_file"):
    st.write("当前加载的文件：",st.session_state.get("uploaded_file"))
    df_controler = load_sheet(st.session_state.uploaded_file, '控制器')

    st.session_state['name_list'] = list(df_controler['名称'])

    st.multiselect('选择在MODBUS中要使用的硬件端口', [
                   "ETH1", "ETH2", "COM1", "COM2"], key="hosts_multiselect_key")
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
            st.multiselect(
                '选择在当前端口中要使能的Panel', st.session_state['name_list'], key=host+"_panel_multiselect_key")
            st.session_state['export_configs']["hosts"][host] = {
                "properties": {
                    "baudrate": st.session_state[host+"_baudrate_selectbox_key"],
                    "transfmt": st.session_state[host+"_baudrate_transfmt_key"]
                },
                "panels": st.session_state[host+"_panel_multiselect_key"]
            }

        else:
            st.text_input("IP:", key=host+"_ip_text_input_key",
                          value="192.168.1.1")
            st.number_input("Port:", key=host +
                            "_port_number_input_key", value=9000)
            options = st.multiselect(
                '选择在当前端口中要使能的Panel', st.session_state['name_list'], key=host+"_panel_multiselect_key")
            st.session_state['export_configs']["hosts"][host] = {
                "properties": {
                    "IP": st.session_state[host+"_ip_text_input_key"],
                    "Port": st.session_state[host+"_port_number_input_key"]
                },
                "panels": st.session_state[host+"_panel_multiselect_key"]
            }

    # st.session_state['export_configs']["file"] = st.session_state.uploaded_file.name


st.sidebar.write(st.session_state)