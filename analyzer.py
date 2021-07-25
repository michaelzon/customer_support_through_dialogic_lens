import nltk
from nltk.tokenize import word_tokenize
from nltk import bigrams
from nltk.util import ngrams
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import pdb
import copy
import pickle

import pprint

pp = pprint.PrettyPrinter(indent=4)


# function for converting string booleans to boolean datatypes
def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'TRUE':
        return True
    elif s == 'False':
        return False
    elif s == 'FALSE':
        return False
    else:
        raise ValueError  # evil ValueError that doesn't tell you what the wrong value was


# Principle 1: dialogic loop
dialogic_loop_unigram_proxies = ['dm', '?']

# Principle 2: usefullness of information
usefulness = SentimentIntensityAnalyzer()

# Principle 3: Generation of return visits
generation_of_return_visits_unigram_proxies = ['https', 'faq', 'f.a.q']
generation_of_return_visits_trigram_proxies = [('frequently', 'asked', 'questions'), ('frequently', 'asked', 'question')]

# Principle 4: Rule of Conservation of Visitors
conservation_of_visitors_proxies = [('follow', 'us'), ('follow', 'our')]

# # pickle open and load for full csv
pickle_in_full_csv = open('entities_complete.pickle', 'rb')
entities = pickle.load(pickle_in_full_csv)
pickle_in_full_csv.close()

company_stats = {}
acc_sentiment = 0
n_tweets = 0

# creating initial dict where every principle frequency is set to zero to avoid creating dicts within conditions
for key, value in entities.items():
    company_name = value['company']
    if company_name not in company_stats:
        company_stats[company_name] = dict(dialogic_loop = 0, usefulness_of_information = 0,
                                           generation_of_return_visits = 0, conservation_of_visitors = 0,
                                           amount_of_outbounds = 0, amount_of_inbounds = 0, accumulated_sentiment = 0,
                                           sentiment_label = '' , amount_of_conversations = 1)
    else:
        company_stats[company_name]['amount_of_conversations'] += 1

# measuring unigram proxies, a thread is a collection of tweets
for key, value in entities.items():
    thread = value['thread']
    company_name = value['company']
    for tweet in thread:
        dialogic_loop_confirmed = False
        generation_of_return_visit_unigram_confirmed = False
        generation_of_return_visit_trigram_confirmed = False
        conservation_of_visitors_confirmed = False
        tweet_text = tweet['text'].lower()
        inbound = str_to_bool(tweet['inbound'])

        # only analyzing outbound tweets for the principles, as those are from companies
        if not inbound:
            company_stats[company_name]['amount_of_outbounds'] += 1
            for word in word_tokenize(tweet_text):
                for proxy_dialogic_loop in dialogic_loop_unigram_proxies:
                    if not dialogic_loop_confirmed:
                        if word == proxy_dialogic_loop:
                            company_stats[company_name]['dialogic_loop'] += 1
                            dialogic_loop_confirmed = True
                        else:
                            continue

                for proxy_return_visit in generation_of_return_visits_unigram_proxies:
                    if not generation_of_return_visit_unigram_confirmed:
                        if word == proxy_return_visit:
                            company_stats[company_name]['generation_of_return_visits'] += 1
                            generation_of_return_visit_unigram_confirmed = True
                        else:
                            continue

            # now creating tuples on text within tweets for two-worded proxies, also known as bigrams
            tokens = word_tokenize(tweet_text)
            tuples = (list(bigrams(tokens)))
            for phrase in tuples:
                for proxy_conservation in conservation_of_visitors_proxies:
                    if not conservation_of_visitors_confirmed:
                        if phrase == proxy_conservation:
                            company_stats[company_name]['conservation_of_visitors'] += 1
                            conservation_of_visitors_confirmed = True
                        else:
                            continue

            # transforming tweet text in three-worded phrases for detection of trigrams
            trigrams = ngrams(tokens, 3)
            for phrase in trigrams:
                for proxy_return_visit in generation_of_return_visits_trigram_proxies:
                    if not generation_of_return_visit_trigram_confirmed:
                        if phrase == proxy_return_visit:
                            company_stats[company_name]['generation_of_return_visits'] += 1
                            generation_of_return_visit_trigram_confirmed = True
                        else:
                            continue

        # generating sentiment score on replies towards companies
        elif inbound:
            company_stats[company_name]['amount_of_inbounds'] += 1
            tweet_sentiment_score = usefulness.polarity_scores(tweet_text)["compound"]
            company_stats[company_name]['accumulated_sentiment'] += tweet_sentiment_score
        else:
            raise ValueError

for company, stats in company_stats.items():
    v = stats['accumulated_sentiment']
    n = stats['amount_of_inbounds']

    # avoid error on dividing by zero
    if n == 0:
        usefulness_score = 0
    else:
        usefulness_score = v/n
    company_stats[company]['usefulness_of_information'] = round(usefulness_score, 3)
    if usefulness_score > 0:
        company_stats[company]['sentiment_label'] = 'POS'
    elif usefulness_score == 0:
        company_stats[company]['sentiment_label'] = 'NEU'
    elif usefulness_score < 0:
        company_stats[company]['sentiment_label'] = 'NEG'

dictionary_company_stats = copy.deepcopy(company_stats)

# for another cleaning program, pickle out for full csv
pickle_out_stats = open('company_stats_complete.pickle', 'wb')
pickle.dump(dictionary_company_stats, pickle_out_stats)
pickle_out_stats.close()

# pp.pprint(entities)
# pp.pprint(company_stats)