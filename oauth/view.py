from django.http import HttpResponse
from django.shortcuts import render
 
import urllib
import urllib2
import json
import redis
 
client_id = '59e20ba35722b5a2a905'
client_secret = '1d2bc69a9c54627f8e0c45cb8e2d63a5d3ca2c5d'
code = ''
r = redis.StrictRedis(host='127.0.0.1', port=6379)
 
def login(request):
    context          = {}
    context['login'] = 'Click and login now!'
    return render(request, 'login.html', context)
	
def loginWithGithub(request):
	code = request.GET.get('code','')
	requrl = 'https://github.com/login/oauth/access_token'
	data = {'client_id':client_id,'client_secret':client_secret,'code':code}
	data_urlencode = urllib.urlencode(data)
	req = urllib2.Request(url = requrl,data =data_urlencode)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	tmp = res.split('&')
	tokeninfo = tmp[0].split('=')
	access_token = tokeninfo[1]
	
	tokenurl = 'https://api.github.com/user?access_token='+access_token
	tokenreq = urllib2.Request(tokenurl)
	res_data = urllib2.urlopen(tokenreq)
	res = res_data.read()
	emailaddr_json = json.loads(res)
	email_addr = emailaddr_json['email']

	return render(request, 'redirect_back.html',{'email_addr':email_addr})

def renderSearchPage(request):
	domain = request.GET.get('domain','')
	#r = redis.StrictRedis(host='127.0.0.1', post=6379)
        print domain
        listlen = r.llen(domain)
        expertlist = r.lrange(domain,0,listlen)
	answerlist = []
	for item in expertlist:
	    print item
	    expert_name = r.get(item+':n')
	    expert_hi = r.get(item+':hi')
	#    expert_hi_num = int(expert_hi)
	    answerlist.append({'ID':item,'name':expert_name,'hi':expert_hi})
	return render(request, 'searchPage.html',{'domain':domain,'answerlist':answerlist})

def renderSearchPage(request):
	expert_name = request.GET.get('expert_name','')
	answerlist = []
    return render(request, 'coauthor_page.html',{'name':expert_name,'answerlist':answerlist})