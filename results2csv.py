import csv
import pickle
import itertools
import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)

pickle_in_companies_without_outbounds_list = open('companies_without_outbounds_list_complete.pickle', 'rb')
companies_without_outbounds_list = pickle.load(pickle_in_companies_without_outbounds_list)
pickle_in_companies_without_outbounds_list.close()

pickle_in_companies_with_outbounds_list = open('companies_with_outbounds_list_complete.pickle', 'rb')
companies_with_outbounds_list = pickle.load(pickle_in_companies_with_outbounds_list)
pickle_in_companies_with_outbounds_list.close()

pickle_in_invalid_companies = open('invalid_companies_complete.pickle', 'rb')
invalid_companies = pickle.load(pickle_in_invalid_companies)
pickle_in_invalid_companies.close()

pickle_in_valid_companies = open('valid_companies_complete.pickle', 'rb')
valid_companies = pickle.load(pickle_in_valid_companies)
pickle_in_valid_companies.close()

fields = ['company']

# specificing for sprintcare as that is the first key in the dict
for key in valid_companies['sprintcare'].keys():
    fields.append(key)

# print(fields)

with open("results_final.csv", "w", newline='') as f:
    w = csv.DictWriter(f, fields)
    w.writeheader()
    for k in valid_companies:
        w.writerow({field: valid_companies[k].get(field) or k for field in fields})

