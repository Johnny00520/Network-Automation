import sys, subprocess, smtplib, os
from scapy.all import *

# Reference https://scapy.net/
# If you want to test this program, simply change
# toAddr as your email address

#To restore previously saved pcap file:
pcapFile = rdpcap("tcpdump-obj4-3.pcap")

v2_alert = pcapFile[10].show(dump=True)
v2_alert2 = pcapFile[12].show(dump=True)
v3_alert = pcapFile[27].show(dump=True)
v3_alert2 = pcapFile[29].show(dump=True)
v3_alert3 = pcapFile[31].show(dump=True)
v3_alert4 = pcapFile[33].show(dump=True)
v3_alert5 = pcapFile[35].show(dump=True)

toAddr = "chch6597@colorado.edu"
fromAddr = "chch6597@colorado.edu"
email_username = "chch6597@colorado.edu"
userPwd = 'johnny_77520'
server = smtplib.SMTP("smtp.gmail.com:587")
server.ehlo()
server.starttls()
server.login(email_username, userPwd)

header = 'To:' + toAddr + '\n' + 'From: ' + email_username + '\n' + 'Subject: Trap Report of your network \n'
message = " \n" + header + "\n\n " + v2_alert + "\n\n" + v2_alert2 + "\n\n" + v3_alert + "\n\n" + v3_alert2 + "\n\n" + v3_alert3 + "\n\n" + v3_alert4 + "\n\n" + v3_alert4 + "\n\n" + v3_alert5

server.sendmail(toAddr, fromAddr, message)
server.quit()


