# app.py
import streamlit as st
from utils.summarizer import summarize_post
from utils.translator import translate_text
from utils.sentiment import sentiment_score

st.set_page_config(page_title="Social Media Analyzer", layout="wide")
st.title("Social Media Post & Comment Analyzer")

# --- Input Section ---
st.header("Input URL or Text")
url = st.text_input("Post URL (optional)")
post_text = st.text_area("Or paste the post text here")

# --- Comments Section ---
st.header("Comments")
comments_input = st.text_area("Paste comments here, one per line")

# --- Process Button ---
if st.button("Analyze"):
    if url:
        st.info(f"Processing URL: {url}")

    # Summarize post
    summary = summarize_post(post_text) if post_text else ""
    st.subheader("Post Summary")
    st.write(summary)

    # Translate post
    translated_post = translate_text(post_text)
    st.subheader("Translated Post")
    st.write(translated_post)

    # Sentiment of post
    post_sentiment = sentiment_score(post_text)
    st.subheader("Post Sentiment")
    st.write(post_sentiment)

    # Process comments
    if comments_input.strip():
        st.subheader("Comments Analysis")
        comments_list = comments_input.strip().split("\n")
        results = []
        for c in comments_list:
            translated_c = translate_text(c)
            sentiment_c = sentiment_score(c)
            results.append(
                {"Comment": c, "Translated": translated_c, "Sentiment": sentiment_c}
            )
        st.table(results)
