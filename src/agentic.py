from typing import Any, Dict, List, Optional
import json
import os

try:
    from recommender import recommend_songs
except ImportError:
    from .recommender import recommend_songs


class Agent:
    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class DataAgent(Agent):
    """Prepares and normalizes input state for downstream agents."""

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # ensure songs and user_prefs present
        state.setdefault("songs", state.get("songs", []))
        state.setdefault("user_prefs", state.get("user_prefs", {}))
        return {}


class RecommenderAgent(Agent):
    """Calls the existing recommender logic and attaches recommendations."""

    def __init__(self, k: int = 5):
        self.k = k

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        user_prefs = state.get("user_prefs", {})
        songs = state.get("songs", [])
        scored = recommend_songs(user_prefs, songs, k=self.k)
        # scored is List[Tuple[song_dict, score, reasons]]
        recs = [
            {"song": s, "score": float(score), "reasons": reasons}
            for (s, score, reasons) in scored
        ]
        return {"recommendations": recs}


class PolicyAgent(Agent):
    """Applies simple filtering / business rules."""

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        recs = state.get("recommendations", [])
        # Example policy: remove songs with missing title
        filtered = [r for r in recs if r.get("song", {}).get("title")]
        return {"recommendations": filtered}


class EvalAgent(Agent):
    """Computes basic metrics (average score) used to decide human review."""

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        recs = state.get("recommendations", [])
        if not recs:
            return {"avg_score": 0.0}
        avg = sum(r.get("score", 0.0) for r in recs) / len(recs)
        return {"avg_score": avg}


class HumanReviewAgent(Agent):
    """Sends low-confidence or flagged recommendations to a human review queue."""

    def __init__(self, queue_path: Optional[str] = None, threshold: float = 0.5):
        self.threshold = threshold
        self.queue_path = queue_path or os.path.join("data", "human_review_queue.jsonl")
        os.makedirs(os.path.dirname(self.queue_path), exist_ok=True)

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        avg = state.get("avg_score", 1.0)
        if avg < self.threshold:
            payload = {
                "user_prefs": state.get("user_prefs"),
                "recommendations": state.get("recommendations", []),
                "avg_score": avg,
            }
            with open(self.queue_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(payload) + "\n")
            return {"sent_to_human": True}
        return {"sent_to_human": False}


class Orchestrator:
    def __init__(self, agents: List[Agent], human_threshold: float = 0.5, debug: bool = False):
        self.agents = agents
        self.human_threshold = human_threshold
        self.debug = debug

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        state = dict(context)
        for i, agent in enumerate(self.agents, 1):
            agent_name = agent.__class__.__name__
            if self.debug:
                print(f"  Step {i}: Running {agent_name}...")
            out = agent.act(state)
            if out:
                state.update(out)
                if self.debug:
                    # Show what this agent added/changed
                    for key, value in out.items():
                        if key == "recommendations":
                            print(f"    → Generated {len(value)} recommendations")
                        elif key == "avg_score":
                            print(f"    → Average score: {value:.2f}")
                        elif key == "sent_to_human":
                            print(f"    → Sent to human review: {value}")
                        else:
                            print(f"    → {key}")
        return state
