from django.urls import path, include
from rest_framework.routers import SimpleRouter

from courses.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonListApiView,
    LessonRetrieveApiView,
    LessonUpdateApiView,
    LessonDestroyApiView,
    PaymentListView,
)
from courses.apps import CoursesConfig

app_name = CoursesConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)


urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/destroy/",
        LessonDestroyApiView.as_view(),
        name="lessons_destroy",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"
    ),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("", include(router.urls)),
]


urlpatterns += router.urls