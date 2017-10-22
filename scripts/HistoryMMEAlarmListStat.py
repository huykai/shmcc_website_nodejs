
#coding=utf-8



import cgi
import cx_Oracle
import time


# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
curdate=time.strftime('%Y/%m/%d',time.localtime(time.time()))
curtime=time.strftime('%H',time.localtime(time.time()))
#curdatetime=time.strftime('%Y/%m/%d/%H:%M',time.localtime(time.time()))
# Get data from fields
location = form.getvalue('location')
if (location == None):
	location=1

selectsgsn=form.getvalue('selectsgsnname')
if(selectsgsn==None):
	selectsgsn='all'
startdate = form.getvalue('selectstartdate')
if (startdate == None):
	startdate=curdate
stopdate = form.getvalue('selectstopdate')
if (stopdate == None):
	stopdate=curdate
starttime = form.getvalue('selectstarttime')
if (starttime == None ):
	starttime="00"
stoptime = form.getvalue('selectstoptime')
if (stoptime == None):
	stoptime=curtime

selectalarm = form.getvalue('selectalarm')
if (selectalarm == None or selectalarm==''):
	selectalarm='all'
	
startdatetime=startdate+"/"+starttime+":00"
stopdatetime=stopdate+"/"+stoptime+":00"
#print curtime
db = cx_Oracle.connect('kiu', 'antkiu123', '10.221.213.28:1521/OSS')
cursor=db.cursor()


# ALARM
sqlstring="""
select
alarm_number,count(*),
max(alarm_type),max(severity),
max(text)
from fx_alarm,objects
where 
NE_ID=objects.int_id and (objects.object_class=463 or objects.object_class=3766 )
"""

if (selectsgsn!='all'):
	sqlstringsgsn=" and objects.name=\'"+selectsgsn+"\' " 
else:
	sqlstringsgsn=" "
	
if (selectalarm!='all'):
	sqlstringalarm=" and alarm_number=\'"+selectalarm+"\' "
else:
	sqlstringalarm=" "
	
sqlstringtime=" and to_char(fx_alarm.alarm_time,\'yyyy/mm/dd/hh24:mi\')<\'"+stopdatetime+"\' and to_char(fx_alarm.alarm_time,\'yyyy/mm/dd/hh24:mi\')>\'"+startdatetime+"\' "

sqlstringgroup="""
group by alarm_number
order by count(*) desc
"""

sqlstring=sqlstring+sqlstringsgsn+sqlstringalarm+sqlstringtime+sqlstringgroup 
#print sqlstring

cursor.execute(sqlstring)

row=cursor.fetchall()


print 'Status: 200 OK'
print 'Content-type: text/xml charset=GB2312;\n'


print "<?xml version=\"1.0\" encoding=\"GB2312\"?>"
print "<response>"
print "<location>"
print "<locationid>1</locationid>"
print "<passed>true</passed>"
print "<message>现网告警</message>"
print "<Title>"
print "<name>告警号</name>"
print "<name>告警数量</name>"
print "<name>告警类型</name>"
print "<name>告警级别</name>"
print "<name>告警描述</name>"
print "</Title>"

for x in row:
	print "<Item>"
	for y in x:
		print "<ItemCol>"
		print "<value>"
		print y
		print "</value>"
		print "</ItemCol>"
	print "</Item>"

print "</location>"



print "</response>"
