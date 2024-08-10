from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers as CustomSerializers
from .models import State, LGA


class FetchStatesView(APIView):
  def get(self, request):
    states = State.objects.all()
    state_serializer = CustomSerializers.StateSerializer(instance=states, many=True)    
    data = {
      "states": state_serializer.data,  
    }
    return Response(data, status=status.HTTP_200_OK)
fetch_states = FetchStatesView.as_view()


class FetchLGAView(APIView):
  def get(self, request):
    print(request.query_params)
    state_id = request.query_params.get("state_id")
    lgas = LGA.objects.filter(state__id=state_id)
    lga_serializer = CustomSerializers.LGASerializer(instance=lgas, many=True)    
    data = {
      "lgas": lga_serializer.data,  
    }
    return Response(data, status=status.HTTP_200_OK)
fetch_lgas = FetchLGAView.as_view()
