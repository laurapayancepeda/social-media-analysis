# utils/summarizer.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Model
model_name = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Use text-generation pipeline
summarizer = pipeline(
    "text-generation",  # use text-generation instead of text2text-generation
    model=model,
    tokenizer=tokenizer,
    device=-1,  # CPU
)


def summarize_post(text, max_length=130, min_length=30):
    if not text or not isinstance(text, str):
        return ""
    # Generate summary using text-generation
    result = summarizer(
        text,
        max_length=max_length,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
    )
    # The generated text is in result[0]['generated_text']
    return result[0]["generated_text"]
