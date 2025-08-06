from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Post, Category
from django.db.models import Q

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-published_date')
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query))
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['query'] = self.request.GET.get('q', '')
        return context
