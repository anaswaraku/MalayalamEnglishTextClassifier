import streamlit as st
import pickle
import string

# 1. Load your trained model (assumes it's in the same folder)
@st.cache_resource
def load_model(path="model.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)

model = load_model()

# 2. Set up the UI
st.title("Language Detector: English vs Malayalam vs Digits/Punctuation")
st.write("Paste text below; the model will tell you if it's English, Malayalam, or just digits/punctuation.")

# 3. Get user input
user_input = st.text_area("Enter text to classify:", height=150)

# 4. Handle the button click
if st.button("Classify"):
    if not user_input.strip():
        st.write("Text? Empty input gets no wisdom.")
    elif all(ch in string.digits + string.punctuation for ch in user_input):
        st.write("Prediction: **Digits/Punctuation**")
    else:
        try:
            pred = model.predict([user_input])[0]
            if pred=='eng':
                st.write(f"Prediction: English Language")
            elif pred=='mal':
                st.write(f"Prediction: Malayalam Language")
        except Exception as e:
            st.error("Predict threw an exception—check inputs and model compatibility.")
            st.exception(e)
