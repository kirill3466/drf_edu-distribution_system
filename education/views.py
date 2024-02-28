from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Access, Lesson, Product
from .serializers import (LessonSerializer, ProductSerializer,
                          ProductStatsSerializer)


class ProductListView(ListAPIView):
    queryset = Product.objects.all().select_related('owner')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class LessonListView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if Access.objects.filter(student=user, access_check=True).exists():
            return Lesson.objects.filter(
                product__product_access__student=user,
                product__product_access__access_check=True
            ).select_related('product')
        else:
            return Lesson.objects.none()


class ProductStatsView(ListAPIView):
    queryset = Product.objects.all().select_related('owner')
    serializer_class = ProductStatsSerializer
    permission_classes = [IsAuthenticated]
