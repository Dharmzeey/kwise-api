from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from .service import Cart


class GetCartView(APIView):
    
    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {   
                "data": list(cart.__iter__()),
                "grand_total_price": cart.get_total_price()                
            },
            status=status.HTTP_200_OK
            )
get_cart = GetCartView.as_view()


class ModifyCartView(APIView):
    """
    API to handle update, reduce, delete cart operations
    """

    def post(self, request, **kwargs):
        product_uuid = request.data["product_id"]
        action = request.data.get("action")
        cart = Cart(request)
        
        if action == "increament":
            cart.increament(product_uuid=product_uuid)
        
        elif action == "decreament":
            cart.decreament(product_uuid=product_uuid)
            
        elif action == "update":
            quantity = request.data.get("quantity", 0)
            cart.update(product_uuid=product_uuid, quantity=quantity)
            
        elif action == "remove":
            cart.remove(product_uuid=product_uuid)
            
        elif action == "clear":
            cart.clear()

        elif action == "add":
            cart.add(product_uuid=product_uuid)
            
        else:
            return Response(
                {"error": "Action not recognized"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        return Response(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED
        )
modify_cart = ModifyCartView.as_view()


class CheckOutView(APIView):
  def post(self, request):
    #   RE CALCULATE EVERYTHING AGAIN
    data = {"message": "You order has been completed successfully"}
    return Response(data, status=status.HTTP_200_OK)
check_out = CheckOutView.as_view()