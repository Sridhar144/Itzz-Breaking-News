from django.shortcuts import render, HttpResponse
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline
from .ml_functions import manual_testing

# Create your views here.
from joblib import load


random_forest = load('C:/Users/Admin/Desktop/Web_Develop/NewsOrion/Notebooks/News-predictor.joblib')

def predictor(request):
    if request.method == 'POST':
        text = request.POST['text']
        # Perform required tasks with the text input
        # ...
        # text=float(text)
        # print(type(text))
        # predictions, q,w,e = manual_testing(text)

        predictions, pred_lr, pred_dt, pred_rfc  = manual_testing(text)
        print(pred_lr[0], pred_dt[0], pred_rfc[0])
        ans=0
        if pred_lr[0]:
            ans+=1
        if predictions[0]:
            ans+=1
        if pred_dt[0]:
            ans+=1
        if pred_rfc[0]:
            ans+=1
        if ans==4:
            background_color='#00FF00'
        elif ans == 3:
            background_color = '#ff5555' 
        
        elif ans==2:
            background_color='#0000FF'
            
        elif ans==1:
            background_color='#FFFF00'
        else: 
            background_color='#55aa55'
        # pred_rf=random_forest.predict([text])
        if predictions[0]==1:
            if ans>=2:
                print(f"success Your output for {text} news is Not a Fake news by gradientboost mainly!")
                return render(request, 'news_predictor_output.html', {'conf':ans,'confp':ans*25,'news':'Real', 'background':background_color, 'text':text})
            return render(request, 'news_predictor_output.html', {'conf':ans,'confp':0,'news':'Fake', 'background':'#FFFFFF', 'text':text})
            # return HttpResponse("success Your output for {text} news is Not a Fake news, confidence score is {ans}/4!!")
        elif pred_rfc[0]==1:
            # if ans>=2:
            
            print(f"success Your output for {text} news is Not a Fake news by randomforest mainly")
            return render(request, 'news_predictor_output.html', {'conf':ans,'confp':ans*25,'news':'Real', 'background':background_color, 'text':text})
            return render(request, 'news_predictor_output.html', {'conf':ans,'confp':0,'news':'Fake', 'background':'#FFFFFF', 'text':text})
            # return HttpResponse("success Your output for {text} news is Not a Fake news, confidence score is {ans}/4!!")
        elif pred_dt[0]==1:
            # if ans>=2:
            
            print(f"success Your output for {text} news is Not a Fake news by decision tree ainly")
            return render(request, 'news_predictor_output.html', {'conf':ans,'confp':ans*25,'news':'Real', 'background':background_color, 'text':text})
            return render(request, 'news_predictor_output.html', {'conf':ans,'confp':0,'news':'Fake', 'background':'#FFFFFF', 'text':text})
            # return HttpResponse("success Your output for {text} news is Not a Fake news, confidence score is {ans}/4!!")
        elif pred_lr[0]==1:
            if ans>=2:
            
                print(f"success Your output for {text} news is Not a Fake news by linear regression mainly!")
                return render(request, 'news_predictor_output.html', {'conf':ans,'confp':ans*25,'news':'Real', 'background':background_color, 'text':text})
            return render(request, 'news_predictor_output.html', {'conf':ans,'confp':0,'news':'Fake', 'background':'#FFFFFF', 'text':text})
            # return HttpResponse("success Your output for {text} news is Not a Fake news, confidence score is {ans}/4!!")
        else:
            print(f"success Your output for {text} news is Fake news")
            # return HttpResponse("success Your output for {text} news is Fake news")
            return render(request, 'news_predictor_output.html', {'conf':ans,'confp':ans*25,'news':'Fake', 'background':background_color, 'text':text})
    return render(request, 'news/news_predictor.html')


# def predictor_output(request):
    

def scrape(request, name):
    Headline.objects.all().delete()
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = f"https://www.theonion.com/{name}"
    content = session.get(url).content
    soup = BSoup(content, "html.parser")

    News = soup.find_all("div", {"class": "sc-cw4lnv-13 hHSpAQ"})

    for article in News:
        main = article.find_all("a", href=True)

        linkx = article.find("a", {"class": "sc-1out364-0 dPMosf js_link"})
        link = linkx["href"]

        titlex = article.find("h2", {"class": "sc-759qgu-0 cvZkKd sc-cw4lnv-6 TLSoz"})
        title = titlex.text

        imgx = article.find("img")["data-src"]

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = imgx
        new_headline.save()
    return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    for con in headlines:
        print(con)
    return render(request, "news/home.html", context)



# views