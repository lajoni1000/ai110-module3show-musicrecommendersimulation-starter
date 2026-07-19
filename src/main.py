"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    # print(f"Loaded songs: {len(songs)}")   # temporary test to see if songs are loaded correctly
    # Starter example profile
    user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8, "likes_acoustic": False}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Heading summarizing the default profile we searched for
    print()
    print("=" * 60)
    print("TOP MUSIC RECOMMENDATIONS")
    print("=" * 60)
    print("Profile:")
    print(f"  Favorite Genre: {user_prefs['favorite_genre']}")
    print(f"  Favorite Mood: {user_prefs['favorite_mood']}")
    print(f"  Target Energy: {user_prefs['target_energy']}")
    print(f"  Likes Acoustic: {'YES' if user_prefs['likes_acoustic'] else 'NO'}")

    # One numbered block per recommendation: title/artist, score, reasons
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  {rank}. {song['title']} - {song['artist']}")
        print(f"     Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"       - {reason}")

    print()


if __name__ == "__main__":
    main()
