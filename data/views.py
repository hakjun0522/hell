from django.shortcuts import render
import requests
# import base64
from bs4 import BeautifulSoup


# Create your views here.
def news_search(request):
    keyword = request.GET.get('q','') # Assuming 'q' is the query parameter
    news_list =[]

    if keyword:
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')

        for news_item in soup.find_all('a', class_='news_tit'):
            title = news_item.get('title')
            link = news_item.get('href')
            #관련 뉴스 아이템의 설명 추출
            description = news_item.find_next_sibling('div',class_='news_dsc').get_text(strip=True)
            news_list.append({'title':title, 'link':link,'description':description})
        
    #     for img in soup.find_all('a',class_='dsc_thumb'):
    #         for images in img.find_all('img',class_='thumb'):
    #             image1 = images.get('src')
    #             image = base64.b64decode(image1)
    #             news_list.append({'image':image})
    # print(news_list)

    return render(request, 'data/newssearch.html',{'news_list':news_list})