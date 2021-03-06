from django.conf.urls import url
from . import views

# Add views for app "polls" here
urlpatterns = [
	# /delta3
    url(r'^$', views.home, name='home'),
	# /delta3/login
	url(r'^login', views.login, name='login'),
	# /delta3/register
	url(r'^register', views.register, name='register'),
	# /delta3/comments
	url(r'^comments', views.comments, name='comments'),
	# /delta3/search
	url(r'^search', views.search, name='search'),
	# /delta3/about
	url(r'^about', views.about, name='about'),
]