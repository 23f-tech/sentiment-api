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


happy_words = {
    "love", "loved", "like", "liked", "great", "excellent", "amazing",
    "awesome", "fantastic", "wonderful", "good", "best", "happy",
    "glad", "joy", "joyful", "perfect", "positive", "enjoy",
    "enjoyed", "satisfied", "success", "brilliant", "nice",
    "beautiful", "thanks", "thank", "helpful", "excited",
    "excellent", "cool", "fun", "win", "winner", "pleased"
}

sad_words = {
    "sad", "bad", "terrible", "awful", "horrible", "hate", "hated",
    "angry", "upset", "disappointed", "disappointing", "poor",
    "worst", "pain", "hurt", "cry", "failed", "fail", "failure",
    "problem", "issue", "broken", "wrong", "negative", "unhappy",
    "annoyed", "frustrated", "delay", "delayed", "loss", "lost",
    "sorry", "regret", "boring", "useless", "disaster", "rude"
}


def classify_sentiment(sentence: str) -> str:
    text = sentence.lower()
    words = re.findall(r"[a-z']+", text)

    happy_score = sum(1 for word in words if word in happy_words)
    sad_score = sum(1 for word in words if word in sad_words)

    happy_phrases = [
        "well done",
        "very good",
        "so good",
        "really good",
        "works well",
        "love this",
        "thank you",
        "i am happy",
        "i'm happy",
        "i feel good",
        "made my day",
        "great job"
    ]

    sad_phrases = [
        "not good",
        "very bad",
        "so bad",
        "really bad",
        "does not work",
        "did not work",
        "doesn't work",
        "too slow",
        "waste of time",
        "i am sad",
        "i'm sad",
        "i feel bad",
        "let me down"
    ]

    for phrase in happy_phrases:
        if phrase in text:
            happy_score += 2

    for phrase in sad_phrases:
        if phrase in text:
            sad_score += 2

    if happy_score > sad_score:
        return "happy"

    if sad_score > happy_score:
        return "sad"

    return "neutral"


@app.post("/sentiment")
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


@app.post("/")
async def sentiment_analysis_root(request: SentimentRequest):
    return await sentiment_analysis(request)


@app.get("/")
async def root():
    return {"message": "Sentiment API is running"}