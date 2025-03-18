from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .mtn_auth import get_mtn_access_token

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
            # Call MTN API for balance
            token = get_mtn_access_token()
            response = "END Your balance is $10" if token else "END Error retrieving balance"
        elif text == "2":
            response = "CON Choose a data plan\n1. 1GB - $5\n2. 2GB - $10"
        else:
            response = "END Invalid option"

        return HttpResponse(response)

    return HttpResponse("Invalid request", status=400)
