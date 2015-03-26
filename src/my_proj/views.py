from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from profiles.models import *
from django.db.models import F
from django.template.loader import get_template
from django.shortcuts import render, render_to_response

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from profiles.serializers import StartUpSerializer

from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView



class HomePage(generic.TemplateView):
    template_name = "home.html"


class AboutPage(generic.TemplateView):
    template_name = "about.html"

class StartUpCreate(CreateView):
    model = StartUpIdea
    template_name = "create_startup.html"
    fields = ['creator','name', 'description','category','tags']
    
class BrowsePage(generic.ListView):
    model = StartUpIdea
    template_name = "main_browse.html"
    
    def get_queryset(self):
        return StartUpIdea.objects.order_by('-pub_date')
        
class NameBrowsePage(generic.ListView):
    model = StartUpIdea
    template_name = "main_browse.html"
    
    
    def get_queryset(self):
        return StartUpIdea.objects.order_by('name')
        
class DateBrowsePage(generic.ListView):
    model = StartUpIdea
    template_name = "main_browse.html"
    
    
    def get_queryset(self):
        return StartUpIdea.objects.order_by('-pub_date')
    
class StartUpDetail(generic.DetailView):
    model = StartUpIdea
    template_name = "startup_detail.html"
    
class UpdateStartup(UpdateView):
    template_name = "create_startup.html"
    model = StartUpIdea
    fields = ['name', 'description','category','tags']
    success_url = "/my_startups"
    
class DeleteStartup(DeleteView):
    template_name = "delete_startup_confirm.html"
    model = StartUpIdea
    success_url = "/my_startups"
    
class UserListings(generic.ListView):
    template_name = "user_listings.html"
    model = StartUpIdea
    
class CategoryListView(generic.ListView):
    template_name = "browse.html"
    def get_queryset(self):
        category_id = self.kwargs['category_id']
        try:
            category = Category.objects.get(pk=category_id)
            return StartUpIdea.objects.filter(category=category)
        except Category.DoesNotExist:
            return StartUpIdea.objects.none()
            
class TagIndexView(generic.ListView):
    template_name = "browse.html"
    model = StartUpIdea
    context_object_name = 'startups'
    
    def get_queryset(self):
        return StartUpIdea.objects.filter(tags__slug=self.kwargs.get('slug'))
        
    
def like_startup(request, startup_id):
    StartUpIdea.objects.filter(pk=startup_id).update(likes=F('likes') + 1)
    object = StartUpIdea.objects.get(pk=startup_id)
    context = {'object':object}
    
    return render(request, 'startup_detail.html', context)
    
def dislike_startup(request, startup_id):
    StartUpIdea.objects.filter(pk=startup_id).update(likes=F('likes') - 1)
    object = StartUpIdea.objects.get(pk=startup_id)
    context = {'object':object}
    
    return render(request, 'startup_detail.html', context)
    
    
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def json_list(request, k, date1, date2):
    
    if request.method == 'GET':
        startups = StartUpIdea.objects.filter(pub_date__range=[date1, date2]).order_by('-likes')[:int(k)]
        serializer = StartUpSerializer(startups, many=True)
        return JSONResponse(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StartUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
        

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels."""
        cat_list = []
        for e in Category.objects.all():
            cat_list.append(str(e.name))
        #return ['cat1', 'cat2', 'cat3', 'cat4', 'cat5' ]
        return cat_list

    def get_data(self):
        """Return 3 dataset to plot."""
        int_list = []
        counter = 1
        
        for e in Category.objects.all():
            int_list.append(int(StartUpIdea.objects.filter(category__id=counter).count()))
            counter = counter + 1
            
        return [int_list]
        
        '''
        return [[StartUpIdea.objects.filter(category__id=1).count(), 
        StartUpIdea.objects.filter(category__id=2).count(), 
        StartUpIdea.objects.filter(category__id=3).count(), 
        StartUpIdea.objects.filter(category__id=4).count(), 
        StartUpIdea.objects.filter(category__id=5).count()]]
        '''


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()

'''    
def like_startup(request):
    context = RequestContext(request)
    startup_id = None
    if request.method == 'GET':
        startup_id = request.GET['startup_id']
        
    likes = 0
    if startup_id:
        startup = StartUpIdea.objects.get(id=int(startup_id))
        if startup:
            likes = startup.likes + 1
            startup.likes = likes
            startup.save()
    
    return HttpResponse(likes)
'''