import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
)

from django.shortcuts import get_object_or_404

from courses.filters import PaymentFilter
from courses.models import Course, Lesson, Payment, Subscription
from courses.paginators import MyPaginator
from courses.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
    PaymentSerializer,
)
from courses.services import  create_session
from users.permissions import IsModer, IsOwner, IsOwnerAndNotModer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = MyPaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                IsOwnerAndNotModer,
            )

        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_id")
        course = Course.objects.get(id=course_id)
        serializer.save(course=course)


class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwnerAndNotModer)
    pagination_class = MyPaginator

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return Lesson.objects.filter(course_id=course_id)


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwnerAndNotModer)


class PaymentListView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class CoursePaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(id=course_id)
        payment = serializer.save(user=self.request.user, paid_course=course)

        try:
            course_name = course.title
            session_id, payment_link = create_session(payment.payment_amount, f'к оплате {course_name}')
            payment.session_id = session_id
            payment.payment_link = payment_link
            payment.save()
        except stripe.error.StripeError as e:
            print(f"Ошибка при создании сессии Stripe: {e}")
            raise



class SubscriptionView(APIView):
    def post(self, request, course_id, *args, **kwargs):
        user = request.user

        course = get_object_or_404(Course, id=course_id)
        subscription, created = Subscription.objects.get_or_create(
            user=user, course=course
        )

        if created:
            message = "подписка добавлена"
        else:
            subscription.delete()
            message = "подписка удалена"

        return Response({"message": message}, status=status.HTTP_200_OK)