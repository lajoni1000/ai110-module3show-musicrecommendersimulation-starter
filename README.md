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

3. Run the app (from the project root):

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

.venv) PS C:\Users\hanny\OneDrive\Documentos\Foundations of AI Engineering\ai110-module3show-musicrecommendersimulation-starter> python -m src.main                                                    

============================================================
PROFILE: 1. High-energy (aligned preferences)
============================================================
Profile:
  Favorite Genre: edm
  Favorite Mood: uplifting
  Target Energy: 0.95
  Likes Acoustic: NO

  1. Voltage Rising - Pulsewave
     Score: 4.00
       - +2.0 genre match (edm)
       - +1.0 mood match (uplifting)
       - +1.00 energy match

  2. Gym Hero - Max Pulse
     Score: 0.98
       - +0.98 energy match

  3. Iron Verdict - Ashen Crown
     Score: 0.97
       - +0.97 energy match

  4. Storm Runner - Voltline
     Score: 0.96
       - +0.96 energy match

  5. Midnight Circuit - Bassline Ghost
     Score: 0.95
       - +0.95 energy match


============================================================
PROFILE: 2. Low-energy / chill (with acoustic bonus)
============================================================
Profile:
  Favorite Genre: lofi
  Favorite Mood: chill
  Target Energy: 0.35
  Likes Acoustic: YES

  1. Library Rain - Paper Lanterns
     Score: 4.50
       - +2.0 genre match (lofi)
       - +1.0 mood match (chill)
       - +1.00 energy match
       - +0.5 acoustic bonus

  2. Midnight Coding - LoRoom
     Score: 4.43
       - +2.0 genre match (lofi)
       - +1.0 mood match (chill)
       - +0.93 energy match
       - +0.5 acoustic bonus

  3. Focus Flow - LoRoom
     Score: 3.45
       - +2.0 genre match (lofi)
       - +0.95 energy match
       - +0.5 acoustic bonus

  4. Spacewalk Thoughts - Orbit Bloom
     Score: 2.43
       - +1.0 mood match (chill)
       - +0.93 energy match
       - +0.5 acoustic bonus

  5. Coffee Shop Stories - Slow Stereo
     Score: 1.48
       - +0.98 energy match
       - +0.5 acoustic bonus


============================================================
PROFILE: 3. Different genre and mood (r&b / romantic)
============================================================
Profile:
  Favorite Genre: r&b
  Favorite Mood: romantic
  Target Energy: 0.48
  Likes Acoustic: NO

  1. Velvet Hours - Silk Avenue
     Score: 4.00
       - +2.0 genre match (r&b)
       - +1.0 mood match (romantic)
       - +1.00 energy match

  2. Dust and Diesel - Red Clay Road
     Score: 0.96
       - +0.96 energy match

  3. Midnight Coding - LoRoom
     Score: 0.94
       - +0.94 energy match

  4. Focus Flow - LoRoom
     Score: 0.92
       - +0.92 energy match

  5. Island Time - Palm Riddim
     Score: 0.92
       - +0.92 energy match


============================================================
PROFILE: 4a. ADVERSARIAL: conflicting genre vs mood (metal / happy)
============================================================
Profile:
  Favorite Genre: metal
  Favorite Mood: happy
  Target Energy: 0.9
  Likes Acoustic: NO

  1. Iron Verdict - Ashen Crown
     Score: 2.92
       - +2.0 genre match (metal)
       - +0.92 energy match

  2. Sunrise City - Neon Echo
     Score: 1.92
       - +1.0 mood match (happy)
       - +0.92 energy match

  3. Rooftop Lights - Indigo Parade
     Score: 1.86
       - +1.0 mood match (happy)
       - +0.86 energy match

  4. Midnight Circuit - Bassline Ghost
     Score: 1.00
       - +1.00 energy match

  5. Storm Runner - Voltline
     Score: 0.99
       - +0.99 energy match


============================================================
PROFILE: 4b. EDGE CASE: out-of-range target_energy (1.5)
============================================================
Profile:
  Favorite Genre: pop
  Favorite Mood: happy
  Target Energy: 1.5
  Likes Acoustic: NO

  1. Sunrise City - Neon Echo
     Score: 3.32
       - +2.0 genre match (pop)
       - +1.0 mood match (happy)
       - +0.32 energy match

  2. Gym Hero - Max Pulse
     Score: 2.43
       - +2.0 genre match (pop)
       - +0.43 energy match

  3. Rooftop Lights - Indigo Parade
     Score: 1.26
       - +1.0 mood match (happy)
       - +0.26 energy match

  4. Iron Verdict - Ashen Crown
     Score: 0.48
       - +0.48 energy match

  5. Voltage Rising - Pulsewave
     Score: 0.45
       - +0.45 energy match
---

## Experiments You Tried

### Experiment 1: Weight Shift

To evaluate how sensitive the recommender was to different scoring weights, I temporarily changed the scoring algorithm in `recommender.py`.

**Original weights:**
- Genre match: +2.0
- Mood match: +1.0
- Energy similarity: up to +1.0
- Acoustic bonus: +0.5

**Experimental weights:**
- Genre match: +1.0
- Mood match: +1.0
- Energy similarity: up to +2.0
- Acoustic bonus: +0.5

#### Results

The experiment showed that increasing the importance of energy made songs with similar energy levels much more competitive, even if they did not match the requested genre.

For example, in the **High-Energy EDM** profile, the top recommendation ("Voltage Rising") remained the same because it perfectly matched the user's genre, mood, and energy preferences. However, songs that matched only the target energy nearly doubled their scores, moving much closer to the top recommendation.

The biggest change occurred in the **Metal / Happy** adversarial profile. Before the experiment, the metal song ranked clearly above the happy pop song because genre was weighted twice as much as mood. After reducing the genre weight and increasing the energy weight, both songs received the same overall score (2.84), showing that the recommender became much more sensitive to energy similarity.

### Behavior for Different User Types

The recommender behaved differently depending on the user's preferences:

- **High-Energy EDM:** Recommended energetic EDM songs first, with other high-energy songs following.
- **Low-Energy Lofi:** Favored calm, acoustic songs that matched the requested genre and mood.
- **R&B Romantic:** Found one perfect match, then recommended songs with similar energy because there were fewer songs matching both the requested genre and mood.
- **Conflicting Metal/Happy:** Demonstrated how changing the scoring weights affected the balance between genre and mood.
- **Edge Case (Energy = 1.5):** The recommender still produced recommendations even though the energy value was outside the expected range (0.0–1.0), revealing that the current implementation does not validate user input.

### Conclusion

The experiment demonstrated that the recommender is sensitive to feature weights. Increasing the influence of energy changed the ranking of several songs and made energy-only matches more competitive. However, the changes made the recommendations different rather than clearly more accurate. This experiment helped illustrate how weighting decisions affect recommendation behavior.

---

## Limitations and Risks

## Limitations and Risks

- Recommendations are limited to the songs available in the dataset.
- The model only considers genre, mood, energy, and acoustic preference.
- Some genres and mood combinations are underrepresented.
- The scoring system gives more weight to genre, which may overpower other user preferences in some cases.
- The current implementation does not validate user inputs (for example, an energy value outside the expected 0.0–1.0 range), which may produce unreliable recommendations.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



