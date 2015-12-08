from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import *
# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class ReviewCreateView(CreateView):
  model = Review
  template_name = "review/review_form.html"
  fields = ['title', 'description']
  success_url = reverse_lazy('review_list')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(ReviewCreateView, self).form_valid(form)

class ReviewListView(ListView):
  model = Review
  template_name = "review/review_list.html"

class ReviewDetailView(DetailView):
  model = Review
  template_name = "review/review_detail.html"

  def get_context_data(self, **kwargs):
    context = super(ReviewDetailView, self).get_context_data(**kwargs)
    review = Review.objects.get(id=self.kwargs['pk'])
    comments = Comment.objects.filter(review=review)
    context['comments'] = comments
    return context

class ReviewUpdateView(UpdateView):
  model = Review
  template_name = "review/review_form.html"
  fields = ['title', 'description']

  def get_object(self, *args, **kwargs):
    object = super(ReviewUpdateView, self).get_object(*args, **kwargs)
    if object.user != self.request.user:
      raise PermissionDenied()
    return object

class ReviewDeleteView(DeleteView):
  model = Review
  template_name = "review/review_confirm_delete.html"
  success_url = reverse_lazy('review_list')

  def get_object(self, *args, **kwargs):
    object = super(ReviewDeleteView, self).get_object(*args, **kwargs)
    if object.user != self.request.user:
      raise PermissionDenied()
    return object

class CommentCreateView(CreateView):
  model = Comment
  template_name = "comment/comment_form.html"
  fields = ['text']

  def get_success_url(self):
    return self.object.review.get_absolute_url()

  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.review = Review.objects.get(id=self.kwargs['pk'])
    return super(CommentCreateView, self).form_valid(form)

class CommentUpdateView(UpdateView):
  model = Comment
  pk_url_kwarg = 'comment_pk'
  template_name = "comment/comment_form.html"
  fields = ['text']

  def get_object(self, *args, **kwargs):
    object = super(CommentUpdateView, self).get_object(*args, **kwargs)
    if object.user != self.request.user:
      raise PermissionDenied()
    return object

  def get_success_url(self):
    return self.object.review.get_absolute_url()

class CommentDeleteView(DeleteView):
  model = Comment
  pk_url_kwarg = 'comment_pk'
  template_name = "comment/comment_confirm_delete.html"

  def get_object(self, *args, **kwargs):
    object = super(CommentDeleteView, self).get_object(*args, **kwargs)
    if object.user != self.request.user:
      raise PermissionDenied()
    return object

  def get_success_url(self):
    return self.object.review.get_absolute_url()

class VoteFormView(FormView):
  form_class = VoteForm

  def form_valid(self, form):
    user = self.request.user
    review = Review.objects.get(pk=form.data["review"])
    try:
      comment = Comment.objects.get(pk=form.data["comment"])
      prev_votes = Vote.objects.filter(user=user, comment=comment)
      has_voted = (prev_votes.count()>0)
      if not has_voted:
        Vote.objects.create(user=user, comment=comment)
      else:
        prev_votes[0].delete()
      return redirect(reverse('review_detail', args=[form.data["review"]]))
    except:
      prev_votes = Vote.objects.filter(user=user, review=review)
      has_voted = (prev_votes.count()>0)
      if not has_voted:
        Vote.objects.create(user=user, review=review)
      else:
        prev_votes[0].delete()
    return redirect('review_list')

class UserDetailView(DetailView):
  model = User
  slug_field = 'username'
  template_name= 'user/user_detail.html'
  context_object_name = 'user_in_view'

  def get_context_data(self, **kwargs):
    context = super(UserDetailView, self).get_context_data(**kwargs)
    user_in_view= User.objects.get(username=self.kwargs['slug'])
    reviews = Review.objects.filter(user=user_in_view)
    context['reviews'] = reviews
    comments = Comment.objects.filter(user=user_in_view)
    context['comments'] = comments
    return context

class SearchReviewListView(ReviewListView):
  def get_queryset(self):
    incoming_query_string = self.request.GET.get('query','')
    return Review.objects.filter(title__icontains=incoming_query_string)




