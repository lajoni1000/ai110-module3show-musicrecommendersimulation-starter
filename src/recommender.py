import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with typed fields."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": row["id"],
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre: strongest signal, worth +2.0
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append(f"+2.0 genre match ({song['genre']})")

    # Mood: worth +1.0
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append(f"+1.0 mood match ({song['mood']})")

    # Energy: similarity from 0 to 1, higher when energies are close
    similarity = 1 - abs(user_prefs["target_energy"] - song["energy"])
    score += similarity
    reasons.append(f"+{similarity:.2f} energy match")

    # Acoustic bonus: only when the user asks for it and the song is highly acoustic
    if user_prefs["likes_acoustic"] and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("+0.5 acoustic bonus")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank by score descending, and return the top k as (song, score, explanation)."""
    results: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if isinstance(reasons, list) else str(reasons)
        results.append((song, score, explanation))

    results.sort(key=lambda result: result[1], reverse=True)
    return results[:k]
