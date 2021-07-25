import csv
import pdb
import copy
import pickle

import pprint

pp = pprint.PrettyPrinter(indent=4)

entities = {}

key = str
company = str
customer = str
thread = list

company_name = str
customer_name = str


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

with open('sheets/sample.csv') as f:
    dict_reader = csv.DictReader(f)
    for tweet in dict_reader:

        # the author is a communicator who sends a tweet
        author = tweet['author_id'].replace('_', '').lower()
        text = tweet['text'].lower()

        # converting to boolean data types to check if something is from consumer
        inbound = str_to_bool(tweet['inbound'])

        if not inbound:

            # using the @-tag within the tweet to see to which consumer the company replies
            for word in text.split(' '):
                if '@' in word:

                    # slice the @-symbol from the string and use part of the key for entities dict (company_customer)
                    sliced_customer_name = word[1:]
                    sliced_customer_name = sliced_customer_name.replace('_', '')
                    if sliced_customer_name.isdigit():
                        customer_name: str = sliced_customer_name
                        # print(customer_name)

                        # creating temporary key to check if it already exists in dictionary
                        temp_key = author + '_' + customer_name
                        if temp_key in entities:
                            entities[temp_key]['thread'].append(tweet)

                        # otherwise the new customer - company combination key is added plus the tweet
                        else:
                            key = temp_key
                            entities[key] = dict(company=author, customer=customer_name, thread=[tweet])

                    # break statement so unnecessary word iterations on tweet are avoided (when word does not have '@')
                    break

        # similar code for inbound tweets
        elif inbound:
            for word in text.split(' '):
                if '@' in word:

                    # avoid keys with un-alphabetical characters, customers place a ! behind mention within tweet
                    sliced_company_name = word[1:]
                    sliced_company_name = sliced_company_name.replace('_', '')
                    sliced_company_name = sliced_company_name.replace(',', '')
                    sliced_company_name = sliced_company_name.replace('!', '')
                    sliced_company_name = sliced_company_name.replace('.', '')

                    # check if the string contains only alphabetical letters, if so it is directed to a known company
                    if sliced_company_name.isalpha() or sliced_company_name == 'o2':
                        company_name = sliced_company_name.lower()
                        inbound_temp_key = company_name + '_' + author

                        # if the company - customer key combination exists within entity dict then just add tweet
                        if inbound_temp_key in entities:
                            entities[inbound_temp_key]['thread'].append(tweet)

                        else:
                            key = inbound_temp_key
                            entities[key] = dict(company=company_name, customer=author, thread=[tweet])

                    break

        # check if tweet is neither inbound or outbound for accuracy
        else:
            raise ValueError

dictionary_entities = copy.deepcopy(entities)

# pickle out for full csv
pickle_out = open('entities_sample.pickle', 'wb')

pickle.dump(dictionary_entities, pickle_out)

pickle_out.close()

# pp.pprint(entities)



