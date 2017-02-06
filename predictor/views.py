from django.shortcuts import render

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    context = {}
    context['authenticated'] = request.user.is_authenticated()
    if context['authenticated'] == True:
        context['username'] = request.user.username
    return render(request, 'index_test.html',context)
# Create your views here.


def test(request,id):
    # return HttpResponse('Hello from Python!')
    # test_id = request.GET.get('test_id', '')
    context = {}
    context['authenticated'] = request.user.is_authenticated()
    if context['authenticated'] == True:
        context['username'] = request.user.username
        context['test_id'] = id
    return render(request, 'test.html',context)
