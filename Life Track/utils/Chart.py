from transformers import pipeline

summarizer = pipeline("summarization")

def generate_daily_summary(data):
    text = f"""
    On {data['date']}, you were at {data['location']} doing {data['activity']}.
    You listened to {', '.join(data['genres'])} music.
    The weather was {data['weather']}.
    You met with {', '.join(data['people'])}.
    You felt {data['mood']}.
    """

    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']
