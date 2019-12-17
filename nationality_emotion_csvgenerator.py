import csv
import pickle
import os
from collections import defaultdict
# extract artist nationality from artists.csv
# artist_nationality = {}
# artist_info = csv.DictReader(open('artists.csv', 'r'))
# nationality = set()
# for row in artist_info:
#     print(row)
#     artist_nationality[row['name']] = row['nationality'].split(',')
#     for g in row['nationality'].split(','):
#         nationality.add(g)
# print(nationality)
# print(len(nationality))
# print(artist_nationality)
# pickle.dump(artist_nationality, open('artist_nationality', 'wb'))
# pickle.dump(nationality, open('nationality', 'wb'))


emotions = ["Amusement", "Anger", "Awe", "Content", "Disgust", "Excitement", "Fear", "Sad"]

with open('nationality', 'rb') as handle:
    nationality = list(pickle.load(handle))
    print(nationality)
with open('artist_nationality', 'rb') as handle:
    artist_nationality = pickle.load(handle)
    print(artist_nationality)


listOfNationality_Emotion = []
for e in emotions:
    listOfNationality_Emotion.append(defaultdict(list))

with open('combined_scores', 'rb') as handle:
    combined_scores = pickle.load(handle)
    for p, s in combined_scores.items():
        sum4s = s[s > 0].sum()
        s = s.tolist()[0]
        artist = ' '.join(p.rsplit('_', 1)[0].split('_'))
        p_nationality = artist_nationality[artist]

        for n in p_nationality:
            for i in range(len(emotions)):
                if s[i] < 0:
                    score = 0
                else:
                    score = s[i] / float(sum4s)
                listOfNationality_Emotion[i][n].append(score)

    for idx, nationality_emotion in enumerate(listOfNationality_Emotion):
        n_e = dict()
        for n, s in nationality_emotion.items():
            n_e[n] = sum(s) / len(s)

        pickle.dump(n_e, open('./nationality_emotion/' + 'nationality_' + emotions[idx], 'wb'))
        with open('./nationality_emotion/' + 'nationality_' + emotions[idx], 'rb') as handle:
            nationality_emotion = pickle.load(handle)

        with open('./static/nationality_emotion/'+'nationality_' + emotions[idx] + '_scores.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(['Nationality', 'Value'])
            for n, e in nationality_emotion.items():
                writer.writerow([n, e])
