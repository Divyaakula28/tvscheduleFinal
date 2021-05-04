from django.shortcuts import render
from django.http import HttpResponse
import requests
import numpy as np
import json
import pytz
from datetime import datetime
from .models import User
from django.db.models import Q



# Create your views here.
def home(req):
	def get_ip(req):
		address=req.META.get('HTTP_X_FORWARDED_FOR')
		if address:
			ip=address.split(',')[-1].strip()
		else:
			ip=req.META.get('REMOTE_ADDR')	
		return ip
	ip=get_ip(req)
	u=User(user=ip)	
	result=User.objects.filter(Q(user__icontains=ip))
	if len(result)==1:
		print("user exist")
	elif len(result)>1:
		print('user exist')	
	else:
		u.save()
		#print("user")
	count=User.objects.all().count()	
	print("totoal users",count)
	return render(req,'home1.html')
def home1(req):
	return render(req,'options.html')
def loc(req):
	if req.method=='POST':
		channel=req.POST['select']
		url = "https://indian-tv-schedule.p.rapidapi.com/TodaySchedule"
		querystring = {"channel":channel}
		headers = {
   			'x-rapidapi-host': "indian-tv-schedule.p.rapidapi.com",
   			'x-rapidapi-key': "6966652bc2msh4a15d38b3376026p16047ejsnb10766d15552"
   			}
		response = requests.request("GET", url, headers=headers, params=querystring)
		k1=response.text
		print(k1)
		k2 = json.loads(k1)
		length=len(k2)
		time=list(k2.keys())
		r=[]
		s=[]
		for i in range(len(time)):
			o=time[i]
			j=o[0]+o[1]
			k=o[3]+o[4]
			r.append(j)
			s.append(k)
		hr= [int(i) for i in r]
		mn= [int(i) for i in s]
	
		new_d = {}
		for sub in k2.values():
			for key, value in sub.items():
				new_d.setdefault(key, []).append(value)
		programs=list(new_d.values())[0]
		typep=list(new_d.values())[2]
		diss=list(new_d.values())[1]
		return render(req,'search3.html',{'time':time,'programs':programs,'diss':diss,'type':typep,'hr':hr,'mn':mn})
	return render(req,'search1.html')


def drop(req):
	if req. method=='POST':
		name=req.POST['lang']
		url = "https://indian-tv-schedule.p.rapidapi.com/searchChannel"
		querystring = {"lang":name}
		headers = {
    'x-rapidapi-host': "indian-tv-schedule.p.rapidapi.com",
    'x-rapidapi-key': "8b3ed7e76cmsh2ce38fcd37b82b4p1164d2jsn6fa39b33ac0b"
    }
		response = requests.request("GET", url, headers=headers, params=querystring)
		x=response.text
		x=x.replace('[','')
		x=x.replace(']','')
		x=x.replace('"','')	
		x=(x.split(","))
		x.sort()
		return render(req,'search1.html',{'x':x}) 		
	return render(req, 'search0.html')
		
def nav(req):
	return render(req,'h1.html')
	
def dis(req):
	return render(req,'discriptive.html')
def all(req):
	if req. method=='POST':
		name=req.POST['lang']
		url = "https://garudadevapi.herokuapp.com/GetTodaysMovies?lang="+name
		response = requests.request("GET", url)
		x=response.text
		#print(x)
		x=x.replace('<br>',':-')
		x=x.split(':-')
		t=[]
		tt=[]
		c=[]
		m=[]
		r=[]
		t1=[]
		c1=[]
		m1=[]
		r1=[]
		for i in range(len(x)):
			if i%2!=0:
				x1=x[i]
				x5=x1.split(":")[0]
				c.append(x5)
				x1=x1.replace(x5+':',"")
				o=x1
				if o[-1]==')' and o[-2]=='(':
					o=o[:-2]
					m.append(o)
					r.append("None")
				else:
					o=o[:-1]
					#print(o)	
					x3=o.split('(')
					#print(x3)
					m.append(x3[0])
					r.append(x3[1])
			
			else:
				t.append(x[i])
				k=x[i].split(':')
				tt.append(k[0])

		return render(req,'present1.html',{'x1':t,'x2':c,'x3':m,'x4':r}) 				
	return render(req,"all0.html")		

def test(req):
	if req. method=='POST':
		name=req.POST['lang']
		timer=req.POST['appt']
		#print("hello"+timer+"hii")
		url = "https://garudadevapi.herokuapp.com/GetTodaysMovies?lang="+name
		response = requests.request("GET", url)
		x=response.text
		#print(x)
		x=x.replace('<br>',':-')
		x=x.split(':-')
		t=[]
		tt=[]
		c=[]
		m=[]
		r=[]
		t1=[]
		c1=[]
		m1=[]
		r1=[]
		for i in range(len(x)):
			if i%2!=0:
				x1=x[i]
				x5=x1.split(":")[0]
				c.append(x5)
				x1=x1.replace(x5+':',"")
				o=x1
				if o[-1]==')' and o[-2]=='(':
					o=o[:-2]
					m.append(o)
					r.append("None")
				else:
					o=o[:-1]
					#print(o)	
					x3=o.split('(')
					#print(x3)
					m.append(x3[0])
					r.append(x3[1])
			
			else:
				t.append(x[i])
				k=x[i].split(':')
				tt.append(k[0])
		if timer==None:
			now = datetime.now()
			ct = now.strftime("%H")
		else:	
			timer=timer.split(':')
			ct=int(timer[0])
		tt=tt[:-1]
		for i in range(len(tt)):
			tt1=int(tt[i])
			#print(tt1)
			if (ct==tt1 or ct-1==tt1 or ct-2==tt1):
				t1.append(t[i])
				c1.append(c[i])
				m1.append(m[i])
				r1.append(r[i])
		#print(t1)
		return render(req,'present1.html',{'x1':t1,'x2':c1,'x3':m1,'x4':r1})  				
	return render(req,"selected.html")	
	
	
	
def present(req):
	if req. method=='POST':
		name=req.POST['lang']
		url = "https://garudadevapi.herokuapp.com/GetTodaysMovies?lang="+name
		response = requests.request("GET", url)
		x=response.text
		#print(x)
		x=x.replace('<br>',':-')
		x=x.split(':-')
		t=[]
		tt=[]
		c=[]
		m=[]
		r=[]
		t1=[]
		c1=[]
		m1=[]
		r1=[]
		for i in range(len(x)):
			if i%2!=0:
				x1=x[i]
				x5=x1.split(":")[0]
				c.append(x5)
				x1=x1.replace(x5+':',"")
				o=x1
				if o[-1]==')' and o[-2]=='(':
					o=o[:-2]
					m.append(o)
					r.append("None")
				else:
					o=o[:-1]
					#print(o)	
					x3=o.split('(')
					#print(x3)
					m.append(x3[0])
					r.append(x3[1])
			
			else:
				t.append(x[i])
				k=x[i].split(':')
				tt.append(k[0])

		IST = pytz.timezone('Asia/Kolkata')
		datetime_ist = datetime.now(IST)
		ct=datetime_ist.strftime(' %H')
		ct=int(ct)
		#print(ct)
		tt=tt[:-1]
		for i in range(len(tt)):
			tt1=int(tt[i])
			#print(tt1)
			if (ct==tt1 or ct-1==tt1 or ct-2==tt1):
				t1.append(t[i])
				c1.append(c[i])
				m1.append(m[i])
				r1.append(r[i])
		#print(t1)
		return render(req,'present1.html',{'x1':t1,'x2':c1,'x3':m1,'x4':r1}) 				
	return render(req,"present.html")	
	
