from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from apps.clients.models import Client
from rest_framework import generics
from .serializers import ClientSerializer, ClientListSerializer
from rest_framework.exceptions import NotFound


class ClientListView(generics.ListAPIView):

    queryset = Client.objects.only('client_name', 'sector', 'client_phone').all()
    serializer_class = ClientListSerializer
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"success": True, "data": response.data})


class ClientCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClientDetailView(generics.RetrieveUpdateAPIView):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response({"success": False, "data": str(e)})

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response({"success": False, "data": str(e)})


class ProfileList(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile_list.html"

    def get(self, request):
        queryset = Client.objects.get(id=1)
        return Response({'profile': queryset})

