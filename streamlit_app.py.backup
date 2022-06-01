from re import L
import streamlit as st
import graphviz as graphviz
import json
import test_schema
import os

def get_example_usecases():
    file_list=[]
    for root,dirs,files in os.walk(r"./input"):
        file_list.extend(files)
    return file_list

print(get_example_usecases())
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
            if "features" in task.keys() and "source" in task["features"].keys():
                graph.node(str(task["features"]["source"]),shape='box')
                graph.edge(str(task["features"]["source"]), task["id"],task["name"])
            if "features" in task.keys() and "target" in task["features"].keys():
                graph.node(str(task["features"]["target"]),shape='box')
                graph.edge(task["id"],str(task["features"]["target"]))
                         
        st.graphviz_chart(graph)
            

st.header("Use Case to Data Flow")
usecase_file = st.file_uploader("choose a local use case JSON file")
file_name = st.selectbox("or use example use cases",options=get_example_usecases(),index=0)

usecase_str =""
if usecase_file is not None:
    usecase_str = usecase_file.read().decode("utf-8")

if usecase_file is None and file_name is not None:
    with open('./input/'+file_name, 'r') as f:
        usecase_str = f.read()

col1, col2 = st.columns(2)
if usecase_str is not None:
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