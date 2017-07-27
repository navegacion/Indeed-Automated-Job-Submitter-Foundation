import urllib.request
import json
import time, os
from datetime import datetime
import http.cookiejar, urllib.request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import random
from bs4 import BeautifulSoup
import http.cookiejar
import requests
import logging
import http.client as http_client
from requests_toolbelt import MultipartEncoder
import re

def html_decode(s):
	htmlCodes = (("'", '&#39;'),('"', '&quot;'),('>', '&gt;'),('<', '&lt;'),('&', '&amp;'))
	for code in htmlCodes:
		s = s.replace(code[1], code[0])
	return s

def grab_apply_url(job_id):
	keys = ["jobId", "jobTitle", "jobCompany", "jobLocation", "jobUrl", "jobMeta", "jk", "postUrl", "coverletter", "continueUrl", "jobLong", "jobState", "jobCity", "jobKey", "ecu", "logTk", "logType", "flowPage", "flowType", "resume", "postFormat", "apiToken", "co", "pingbackUrl"]

	httpReq = urllib.request.Request("https://www.indeed.com/m/viewjob?jk=" + job_id)
	httpReq.add_header('User-Agent', 'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0')
	r = str(urlopen(httpReq).read())

	values = [r.split("jobid=\\'")[1].split("\\'")[0], r.split("jobtitle=\\'")[1].split("\\'")[0], r.split("jobcompanyname=\\'")[1].split("\\'")[0], r.split("joblocation=\\'")[1].split("\\'")[0], r.split("joburl=\\'")[1].split("\\'")[0], r.split("jobmeta=\\'")[1].split("\\'")[0], r.split("jk=\\'")[1].split("\\'")[0], r.split("posturl=\\'")[1].split("\\'")[0], r.split("coverletter=\\'")[1].split("\\'")[0], r.split("continueUrl=\\'")[1].split("&amp;")[0], r.split("jobLong=")[1].split("&amp;")[0], r.split("jobState=")[1].split("&amp;")[0], r.split("jobCity=")[1].split("&amp;")[0], r.split("jobKey=")[1].split("&amp;")[0], r.split("ecu=")[1].split("&amp;")[0], r.split("logTk=")[1].split("&amp;")[0], r.split("logType=")[1].split("&amp;")[0], r.split("flowPage=")[1].split("&amp;")[0], r.split("flowType=")[1].split("\\'")[0], r.split("resume=\\'")[1].split("\\'")[0], "JSON", r.split("apitoken=\\'")[1].split("\\'")[0], r.split("co=")[1].split("\\'")[0], r.split("pingbackUrl=\\'")[1].split("&amp;")[0]]

	dic = {}

	for key in keys:
		dic.update({key:values[keys.index(key)]})

	if("questions" in r):
		dic.update({"questions":r.split("questions=\\'")[1].split("\\' ")[0]})

	job_apply_url = "https://apply.indeed.com/indeedapply/resumeapply?"

	for key, value in dic.items():
		job_apply_url += key + "=" + urllib.parse.quote_plus(value) + "&"

	job_apply_url = job_apply_url[:-1]

	httpReq = urllib.request.Request(job_apply_url)
	httpReq.add_header('User-Agent', 'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0')
	r = str(urlopen(httpReq).read())


	keys.extend(["mob", "hl", "mode"])
	values.extend(["1", "en_US", "upload"])

	for key in keys:
		dic.update({key:values[keys.index(key)]})

	job_apply_url = "https://apply.indeed.com/indeedapply/resumeapply?"

	for key, value in dic.items():
		job_apply_url += key + "=" + urllib.parse.quote_plus(value) + "&"

	job_apply_url = job_apply_url[:-1]

	return job_apply_url

jobappurl = grab_apply_url("8d59d6cfbdcf3405") # this is the job's ID e.g. https://www.indeed.com/cmp/National-Franchise/jobs/Full-Charge-Bookkeeper-Must-Have-Quickbook-Experience-8d59d6cfbdcf3405?sjdu=QwrRXKrqZ3CNX5W-O9jEvdYCwLOj3wp-6rgZDaxa_7D1geRaWqZjdl7uzBuT5xm3AE6JEGkSzcaoqX7dWI8rk_HROYK8m_iX3bonLcI-K9fkl2lDFN6tXJRai125ruu7kUZFzEAa20OEr3Bui-ewRg -> 8d59d6cfbdcf3405 is the ID you'd put in here.

httpReq = urllib.request.Request(jobappurl)
httpReq.add_header('User-Agent', 'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0')
r = str(urlopen(httpReq).read().decode('utf8'))

soup = BeautifulSoup(r, "html.parser")

dic = {}

form = soup.find('form')
inputs = form.find_all('input')

questions = {}
questions_log = []

for f in inputs:
	key = f['name']
	value = f['value']
	if("q_" in key and key not in questions):
		questions.update({key:value})
		questions_log.extend([key])
	else:
		dic.update({key:value})

for i in range(len(questions_log)):
	while True:
		try:
			question_orginal = str(soup.find('label', {'id': 'q_' + str(i) + '_label'}).text)
			question_ask = str(input(question_orginal[:-2] + (" [y|n]")))
		except ValueError:
			continue
		else:
			questions[questions_log[i]] = question_ask
			break

for key, value in questions.items():
	dic.update({key:value})


dic["applicant.name"] = "Jon Doe"
dic["applicant.email"] = "jon.doe@mail.com"
dic["applicant.applicationMessage"] = "Joe doe was here."
dic["retypeemail_visible"] = "1"
dic["applicant.retypeEmail"] = "jon.doe@mail.com"

dic.update({'resume': ('resume.docx', open('resume.docx', 'rb'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})

datas = MultipartEncoder(dic)
httpReq = requests.post("https://apply.indeed.com/indeedapply/applyv2?hl=en_US", data=datas, headers={"Content-Type": datas.content_type})
r = httpReq.content.decode('utf8')

f = open("f.html", "w")
f.write(r)
f.close