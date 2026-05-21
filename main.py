from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SentimentRequest(BaseModel):
    sentences: List[str]


class SentimentResult(BaseModel):
    sentence: str
    sentiment: str


class SentimentResponse(BaseModel):
    results: List[SentimentResult]


happy_words = {
    "love", "loved", "like", "liked", "great", "excellent", "amazing",
    "awesome", "fantastic", "wonderful", "good", "best", "happy",
    "glad", "joy", "joyful", "delight", "delighted", "perfect",
    "positive", "enjoy", "enjoyed", "satisfied", "success", "win",
    "brilliant", "nice", "beautiful", "thank", "thanks", "helpful"
}

sad_words = {
    "sad", "bad", "terrible", "awful", "horrible", "hate", "hated",
    "angry", "upset", "disappointed", "disappointing", "poor",
    "worst", "pain", "hurt", "cry", "crying", "failed", "fail",
    "failure", "problem", "issue", "broken", "wrong", "negative",
    "unhappy", "annoyed", "frustrated", "delay", "delayed", "loss",
    "lost", "sorry", "regret", "boring", "useless"
}


def classify_sentiment(sentence: str) -> str:
    text = sentence.lower()
    words = re.findall(r"[a-z']+", text)

    happy_score = sum(1 for word in words if word in happy_words)
    sad_score = sum(1 for word in words if word in sad_words)

    # Extra phrase handling
    happy_phrases = [
        "well done", "very good", "so good", "really good",
        "works well", "love this", "thank you"
    ]

    sad_phrases = [
        "not good", "very bad", "so bad", "really bad",
        "does not work", "did not work", "too slow", "waste of time"
    ]

    for phrase in happy_phrases:
        if phrase in text:
            happy_score += 2

    for phrase in sad_phrases:
        if phrase in text:
            sad_score += 2

    if happy_score > sad_score:
        return "happy"
    elif sad_score > happy_score:
        return "sad"
    else:
        return "neutral"


@app.post("/sentiment", response_model=SentimentResponse)
async def sentiment_analysis(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": classify_sentiment(sentence)
            }
            for sentence in request.sentences
        ]
    }


@app.get("/")
async def root():
    return {"message": "Sentiment API is running"}