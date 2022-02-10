import streamlit as st
import graphviz as graphviz
import json
import test_schema


def draw_dataflow(task_seq):
    if task_seq is not None:
        graph = graphviz.Digraph()
        for task_index in range(len(task_seq)):
            task = task_seq[task_index]
            origin = task["origin"]
            if len(origin)>0:
                if isinstance (origin,list):
                    for origin_index in range(len(origin)):
                         graph.edge(origin[origin_index], task["id"],task["name"])
                else:
                    graph.edge(origin, task["id"],task["name"])
            else:
                if "source" in task["features"].keys():
                    graph.node(str(task["features"]["source"]),shape='box')
                    graph.edge(str(task["features"]["source"]), task["id"],task["name"])
                         
        st.graphviz_chart(graph)
            

st.header("Use Case to Data Flow")
usecase_file = st.uploaded_file = st.file_uploader("Choose a Use Case JSON file")
col1, col2 = st.columns(2)
if usecase_file is not None:
    usecase_str = usecase_file.read().decode("utf-8")
    with col1:
        usecase_dict = json.loads(usecase_str)
        #todo: json schema validate
        schema = test_schema.get_schema("./joe_schema.json")
        is_valid, msg = test_schema.validate_json(schema,usecase_dict)
        if is_valid:
            task_sequence = usecase_dict["usecase"]["task_sequence"]
            st.json(task_sequence)
        else:
            st.error("Given JSON data is InValid")
            st.error(msg)
        
        
    with col2:    
        draw_dataflow(task_sequence)
