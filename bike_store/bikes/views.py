from rest_framework.views import APIView
from .datastore import get_instance, list_instances, delete_instance
from .serializers import BikeSerializer
from rest_framework.response import Response
from rest_framework import status


class BikesListView(APIView):

    def get(self, request):
        cursor = request.GET.get("cursor")
        results, cursor = list_instances(cursor=cursor)
        serializer = BikeSerializer(results, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BikeView(APIView):

    def get(self, request, id):
        instance = get_instance(id)
        serializer = BikeSerializer(instance)
        return Response(serializer.data)

    def post(self, request, id):
        instance = get_instance(id)
        serializer = BikeSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        delete_instance(id)
        return Response("Invalid action_type", status=status.HTTP_204_NO_CONTENT)
