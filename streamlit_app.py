import streamlit as st


st.set_page_config(layout="wide")
# how-to-keep-widget-value-remembered-in-multi-page-app
for key, val in st.session_state.items():
    if not key.endswith('__do_not_persist'):
        st.session_state[key] = val

st.header("FS 30i Port Config")
st.caption("1. Select the FS30i configuration file you want to load")
st.caption("2. Select the hardware interfaces that need to be mapped")
st.caption("3. Configure hardware interfaces")
st.caption("4. Select the panel you want to map to the hardware interface")

st.header("FS 30i Object Mapping")
st.caption("1. Select the hardware interface you want to map")
st.caption("2. Select the types of objects you want to map")
st.caption("3. Configure base address of Modbus for each type")
st.caption("4. Configure Modbus addresses manually")
st.caption("5. Export objects mapping CSV file")


# st.divider()


