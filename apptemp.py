import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

# Custom CSS styling
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stTextArea>div>div>textarea {
            background-color: #ffffff;
            border: 1px solid #ced4da;
            border-radius: 5px;
            padding: 10px;
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #357abd;
            transform: scale(1.02);
        }
        .title {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .spam-result {
            background-color: #ff6b6b;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
        .ham-result {
            background-color: #51cf66;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Load models
with open('/Users/vishwanathashrith/Desktop/front/spam sms/vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

with open('/Users/vishwanathashrith/Desktop/front/spam sms/model.pkl', 'rb') as f:
    model = pickle.load(f)

# App layout
st.markdown('<h1 class="title">Email/SMS Spam Classifier</h1>', unsafe_allow_html=True)

input_sms = st.text_area("Enter the message", height=150)

if st.button('Predict'):
    # 1. preprocess
    transformed_sms = transform_text(input_sms)
    # 2. vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. Display
    if result == 1:
        st.markdown('<div class="spam-result">Spam Alert! 🚨</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ham-result">Not Spam (Ham) 👍</div>', unsafe_allow_html=True)