from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from .models import Course


class OwnerMixin:
    """
    Mixin to filter courses by the current user (owner).
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    """
    Mixin to automatically set the current user as the owner when the form is valid.
    """

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Mixin for handling courses (inherits OwnerMixin to filter by owner).
    """

    model = Course
    fields = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    Mixin for handling course create and update views
    (inherits OwnerCourseMixin and OwnerEditMixin).
    """

    template_name = "courses/manage/course/form.html"
