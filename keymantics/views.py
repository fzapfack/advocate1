from django.shortcuts import render
from django.http import HttpResponseRedirect
from keymantics.utils.scrapper import Scrapper

# Create your views here.
def keymantics_open(request):
    # return HttpResponse('Hello from Python!')
    context = {}
    return render(request, 'keymantics/open_page.html', context)

def keymantics_results(request):
    print(request.POST)
    if request.method == 'POST':
        query = request.POST.get('query')
        scrapper = Scrapper()
        res = scrapper.predict(query)
        if res is None:
            return render(request, 'keymantics/page_not_found.html')
        else:
            context = {'query': query,
                       'type': res[0],
                       'product': res[1],}
            return render(request, 'keymantics/page_results.html', context)
    else:
        return HttpResponseRedirect('/keymantics/')
