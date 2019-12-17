import csv
import pickle
from collections import defaultdict
import os
emotions = ["Amusement", "Anger", "Awe", "Content", "Disgust", "Excitement", "Fear", "Sad"]

# PREPROCESSING ARTIST_EMOTION CSV
artist_name = []
artist_info = csv.DictReader(open('artists.csv', 'r'))
for row in artist_info:
    artist_name.append('_'.join(row['name'].split(' ')))

pickle.dump(artist_name, open('artist_names', 'wb'))

with open('artist_names', 'rb') as handle:
    artist_names = pickle.load(handle)
    print(artist_names)

# for name in artist_names:
directory = "./model_results"

# combined_scores = dict()
# for name in os.listdir(directory):
#     # with open(directory + '/' + name + '_emotion', 'rb') as handle:
#     #     x = pickle.load(handle)
#     #     print(x)
#     artist_emotion = defaultdict(list)
#     with open(directory+'/'+name, 'rb') as handle:
#         artist_score = pickle.load(handle)
#         for p, s in artist_score.items():
#             sum4s = s[s > 0].sum()
#             s = s.tolist()[0]
#             for i in range(len(emotions)):
#                 if s[i] < 0:
#                     score = 0
#                 else:
#                     score = s[i] / float(sum4s)
#                 artist_emotion[emotions[i]].append(score)
#     a_e = dict()
#     for a, e in artist_emotion.items():
#         a_e[a] = sum(e)/len(e)
#     pickle.dump(a_e, open('./artist_emotion/'+name+'_emotion', 'wb'))
#
#     with open('./artist_emotion/' + name + '_emotion', 'rb') as handle:
#         artist_emotion = pickle.load(handle)
#
#     with open('./static/artist_emotion/'+name + '_scores.csv', 'w') as writeFile:
#         writer = csv.DictWriter(writeFile, fieldnames=emotions)
#         writer.writeheader()
#         writer.writerow(artist_emotion)


