from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .mixins import OwnerCourseEditMixin, OwnerCourseMixin


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
