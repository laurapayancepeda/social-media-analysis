# app.py
import streamlit as st
import pandas as pd
from utils.metadata import detect_language, extract_entities, detect_country
from utils.translator import translate_text
from utils.sentiment import sentiment_score
from utils.summarizer import summarize_post

st.set_page_config(page_title="Social Media Analysis", layout="wide")

st.title("Social Media Post & Comment Analyzer")

# --- Input Section ---
st.header("Input Post Data")

url = st.text_input("Post URL")
post_text = st.text_area("Post Text")
comments_text = st.text_area("Comments (one per line)")

# --- Process Button ---
if st.button("Analyze"):
    if not url or not post_text:
        st.warning("Please enter a URL and Post Text.")
    else:
        # --- Post Metadata ---
        st.subheader("Post Metadata")
        language = detect_language(post_text)
        countries = detect_country(post_text)
        entities = extract_entities(post_text)
        summary = summarize_post(post_text)

        st.write(f"**Language:** {language}")
        st.write(f"**Detected Countries:** {countries}")
        st.write(f"**Entities (Org Names etc.):** {entities}")
        st.write(f"**Post Summary:** {summary}")

        post_sentiment = sentiment_score(post_text)
        st.write(f"**Post Sentiment:** {post_sentiment}")

        # --- Comments ---
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
            st.dataframe(df_comments)

        # --- Download Option ---
        st.subheader("Download Results")
        all_data = {
            "URL": url,
            "Post Text": post_text,
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
