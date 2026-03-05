import streamlit as st
import pandas as pd

from utils.scraper import scrape_post
from utils.translator import translate_text
from utils.sentiment import sentiment_score
from utils.summarizer import summarize_post
from utils.nlp_utils import extract_orgs, detect_country

st.set_page_config(page_title="Social Media Analyzer", layout="wide")

st.title("Social Media Post & Comment Analyzer")

# --- Input Section ---
st.subheader("1️⃣ Input Post URLs")
urls = st.text_area("Enter post URLs (one per line):").splitlines()

st.subheader("2️⃣ Input Comments (optional)")
comments_input = st.text_area("Enter comments (one per line per URL):").splitlines()

# --- Process Button ---
if st.button("Analyze Posts"):
    rows = []
    comment_idx = 0

    for url in urls:
        url = url.strip()
        if not url:
            continue

        post_text = scrape_post(url)
        translated_post = translate_text(post_text)
        country = detect_country(post_text)
        orgs = extract_orgs(post_text)
        post_sent = sentiment_score(post_text)
        summary = summarize_post(post_text)

        # --- Handle comments ---
        comment_text = ""
        comment_translation = ""
        comment_sent = None
        if comment_idx < len(comments_input):
            comment_text = comments_input[comment_idx]
            comment_translation = translate_text(comment_text)
            comment_sent = sentiment_score(comment_text)
            comment_idx += 1

        row = {
            "Post Link": url,
            "Post": post_text,
            "Translated Post": translated_post,
            "Country": country,
            "Org Name": ", ".join(orgs),
            "Post Sentiment": post_sent,
            "Comment": comment_text,
            "Comment Translation": comment_translation,
            "Comment Sentiment": comment_sent,
            "Text Summary": summary,
        }

        rows.append(row)

    df = pd.DataFrame(rows)
    st.dataframe(df)

    # Download as Excel
    st.download_button(
        label="📥 Download Excel",
        data=df.to_excel(index=False, engine="openpyxl"),
        file_name="social_media_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
