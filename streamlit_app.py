import streamlit as st
import languages

st.set_page_config(layout="wide")
# # how-to-keep-widget-value-remembered-in-multi-page-app
# for key, val in st.session_state.items():
#     if not key.endswith('__do_not_persist'):
#         st.session_state[key] = val


lang = st.sidebar.selectbox('Languages', list(languages.texts.keys()),key="languages",label_visibility="hidden")
st.session_state["current_text"] = languages.texts[lang]
current_text = st.session_state.current_text

st.header(current_text["UI_HPConfig_0"])
st.caption(current_text["UI_CPConfig_1"])
st.caption(current_text["UI_CPConfig_2"])
st.caption(current_text["UI_CPConfig_3"])
st.caption(current_text["UI_CPConfig_4"])

st.header(current_text["UI_HMapping_0"])
st.caption(current_text["UI_COMapping_1"])
st.caption(current_text["UI_COMapping_2"])
st.caption(current_text["UI_COMapping_3"])
st.caption(current_text["UI_COMapping_4"])
st.caption(current_text["UI_COMapping_5"])


# st.divider()


