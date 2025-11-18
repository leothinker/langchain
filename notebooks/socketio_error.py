import socketio
import streamlit as st

if 'some_boolean' not in st.session_state:
    st.session_state.some_boolean = True
if 'some_param' not in st.session_state:
    st.session_state.some_param = 50

sio = socketio.Client()
sio.connect('http://localhost:5000')


@sio.event
def connect():
    if st.session_state.some_boolean:
        st.session_state.some_param = 10
