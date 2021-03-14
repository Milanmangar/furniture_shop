from rest_framework import viewsets, status
from rest_framework.response import Response
import logging
import traceback
import copy

from table.models import Table, Leg
from table.serializers_table.serializers import TableSerializer

logger = logging.getLogger("table")


class TableViewset(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def create(self, request, *args, **kwargs):
        """
        creates new Table

        args:
            self: reference to the current instance of the class
            request(HttpRequest obj): contains data about the api request
        return:
            response(dict)
                success(code=200): {"result": {"key": "value", ...},
                                    "success_message": "success_message", "status": "success"}
                error(code=500):  {"error_message": {"key": [], ...}, "status": "error"}
                error(code=500):  {"error_message": "something went wrong", "status": "error"}
        """
        try:
            data = copy.deepcopy(request.data)
            data["name"] = data["name"].title()
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response({"result": serializer.data, "success_message": "'{}' Table created successfully".
                                format(data["name"].title()), "status": "success"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error_message": serializer.errors, "status": "error"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.info("\non root post request got an error: {}\n".format(traceback.format_exc()))
            return Response({"error_message": "something went wrong", "status": "error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """
        retrieves all table data

        args:
            self: reference to the current instance of the class
            request(HttpRequest obj): contains data about the api request
        return:
            response(dict)
                success(code=200): {"result": [{"keys": "values", ...},...], "status": "success"}
                error(code=500):  {"error_message": "something went wrong", "status": "error"}
        """

        try:
            query_set = self.get_queryset()
            serialized_result = self.get_serializer(query_set, many=True)
            return Response({"result": serialized_result.data, "status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.info("\non root get request got an error: {}\n".format(traceback.format_exc()))
            return Response({"error_message": "something went wrong", "status": "error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """
        retrieves one table with given table name

        args:
            self: reference to the current instance of the class
            request(HttpRequest obj): contains data about the api request
            pk(str): table name
        return:
            response(dict)
                success(code=200): {"result": {"keys": "values", ...}, "status": "success"}
                error(code=500):  {"error_message": "something went wrong", "status": "error"}
        """
        try:
            try:
                query_set = self.get_queryset().get(name__iexact=pk)
            except Exception as e:
                return Response({"error_message": '{}'.format(e), "status": "error"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serialized_result = self.get_serializer(query_set)
            return Response({"result": serialized_result.data, "status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.info("\non root retrieve request got an error: {}\n".format(traceback.format_exc()))
            return Response({"error_message": "something went wrong", "status": "error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """
        updates table with given table name

        args:
            self: reference to the current instance of the class
            request(HttpRequest obj): contains data about the api request
            pk(str): table name
        return:
            response(dict)
                success(code=200): {"result": {"keys": "values", ...}, "success_message": "success_message",
                                    "status": "success"}
                error(code=500):  {"error_message": "", "status": "error"}
        """
        try:
            try:
                instance = self.queryset.get(name=pk)
                if "name" not in request.data:
                    instance.description = request.data["description"]
                    instance.price = request.data["price"]
                    instance.legs = Leg.objects.get(name__iexact=request.data["legs"])
                    instance.save()
                else:
                    return Response({"error_message": "'name' field should not be passed", "status": "error"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error_message": '{}'.format(e), "status": "error"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serializer = self.serializer_class(instance)
            return Response({"result": serializer.data, "success_message": "'{}' Table updated successfully".
                            format(instance.name.title()), "status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.info("\non root retrieve request got an error: {}\n".format(traceback.format_exc()))
            return Response({"error_message": "something went wrong", "status": "error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        """
        updates table partially with given table name

        args:
            self: reference to the current instance of the class
            request(HttpRequest obj): contains data about the api request
            pk(str): table name
        return:
            response(dict)
                success(code=200): {"result": {"keys": "values", ...}, "success_message": "success_message",
                                    "status": "success"}
                error(code=500):  {"error_message": "something went wrong", "status": "error"}
        """
        try:
            instance = self.queryset.get(pk=kwargs.get('pk'))
            serializer = self.serializer_class(instance, data=request.data, partial=True, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"result": serializer.data,
                                 "success_message": "'{}' Table partially updated successfully".
                                format(instance.name.title()), "status": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"error_message": serializer.errors, "status": "error"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"result": serializer.data, "status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.info("\non root retrieve request got an error: {}\n".format(traceback.format_exc()))
            return Response({"error_message": "something went wrong", "status": "error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
        delete table with given table name

        args:
            self: reference to the current instance of the class
            request(HttpRequest obj): contains data about the api request
            pk(str): table name
        return:
            response(dict)
                success(code=200): {"result": {"keys": "values", ...}, "status": "success"}
                error(code=500):  {"error_message": "something went wrong", "status": "error"}
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "'{}' deleted successfully".format(kwargs.get('pk')),
                         "status": "success"},status=status.HTTP_204_NO_CONTENT)
