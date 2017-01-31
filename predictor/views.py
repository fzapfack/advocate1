from django.shortcuts import render

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    context = {}
    context['authenticated'] = request.user.is_authenticated()
    if context['authenticated'] == True:
        context['username'] = request.user.username
    return render(request, 'index.html',context)
# Create your views here.
