from django.shortcuts import render
from forms import *
from django.forms.formsets import formset_factory
from delta3.models import Gif, User, Comment
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.db import connection, transaction
import logging
logger = logging.getLogger(__name__)

import re

from django.template import Context

def home(request):
	return render(request, 'delta3/login.html')
	
def login(request):
	# Check if username matches password
	if request.REQUEST.get('username') and request.REQUEST.get('password'):
		un = request.REQUEST.get('username')
		pwd = request.REQUEST.get('password')
		sql = 'SELECT * from delta3_user where username=' + '"' + un + '"' + ' and password=' + '"' + pwd + '"' 
		logger.debug("sql = ..." + sql)        
		users = User.objects.raw(sql)        
		if len(list(users)) > 0:
			# login(request, user)
			return render(request, 'delta3/search.html', {'form': SearchForm})
	return render(request, 'delta3/login.html', {'form': LoginForm})

def comments(request):
       
        def parsecomment(comment):
            if re.match("<script>", comment, re.IGNORECASE) or re.match("<.*on(error|load|click|hover).*>", comment, re.IGNORECASE):
                raise ValueError("XSS detected\n")
            return comment

	request_method = request.method
	
	# If GET request, render comments form and clear out comment_display variable
	if (request_method == 'GET'):
		img_left = "http://static.comicvine.com/uploads/original/11111/111112756/3141240-0483057803-Chuck.jpg"
		img_right = "http://4.bp.blogspot.com/_JzInBXovu8w/SfHCOysBbiI/AAAAAAAAAgo/WapyJWFBJz4/s400/chuck-norris.jpg"
		context = {'form': CommentsForm, 'thanks_statement': "", 'all_comments_statement': "", 'img_left': img_left, 'img_right': img_right}
		return render(request, 'delta3/comments.html', context)
	
	# If POST request, 
	elif (request_method == 'POST'):
		# TODO Get username from database and add to Comment Model
		comment = request.POST.get('comment_submit')
                comment = parsecomment(comment)
		# Create Comment model and save to database
		#c = Comment(user=username, content=comment)
		c = Comment(content=comment)
		c.save()
		all_comments = Comment.objects.all().order_by('-id') # Most recent first
		thanks_statement = "Thanks for your comment: "
		all_comments_statement = "All comments: "
		img_left = "http://www.clipartbest.com/cliparts/nTX/EB7/nTXEB7jTB.jpeg"
		img_right = "http://media.giphy.com/media/1HrVMip45ciJy/giphy.gif"
		context = {'form': CommentsForm, 'comment_display': comment, 'all_comments': all_comments, 'thanks_statement': thanks_statement, 'all_comments_statement': all_comments_statement, 'img_left': img_left, 'img_right': img_right}
		return render(request, 'delta3/comments.html', context)
		#context = Context({'form': CommentsForm, 'comment_display': comment, 'all_comments': all_comments, 'thanks_statement': thanks_statement, 'all_comments_statement': all_comments_statement, 'img_left': img_left, 'img_right': img_right}, autoescape=False)
		#return render(request, 'delta3/comments.html', context)

def search(request):
	if request.method == 'POST':
		if(request.POST.get('searchterm')):
			searchterm = str(request.POST.get('searchterm'))
                        sql = 'SELECT * from delta3_gif where gif_name="%s"' % searchterm
			g = Gif.objects.raw(sql)
			# g = Gif.objects.raw('SELECT * from delta3_gif where gif_name=""; SELECT * from delta3_user')
			if len(list(g)) > 0:
				response = ""
				# html = ""
				# for x in g:	
				# 	response = response + str(x) + "<br>"
				# 	url = str(x.gif_url)
				# 	html = html + '<img src="' + url + '"\><br>'
			return render(request, 'delta3/search.html',{'gifs': g, 'query': sql,})
				# return HttpResponse(html)
	# cursor = connection.cursor()
	# cursor.execute('select * from delta3_gif; show tables;')

	return render(request, 'delta3/search.html', {'form': SearchForm})

def about(request):
	return render(request, 'delta3/about.html')

def register(request):

	def parseage(age):
		return int(age)
             
	# Exceptions are manually being created for POC
	# These exceptions will handled by the middlewares.py's "process_exception"
	# Raise ValueError exception if a digit is in firstname or lastname
	if request.REQUEST.get('password') and request.REQUEST.get('username'):
		
		firstname_in = request.REQUEST.get('firstname')
		if any(char.isdigit() for char in firstname_in):
			raise ValueError("Integer detected in firstname in /delta3/register")
		
		lastname_in = request.REQUEST.get('lastname')
		if any(char.isdigit() for char in lastname_in):
			raise ValueError("Integer detected in lastname in /delta3/register")
		
		age = request.REQUEST.get('age')
		age_in = parseage(age)
		un_in = request.REQUEST.get('username')
		pwd_in = request.REQUEST.get('password')
		
		#save new user in database
		sql = 'SELECT * from delta3_user where username=' + '"' + un_in + '"' 
		logger.debug("sql = ..." + sql)        
		users = User.objects.raw(sql)        
		if len(list(users)) <= 0:
			sql = 'INSERT INTO delta3_user (username, password, firstname, lastname, age) VALUES(' + '"' + un_in + '",' + '"' + pwd_in + '",' + '"' + firstname_in + '",' + '"' + lastname_in + '",' + '"' + str(age_in) + '"' + ')' 
			cursor = connection.cursor()
			cursor.execute(sql)
			#transaction.commit_unless_managed()
			logger.debug("sql = ..." + sql)        
			return render(request, 'delta3/login.html')
		else:
			logger.debug("username already exists")        
	return render(request, 'delta3/register.html', {'form': RegisterForm})
