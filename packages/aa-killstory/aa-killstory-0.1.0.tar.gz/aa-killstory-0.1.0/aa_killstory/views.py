from django.shortcuts import render

def index(request):
    return render(request, 'aa_killstory/index.html')
