from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Course


class OwnerMixin(object):
    """
    Mixin to filter courses by the current user (owner).
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
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


class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    View to list courses created by the current user.
    """

    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    View to create a new course (uses OwnerCourseEditMixin for template and form).
    """

    permission_required = "courses.add_course"


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    View to update an existing course (uses OwnerCourseEditMixin for template and form).
    """

    permission_required = "courses.change_course"


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """
    View to delete a course (uses OwnerCourseMixin for filtering and deletion).
    """

    template_name = "courses/manage/course/delete.html"
    permission_required = "courses.delete_course"
