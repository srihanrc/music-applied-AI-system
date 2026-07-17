import json
import os

QUEUE_PATH = os.path.join("data", "human_review_queue.jsonl")
RESULTS_PATH = os.path.join("data", "human_review_results.jsonl")


def review_queue():
    if not os.path.exists(QUEUE_PATH):
        print("No human-review queue was found.")
        return

    with open(QUEUE_PATH, "r", encoding="utf-8") as file:
        items = [
            json.loads(line)
            for line in file
            if line.strip()
        ]

    if not items:
        print("No recommendations are waiting for review.")
        return

    remaining_items = []

    for number, item in enumerate(items, start=1):
        print("\n" + "=" * 60)
        print(f"Review item {number}")
        print(f"User preferences: {item.get('user_prefs')}")
        print(f"Average score: {item.get('avg_score', 0):.2f}")
        print("\nRecommendations:")

        for recommendation in item.get("recommendations", []):
            song = recommendation.get("song", {})

            print(
                f"- {song.get('title', 'Unknown title')} "
                f"by {song.get('artist', 'Unknown artist')}"
            )
            print(f"  Score: {recommendation.get('score', 0):.2f}")
            print(f"  Reasons: {recommendation.get('reasons', [])}")

        decision = input(
            "\nEnter approve, reject, or skip: "
        ).strip().lower()

        if decision == "skip":
            remaining_items.append(item)
            continue

        if decision not in {"approve", "reject"}:
            print("Invalid decision. Keeping this item in the queue.")
            remaining_items.append(item)
            continue

        comments = input("Enter optional comments: ").strip()

        review_result = {
            **item,
            "human_decision": decision,
            "human_comments": comments,
        }

        with open(RESULTS_PATH, "a", encoding="utf-8") as file:
            file.write(json.dumps(review_result) + "\n")

        print(f"Recommendation set marked as {decision}.")

    # Keep only skipped or unreviewed items in the queue
    with open(QUEUE_PATH, "w", encoding="utf-8") as file:
        for item in remaining_items:
            file.write(json.dumps(item) + "\n")

    print("\nHuman review completed.")


if __name__ == "__main__":
    review_queue()