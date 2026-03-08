# app.py
import streamlit as st

st.set_page_config(page_title="Social Media Analyzer", layout="wide")

import pandas as pd
from utils.metadata import detect_language, extract_entities, detect_country
from utils.translator import translate_text
from utils.sentiment import sentiment_score
from utils.summarizer import summarize_post
from utils.scraper import scrape_post

st.title("Social Media Post & Comment Analyzer")

# --- Input Section ---
st.header("Input Post Data")
url = st.text_input("Post URL")
post_text = st.text_area("Post Text")
comments_text = st.text_area("Comments (one per line)")

# --- Process Button ---
if st.button("Analyze"):
    if not url and not post_text:
        st.warning("Please enter a URL or Post Text.")
    else:
        # Scrape post if URL is provided but text is empty
        if url and not post_text:
            post_text = scrape_post(url)

        # --- Post Metadata ---
        st.subheader("Post Metadata")
        language = detect_language(post_text)

        # Translate post if not English
        if language != "en":
            post_translated = translate_text(post_text, target="en")
        else:
            post_translated = post_text

        countries = detect_country(post_translated)
        entities = extract_entities(post_translated)  # still returns []
        summary = summarize_post(post_translated)  # full text or first paragraph

        st.write(f"**Original Language:** {language}")
        st.write(f"**Post Text (Translated if needed):** {post_translated}")
        st.write(f"**Detected Countries:** {countries}")
        st.write(f"**Entities:** {entities}")
        st.write(f"**Post Summary:** {summary}")

        post_sentiment = sentiment_score(post_translated)
        st.write(f"**Post Sentiment:** {post_sentiment}")

        # --- Comments Analysis ---
        if comments_text.strip():
            st.subheader("Comments Analysis")
            comments_list = [
                c.strip() for c in comments_text.strip().split("\n") if c.strip()
            ]
            comment_data = []
            for i, comment in enumerate(comments_list, start=1):
                lang = detect_language(comment)
                translation = (
                    translate_text(comment, target="en") if lang != "en" else comment
                )
                sentiment = sentiment_score(translation)
                countries_comment = detect_country(translation)
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
            st.dataframe(df_comments)

        # --- Download Results ---
        st.subheader("Download Results")
        all_data = {
            "URL": url,
            "Post Text": post_translated,
            "Language": language,
            "Detected Countries": ", ".join(countries),
            "Entities": ", ".join(entities),
            "Summary": summary,
            "Post Sentiment": post_sentiment,
        }
        df_post = pd.DataFrame([all_data])

        with pd.ExcelWriter("analysis.xlsx") as writer:
            df_post.to_excel(writer, sheet_name="Post", index=False)
            if comments_text.strip():
                df_comments.to_excel(writer, sheet_name="Comments", index=False)

        st.success("Analysis complete! Excel file saved as 'analysis.xlsx'.")
