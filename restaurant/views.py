'''
rendering templates
'''
from django.shortcuts import render
from .models import Records
from .request import get_transactions_records


def home(request):
    '''
    render home template
    '''
    transactions_records = get_transactions_records()
    # ordering = ('Amount')
    sorted_branches = Records.sort_by_branch(transactions_records)
    context = {
        "records": transactions_records,
        "sor": sorted_branches
    }
    return render(request, 'home.html', context)

