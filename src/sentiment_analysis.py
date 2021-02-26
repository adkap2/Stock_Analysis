from main import *
from vaderSentiment.vaderSentiment.vaderSentiment import *

def get_sent(db):
    """ get_sent(db) -> thread_weights (Dictionary containing each comment
    and the positive/negative weight associated with it)
    takes compounded weight from sentence and if its >= 0.05 considers positive
    and if < -0.05 then negative.
    """
    wsb = db.wsb
    threads = wsb.find({})
    analyzer = SentimentIntensityAnalyzer()
    thread_weights = []
    count = 0
    # Iterate through each thread submission
    for thread in threads:
        count += 1
        pos, neg = 0, 0
        neut = 0
        # Make dictionaries to store data
        compound_dic = {}
        dic_of_compounds = {}
        # Take each sentence from thread and get polarity value fro
        # vader sentiment analyzer
        for sentence, score in thread["comments"]:
            # Takes compound score and categorizes it as postive or negative
            # Based on its value.
            vs = analyzer.polarity_scores(sentence)
            if vs['compound'] >= 0.05:
                pos += 1
            elif vs['compound'] <= -.05:
                neg += 1
            else:
                neut += 1
        # Places total values in dictionary
        compound_dic['positive'] = pos
        compound_dic['negative'] = neg
        compound_dic['neutral'] = neut
        # Adds dictionary of that thread to total dictionary
        dic_of_compounds[thread['thread']] = compound_dic
        thread_weights.append(dic_of_compounds)
    return thread_weights

def count_instances(db):
    """count_instances(db) -> counts (List)
    takes in the data base and counts instances of certain words mentioned
    like GME or gamestop then adds it to a list to be plotted
    """
    # get the wsb database
    wsb = db.wsb
    # get all threads in wsb
    threads = wsb.find({})
    counts = []
    # Iterate through threads and count how many times
    # Each buzzword is used
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
        # Iterate through sentence in threads
        for sentence, score in thread['comments']:
            print(sentence)
            game_stop_count += sentence.lower().split().count(word1)
            game_stop_count += sentence.lower().split().count(word2)
            palantir_count += sentence.lower().split().count(word3)
            palantir_count += sentence.lower().split().count(word4)
            palantir_count += sentence.lower().split().count(word5)
            palantir_count += sentence.lower().split().count(word6)
            palantir_count += sentence.lower().split().count(word7)
        # Appeads total counts of mentions to each counts
        # Taking Palintir values as comparison to GME for sanity checks
        counts.append((game_stop_count, palantir_count))
    return counts
