from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ussd_callback(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId', '')
        phone_number = request.POST.get('phoneNumber', '')
        service_code = request.POST.get('serviceCode', '')
        text = request.POST.get('text', '')

        # USSD Menu Logic
        if text == "":
            response = "CON Welcome to My Service\n1. Check Balance\n2. Buy Data"
        elif text == "1":
            response = "END Your balance is $10"
        elif text == "2":
            response = "CON Choose a data plan\n1. 1GB - $5\n2. 2GB - $10"
        elif text == "2*1":
            response = "END You have purchased 1GB for $5"
        else:
            response = "END Invalid option"

        return HttpResponse(response)

    return HttpResponse("Invalid request", status=400)
