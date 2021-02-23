from main import *

def get_sent(db):
    wsb = db.wsb
    #thread1 = wsb.find_one({'thread': 'Daily Discussion Thread for February 19, 2021'})
    #thread = wsb.find_one({"thread" : "Daily Discussion Thread for February 22, 2021"})
    thread1 = wsb.find_one({"thread": "Daily Discussion Thread for February 19, 2021"})
    pprint.pprint(thread1)
    analyzer = SentimentIntensityAnalyzer()
    compound = 0
    compound_dic = {}
    dic_of_componds = {}
    pos = 0
    neg = 0
    neut = 0
    for sentence, score in thread1["comments"]:
        vs = analyzer.polarity_scores(sentence)
        if vs['compound'] >= 0.05:
            pos += 1
        elif vs['compound'] <= -.05:
            neg += 1
        else:
            neut += 1
        compound += vs['compound']
    compound_dic['positive'] = pos
    compound_dic['negative'] = neg
    compound_dic['neutral'] = neut
    dic_of_componds["Daily Discussion Thread for February 19, 2021"] = compound_dic
    #print("{:-<65} {}".format(sentence, thread['vs']))
    return dic_of_componds

def count_instances(db):
    wsb = db.wsb

    thread0 = wsb.find_one({"thread" : "Daily Discussion Thread for February 22, 2021"})

    thread = wsb.find_one({"thread": "Daily Discussion Thread for February 19, 2021"})
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
        #print(sentence)
        game_stop_count += sentence.lower().split().count(word1)
        game_stop_count += sentence.lower().split().count(word2)
        palantir_count += sentence.lower().split().count(word3)
        palantir_count += sentence.lower().split().count(word4)
        palantir_count += sentence.lower().split().count(word5)
        palantir_count += sentence.lower().split().count(word6)
        palantir_count += sentence.lower().split().count(word7)
    return (game_stop_count, palantir_count)
