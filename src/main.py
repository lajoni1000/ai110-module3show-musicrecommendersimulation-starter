"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# Phase 4 evaluation profiles. Each entry pairs a display "name" with the
# "prefs" dict that score_song expects (favorite_genre, favorite_mood,
# target_energy, likes_acoustic). Genre/mood values all exist in songs.csv.
PROFILES = [
    {
        "name": "1. High-energy (aligned preferences)",
        "prefs": {"favorite_genre": "edm", "favorite_mood": "uplifting", "target_energy": 0.95, "likes_acoustic": False},
    },
    {
        "name": "2. Low-energy / chill (with acoustic bonus)",
        "prefs": {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.35, "likes_acoustic": True},
    },
    {
        "name": "3. Different genre and mood (r&b / romantic)",
        "prefs": {"favorite_genre": "r&b", "favorite_mood": "romantic", "target_energy": 0.48, "likes_acoustic": False},
    },
    {
        "name": "4a. ADVERSARIAL: conflicting genre vs mood (metal / happy)",
        "prefs": {"favorite_genre": "metal", "favorite_mood": "happy", "target_energy": 0.90, "likes_acoustic": False},
    },
    {
        "name": "4b. EDGE CASE: out-of-range target_energy (1.5)",
        "prefs": {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 1.5, "likes_acoustic": False},
    },
]


def print_recommendations(name: str, prefs: dict, recommendations: list) -> None:
    """Print one profile's heading, preferences, and its top recommendations."""
    # Heading summarizing the profile we searched for
    print()
    print("=" * 60)
    print(f"PROFILE: {name}")
    print("=" * 60)
    print("Profile:")
    print(f"  Favorite Genre: {prefs['favorite_genre']}")
    print(f"  Favorite Mood: {prefs['favorite_mood']}")
    print(f"  Target Energy: {prefs['target_energy']}")
    print(f"  Likes Acoustic: {'YES' if prefs['likes_acoustic'] else 'NO'}")

    # One numbered block per recommendation: title/artist, score, reasons
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  {rank}. {song['title']} - {song['artist']}")
        print(f"     Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"       - {reason}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")  # load the catalog once, reused for every profile

    # Evaluate each profile with the same k and output format
    for profile in PROFILES:
        recommendations = recommend_songs(profile["prefs"], songs, k=5)
        print_recommendations(profile["name"], profile["prefs"], recommendations)


if __name__ == "__main__":
    main()
