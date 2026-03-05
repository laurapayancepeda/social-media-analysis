# utils/summarizer.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load model & tokenizer explicitly
model_name = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Use text2text-generation pipeline (works in all recent transformers)
summarizer = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1,  # CPU, set 0 if you have GPU
)


def summarize_post(text, max_length=130, min_length=30):
    """
    Summarize a single text post
    """
    if not text or not isinstance(text, str):
        return ""
    result = summarizer(
        text, max_length=max_length, min_length=min_length, do_sample=False
    )
    return result[0]["generated_text"]
