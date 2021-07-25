import csv
import pickle
import itertools
import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)

pickle_in_companies_without_outbounds_list = open('companies_without_outbounds_list_sample.pickle', 'rb')
companies_without_outbounds_list = pickle.load(pickle_in_companies_without_outbounds_list)
pickle_in_companies_without_outbounds_list.close()

pickle_in_companies_with_outbounds_list = open('companies_with_outbounds_list_sample.pickle', 'rb')
companies_with_outbounds_list = pickle.load(pickle_in_companies_with_outbounds_list)
pickle_in_companies_with_outbounds_list.close()

pickle_in_invalid_companies = open('invalid_companies_sample.pickle', 'rb')
invalid_companies = pickle.load(pickle_in_invalid_companies)
pickle_in_invalid_companies.close()

pickle_in_valid_companies = open('valid_companies_sample.pickle', 'rb')
valid_companies = pickle.load(pickle_in_valid_companies)
pickle_in_valid_companies.close()

fields = ['company']

for key in valid_companies['sprintcare'].keys():
    fields.append(key)

# print(fields)

with open("results_sample.csv", "w", newline='') as f:
    w = csv.DictWriter(f, fields, restval= ' ')
    w.writeheader()
    for k in valid_companies:
        w.writerow({field: valid_companies[k].get(field) or k for field in fields})


# print('valid_companies')
# pp.pprint(valid_companies)
# print()
#
# print('invalid_companies')
# pp.pprint(invalid_companies)
# print()
#
# print(len(companies_without_outbounds_list))
# print(len(companies_with_outbounds_list))
