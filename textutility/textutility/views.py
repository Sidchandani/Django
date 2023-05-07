# This file is creted by Sid
# "python manage.py runserver " RUN THIS WHERE manage.py lives
# "python -m django startproject textutility" TO START A NEW PROJECT
# "python manage.py startapp shop " To Create a app inside a project 
# https://www.codewithharry.com/videos/python-django-tutorials-hindi-0/


from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')
    
    # return HttpResponse("Home")

def basic(request):
    return render(request, 'basic.html')
    
def about(request):
    return render(request, 'about.html')
    

def analyze(request):
    #Get the text
    djtext = request.GET.get('text', 'default')

    # Check checkbox values
    removepunc = request.GET.get('removepunc', 'off')
    fullcaps = request.GET.get('fullcaps', 'off')
    newlineremover = request.GET.get('newlineremover', 'off')
    extraspaceremover = request.GET.get('extraspaceremover', 'off')
    perform=False


    #Check which checkbox is on
    if removepunc == "on":
        analyzed = ""
        perform=True
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char
        params = {'purpose':'Removed Punctuations', 'analyzed_text': analyzed}


    if(fullcaps=="on"):
        if perform:
            djtext=analyzed

        analyzed = ""
        perform=True

        for char in djtext:
            analyzed = analyzed + char.upper()


        params = {'purpose': 'Changed to Uppercase', 'analyzed_text': analyzed}

    if(extraspaceremover=="on"):

        if perform:
            djtext=analyzed

        analyzed = ""
        perform=True
            
        for index, char in enumerate(djtext):
            try:
                if not(djtext[index] == " " and djtext[index+1]==" "):
                    analyzed = analyzed + char
            except IndexError:  # DUE TO INDEX+1 
                pass

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        


    if (newlineremover == "on"):
        if perform:
            djtext=analyzed

        analyzed = ""
        perform=True
            
        for char in djtext:
            if char != "\n":
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}

    if perform :
        return render(request, 'analyze.html', params)
    else:
        return HttpResponse("<h1>Error</h1>")

# def capfirst(request):
#     return HttpResponse("capitalize first")

# def newlineremove(request):
#     return HttpResponse("newline remove first")

# def spaceremove(request):
#     return HttpResponse("space remover back")

# def charcount(request):
#     return HttpResponse("charcount ")


