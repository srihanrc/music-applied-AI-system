"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nLoaded songs: {len(songs)}")
    print("Top recommendations:\n")

    for song, score, reasons in recommendations:
        reason_text = "; ".join(reasons) if reasons else "No strong matches"
        print(f"Title  : {song['title']}")
        print(f"Artist : {song['artist']}")
        print(f"Genre  : {song['genre']}")
        print(f"Mood   : {song['mood']}")
        print(f"Score  : {score:.2f}")
        print(f"Reasons: {reason_text}")
        print("-" * 50)


if __name__ == "__main__":
    main()
