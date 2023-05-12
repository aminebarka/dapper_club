from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from .models import VerificationUser, Account
from django.contrib import messages
from django.http import JsonResponse

from twilio.rest import Client


def sent_otp(mobile, u_user):
    mobile_no = '+91'+str(mobile)
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    service_id = settings.SERVICE_ID
    client = Client(account_sid, auth_token)
    print(account_sid, auth_token, service_id)
    verification = client.verify \
                    .services(service_id) \
                    .verifications \
                    .create(to=mobile_no, channel='sms')

    if VerificationUser.objects.filter(user=u_user).exists():
        user = get_object_or_404(VerificationUser, user=u_user)
        print(user)
        user.otp_attempt += 1
        user.save()
    else:
        user = VerificationUser()
        user.user = u_user
        user.otp_attempt += 1
        user.save()

    print(verification.sid)
    return user.id


def verify_otp(mobile, otp):
    mobile_no = '+91'+str(mobile)
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    service_id = settings.SERVICE_ID
    client = Client(account_sid, auth_token)
    verification_check = client.verify \
                    .services(service_id) \
                    .verification_checks \
                    .create(to=mobile_no, code=otp)

    if verification_check.status == 'approved':
        return True
    else:
        return False


def otp_activation(request, phone_number, uid, verification_user):
    try:
        if request.method == 'POST':
            otp = request.POST['otp']
            verify = verify_otp(phone_number, otp)
            if verify:
                user = Account.objects.get(pk=uid)
                user.is_active = True
                user.save()
                user_verification = VerificationUser.objects.get(pk=verification_user)
                user_verification.otp = otp
                user_verification.otp_verification = True
                user_verification.save()
                request.session['id'] = uid
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'invalid otp')
                return redirect('registration')
        context = {
            'phone_number':phone_number,
            'uid' : uid,
            'verification_user':verification_user
        }
        return render(request, 'accounts/otp_activation.html', context)
    
    except:
        return HttpResponse('error')


def resent_otp(request):

    phone_no = request.GET.get('phone_number', None)
    uid = request.GET.get('uid', None)
    user = get_object_or_404(Account,pk=uid)
    sent_otp(phone_no,user)
    data={
        'status': True
    }
    print(data['status'])
    return JsonResponse(data)


def mobile_otp(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        if Account.objects.filter(phone_number=phone_number).exists():
            user = Account.objects.get(phone_number__exact=phone_number)
            verification_user = sent_otp(phone_number, user)
            uid = user.pk
            context = {
                'phone_number' : phone_number,
                'uid' : uid,
                "verification_user" : verification_user,
            }
            messages.success(request, 'OTP sent to  your mobile number')
            return render(request, 'accounts/otp_activation.html', context)

        else:
            messages.error(request, 'Invalid phone number!')

    return render(request, 'accounts/phone_number.html')