from django.contrib.auth.models import User
from django.db.models import Count, Avg, F
from rest_framework import serializers

from .models import Access, Lesson, Product


class ProductSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(
        source='lessons.count', read_only=True
    )
    start_date = serializers.DateTimeField(
        format="%d.%m.%Y %H:%M", input_formats=['%Y-%m-%dT%H:%M:%SZ']
    )
    end_date = serializers.DateTimeField(
        format="%d.%m.%Y %H:%M", input_formats=['%Y-%m-%dT%H:%M:%SZ']
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'lesson_count', 'start_date', 'end_date'
        ]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url']


class ProductStatsSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()
    average_filled_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'students_count',
            'average_filled_percentage',
            'purchase_percentage'
        )

    def get_students_count(self, obj):
        return Access.objects.filter(product=obj).count()

    def get_average_filled_percentage(self, obj):
        groups = obj.groups.all().annotate(
            filled_percentage=(Count('students') * 100.0) / F('max_students')
        )
        return groups.aggregate(
            Avg('filled_percentage')
        )['filled_percentage__avg'] or 0

    def get_purchase_percentage(self, obj):
        total_users = User.objects.count()
        students_count = self.get_students_count(obj)
        return (students_count / total_users) * 100 if total_users else 0
