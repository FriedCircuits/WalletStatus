#! /usr/bin/python
#Wallet Status - William Garrido - License - CC-SA
#http://mobilewill.us and http://github.com/friedcircuits

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from urllib2 import urlopen, Request
import urllib2
import re
import time

#Base URL - 1: P2Pool Static 2: Address stats 3: Address balance API
poolURL = 'http://poolURL/static/'
URLAdd = 'http://explorer.vertcoin.org/address/'
URLBal = 'http://explorer.vertcoin.org/chain/Vertcoin/q/addressbalance/'

#Wallet IDs to check
wallets = ['wallet1', 'wallet2']
balance = [0, 0]
#hashRate = [0,0]
transactions = [0,0]
coin = 'Vertcoin'
coinShort = 'VTC'
transOut = 0

failCount = 0
totalFailed = 0
totalRuns = 0


#Time in between checks in seconds
checkTimer = 900 
failTimer = 120

firstRun = 1

#Gmail Settings
GMAIL_USER = 'user@domain.com'
GMAIL_PASS = 'password'
SMTP_SERVER = 'smtp.server.com'
SMTP_PORT = 587
RECIPIENT = 'user@domain.com'


def send_email(recipient, subject, text, html):
    smtpserver = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = recipient
    
    #Old code below
    #header = 'To:' + recipient + '\n' + 'From: ' + GMAIL_USER
    #header = header + '\n' + 'Subject:' + subject + '\n'
    #msg = header + '\n' + text + ' \n\n'
    
    html = """\
    <html>
       <head></head>
         <body>
           <p>"""+html+"""\
	  </p>
       </body>
    </html>
    """ 
    
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    
    smtpserver.sendmail(GMAIL_USER, recipient, msg.as_string())
    smtpserver.close()
    
#Searches site for current transactions
def get_trans(soupAdd, wallet_id):
	x = soupAdd.find(text=re.compile("Transactions in:"))
	trans = x.split(':')
	trans = trans[1]
	x = soupAdd.find(text=re.compile("Transactions out:"))
	transOut = x.split(':')
	trans = int(trans) + int(transOut[1])
	#print transOut[1]
	return trans
	

#Searches site for pool stats (not working, site dyanmicly loads nodes miners
def get_poolStats(soupPool, wallet_id):
	x = soupPool.find(text=re.compile(wallet_id))
	#x = str(x)
	#name = x.split(':')
	#name = name[0]
	print x
	return x



#Loops through each wallet id and check if transaction count has changed since last check, compiles into email body and sends if there is data
#First run change says 0	
email_body=""
loop = 1
print '______________________'
while loop == 1 :
 	
 	email_body=""
 	email_body_html=""
 	failCount = 0
 	totalRuns += 1
	for idx in range(0, len(wallets)):
		wallet_id = wallets[idx]
		transURL = URLAdd + str(wallet_id)
		balURL = URLBal + wallet_id
		user_agent = 'Mozilla/5.0'
		#print URL2

		try:
		     req = Request(balURL, headers = {'User-Agent' : user_agent})
		     balpage = urlopen(req).read()
		except urllib2.HTTPError, e:
		     #print e.fp.read()
		     print 'HTTP Error: ' + str(e.code)
		     print 'Balance fetch failed'
		     failCount += 1
		     break

		#print balpage
		
		try:
		     req2 = Request(transURL, headers = {'User-Agent' : user_agent}) 
		     transpage = urlopen(req2).read()
		except urllib2.HTTPError, e:
		     #print e.fp.read()
		     print 'HTTP Error: ' + str(e.code)
		     print 'Transaction fetch failed' 
		     failCount += 1
		     break
		     
		try:
		     req3 = Request(poolURL, headers = {'User-Agent' : user_agent}) 
		     poolpage = urlopen(req3).read()
		except urllib2.HTTPError, e:
		     #print e.fp.read()
		     print 'HTTP Error: ' + str(e.code)
		     print 'Pool fetch failed'
		     failCount += 1
		     break
		     	     


		soupAdd = BeautifulSoup(transpage)
		soupPool = BeautifulSoup(poolpage)
		
		transCount = get_trans(soupAdd, wallet_id)
		#poolStats = get_poolStats(soupPool, wallet_id)
		
		
		balNow = balpage
		if (balNow != balance[idx]):
			balChange = float(balNow) - float(balance[idx])
			transChange = int(transCount) - int(transactions[idx])
			balance[idx] = balNow
			transactions[idx] = transCount
			if (firstRun):
				balChange = 0
				transChange = 0
			
			
			email_body += str(wallet_id) + ' currently has ' + str(balNow) +  coinShort + '. Tranactions in: ' + str(transCount) + ' Transactions out: ' + str(transOut) + '. Change: ' + str(balChange) + coinShort + ', in ' + str(transChange) + ' transactions, ' + ' in the past ' + str(checkTimer/60) + ' minutes\n'
			email_body_html += '<FONT COLOR=blue><b><a href=' + transURL + '> ' + str(wallet_id) + '</a>: </b></FONT>' + '<BR> Currently has <FONT COLOR=RED><b>' + str(balNow) + '</b></FONT>' + coinShort + ' <BR> Transactions in: <FONT COLOR=RED><b>' + str(transCount) + '</b></FONT> <BR> Transactions out: <FONT COLOR=RED><b>' + str(transOut) + '</b></FONT><BR> Change: <FONT COLOR=RED><b>' + str(balChange) + '</b></FONT> ' + coinShort + ', in <FONT COLOR=RED><b>' + str(transChange) + '</b></FONT> transactions, in the past <FONT COLOR=BLUE><b>' + str(checkTimer/60) + '</b></FONT> minutes<br><br>\n'
		
	if (email_body != ""):
		email_body_html += '<B>Failed fetch error count: </B>' + str(failCount) + '\n'	
		print email_body
		send_email(RECIPIENT, coin + '-P2Pool - Current Status', email_body, email_body_html)
	else:
		if (failCount == 0):     
		     print "No Change"
		else:
		     print 'Complete fetch failure'
	
	#Check if we had a failed fetch if so try again. If first run flag won't be cleared till we have a successfull fetch
	if (failCount > 0):
	     totalFailed += 1
	     print 'Failed Fetch Count: ' + str(failCount)
	     print 'Running total failed runs: ' + str(totalFailed)
	     print 'Total runs: ' + str(totalRuns)
	     print 'Percent failed ' + str((totalRuns/totalFailed)*100) + '%'
	     print 'Error: Waiting to try again in ' + str(failTimer) + ' seconds'
	     time.sleep(failTimer)
	else:	
	     firstRun = 0			
	     time.sleep(checkTimer)
	     
	print '______________________'
	
print "Done"
