# app.py
import streamlit as st
from utils.summarizer import summarize_post
from utils.translator import translate_text
from utils.sentiment import sentiment_score
from utils.metadata import detect_language, extract_entities, detect_country

st.title("Social Media Post Analyzer")

# Input section
st.header("Input Post & Comments")
post_content = st.text_area("Enter Post Content")
comments = st.text_area("Enter Comments (one per line)")

if st.button("Analyze"):
    if post_content.strip() == "":
        st.warning("Please enter post content")
    else:
        st.subheader("Post Analysis")
        st.write("**Original Post:**", post_content)
        st.write("**Language:**", detect_language(post_content))
        st.write("**Entities:**", extract_entities(post_content))
        st.write("**Countries mentioned:**", detect_country(post_content))
        st.write("**Sentiment:**", sentiment_score(post_content))
        st.write("**Summary:**", summarize_post(post_content))

        if comments.strip() != "":
            st.subheader("Comments Analysis")
            for i, c in enumerate(comments.split("\n"), 1):
                st.write(f"Comment {i}: {c}")
                st.write("  - Translation:", translate_text(c))
                st.write("  - Sentiment:", sentiment_score(c))
