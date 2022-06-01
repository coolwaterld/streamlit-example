import streamlit as st
st.header("Configuration:")
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
     bytes_data = uploaded_file.read()
     st.write("filename:", uploaded_file.name)
     st.write(bytes_data)

st.header("Hardware type:")
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
hardware = st.radio("Which hardware do you want to deploy the applications?",('IEVD', 'IPC 127E', 'IPC 227E', 'IPC 427E', 'IPC 847E'))

resource = {"IEVD":{"cpu":100,"memory":100,"flash":100},
"IPC 127E":{"cpu":200,"memory":200,"flash":200},
"IPC 227E":{"cpu":300,"memory":300,"flash":300},
"IPC 427E":{"cpu":400,"memory":400,"flash":400},
"IPC 847E":{"cpu":500,"memory":500,"flash":500}
}


cpu_usage_value = 50
memory_usage_value = 50
flash_usage_value = 50
st.header("Resurce:")
st.write('cpu usage:')
cpu_usage_percent = st.progress(cpu_usage_value/resource[hardware]["cpu"])
st.write('memory usage:')
memory_usage_percent = st.progress(memory_usage_value/resource[hardware]["memory"])
st.write('flash usage:')
flash_usage_percent = st.progress(flash_usage_value/resource[hardware]["flash"])


st.header("Application:")
Optimized_S7 = st.checkbox('Optimized S7')
Optimized_S7_Connections = st.selectbox(
     'Connections?',
     (1,8),key=1)
Optimized_S7_Aquisition_Cycle = st.selectbox(
     'Aquisition Cycle?',
     (100,500),
     key=2)
Optimized_S7_tags = st.select_slider(
     'Tags',
     options=[600,800,1000,1200,1400,1600,1800,2000],
     key=3)

OPC_UA = st.checkbox('OPC UA')
OPC_UA_Connections = st.selectbox(
     'Connections?',
     (1,8),
     key=4)
OPC_UA_Aquisition_Cycle = st.selectbox(
     'Aquisition Cycle?',
     (100,500),
     key=5)
OPC_UA_tags = st.select_slider(
     'Tags',
     options=[600,800,1000,1200,1400,1600,1800,2000],key = 6)

# col1, col2, col3 , col4, col5= st.columns(5)

# with col1:
    
#     st.button('IEVD')

# with col2:
#     st.image("https://www.distec.co.uk/wp-content/uploads/2019/11/Siemens-SIMATIC-IPC127E-480x395.jpg")
#     st.button('IPC 127E')

# with col3:
#     st.image("https://www.distec.co.uk/wp-content/uploads/2019/11/Siemens-SIMATIC-IPC227E-480x395.jpg")
#     st.button('IPC 227E')
# with col4:
#     st.image("https://www.distec.co.uk/wp-content/uploads/2019/11/Siemens-SIMATIC-IPC427E-480x395.jpg")
#     st.button('IPC 427E')
# with col5:
#     st.image("https://www.distec.co.uk/wp-content/uploads/2019/11/Siemens-SIMATIC-IPC847E-480x395.jpg")
#     st.button('IPC 847E')