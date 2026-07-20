"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs
    from agentic import (
        Orchestrator,
        DataAgent,
        RecommenderAgent,
        PolicyAgent,
        EvalAgent,
        HumanReviewAgent,
    )
except ImportError:
    from .recommender import load_songs, recommend_songs
    from .agentic import (
        Orchestrator,
        DataAgent,
        RecommenderAgent,
        PolicyAgent,
        EvalAgent,
        HumanReviewAgent,
    )


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        {
            "name": "Normal pop listener",
            "prefs": {"genre": "pop", "mood": "happy", "energy": 0.80},
        },
        {
            "name": "Nonexistent taste",
            "prefs": {"genre": "death_metal", "mood": "existential", "energy": 0.50},
        },
        {
            "name": "Whitespace/case test",
            "prefs": {"genre": "  POP  ", "mood": "Happy", "energy": 0.80},
        },
        {
            "name": "Minimal profile",
            "prefs": {"energy": 0.00},
        },
        {
            "name": "Extreme energy",
            "prefs": {"genre": "pop", "mood": "happy", "energy": 999.0},
        },
    ]

    print(f"\nLoaded songs: {len(songs)}")

    for profile in profiles:
        user_prefs = profile["prefs"]

        # If orchestrator is available, run through the agentic workflow
        if Orchestrator is not None:
            print("\n[AGENTIC WORKFLOW]")
            orchestrator = Orchestrator(
                agents=[
                    DataAgent(),
                    RecommenderAgent(k=5),
                    PolicyAgent(),
                    EvalAgent(),
                    HumanReviewAgent(threshold=0.6),
                ],
                debug=True,
            )
            result = orchestrator.run({"user_prefs": user_prefs, "songs": songs})
            recommendations = result.get("recommendations", [])
            avg_score = result.get("avg_score")
            sent_to_human = result.get("sent_to_human", False)
        else:
            # fallback: call functional recommender
            recommendations = [
                {"song": s, "score": score, "reasons": reasons}
                for (s, score, reasons) in recommend_songs(user_prefs, songs, k=5)
            ]
            avg_score = None
            sent_to_human = False

        print("\n" + "=" * 60)
        print(f"PROFILE: {profile['name']}")
        print(f"Preferences: {user_prefs}")
        if avg_score is not None:
            print(f"Avg score: {avg_score:.2f}")
        print(f"Sent to human review: {sent_to_human}")
        print("=" * 60)

        for rec in recommendations:
            song = rec.get("song")
            score = rec.get("score", 0.0)
            reasons = rec.get("reasons") or []
            reason_text = "; ".join(reasons) if reasons else "No strong matches"
            print(f"Title  : {song.get('title')}")
            print(f"Artist : {song.get('artist')}")
            print(f"Genre  : {song.get('genre')}")
            print(f"Mood   : {song.get('mood')}")
            print(f"Score  : {score:.2f}")
            print(f"Reasons: {reason_text}")
            print("-" * 50)


if __name__ == "__main__":
    main()
