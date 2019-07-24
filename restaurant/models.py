import itertools
from dateutil.parser import parse
'''
defining the Record object
'''


class Records:
    '''
    class to define a record object
    '''
    def __init__(self, id, Name, Amount, Branch, highestInBranch, Timestamp):
        self.id = id
        self.Name = Name
        self.Amount = Amount
        self.Branch = Branch
        self.highestInBranch = highestInBranch
        self.Timestamp = parse(Timestamp)

    @staticmethod
    def sort_by_branch(records):

        def get_branch_name(record):
            return record.Branch

        sorted_list = sorted(records, key=get_branch_name)

        grouped_transactions = itertools.groupby(sorted_list, key=get_branch_name)

        data = []

        for branch, transactions in grouped_transactions:
            data.append({
                'name': branch,
                'transactions': list(transactions)
            })

        return data
