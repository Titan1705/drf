from rest_framework.serializers import ModelSerializer, SerializerMethodField

from courses.models import Course, Lesson, Payment


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("id", "title", "lessons_count")


class CourseDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("title", "lessons_count", "lessons")


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_date",
            "paid_course",
            "separately_paid_lesson",
            "payment_amount",
            "payment_method",
        ]