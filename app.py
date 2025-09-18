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
st.write("Paste text below; the app will detect if it's English, Malayalam, or just digits/punctuation.")

# Helper: check if text contains Malayalam characters
def has_malayalam(text):
    return any('\u0D00' <= ch <= '\u0D7F' for ch in text)

# 3. Get user input
user_input = st.text_area("Enter text to classify:", height=150)

# 4. Handle the button click
if st.button("Classify"):
    text = user_input.strip()
    if not text:
        st.write("⚠️ Empty input.")
    elif all(ch in string.digits + string.punctuation for ch in text):
        st.write("Prediction: **Digits/Punctuation**")
    elif has_malayalam(text):
        st.write("Prediction: **Malayalam Language**")
    else:
        try:
            # For English or mixed Latin, rely on model
            pred = model.predict([text])[0]
            if pred == 'eng':
                st.write("Prediction: **English Language**")
            elif pred == 'mal':
                st.write("Prediction: **Malayalam Language** (model-based)")
            else:
                st.write(f"Prediction: **{pred}** (from model)")
        except Exception as e:
            st.error("Predict threw an exception—check inputs and model compatibility.")
            st.exception(e)
