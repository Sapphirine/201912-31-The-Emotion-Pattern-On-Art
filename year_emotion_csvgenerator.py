import pickle
import os
import csv
from collections import defaultdict
# PREPROCESSING YEAR_EMOTION CSV
emotions = ["Amusement", "Anger", "Awe", "Content", "Disgust", "Excitement", "Fear", "Sad"]

# extract artist year from artists.csv
# artist_year = {}
# artist_info = csv.DictReader(open('artists.csv', 'r'))
# for row in artist_info:
#     print(row)
#     artist_year[row['name']] = row['years']
# # print(artist_year)
# pickle.dump(artist_year, open("artist_year", "wb"))

with open('artist_year', 'rb') as handle:
    artist_years = pickle.load(handle)
    print(artist_years)


directory = './model_results'
combined_scores = dict()
for sub_foldername in os.listdir(directory):
    print(sub_foldername)
    with open(directory+'/'+sub_foldername, 'rb') as handle:
        x = pickle.load(handle)
        combined_scores.update(x)
pickle.dump(combined_scores, open('combined_scores', "wb"))


with open('combined_scores', 'rb') as handle:
    combined_scores = pickle.load(handle)
    # listOfYear_Emotion = [defaultdict(list)]
    listOfYear_Emotion = [defaultdict(list), defaultdict(list),
                          defaultdict(list), defaultdict(list),
                          defaultdict(list), defaultdict(list),
                          defaultdict(list), defaultdict(list)]

    for p, s in combined_scores.items():
        print(p)
        sum4s = s[s > 0].sum()
        s = s.tolist()[0]
        print(sum4s)
        artist = ' '.join(p.rsplit('_', 1)[0].split('_'))
        year_range = [int(artist_years[artist][0:4]), int(artist_years[artist][-4:])]
        print(year_range)
        year_mid = int((year_range[0]+year_range[1])/2)
        print('year mid', year_mid)

        for i in range(len(emotions)):
            if s[i] < 0:
                score = 0
            else:
                score = s[i] / float(sum4s)
            listOfYear_Emotion[i][year_mid].append(score)
            #print(listOfYear_Emotion)

    for idx, y_e in enumerate(listOfYear_Emotion):
        d1 = defaultdict(float)
        d2 = defaultdict(float)
        d3 = defaultdict(float)
        for y, e in y_e.items():
            d1[y] = sum(e)/len(e)
            d2[y] = max(e)
            d3[y] = min(e)
        pickle.dump(d1, open('./year_emotion/'+'year_'+emotions[idx], 'wb'))
        pickle.dump(d2, open('./year_emotion/'+'year_'+emotions[idx]+'_max', 'wb'))
        pickle.dump(d3, open('./year_emotion/'+'year_'+emotions[idx]+'_min', 'wb'))

for e in emotions:
    with open('./year_emotion/'+'year_'+e, 'rb') as handle:
        year_emotion = pickle.load(handle)
        # print(year_Amusement)
    with open('./year_emotion/'+'year_'+e+'_max', 'rb') as handle:
        year_emotion_max = pickle.load(handle)
        # print(year_Amusement)
    with open('./year_emotion/'+'year_'+e+'_min', 'rb') as handle:
        year_emotion_min = pickle.load(handle)
        # print(year_Amusement)
    with open('year_'+e+'_scores.csv', 'w') as writeFile:
        writer = csv.DictWriter(writeFile, fieldnames=['year', 'avg', 'max', 'min'])
        writer.writeheader()
        for year, score in year_emotion.items():
            writer.writerow({'year': year, 'avg':score, 'max': year_emotion_max[year], 'min': year_emotion_min[year]})
