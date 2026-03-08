import streamlit as st
import pandas as pd
from io import BytesIO

from utils.metadata import detect_language, extract_entities, detect_country
from utils.translator import translate_text
from utils.sentiment import sentiment_score
from utils.summarizer import summarize_post

st.set_page_config(page_title="Social Media Analysis", layout="wide")

st.title("Social Media Post & Comment Analyzer")

# -----------------------------
# Input
# -----------------------------

st.header("Input Post Data")

url = st.text_input("Post URL")
post_text = st.text_area("Post Text")
comments_text = st.text_area("Comments (one per line)")

# -----------------------------
# Analyze
# -----------------------------

if st.button("Analyze"):
    if not post_text:
        st.warning("Please enter Post Text")
        st.stop()

    # Post metadata
    st.subheader("Post Metadata")

    language = detect_language(post_text)
    countries = detect_country(post_text)
    entities = extract_entities(post_text)
    summary = summarize_post(post_text)

    st.write("Language:", language)
    st.write("Detected Countries:", countries)
    st.write("Entities:", entities)
    st.write("Summary:", summary)

    post_sentiment = sentiment_score(post_text)

    st.write("Post Sentiment:", post_sentiment)

    # -----------------------------
    # Comments analysis
    # -----------------------------

    df_comments = None

    if comments_text.strip():
        st.subheader("Comments Analysis")

        comments_list = [c.strip() for c in comments_text.split("\n") if c.strip()]

        comment_data = []

        for i, comment in enumerate(comments_list, start=1):
            lang = detect_language(comment)

            translation = translate_text(comment) if lang != "en" else comment

            sentiment = sentiment_score(translation)

            countries_comment = detect_country(comment)

            comment_data.append(
                {
                    "Comment #": i,
                    "Original Comment": comment,
                    "Language": lang,
                    "Translation": translation,
                    "Sentiment": sentiment,
                    "Detected Countries": countries_comment,
                }
            )

        df_comments = pd.DataFrame(comment_data)

        st.dataframe(df_comments, use_container_width=True)

    # -----------------------------
    # Download Excel
    # -----------------------------

    st.subheader("Download Results")

    post_data = {
        "URL": url,
        "Post Text": post_text,
        "Language": language,
        "Detected Countries": ", ".join(countries),
        "Entities": ", ".join(entities),
        "Summary": summary,
        "Post Sentiment": post_sentiment,
    }

    df_post = pd.DataFrame([post_data])

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_post.to_excel(writer, sheet_name="Post", index=False)

        if df_comments is not None:
            df_comments.to_excel(writer, sheet_name="Comments", index=False)

    st.download_button(
        label="Download Excel",
        data=output.getvalue(),
        file_name="analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
