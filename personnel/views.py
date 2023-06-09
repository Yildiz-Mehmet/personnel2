from django.shortcuts import render
from .serializers import DepartmentSerializer,PersonnelSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from .models import Department,Personnel


class DepartmentListCreateView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdminOrReadOnly,
    )

class PersonnelListCreateView(ListCreateAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer

    permission_classes =[IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:

            return self.update(request, *args, **kwargs)
        data = {
            'message':'You are not authorized to update!'
        }
        return Response(data,status=status.HTTP_401_UNAUTHORİZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.perform_destroy(instance)
        if self.request.user.is_superuser:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'message':'You are not authorized to delete!'
        }
        return Response(data,status=status.HTTP_401_UNAUTHORİZED)



class PersonnelRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer

    permission_classes = (
        IsAuthenticated,
        IsAdminOrReadOnly,
    )

class DepartmentRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    permission_classes =[IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:

            return self.update(request, *args, **kwargs)
        data = {
            'message':'You are not authorized to update!'
        }
        return Response(data,status=status.HTTP_401_UNAUTHORİZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.perform_destroy(instance)
        if self.request.user.is_superuser:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'message':'You are not authorized to delete!'
        }
        return Response(data,status=status.HTTP_401_UNAUTHORİZED)


class DepartmentPersonnelView(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    permission_classes = (
        IsAuthenticated,
        IsAdminOrReadOnly,
    )

    def get_queryset(self):
        
        department = self.kwargs['department']
        return Department.objects.filter(name__iexact=department)

    