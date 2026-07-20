# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **PlaylistPilot 1.0**  

---

## 2. Intended Use  

PlaylistPilot 1.0 is designed to recommend songs from a small music catalog based on a user's preferences. It generates content-based recommendations by comparing the user's favorite genre, favorite mood, target energy level, and acoustic preference with the characteristics of each song in the dataset.

The recommender assumes that users know their own preferences and provide valid inputs. It also assumes that the available dataset contains enough songs matching those preferences. Since the system only recommends songs already in its catalog, it cannot suggest music outside the dataset or learn from a user's listening history.

This recommender was developed as a classroom project to demonstrate how a simple content-based recommendation system works. It is intended for learning and experimentation rather than for real-world music streaming or personalized commercial recommendations.

---

## 3. How the Model Works  

The recommender compares each song in the dataset to the user's preferences and gives the song a score based on how well it matches.

It looks at four main features of each song:

- Genre
- Mood
- Energy level
- Whether the song is acoustic

The user provides their favorite genre, favorite mood, preferred energy level, and whether they prefer acoustic music.

Songs that match the user's favorite genre receive the most points because genre is the strongest preference in the scoring system. Songs that also match the user's preferred mood receive additional points. The recommender then checks how close each song's energy level is to the user's target energy. Songs with a similar energy level receive a higher score. Finally, if the user prefers acoustic music, acoustic songs receive a small bonus.

After every song receives a score, the recommender ranks the songs from highest to lowest and returns the top recommendations along with a short explanation of why each song was selected.

Compared to the starter project, I implemented a complete weighted scoring system that considers multiple song features instead of relying on a single characteristic. I also added human-readable explanations for each recommendation and tested how changing the scoring weights affected the recommendations during the evaluation phase.

---

## 4. Data  

The recommender uses a catalog of 20 songs stored in a CSV file. Each song includes information such as the title, artist, genre, mood, energy level, and whether it is acoustic. These features are used by the recommender to compare songs with a user's preferences.

The dataset includes a variety of genres and moods, including pop, EDM, lofi, rock, metal, R&B, country, and reggae. The moods represented include happy, uplifting, chill, romantic, intense, and others, providing enough variety to test different user profiles.

As part of this project, I expanded the starter dataset by adding 10 additional songs. 

Although the dataset covers several musical styles, it is still relatively small and cannot represent the full diversity of musical tastes. 

---

## 5. Strengths  

The recommender performed well when the user's preferences matched songs that were well represented in the dataset. For example, the **High-Energy EDM** and **Low-Energy Lofi** profiles consistently received recommendations that matched the requested genre, mood, and energy level. 

The scoring system also captured the importance of combining multiple features instead of relying on only one. The explanations generated for each recommendation made it easy to understand why a song was selected.

Overall, the recommendations matched my intuition when there were several songs in the dataset that closely matched the user's preferences. 

---

## 6. Limitations and Bias 

Although the recommender works well for many user profiles, it has several limitations.

First, it only considers four song features: genre, mood, energy level, and whether a song is acoustic. It does not consider other characteristics.

The system also lacks input validation. During testing, I intentionally used an invalid energy value (1.5), even though the expected range is 0.0 to 1.0. Instead of rejecting the input or displaying an error message, the recommender still generated recommendations. This showed that the model assumes users always provide valid inputs and would benefit from input validation to improve reliability.

The dataset is also relatively small, so some genres and mood combinations have only one or two matching songs. During testing, the **R&B Romantic** profile found one excellent match, but the remaining recommendations were chosen mostly because they had similar energy levels. This shows that some musical styles are underrepresented in the dataset.

Another limitation is that the scoring system gives the highest weight to genre. During the **Metal / Happy** test, the recommender preferred a metal song over happy songs because the genre match was worth more points than the mood match. This demonstrates that the model can overemphasize one preference even when another preference may be equally important to the user.

Finally, users whose preferences closely match the available songs receive better recommendations than users whose tastes are less represented in the dataset. This means the recommender may unintentionally favor users with common genres or moods while providing less diverse recommendations for users with less represented preferences.

---

## 7. Evaluation  

### Which user profiles I tested

I evaluated the recommender using five different user profiles:

- High-Energy EDM
- Low-Energy Lofi (with acoustic preference)
- R&B Romantic
- Metal / Happy (adversarial profile with conflicting preferences)
- Edge Case (invalid target energy of 1.5)

These profiles were chosen to test different genres, moods, energy levels, and unusual inputs.

### What I looked for in the recommendations

For each profile, I checked whether the top recommendations matched the requested genre, mood, and energy level. I also looked for whether the recommendations changed appropriately when different user preferences were provided and whether the explanation for each recommendation matched the scoring logic.

### What surprised me

The biggest surprise was how much the genre weight influenced the recommendations. For the Metal / Happy profile, the recommender ranked a metal song above happy songs because the genre bonus was larger than the mood bonus.

I was also surprised that the recommender accepted an invalid energy value (1.5) and still generated recommendations instead of validating the input.

### Simple tests and comparisons

I performed a weight-shift experiment by reducing the genre bonus from **+2.0** to **+1.0** and increasing the maximum energy contribution from **+1.0** to **+2.0**.

I then ran the same user profiles again and compared the new recommendations with the original results.

The experiment showed that songs with similar energy levels became much more competitive. The strongest recommendations generally stayed the same, but the rankings became less dependent on genre and more influenced by energy similarity. This demonstrated that the recommender is sensitive to changes in the scoring weights.

---

## 8. Future Work  

There are several ways this recommender could be improved in the future. First, I would add more song features, such as tempo, danceability, valence, release year, language, and popularity, to better represent different aspects of musical taste. I would also implement input validation to ensure users provide valid values, such as keeping the energy preference within the expected range.

Another improvement would be to generate more detailed explanations for each recommendation, helping users understand exactly why a song was selected. To improve diversity, the recommender could avoid returning several songs with very similar characteristics and instead include a wider variety of recommendations that still match the user's preferences.

Finally, I would like to support more complex user tastes by allowing users to rank the importance of different preferences or select multiple favorite genres and moods. Incorporating user feedback or listening history could also make recommendations more personalized over time.
---

## 9. Personal Reflection  

This project helped me understand how content-based recommender systems use weighted features to compare items with a user's preferences. I learned that even a simple scoring algorithm can produce useful recommendations when the available data is well organized.

One thing that surprised me was how much the scoring weights influenced the final recommendations. During the weight experiment, I saw that changing the importance of genre and energy could noticeably change the ranking of songs, especially for users with mixed preferences.

This project also changed the way I think about music recommendation apps. I realized that recommendations are not simply based on finding similar songs—they are the result of many design decisions, such as which features are considered, how much each feature matters, and how the system balances accuracy, diversity, and fairness.
