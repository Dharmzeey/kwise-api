from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from authentication.permissions import IsUserVerified
from cart.service import Cart

from .models import Payment
from .serializers import PaymentSerializer


class InitiatePayment(APIView):
    permission_classes = [IsAuthenticated, IsUserVerified]
    def post(self, request):
        pk = settings.PAYSTACK_PUBLIC_KEY
        cart = Cart(request)
        payment = Payment.objects.create(amount=cart.get_total_price(), email=request.user.email, user=request.user)
        payment.save()
        serializer = PaymentSerializer(payment)
        data = {
            'payment': serializer.data,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
        }
        return Response(data, status=status.HTTP_200_OK)

initiate_payment = InitiatePayment.as_view()


class VerifyPayment(APIView):
    permission_classes = [IsAuthenticated, IsUserVerified]
    def get(self, request, ref):
        # this will be async called when the paystack finishes
        payment = Payment.objects.get(ref=ref)
        verified = payment.verify_payment()

        if verified:
            # fetch the current session and then establish the orders for all product #pending order gets created here
            print(request.user.username, " funded wallet successfully")
            return render(request, "success.html")
        return render(request, "success.html")


verify_payment = VerifyPayment.as_view()
