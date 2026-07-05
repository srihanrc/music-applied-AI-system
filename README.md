# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Real world recommendations work by combining user behavior like the songs they listen to, whether they skip or save the song.This also looks at the mood of the song lyrics the user likes and gives song recommendations of the same mood. This relies on different features like genre and even the artist that the user likes to listen to. My version will prioritize using features genre, mood, energy, tempo_bpm, valence, danceability and acousticness to predict a user's preferred music type

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

The first step Input collects the user's profile like favorite genres, moods, and energy music they prefer. Then for each song in the CSV dataset, this will compare all the songs with the user's preferences and each song will get scored based on how well it matches the user's profile. After scoring every song, the system sorts the scores from greatest to lowest and returns the top scores for user recommendations. For the "Algorithmic Recipe" the system will prioritize the genre song's than any of the other features.


## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```
Loading songs from data/songs.csv...

Loaded songs: 19
Top recommendations:

Title  : Sunrise City
Artist : Neon Echo
Genre  : pop
Mood   : happy
Score  : 5.94
Reasons: genre match +2; mood match +1; energy closeness +2.94
--------------------------------------------------
Title  : Gym Hero
Artist : Max Pulse
Genre  : pop
Mood   : intense
Score  : 4.61
Reasons: genre match +2; energy closeness +2.61
--------------------------------------------------
Title  : Rooftop Lights
Artist : Indigo Parade
Genre  : indie pop
Mood   : happy
Score  : 3.88
Reasons: mood match +1; energy closeness +2.88
--------------------------------------------------
Title  : Night Drive Loop
Artist : Neon Echo
Genre  : synthwave
Mood   : moody
Score  : 2.85
Reasons: energy closeness +2.85
--------------------------------------------------
Title  : Midnight Cipher
Artist : Neon Rhymes
Genre  : hip hop
Mood   : hype
Score  : 2.76
Reasons: energy closeness +2.76
--------------------------------------------------

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



