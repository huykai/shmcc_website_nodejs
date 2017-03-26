#coding=utf-8



import sys
import cx_Oracle
import time
import smtplib 
import xlsxwriter,xlrd

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.utils import COMMASPACE,formatdate  
from email import encoders  

import os



from MME_statis import *
from SAEGW_statis import *

#to_list=["13802500663@139.com"]
to_list=[]

#设置服务器，用户名、口令以及邮箱的后缀
mail_host="smtp.163.com"
mail_user="huykai"
mail_pass="huykai"
mail_postfix="163.com"
mail_sub="SHMCC PM Report"

def sort(A,num):
     for i in range(len(A)):
         (A[i][0],A[i][num])=(A[i][num],A[i][0])
     A.sort()
     #for i in range(len(A)):
     #    (A[i][0],A[i][num])=(A[i][num],A[i][0])
         

######################
def send_mail(to_list,sub,content):
    '''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(sendMailContent)
    msg['Subject'] = mail_sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False


sendMailContent=""
havePMProblem=0
mail_Contentlist=[]
result=[]

def sendMail(x,files):
	'''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
   '''
	me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
	#msg = MIMEText(sendMailContent)
	msg = MIMEMultipart()   
	msg['Subject'] = mail_sub
	msg['From'] = me
	msg['To'] = ";".join(to_list)
	msg.attach(MIMEText(x))   
	#print msg['To']
	try:
		s = smtplib.SMTP()
		s.connect(mail_host)
		s.login(mail_user,mail_pass)
		
		for f in files:   
			part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data   
			part.set_payload(open(f, 'rb').read())   
			encoders.encode_base64(part)   
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))   
			msg.attach(part) 

		
		s.sendmail(me, to_list, msg.as_string())
		s.close()
		return True
	except Exception, e:
		print str(e)
		return False

def makeContent(content,x):
	newcontent=[]
	newcontent.append(content[0])
	newcontent.append(x[1])
	newcontent.append(x[2])
	newcontent.append(x[3])
	newcontent.append(content[1])
	mail_Contentlist.append(newcontent)
	#print 'newcontent='+content[0]+'	'+x[1]+'	'+x[2]+','+x[3]+'	'+content[1]+'\n'
	return newcontent

def isPMhaveproblem(queryno,x,result):
	#for y in x:
	#	print str(y)+':'
	#print 
	havefound=0
	foundcontent=[]
	foundcontents=[]
	for pm_notify_level_r in pm_notify_level_records:
		#print pm_notify_level_r.queryno
		#print queryno
		if (int(pm_notify_level_r.queryno)!=int(queryno)):
			continue
		#print str(len(x))+':'+str(pm_notify_level_r.queryitem)+':'+str(pm_notify_level_r.pm_level)
		if (pm_notify_level_r.pm_level_compare=="<"):
			if (float(x[int(pm_notify_level_r.queryitem)-1])<float(pm_notify_level_r.pm_level)):
				#print pm_notify_level_r.pm_name+':'+x[0]+' '+x[1]+' '+x[2]+' '+x[3]+':'+x[pm_notify_level_r.queryitem-1]
				foundcontent.append(pm_notify_level_r.pm_name)
				foundcontent.append(str(x[int(pm_notify_level_r.queryitem)-1]))
				foundcontent.append(int(pm_notify_level_r.queryitem)-1)
				makeContent(foundcontent,x)
				#print 'result='+result
				havefound=1
				foundcontents.append(foundcontent)
				foundcontent=[]
		elif(pm_notify_level_r.pm_level_compare==">"):
			if (float(x[int(pm_notify_level_r.queryitem)-1])>float(pm_notify_level_r.pm_level)):
				#print pm_notify_level_r.pm_name+':'+x[0]+' '+x[1]+' '+x[2]+' '+x[3]+':'+x[pm_notify_level_r.queryitem-1]
				foundcontent.append(pm_notify_level_r.pm_name)
				foundcontent.append(str(x[int(pm_notify_level_r.queryitem)-1]))
				foundcontent.append(int(pm_notify_level_r.queryitem)-1)
				makeContent(foundcontent,x)
				#print 'result='+result
				havefound=1
				foundcontents.append(foundcontent)
				foundcontent=[]
	result=[]
	for i in range(len(foundcontents)):
		result.append(foundcontents[i])
	
	return  havefound,result

def writexlsxcell(pos,content,format):
	xlsxsheet.write(pos[0],pos[1],content,format)
	
def writexlsxrow(pos,content,result,format1,format2):
	for cellcontent in content:
		#if (pos[1])==3:
		#	xlsxsheet.write(pos[0],pos[1],cellcontent,format)
		#else:
		#	xlsxsheet.write(pos[0],pos[1],cellcontent,format)
		foundinresult=0
		if len(result)==0:
			writexlsxcell(pos,cellcontent,format1)
		else:
			for cs in result:
				if (pos[1]==cs[2]):
					writexlsxcell(pos,cellcontent,format2)
					foundinresult=1
					break
				else:
					continue
			if (foundinresult==0):
				writexlsxcell(pos,cellcontent,format1)
		
		pos[1]=pos[1]+1
	pos[0]=pos[0]+1
	pos[1]=0

def writexlsxhead(pos,content,format):
	for cellcontent in content:
		#if (pos[1])==3:
		#	xlsxsheet.write(pos[0],pos[1],cellcontent,format)
		#else:
		#	xlsxsheet.write(pos[0],pos[1],cellcontent,format)
		xlsxsheet.write(pos[0],pos[1],cellcontent,format)
		pos[1]=pos[1]+1
	pos[0]=pos[0]+1
	pos[1]=0
	
def writexlsxtitle(pos,length,content,format):
	pos[1]=0
	xlsxsheet.merge_range(pos[0],pos[1],pos[0],pos[1]+length,content[0],format)
	pos[0]=pos[0]+1

class pm_notify_level_record:
	def __init__(self):
		self.queryno=0
		self.queryitem=0
		self.pm_level_compare="<"
		self.pm_level=0
		self.pm_name=""
		
def init_pm_notify_level_record():
	pm_notify_level_records=[]
	pm_notify_level=open(".\\PM_Notify_Level.txt")
	pm_notify_level_strs=pm_notify_level.readlines()
	for pm_notify_level_str in pm_notify_level_strs:
		if(pm_notify_level_str.startswith('#')):
			continue
		pm_notify_level_items=pm_notify_level_str.split(':')
		if (len(pm_notify_level_items)<5):
			continue
		pm_notify_level_r=pm_notify_level_record()
		pm_notify_level_r.queryno=pm_notify_level_items[0]
		pm_notify_level_r.queryitem=pm_notify_level_items[1]
		pm_notify_level_r.pm_level_compare=pm_notify_level_items[2]
		pm_notify_level_r.pm_level=pm_notify_level_items[3]
		pm_notify_level_r.pm_name=pm_notify_level_items[4]
		pm_notify_level_records.append(pm_notify_level_r)
	return pm_notify_level_records
		
class notify_list_record:
	def __init__(self):
		self.name=0
		self.mailaddress=""
		
def init_notify_list_record():
	notify_list_records=[]
	notify_list=open(".\\Notify_List.txt")
	notify_list_strs=notify_list.readlines()
	for notify_list_str in notify_list_strs:
		if(notify_list_str.startswith('#')):
			continue
		notify_list_items=notify_list_str.split(':')
		if (len(notify_list_items)<2):
			continue
		notify_list_r=notify_list_record()
		notify_list_r.name=notify_list_items[0]
		notify_list_r.mailaddress=notify_list_items[1].rstrip('\n')
		notify_list_records.append(notify_list_r)
		to_list.append(notify_list_r.mailaddress)
	return notify_list_records
		
if __name__ == '__main__':

	#define sql param
	param=pm_sql_param()
	notify_list_records=init_notify_list_record()
	pm_notify_level_records=init_pm_notify_level_record()
	#define content array
	contentarray=[[]]
	
	stopdate=time.strftime('%Y/%m/%d',time.localtime(time.time()))
	startdate=time.strftime('%Y/%m/%d',time.localtime(time.time()-3600))
	curtime=time.strftime('%H',time.localtime(time.time()))
	curtime=curtime+":00"
	pretime=time.strftime('%H',time.localtime(time.time()-3600))
	pretimr=pretime+":00"
	#db = cx_Oracle.connect('omc', 'omc', '10.221.255.4:1521/OSS')
	(mmedbuser,mmedbpasswd,mmedburl)=getdbconfig("mmedb")
	#print mmedbuser,mmedbpasswd,mmedburl
	#mmedb = cx_Oracle.connect('omc', 'omc', '127.0.0.1:51063/oss')
	mmedb = cx_Oracle.connect(mmedbuser, mmedbpasswd, mmedburl)
	mmecursor=mmedb.cursor()
	(saegwdbuser,saegwdbpasswd,saegwdburl)=getdbconfig("saegwdb")
	#saegwdb = cx_Oracle.connect('kiu', 'antkiu123', '127.0.0.1:51064/OSS')
	saegwdb = cx_Oracle.connect(saegwdbuser, saegwdbpasswd, saegwdburl)
	saegwcursor=saegwdb.cursor()
	 #begin xlsx generate
	curtimehour=time.strftime('%Y%m%d%H',time.localtime(time.time()))
	curtimestr=curtimehour+":00"
	pretimehour=time.strftime('%Y%m%d%H',time.localtime(time.time()-3600))
	pretimestr=pretimehour+":00"
	xlsxfilename='.\\reports\\SHMCC_MME_PMStatistics_'+pretimehour+'_'+curtimehour+'.xlsx'
	xlsxfile = xlsxwriter.Workbook(xlsxfilename) 
	xlsxsheet = xlsxfile.add_worksheet()        
	
	#top = workbook.add_format({'border':1,'align':'center','bg_color':'cccccc','font_size':13,'bold':True})
	#green = workbook.add_format({'border':1,'align':'center','bg_color':'green','font_size':12})
	#yellow = workbook.add_format({'border':1,'bg_color':'yellow','font_size':12})
	xlsformat_red = xlsxfile.add_format({'border':1,'align':'center','bg_color':'red','font_size':12})
	xlsformat_title = xlsxfile.add_format({'border':1,'align':'center','bg_color':'green','text_wrap':1,'font_size':13})
	xlsformat_head = xlsxfile.add_format({'border':1,'align':'center','valign':'vcenter','bg_color':'gray','text_wrap':1,'font_size':12})
	xlsformat_data = xlsxfile.add_format({'border':1,'align':'right','font_size':12})
	xlsxsheet.set_column('A:AD',16,xlsformat_data)
	#blank = workbook.add_format({'border':1})
	xlsxsheetpos=[0,0]
	
	param.starttime=pretime
	param.stoptime=curtime
	param.startdate=startdate
	param.stopdate=stopdate
	

	#2g attach
	title,row=mme_2g_attach(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'2G Attach 统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(1,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	#print result
	
	#2g pdp
	title,row=mme_2g_pdp(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'2G PDP 统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(2,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# RAU 2G
	title,row=mme_2g_rau(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'2G RAU 统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(3,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# Paging 2G
	title,row=mme_2g_paging(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'2G PAGING 统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(4,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# Attach 3G and SRNS inter/intra
	
	title,row=mme_3g_attach(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'3G ATTACH 统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(5,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# PDP Activate 3G
	
	title,row=mme_3g_pdp(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'3G PDP 统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(6,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	# RAU 统计 3G
	title,row=mme_3g_rau(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'3G RAU 统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(7,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	# Paging 3G
	title,row=mme_3g_paging(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'3G PAGING 统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(8,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# 用户数统计 2/3G
	title,row=mme_users(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'用户数统计2/3/4G'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(9,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
		
	# Attach 4G & Service Request & MME S1/X2 inter/intra
	title,row=mme_4g_attach(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'4G 附着'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(10,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# pdp 4G
	title,row=mme_4g_pdp(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'4G PDN统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(11,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# TAU , Paging
	title,row=mme_4g_taupaging(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'4G TAU&Paging统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(12,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	# MME CPU
	title,row=mme_cpu(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'MME CPU统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(13,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	# 鉴权统计
	title,row=mme_4g_auth(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'4G 鉴权统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(14,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	# CSFB统计
	title,row=mme_4g_csfb(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'4G CSFB统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(15,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	# VoLTE统计
	title,row=mme_4g_volte(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'4G VOLTE统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(16,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_red)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	# SRVCC统计
	title,row=mme_4g_esrvcc(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'4G eSRVCC统计'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(17,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# saegw_4g_pgw��
	title,row=saegw_4g_pgw(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'4G PGW Session'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(18,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# saegw_4g_sgw��
	title,row=saegw_4g_sgw(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'4G SGW Session'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(19,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# saegw_4g_cdr_radius��
	title,row=saegw_4g_cdr_radius(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'4G PGW Radiu CDR'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(20,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# saegw_23g��
	title,row=saegw_23g(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u'23G PDP'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(21,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# pgw_sgw_throughput��
	title,row=pgw_sgw_throughput(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u' PGW SGW Throughput'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(22,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# saegw_gtpu_throughput��
	title,row=saegw_gtpu_throughput(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u' PGW GTPU Throughput'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(23,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# saegw_s1u_throughput��
	title,row=saegw_s1u_throughput(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u' PGW S1U Throughput'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(24,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# saegw_s1u_throughput��
	title,row=saegw_s1u_throughput(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u' PGW S1U Throughput'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(24,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# saegw_session
	title,row=saegw_session(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u' SAEGW Session Statistics'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(25,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# saegw_sgi_throughput
	title,row=saegw_sgi_throughput(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u' SAEGW Sgi throughput'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(26,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	# saegw_ip_pool
	title,row=saegw_ip_pool(saegwcursor,param)
	if title[0]!='error' and len(row)>0:
		writexlsxtitle(xlsxsheetpos,len(row[0])-1,[u' SAEGW IPPOOL Statistics'],xlsformat_title)
		writexlsxhead(xlsxsheetpos,title,xlsformat_head)
		for x in row:
			(isP,result)=isPMhaveproblem(27,x,result)
			if (isP==1):
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
			else:
				writexlsxrow(xlsxsheetpos,x,result,xlsformat_data,xlsformat_data)
	
	
	#last phase 	

	xlsxfile.close()
	
	
	sendMailContent="""
Hi,��λͬ��

������"""
	prehour=pretimehour[-2:]
	curhour=curtimehour[-2:]
	#curday=pretimehour[0:8]
	curmon=pretimehour[4:6]
	curyear=pretimehour[0:4]
	curday=pretimehour[6:8]	
	sendMailContent=sendMailContent+curyear+"��"+curmon+"��"+curday+"��"+prehour+"��"+curhour+"���ͳ������"
					
	files=[]
	files.append(xlsxfilename)
		
	sendMail(sendMailContent,files)
	
	
	#if __name__ == '__main__':
	#    if send_mail(mailto_list,"subject","content"):
	#        print "发送成功"
	#    else:
	#        print "发送失败"
	
	