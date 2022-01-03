from django.core.exceptions import ValidationError
from utils.helpers import ResponseWrapper, CustomModelViewSet
from rest_framework.viewsets import ModelViewSet
from todos.models import Todo
from todos.api.serializers import TodoSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action


class TodoViewSet(CustomModelViewSet):
    logging_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    queryset = Todo.objects.all()
    lookup_field = "slug"
    
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy", "retrieve", "list"]:
            self.serializer_class = TodoSerializer
        else:
            self.serializer_class = TodoSerializer
        return self.serializer_class

    def get_permissions(self):
        permission_classes = [
            permissions.AllowAny
        ]
        return [permission() for permission in permission_classes]
    
    def create_or_update_multitodo(self, request, *args, **kwargs):
        createList = []
        updateList = []
        for data in request.data:
            if data.get("slug", None) is not None:
                updateList.append(data)
            else:
                createList.append(data)
        # perform create
        if len(createList) > 0:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return ResponseWrapper(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # perform update
        if len(updateList) > 0:
            for data in updateList:
                partial = kwargs.pop('partial', False)
                qs = Todo.objects.filter(slug__iexact=data["slug"])
                if qs:
                    instance = qs.first()
                    serializer = self.get_serializer(instance, data=data, partial=partial)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)

                    if getattr(instance, '_prefetched_objects_cache', None):
                        instance._prefetched_objects_cache = {}
            return ResponseWrapper(data=updateList, status=status.HTTP_200_OK, msg="update")
        
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return ResponseWrapper(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['post'])
    def destroy_multitodo(self, request, *args, **kwargs):
        deleteList = []
        for data in request.data:
            if data.get("slug", None) is not None:
                deleteList.append(data)
        
        # perform delete
        if len(deleteList) > 0:
            for data in deleteList:
                qs = Todo.objects.filter(slug__iexact=data["slug"])
                if qs:
                    instance = qs.first()
                    self.perform_destroy(instance)
            return ResponseWrapper(status=status.HTTP_204_NO_CONTENT, msg="delete")
        return ResponseWrapper(status=status.HTTP_400_BAD_REQUEST, msg="delete")