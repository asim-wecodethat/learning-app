from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import ModuleFormSet
from .mixins import OwnerCourseEditMixin, OwnerCourseMixin
from .models import Course


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


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = "courses/manage/module/formset.html"
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({"course": self.course, "formset": formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("manage_course_list")
        return self.render_to_response({"course": self.course, "formset": formset})
