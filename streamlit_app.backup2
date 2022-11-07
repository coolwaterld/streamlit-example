import streamlit as st
# st.header("Configuration:")
# uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
# for uploaded_file in uploaded_files:
#      bytes_data = uploaded_file.read()
#      st.write("filename:", uploaded_file.name)
#      st.write(bytes_data)

st.header("Hardware type:")
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
hardware = st.radio("Which hardware do you want to deploy the applications?",('IEVD', 'IPC 127E', 'IPC 227E', 'IPC 427E', 'IPC 847E'))

resource = {"IEVD":{"cpu":100,"memory":100,"flash":100},
"IPC 127E":{"cpu":200,"memory":200,"flash":200},
"IPC 227E":{"cpu":300,"memory":300,"flash":300},
"IPC 427E":{"cpu":400,"memory":400,"flash":400},
"IPC 847E":{"cpu":500,"memory":500,"flash":500}
}


cpu_usage_value = 0
memory_usage_value = 0
flash_usage_value = 0
# st.write('cpu usage:')
# cpu_usage_percent = st.progress(cpu_usage_value/resource[hardware]["cpu"])
# st.write('memory usage:')
# memory_usage_percent = st.progress(memory_usage_value/resource[hardware]["memory"])
# st.write('flash usage:')
# flash_usage_percent = st.progress(flash_usage_value/resource[hardware]["flash"])



st.header("Application:")
with st.expander("Optimized S7"):
     Optimized_S7 = st.checkbox('Optimized S7')
     Optimized_S7_Connections = st.selectbox(
          'Connections?',
          (1,8),
          key=1,disabled=not Optimized_S7)

     if Optimized_S7:
          cpu_usage_value=cpu_usage_value+Optimized_S7_Connections*5
          memory_usage_value = memory_usage_value+Optimized_S7_Connections*5
          flash_usage_value = flash_usage_value+Optimized_S7_Connections*5

     Optimized_S7_Aquisition_Cycle = st.selectbox(
          'Aquisition Cycle?',
          (100,500),
          key=2,disabled=not Optimized_S7)
     if Optimized_S7:
          cpu_usage_value=cpu_usage_value+Optimized_S7/10
          memory_usage_value = memory_usage_value+Optimized_S7/10
          flash_usage_value = flash_usage_value+Optimized_S7/10

     Optimized_S7_tags = st.select_slider(
          'Tags',
          options=[600,800,1000,1200,1400,1600,1800,2000],
          key=3,disabled=not Optimized_S7)

     if Optimized_S7:
          cpu_usage_value=cpu_usage_value+Optimized_S7_tags/100
          memory_usage_value = memory_usage_value+Optimized_S7_tags/100
          flash_usage_value = flash_usage_value+Optimized_S7_tags/100
with st.expander("OPC UA"):
     OPC_UA = st.checkbox('OPC UA')
     OPC_UA_Connections = st.selectbox(
          'Connections?',
          (1,8),
          key=4,disabled=not OPC_UA)
     if OPC_UA:
          cpu_usage_value=cpu_usage_value+OPC_UA_Connections*6
          memory_usage_value = memory_usage_value+OPC_UA_Connections*6
          flash_usage_value = flash_usage_value+OPC_UA_Connections*6

     OPC_UA_Aquisition_Cycle = st.selectbox(
          'Aquisition Cycle?',
          (80,640),
          key=5,disabled=not OPC_UA)
     if OPC_UA:
          cpu_usage_value=cpu_usage_value+OPC_UA_Aquisition_Cycle/8
          memory_usage_value = memory_usage_value+OPC_UA_Aquisition_Cycle/8
          flash_usage_value = flash_usage_value+OPC_UA_Aquisition_Cycle/8

     OPC_UA_tags = st.select_slider(
          'Tags',
          options=[500,1000,1500,2000],
          key = 6,disabled=not OPC_UA)
     if OPC_UA:
          cpu_usage_value=cpu_usage_value+OPC_UA_tags/50
          memory_usage_value = memory_usage_value+OPC_UA_tags/50
          flash_usage_value = flash_usage_value+OPC_UA_tags/50

     with st.sidebar:
          st.header("Resurce:")

          st.metric("CPU", cpu_usage_value/resource[hardware]["cpu"])
          st.metric("Memory", memory_usage_value/resource[hardware]["memory"])
          st.metric("Flash", flash_usage_value/resource[hardware]["flash"])
          if cpu_usage_value/resource[hardware]["cpu"] > 1 or  cpu_usage_value/resource[hardware]["memory"]> 1 or flash_usage_value/resource[hardware]["flash"]>1:
               st.warning("Hardware resource overload! Suggest change a powerful machine!")
