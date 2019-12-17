import csv
import pickle
import os
from collections import defaultdict
# extract artist genre from artists.csv
# artist_genre = {}
# artist_info = csv.DictReader(open('artists.csv', 'r'))
# genres = set()
# for row in artist_info:
#     print(row)
#     artist_genre[row['name']] = row['genre'].split(',')
#     for g in row['genre'].split(','):
#         genres.add(g)
# print(genres)
# print(len(genres))
# pickle.dump(artist_genre, open('artist_genre', 'wb'))
# pickle.dump(genres, open('genres', 'wb'))

emotions = ["Amusement", "Anger", "Awe", "Content", "Disgust", "Excitement", "Fear", "Sad"]

with open('genres', 'rb') as handle:
    genres = list(pickle.load(handle))
    print(genres)
with open('artist_genre', 'rb') as handle:
    artist_genre = pickle.load(handle)
    print(artist_genre)


listOfGenre_Emotion = []
for g in genres:
    listOfGenre_Emotion.append(defaultdict(list))

with open('combined_scores', 'rb') as handle:
    combined_scores = pickle.load(handle)
    for p, s in combined_scores.items():
        sum4s = s[s > 0].sum()
        s = s.tolist()[0]
        print(sum4s)
        artist = ' '.join(p.rsplit('_', 1)[0].split('_'))
        p_genres = artist_genre[artist]

        for g in p_genres:
            idx = genres.index(g)
            for i in range(len(emotions)):
                if s[i] < 0:
                    score = 0
                else:
                    score = s[i] / float(sum4s)
                listOfGenre_Emotion[idx][emotions[i]].append(score)

    for idx, genre_emotion in enumerate(listOfGenre_Emotion):
        g_e = dict()
        for e, s in genre_emotion.items():
            g_e[e] = sum(s)/len(s)

        pickle.dump(g_e, open('./genre_emotion/' + '_'.join(genres[idx].split(' ')) + '_emotion', 'wb'))

        with open('./genre_emotion/' + '_'.join(genres[idx].split(' ')) + '_emotion', 'rb') as handle:
            genre_emotion = pickle.load(handle)

        with open('./static/genre_emotion/'+'_'.join(genres[idx].split(' ')) + '_scores.csv', 'w') as writeFile:
            writer = csv.DictWriter(writeFile, fieldnames=emotions)
            writer.writeheader()
            writer.writerow(genre_emotion)



