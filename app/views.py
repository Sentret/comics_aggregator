from django.shortcuts import render
from .models import ComicsBook
import itertools
from django.http import HttpResponseNotFound  


def group_by_n(content, n):
    args = [iter(content)] * n
    return ([e for e in t if e != None] for t in itertools.zip_longest(*args))


def main_page(request,shop='all'):
 
   
    mapper = {}
    mapper['all'] = 'Все разделы'
    mapper['labirint'] = 'Лабиринт'
    mapper['chookandgeek'] = 'Чук и Гик'
    mapper['lavkaapelsin'] = 'Лавка Апельсин'
    mapper['ozon'] = 'Озон'

    
    if shop not in ['all','labirint','chookandgeek',
                    'lavkaapelsin','ozon']:
        return HttpResponseNotFound()

    if shop is 'all':
        content = ComicsBook.objects.all()
    else:
        content = ComicsBook.objects.all().filter(source=shop)


    content = list(group_by_n(content,5))
    return render(request, 'app/main_page.html', {'content':content,'page_name':mapper[shop]})




def cheapest_prize(request):
	pass