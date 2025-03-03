from django.http import HttpResponse

# Create your views here.
def getAccessToken(request):
    return HttpResponse("Hello, world. You're at the Mpesa_API index.")
