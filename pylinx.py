#!/usr/bin/python
# Author : Linggar Primahastoko
# Updated Januari 2011
# Add who's unfollow you feature

import tweepy
import fileinput
import httplib
import urllib
import urllib2
import re
import getpass
import os
import sys

CONSUMER_KEY = '8NqlAlI5IFwKKS7eIKWWww'
CONSUMER_SECRET = 'xRIkqJYcBuQjfNU85JVx7O80qKjcwrZwt9qF3qc'


def menu():
	print "------------------------------------"
	print "Twittering with Pylinx        "
	print "need a tweepy module to be installed"
	print "------------------------------------"
	print ""
	print "1. update your status"
	print "2. read your timeline"
	print "3. read your mention"
	print "4. read your direct messages"
	print "5. search"
	print "6. who unfollow you? (new feature)"
	print "7. exit (without logout)"
	print "8. logout"
	print ""
	return input("choose : ")

def pintwit(auth_url):
	global pin

	header = {'Content-type':'application/x-www-form-urlencoded','accept':'text/plain'}

	urlpertama = urllib2.urlopen(auth_url)
	cari1 = re.compile('authenticity_token" type="hidden" value="(.*)"')
	a = re.findall(cari1,urlpertama.read())[0]
	urlpertama.close()
	
	urlpertama = urllib2.urlopen(auth_url)
	cari2 = re.compile('oauth_token" type="hidden" value="(.*)"')
	b = re.findall(cari2,urlpertama.read())[0]
	urlpertama.close

	x = raw_input("input username or email : ")
	y = getpass.getpass()
	
	data = {'authenticity_token':a,'oauth_token':b,'session[username_or_email]':x,'session[password]':y}
	params = urllib.urlencode(data)
	con = httplib.HTTPSConnection("twitter.com:443")
	con.request('POST','/oauth/authorize',params,header)
	response = con.getresponse()
	cari = re.compile('<code>(.*)</code>')
	pin_pertama = re.findall(cari,response.read())
	try:
		pin = pin_pertama[0]
	except:
		print "\nwrong username or password :)\n"
		main()
	return pin

def update_stat(x):
	api.update_status(x)
	print "Twitted!"
	print "\n"

def read_time():
	timeline = api.home_timeline()
	for i in timeline:
		print "--------------------------------------"
		print i.user.screen_name
		print i.text
		print "via", i.source
		print "--------------------------------------"
		print "\n"

def read_ment():
	mention = api.mentions()
	for i in mention:
		print "--------------------------------------"
		print i.user.screen_name
		print i.text
		print "via", i.source
		print "--------------------------------------"
		print "\n"

def search_text(x):
	searching = api.search(x)
	for i in searching:
		print "--------------------------------------"
		print i.from_user
		print i.text
		print "--------------------------------------"
		print "\n"

def directs():
	messages = api.direct_messages()
	for i in messages:
		print "--------------------------------------"
		print i.sender.screen_name
		print i.text
		print "--------------------------------------"
		print "\n"
		
def logout():
	os.remove(".xzsdasAA")
	print "thank's for using pylinx :)"
	sys.exit()

def buatbaru():
		openfile = open("follower.txt", "w")
		openfile.write(nama_user.screen_name + "\n\n")
		for i in tweepy.Cursor(api.followers).items():
			openfile.write(i.screen_name.rstrip() + "\n")
		openfile.close()
		print "updated the follower database"
		print "do it again next time if you feel any changes with your follower/following :)"
		main()
		
def cekunfollow():
	a = []
	b = []
	
	print "gathering the information...take time..."
	
	if not os.path.exists("follower.txt"):
		buatbaru()

	openfile = open("follower.txt","r")
	if openfile.readlines()[0].rstrip() != nama_user.screen_name:
		openfile.close()
		buatbaru()
	else:
		openfile = open("follower.txt","r")
		for y in openfile.readlines()[2:]:
			a.append(str(y.rstrip()))
		openfile.close()
		
	for i in tweepy.Cursor(api.followers).items():
		b.append(i.screen_name) 

	jadi = list(set(a) & set(b))
	anfol = []
	fol = []

	for j in a:
		if j.rstrip() not in jadi:
			anfol.append(j.rstrip())

	for k in b:
		if k.rstrip() not in jadi:
			fol.append(k.rstrip())

	if len(anfol) == 0:
		text1 = "there is no person unfollowing you :)"
	else:
		anpolo = ""
		for i in anfol:
			anpolo = anpolo + "\n" + i.rstrip()
		text1 = "who unfollow you : %s" % anpolo

	if len(fol) == 0:
		text2 = "there is no person following you :("
	else:
		polo = ""
		for i in fol:
			polo = polo + "\n" + i.rstrip()
		text2 = "who is your new follower : %s" % polo

	print text1
	print text2

	buatbaru()	

def main():
	global api
	global ACCESS_KEY
	global ACCESS_SECRET
	global nama_user

	if not os.path.exists(".xzsdasAA"):

		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth_url = auth.get_authorization_url()
		pintwit(auth_url)
		verifier = pin
		auth.get_access_token(verifier)
		ACCESS_KEY = auth.access_token.key
		ACCESS_SECRET = auth.access_token.secret
		keys = ACCESS_KEY
		sec = ACCESS_SECRET

		openfile = open('.xzsdasAA','w')
		kuncistring = str(keys)
		openfile.write(kuncistring)
		openfile.write("\n")
		secstring = str(sec)
		openfile.write(secstring)
		openfile.close()
	
	N = 1                                                                                                                                                                                                                          
	openfile = open('.xzsdasAA', 'r')                                                                                                                                                                                               
	for i in range(N):                                                                                                                                                                                                             
	      ACCESS_KEY = openfile.next().strip()                                                                                                                                                                                         
	openfile.close()

	N = 2                                                                                                                                                                                                                          
	openfile = open('.xzsdasAA', 'r')                                                                                                                                                                                               
	for i in range(N):                                                                                                                                                                                                             
	      ACCESS_SECRET = openfile.next().strip()
	openfile.close()
	
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	nama_user = api.me()

	loop = 1
	choice = 0

	while loop == 1:
		choice = menu()
		if choice == 1:
			update_stat(raw_input("your status : "))
		elif choice == 2:
			read_time()
		elif choice == 3:
			read_ment()
		elif choice == 4:
			directs()
		elif choice == 5:
			search_text(raw_input("input your search: "))
		elif choice == 6:
			cekunfollow()
		elif choice == 7:
			sys.exit()
		elif choice == 8:
			logout()
		else:
			print "please input the correct number :)"

if __name__ == "__main__":
	main()
