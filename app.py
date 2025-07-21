import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

st.markdown("""
    <style>
        /* Base Styles */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
        }
        .stWidgetLabel
        {
        color:#000000;
        }
        .st-emotion-cache-13k62yr{
           background-image: url("https://images.unsplash.com/photo-1720069004713-f72d26684a87?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
           background-size: cover;
           background-repeat: no-repeat;
           background-position: center;
           background-attachment: fixed;
        }
        #sms-spam-classifier
        {
        background-color:#000000;
        }
        /* Text Areas - Now with black text */
        .stTextArea>div>div>textarea {
            color: #000000 !important;  /* Force black text */
            background-color:#F1B3A1 ;
            border: none;
            border-radius: 4px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            min-height: 180px;
            font-size: 44px;
        }
        stTextArea>div>div>textarea::placeholder {
color: #000000 ;
}
textarea[data-testid="stTextArea"] {
font-size: 1px !important;
color: #000 !important;
}

        
        /* Keep all other beautiful styles */
        .main {
            background-size: 400% 400%;
            background-image:url("/Users/vishwanathashrith/Desktop/front/spam sms/img.jpg");
            animation: gradientBG 15s ease infinite;
            padding: 3rem;
            min-height: 100vh;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .st-emotion-cache-qoz3f2 {
  width: 100% !important;
  display: block;
  color:#5C4033;
  font-size:28px;
  text-align: left; /* or center/right based on need */
}
        .st-emotion-cache-seewz2
        {
        background-color:#D72638;
        }
        .st-emotion-cache-kj6hex {
        width: auto;
        position: relative;
        text-align: center;
        }
        .st-emotion-cache-1weic72
        {
        line-height:8;
        font-style:oblique;
        }
        .st-emotion-cache-8atqhb {
        width: 100%;
        line-height: 9;
        }
        t-emotion-cache-qoz3f2 p, .st-emotion-cache-qoz3f2 ol, .st-emotion-cache-qoz3f2 ul, .st-emotion-cache-qoz3f2 dl, .st-emotion-cache-qoz3f2 li {
        font-size: 20px;
        text-align: right;
        }
        .title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-align: center;
            margin-bottom: 2.5rem;
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            animation: gradientShift 8s ease infinite;
            background-size: 200% 200%;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Results - Elegant Cards with Icons */
        .spam-result {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff4757 100%);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            margin: 2rem 0;
            text-align: center;
            font-size: 1.5rem;
            font-weight: 600;
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .spam-result::before {
            content: "⚠️";
            position: absolute;
            font-size: 3rem;
            opacity: 0.15;
            right: 30px;
            top: 20px;
        }
        
        .ham-result {
            background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            margin: 2rem 0;
            text-align: center;
            font-size: 1.5rem;
            font-weight: 600;
            box-shadow: 0 6px 20px rgba(81, 207, 102, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .ham-result::before {
            content: "✓";
            position: absolute;
            font-size: 3rem;
            opacity: 0.15;
            right: 30px;
            top: 20px;
        }
        
        /* Responsive Adjustments */
        @media (max-width: 768px) {
            .main {
                padding: 1.5rem;
            }
            .title {
                font-size: 2rem;
            }
        }
        
        /* Floating Animation for Visual Interest */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
            100% { transform: translateY(0px); }
        }
       st.text_area {
        font-size: 12px;
    }
    .stTextArea label {
    font-size: 28px !important;
    font-weight: bold;
    margin-bottom: 10px;
}
        
        .stButton>button {
            animation: float 3s ease-in-out infinite;
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
st.markdown('<h1 class="title">SMS Spam Classifier  📩 </h1>', unsafe_allow_html=True)

input_sms = st.text_area(" Enter your suspected message here : ", height=150)

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
        st.markdown('<div class="ham-result">Not Spam [Ham] 👍</div>', unsafe_allow_html=True)
        #To run use 
        #streamlit run "/Users/vishwanathashrith/Desktop/front/spam sms/app.py"