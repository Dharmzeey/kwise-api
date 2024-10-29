from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from authentication.permissions import IsUserVerified
from cart.service import Cart

from .models import Payment
from. paystack import Paystack


class InitiatePayment(APIView):
    permission_classes = [IsAuthenticated, IsUserVerified]
    def post(self, request):
        cart = Cart(request)
        payment = Paystack()
        payment_init = payment.initialize_payment(email=request.user.email, amount=cart.get_total_price())
        # data = {"access_code": 'q3e3gf2wws9b7xc'}
        #     # access code is returned to FE to resume and continue tnx
        # return Response(data, status=status.HTTP_200_OK)
        if payment_init[0] == 200: # if the first item in the tuple which is the status code
            payment = Payment.objects.create(user=request.user, amount=cart.get_total_price(), email=request.user.email, access_code=payment_init[1], ref=payment_init[2])
            payment.save()
            data = {"access_code": payment_init[1]}
            # access code is returned to FE to resume and continue tnx
            return Response(data, status=status.HTTP_200_OK)
        elif payment_init[0] == 500:
            data = {"error": "payment initialization timed out"}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            data = {"error": "payment could not be initialized"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
initiate_payment = InitiatePayment.as_view()


class VerifyPayment(APIView):
    permission_classes = [IsAuthenticated, IsUserVerified]
    def get(self, request, ref):
        # this will be async called when the paystack finishes
        payment = Payment.objects.get(ref=ref)
        verified = payment.verify_payment()

        if verified:
            # fetch the current session and then establish the orders for all product #pending order gets created here
            return render(request, "success.html")
        return render(request, "success.html")


verify_payment = VerifyPayment.as_view()
