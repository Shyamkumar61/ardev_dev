from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from apps.clients.models import Client
from rest_framework import generics
from .serializers import ClientSerializer, ClientListSerializer
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from apps.clients.filters import ClientFilter


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        page_count = response.data.get('count') // self.page_size + (1 if response.data.get('count') % self.page_size >
                                                                     0 else 0)
        return Response(OrderedDict([
            ('count', response.data.get('count')),
            ('next', response.data.get('next')),
            ('previous', response.data.get('previous')),
            ('page_count', page_count),
            ('success', True),
            ('data', data)
        ]))


class ClientListView(generics.ListAPIView):

    queryset = Client.objects.only('client_name', 'sector', 'client_phone').all()
    serializer_class = ClientListSerializer
    pagination_class = CustomPagination
    filter_class = ClientFilter

    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        filter_set = self.filter_class(request.GET, self.get_queryset())
        if filter_set.is_valid():
            data = filter_set.qs
        paginated_data = self.paginate_queryset(data)
        serializer = self.get_serializer(paginated_data, many=True)                 #need to restructure
        try:
            if serializer:
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"success": False, "data": str(e)})

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     print(queryset)
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     response = self.get_serializer(queryset, many=True)
    #     return Response({"success": True, "data": response.data})


class ClientCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClientDetailView(generics.RetrieveUpdateAPIView):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        serializer_context = {
            "hide_relationship": self.request.GET.get('hide_relationship', False)
        }
        return serializer_context

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
            serializer.is_valid()
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response({"success": False, "data": str(e)})

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response({"success": False, "data": str(e)})


class ProfileList(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile_list.html"

    def get(self, request):
        queryset = Client.objects.get(id=1)
        return Response({'profile': queryset})

