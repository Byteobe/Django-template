from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>It worked!</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
            }
        </style>
    </head>
    <body>
        <h1>It worked!</h1>
    </body>
    </html>
    '''
    return HttpResponse(html_content)