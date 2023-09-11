import streamlit as st

# Path to the image on your computer
image = "/Users/anton/Desktop/School/AI/Untitled/tictactoe/square.png"  # Replace with the actual path to your image

st.title("Tic Tac Toe")

st.button("X", key="button1")

st.button(" ", key="button2")

if(st.button.key=="button2"):
    print("error")






