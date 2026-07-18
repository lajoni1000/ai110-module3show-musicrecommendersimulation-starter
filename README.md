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

Real-world recommenders like Spotify and TikTok combine **collaborative filtering** (learning from what similar users play, like, and skip) with **content-based filtering** (matching the measurable attributes of the songs themselves), then layer on context like time of day and listening history. My simulation focuses on the **content-based** half: it has no other users' data, so instead of asking "who is like you?" it asks "what is like the music you already enjoy?" It prioritizes matching the *vibe* of a song — its energy and emotional tone — over surface labels, and it aims to stay simple, transparent, and explainable so every recommendation can be traced back to the numbers that produced it.

**Features each `Song` uses:**

- `genre` (categorical) and `mood` (categorical)
- `energy` (numeric, 0–1) — the main "vibe" signal
- `acousticness` (numeric, 0–1) — used when the user likes acoustic music
- `id`, `title`, `artist` are kept for display/identity but not used in scoring
- `valence`, `danceability`, `tempo_bpm` are stored in the data but not scored in this version

**What the `UserProfile` stores:**

- `favorite_genre` — the genre the user prefers
- `favorite_mood` — the mood the user prefers
- `target_energy` — the energy level (0–1) the user is aiming for
- `likes_acoustic` — a flag for whether the user favors acoustic songs

**How the `Recommender` scores a song:** it awards **flat points** for each thing a song gets right, then adds them into one total score:

- **+2.0** for a genre match (exact match on `favorite_genre`)
- **+1.0** for a mood match (exact match on `favorite_mood`)
- **energy similarity** (up to +1.0), computed as `1 − |target_energy − song.energy|`, so the closer the energy, the more points
- **+ acoustic bonus** when `likes_acoustic` is true and the song is highly acoustic

The point values are deliberate: genre counts twice as much as mood, and energy acts as a tie-breaker. Every point awarded is also recorded as a plain-language reason, so each recommendation can be explained back to the user.

**How songs are chosen:** every song in the catalog is scored, the list is sorted by total score descending, and the top-N are returned as the recommendations.

### Data Flow

```
INPUT                    PROCESS                         OUTPUT
─────                    ───────                         ──────
User Prefs      ┐        for each song:                  1. sort by score (desc)
(genre, mood,   ├──────►   score_song(prefs, song)  ───► 2. slice top K
 energy,        │            → (score, reasons)          3. return
 likes_acoustic)│                                           [(song, score, reasons)]
Song Catalog    ┘        collect all scored songs
(songs.csv)
```

Each stage is one function: `load_songs` reads the CSV (no scoring), `score_song` judges a single song in isolation and returns its points plus the reasons for them, and `recommend_songs` runs the loop, sorts, and slices the top K.

### Algorithm Recipe

For each song, `score_song` starts at `score = 0` and an empty `reasons` list, then:

1. **Genre match** — if `song.genre == user.favorite_genre`, add **+2.0** and log `"+2.0 genre match (<genre>)"`.
2. **Mood match** — if `song.mood == user.favorite_mood`, add **+1.0** and log `"+1.0 mood match (<mood>)"`.
3. **Energy similarity** — add `1.0 - abs(user.target_energy - song.energy)` (a value from 0 to 1, higher when energies are close) and log `"+X.XX energy match"`.
4. **Acoustic bonus** — if `user.likes_acoustic` is `True` and `song.acousticness > 0.6`, add **+0.5** and log `"+0.5 acoustic bonus"`.
5. Return `(score, reasons)`.

`recommend_songs` then scores every song, **sorts by total score descending**, and returns the **top K** (default 5). Ties keep catalog order (Python's sort is stable).

**Why these weights:** the point values encode priorities. Genre is worth twice as much as mood (2.0 vs 1.0), so genre is the strongest signal; energy similarity (max 1.0) acts mainly as a tie-breaker between songs that already match on genre; the acoustic bonus is a small nudge, applied only when the user asks for it.

### Potential Biases

- **Genre over-prioritization.** Because genre is the heaviest weight, the system can bury a song that perfectly matches the user's mood and energy just because its genre label differs. A "happy, high-energy" fan might never see a great `indie pop` track because they asked for `pop`.
- **Brittle exact-match labels.** Genre and mood use exact string matching, so `"indie pop"` never matches `"pop"` and `"uplifting"` never matches `"happy"`, even when the songs are musically very similar. Near-misses score zero on those features.
- **Popular-genre echo chamber.** The system only ever reinforces the one genre the user named; it can never surface an adjacent or new genre they might enjoy, which narrows discovery over time.
- **Limited feature use.** `valence`, `danceability`, and `tempo` are ignored in scoring, so two songs with identical genre/mood/energy are treated as interchangeable even if one is far more danceable or emotionally brighter than the other.

---

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



