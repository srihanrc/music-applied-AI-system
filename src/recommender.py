from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from operator import itemgetter
import csv

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
        # Score each song against the user profile and return top-k songs
        scored: List[Tuple[Song, float, List[str]]] = []
        for song in self.songs:
            score, reasons = score_song_obj(user, song)
            scored.append((song, score, reasons))

        scored.sort(key=lambda t: t[1], reverse=True)
        return [t[0] for t in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song_obj(user, song)
        if reasons:
            return "; ".join(reasons)
        return "No strong matches found"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    print(f"Loading songs from {csv_path}...")
    with open(csv_path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # convert numeric fields
            try:
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row.get('energy', 0.0)),
                    'tempo_bpm': float(row.get('tempo_bpm', 0.0)),
                    'valence': float(row.get('valence', 0.0)),
                    'danceability': float(row.get('danceability', 0.0)),
                    'acousticness': float(row.get('acousticness', 0.0)),
                }
            except Exception:
                # skip malformed rows
                continue
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # Genre match: +2 points for exact match
    user_genre = user_prefs.get('genre')
    if user_genre and isinstance(song.get('genre'), str):
        if user_genre.strip().lower() == song['genre'].strip().lower():
            score += 2.0
            reasons.append('genre match +2')

    # Mood match: +1 point for exact match
    user_mood = user_prefs.get('mood')
    if user_mood and isinstance(song.get('mood'), str):
        if user_mood.strip().lower() == song['mood'].strip().lower():
            score += 1.0
            reasons.append('mood match +1')

    # Energy similarity: award up to 3 points based on closeness (energy in [0,1])
    target_energy = user_prefs.get('energy') or user_prefs.get('target_energy')
    if target_energy is not None:
        try:
            song_energy = float(song.get('energy', 0.0))
            diff = abs(song_energy - float(target_energy))
            closeness = max(0.0, 1.0 - diff)  # 1.0 means identical
            energy_points = closeness * 3.0
            score += energy_points
            reasons.append(f'energy closeness +{energy_points:.2f}')
        except Exception:
            pass

    return score, reasons


def score_song_obj(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Helper scoring function that accepts dataclass objects used in tests."""
    user_prefs = {
        'genre': user.favorite_genre,
        'mood': user.favorite_mood,
        'target_energy': user.target_energy,
    }
    # convert Song dataclass to dict-like access expected by score_song
    song_dict = {
        'id': song.id,
        'title': song.title,
        'artist': song.artist,
        'genre': song.genre,
        'mood': song.mood,
        'energy': song.energy,
        'tempo_bpm': song.tempo_bpm,
        'valence': song.valence,
        'danceability': song.danceability,
        'acousticness': song.acousticness,
    }
    return score_song(user_prefs, song_dict)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    return sorted(scored, key=itemgetter(1), reverse=True)[:k]
