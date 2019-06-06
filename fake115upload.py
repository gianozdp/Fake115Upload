#coding: utf-8
__author__ = 'T3rry'

import os,sys
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder 
import json
import hashlib
import getopt
import codecs
#############################################################  Need your cookie
COOKIESTEXT="your cookie"
#############################################################  Need your cookie
COOKIES={}
user_id=""
userkey=""
target="U_1_0"
end_string="000000"
app_ver='11.2.0'
pickcode=""
FileCount=0
header = { "User-Agent" : 'Mozilla/5.0  115disk/11.2.0'}

def usage():
    print(
"""
Usage:sys.args[0] [option]
-l filename: Upload a file form local
-i filename: Import files form hash lists
-o filename: Export all hash to lists from 115
"""
)

def Upload_files_by_sha1_from_links(file):  #link sample : 1.mp4|26984894148|21AEB458C98643D5E5E4374C9D2ABFAAA4C6DA6
	if GetUserKey()==False:
		return
	for l in open(file,'r'):
		link=l.split('|')
		filename=link[0]
		filesize=link[1]
		fileid=link[2].strip()
		if(len(fileid)!=40):
			print 'Error links'
			return
		Upload_file_by_sha1(fileid,filesize,filename)

def GetFileSize(file):
	return os.path.getsize(file)

def GetUserKey():
	global user_id,userkey
	try:
		AddCookie(COOKIESTEXT)
		r = requests.get("http://proapi.115.com/app/uploadinfo",headers=header,cookies=COOKIES)
		resp=json.loads(r.content) 
		user_id=str(resp['user_id'])
		userkey=str(resp['userkey']).upper()
	except Exception as e:
		print "Error cookies"
		return False

def AddCookie(cook):
	for line in COOKIESTEXT.split(';'):
		if line:
			name,value=line.strip().split('=',1)  
			COOKIES[name]=value 

def Upload_file_by_sha1(fileid,filesize,filename):  #quick
	fileid=fileid.upper()
	quickid=fileid
	hash=hashlib.sha1((user_id+fileid+quickid+pickcode+target+'0')).hexdigest()
	a=userkey+hash+end_string
	sig=hashlib.sha1(a).hexdigest().upper()
	URL="http://uplb.115.com/3.0/initupload.php?isp=0&appid=0&appversion=11.2.0&format=json&sig="+sig
	postData={
				'preid':'',
				'filename':filename,
				'quickid':fileid,
				'user_id':user_id,
				'app_ver':app_ver,
				'filesize':filesize,
				'userid':user_id,
				'exif':'',
				'target':target,
				'fileid':fileid
			  }
	r = requests.post(URL, data=postData,headers=header)
	print(r.text)

def Upload_file_from_local(filename):  #slow
	uri='http://uplb.115.com/3.0/sampleinitupload.php'
	AddCookie(COOKIESTEXT)
	postdata={"userid":user_id,"filename":filename,"filesize":GetFileSize(filename),"target":target}
	r = requests.post(uri,headers=header,cookies=COOKIES,data=postdata)
	resp=json.loads(r.content) 
	print resp
	req_headers = {'Content-Type': "multipart/form-data; boundary=----7d4a6d158c9"}
	m = MultipartEncoder(fields=[('name', filename), 
                             ('key', resp['object']),
                             ('policy',resp['policy']),
                             ('OSSAccessKeyId', resp['accessid']),
                             ('success_action_status', '200'),
                             ( 'callback',resp['callback']),
                             ('signature',resp['signature']),
                             ('file',(filename,open(filename, 'rb'), 'video/mp4'))],
                     		 boundary='----7d4a6d158c9'
                    )
	r = requests.post(resp['host'],headers=req_headers,data=m)
	print r.content
	
def Export_115_sha1_to_file(outfile,cid='0'): #
	global FileCount
	uri="http://webapi.115.com/files?aid=1&cid="+cid+"&o=user_ptime&asc=0&offset=0&show_dir=1&limit=5000&code=&scid=&snap=0&natsort=1&source=&format=json"
	url='http://aps.115.com/natsort/files.php?aid=1&cid='+cid+'&o=file_name&asc=1&offset=0&show_dir=1&limit=5000&code=&scid=&snap=0&natsort=1&source=&format=json&type=&star=&is_share=&suffix=&custom_order=&fc_mix='
	AddCookie(COOKIESTEXT)
	resp=''
	r = requests.get(uri,headers=header,cookies=COOKIES)
	if(json.loads(r.content).has_key('data')):
		resp=json.loads(r.content)['data']
	else:
		r = requests.get(url,headers=header,cookies=COOKIES)
		resp=json.loads(r.content)['data']
	of= codecs.open(outfile,'a+', encoding='utf-8')
	for d in resp:	
		if d.has_key('fid'):
			FileCount+=1
			try:
				print d['n'],d['s'],d['sha']
				of.write(d['n']+'|'+str(d['s'])+'|'+d['sha']+'\n')
			except:
				of.write(d['n']+'|'+str(d['s'])+'|'+d['sha']+'\n')
			continue
		elif  d.has_key('cid'):
			Export_115_sha1_to_file(outfile,d['cid'])
	of.close()
			
if __name__ == '__main__':
	if len(sys.argv) == 1:
		usage()
		sys.exit()
	try:
		opts, args = getopt.getopt(sys.argv[1:], "l:i:o:", ["help", "output="])
		for n,v in opts:
			if n in ('-l','--local'):
				Upload_file_from_local(v)	
			elif n in ('-i','--infile'):
				Upload_files_by_sha1_from_links(v)				
			elif n in ('-o','--outfile'):
				Export_115_sha1_to_file(v)
				print 'Total files count:',FileCount
				
	except getopt.GetoptError:
		print("argv error,please input")
		
