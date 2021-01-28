from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from forum.forms import PostForm
from forum.models import Thread, Post


class ThreadListView(ListView):
    model = Thread
    paginate_by = 15


class ThreadDisplay(DetailView):
    model = Thread

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm()
        return context


class ThreadPost(SingleObjectMixin, FormView):
    template_name = "forum/thread_detail.html"
    form_class = PostForm
    model = Thread

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("thread-detail", kwargs={"pk": self.object.pk})

    # Perhaps Here in the validation ?
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Problem seems to be here
class ThreadDetail(View):
    def get(self, request, *args, **kwargs):
        view = ThreadDisplay.as_view()
        return view(request, *args, **kwargs)

    # especially here
    def post(self, request, *args, **kwargs):
        view = ThreadPost.as_view()
        return view(request, *args, **kwargs)


class ThreadCreateView(CreateView):
    model = Thread
    fields = ["title", "content", "categories"]

    def get_success_url(self):
        return reverse("thread-detail", args=(self.object.id,))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ThreadDeleteView(DeleteView):
    model = Thread
    success_url = reverse_lazy("thread-list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post


"""
class PostCreateView(CreateView):
    model = Post
    fields = ["content", "thread"]

    def get_success_url(self):
        return reverse("thread-detail", args=(self.object.id,))

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.thread = Thread.objects.get(pk=self.kwargs["thread_pk"])
        return super().form_valid(form)


class PostFormView(FormView):
    template_name = 'forum/thread_form.html'
    form_class = PostsForm

    def get_success_url(self):
        return reverse("thread-detail", args=(self.object.thread.id,))

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.thread = Thread.objects.get(pk=self.kwargs["thread_pk"])
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
"""
