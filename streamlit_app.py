import streamlit as st


st.set_page_config(layout="wide")
# how-to-keep-widget-value-remembered-in-multi-page-app
for key, val in st.session_state.items():
    if not key.endswith('__do_not_persist'):
        st.session_state[key] = val

#st.page_link("FS30i_MODBUS_CONFIG.py", label="Home", icon="🏠")
st.page_link("pages/A_Port_Config.py", label="FS 30i Port Config", icon="1️⃣")
st.caption("1. 选择要加载的FS30i配置文件")
st.caption("2. 选择需要映射的硬件端口")
st.caption("3. 配置硬件端口")
st.caption("4. 选择在当前端口中要使能的Panel")
st.page_link("pages/B_Object_Mapping.py", label="FS 30i Object Mapping", icon="2️⃣")
st.caption("1. 选择要映射Modbus的要硬件端口")
st.caption("2. 选择需要映射类型")
st.caption("3. 配置类型的基地址")
st.caption("4. 可以手动配置Modbus地址")
st.caption("5. 导出csv文件")

# st.divider()


