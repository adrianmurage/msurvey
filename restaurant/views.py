'''
rendering templates
'''
from django.shortcuts import render


def home(request):
    '''
    render home template
    '''
    return render(request, 'home.html')
