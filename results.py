import nltk
from nltk.tokenize import word_tokenize
from nltk import bigrams
from nltk.util import ngrams
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import pickle
import pdb

import pprint

pp = pprint.PrettyPrinter(indent=4)
# pdb.set_trace()

# pickle open and load for full csv
pickle_in = open('company_stats_complete.pickle', 'rb')
company_stats = pickle.load(pickle_in)

companies_with_outbounds_list = []
companies_without_outbounds_list = []
valid_companies = {}
invalid_companies = {}

for company, stats in company_stats.items():
    q_outbounds = stats['amount_of_outbounds']
    if q_outbounds == 0:
        companies_without_outbounds_list.append(company)
        invalid_companies[company] = stats
    elif q_outbounds != 0:
        companies_with_outbounds_list.append(company)
        valid_companies[company] = stats
        c = stats['conservation_of_visitors']
        d = stats['dialogic_loop']
        g = stats['generation_of_return_visits']
        n = stats['amount_of_outbounds']
        i = stats['amount_of_inbounds']
        l = stats['amount_of_conversations']
        frequency_conservation_of_visitors = round(c / n * 100, 1)
        frequency_dialogic_loop = round(d / n * 100, 1)
        frequency_generation_of_return_visits = round(g / n * 100, 1)
        total_number_of_tweets = (n + i)
        average_conversation_length = round((total_number_of_tweets / l), 3)
        stats['frequency_conservation_of_visitors'] = frequency_conservation_of_visitors
        stats['frequency_dialogic_loop'] = frequency_dialogic_loop
        stats['frequency_generation_of_return_visit'] = frequency_generation_of_return_visits
        stats['total_number_of_tweets'] = total_number_of_tweets
        stats['average_conversation_length'] = average_conversation_length

size_companies_without_outbounds = len(companies_without_outbounds_list)
size_companies_with_outbounds = len(companies_with_outbounds_list)

print('companies_without_outbounds_list')
print('length of companies without outbounds:', size_companies_without_outbounds)
pp.pprint(companies_without_outbounds_list)
print()

print('companies_with_outbounds_list')
print('length of companies with outbounds:', size_companies_with_outbounds)
pp.pprint(companies_with_outbounds_list)
print()

print('invalid_companies')
pp.pprint(invalid_companies)
print()

print('valid_companies')
pp.pprint(valid_companies)
print()

# pickle out for companies without outbounds list
pickle_out_companies_without_outbounds_list = open('companies_without_outbounds_list_complete.pickle', 'wb')
pickle.dump(companies_without_outbounds_list, pickle_out_companies_without_outbounds_list)
pickle_out_companies_without_outbounds_list.close()

# pickle out for companies with outbounds list
pickle_out_companies_with_outbounds_list = open('companies_with_outbounds_list_complete.pickle', 'wb')
pickle.dump(companies_with_outbounds_list, pickle_out_companies_with_outbounds_list)
pickle_out_companies_with_outbounds_list.close()

# pickle out for invalid_companies dict
pickle_out_invalid_companies = open('invalid_companies_complete.pickle', 'wb')
pickle.dump(invalid_companies, pickle_out_invalid_companies)
pickle_out_invalid_companies.close()

# pickle out for invalid_companies dict
pickle_out_valid_companies = open('valid_companies_complete.pickle', 'wb')
pickle.dump(valid_companies, pickle_out_valid_companies)
pickle_out_valid_companies.close()

