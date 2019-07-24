'''
file to handle api requests
'''
import urllib.request
import json
import itertools
from django.conf import settings
from .models import Records


API_KEY = settings.API_KEY

TRANSACTIONS_RECORDS_URL = 'https://api.airtable.com/v0/appJwxwGl1jmkbUXG/Transactions?api_key={}'


def get_transactions_records():
    '''
    get the records in json format
    '''
    get_transaction_records_url = TRANSACTIONS_RECORDS_URL.format(API_KEY)

    with urllib.request.urlopen(get_transaction_records_url) as url:

        transactions_records_data = url.read()
        transactions_records_response = json.loads(transactions_records_data)
        # print(sorted(transactions_records_response, key = lambda i: i['records']['fields]['Amount'], reverse=True))

        transactions_records_results = None

        if transactions_records_response['records']:
            transactions_records_results_list = transactions_records_response['records']
            transactions_records_results = process_transaction_records_results(transactions_records_results_list)
    return transactions_records_results


def process_transaction_records_results(transactions_records_results_list):
    '''
    function to process the json data obtained
    that is stored in the transactions_records_results_list
    '''
    transactions_records_results = []

    def get_branch_name(record):
        '''
        function to get branch names
        '''
        return record['fields']['Branch']

    def get_amount(record):
        '''
        function to get transaction amounts
        '''
        return record['fields']['Amount']

    sorted_list = sorted(transactions_records_results_list, key=get_branch_name)

    grouped_transactions = itertools.groupby(sorted_list, key=get_branch_name)

    for branch, transactions in grouped_transactions:
        t = list(transactions)
        highest = max(t, key=get_amount)

        highest['fields']['isHighest'] = True

    for transactions_records_item in transactions_records_results_list:

        id = transactions_records_item.get('id')
        Name = transactions_records_item.get('fields').get('Name')
        Amount = transactions_records_item.get('fields').get('Amount')
        Branch = transactions_records_item.get('fields').get('Branch')
        highestInBranch = transactions_records_item.get('fields').get('isHighest', False)
        Timestamp = transactions_records_item.get('fields').get('Timestamp')

        transactions_records_object = Records(id, Name, Amount, Branch, highestInBranch, Timestamp)
        transactions_records_results.append(transactions_records_object)

    return transactions_records_results
