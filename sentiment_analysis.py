from main import *
from vaderSentiment.vaderSentiment.vaderSentiment import *

def get_sent(db):
    wsb = db.wsb
    threads = wsb.find({})
    analyzer = SentimentIntensityAnalyzer()
    thread_weights = []
    count = 0
    for thread in threads:
        count += 1
        pos, neg = 0, 0
        neut = 0
        compound_dic = {}
        dic_of_compounds = {}
        for sentence, score in thread["comments"]:
            vs = analyzer.polarity_scores(sentence)
            if vs['compound'] >= 0.05:
                pos += 1
            elif vs['compound'] <= -.05:
                neg += 1
            else:
                neut += 1
        compound_dic['positive'] = pos
        compound_dic['negative'] = neg
        compound_dic['neutral'] = neut
        dic_of_compounds[thread['thread']] = compound_dic
        thread_weights.append(dic_of_compounds)
    return thread_weights

def count_instances(db):
    wsb = db.wsb
    threads = wsb.find({})
    counts = []
    for thread in threads:
        game_stop_count = 0
        palantir_count = 0
        word1 = "gme"
        word2 = "gamestop"
        word3 = "pltr"
        word4 = "palantir"
        word5 = "$pltr"
        word6 = "🚀"
        word7 = "moon"
        for sentence, score in thread['comments']:
            print(sentence)
            game_stop_count += sentence.lower().split().count(word1)
            game_stop_count += sentence.lower().split().count(word2)
            palantir_count += sentence.lower().split().count(word3)
            palantir_count += sentence.lower().split().count(word4)
            palantir_count += sentence.lower().split().count(word5)
            palantir_count += sentence.lower().split().count(word6)
            palantir_count += sentence.lower().split().count(word7)
        counts.append((game_stop_count, palantir_count))
    return counts
