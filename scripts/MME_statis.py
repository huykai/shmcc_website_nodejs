#coding=utf-8

#class pm_sql_param:
#	def __init__(self):
#		self.startdate=""
#		self.stopdate=""
#		self.starttime=""
#		self.stoptime=""
#		self.selectperiod=15
#		self.selectperiodtype='continue'
#		self.selectmmeelement="MMESGSN"
#		self.selectmmesgsn="all"

from GetConfig import *
# Attach 2G
#
def mme_2g_attach(cursor,param):
	title=[
	u"设备ID",
	u"设备名称",
	u"日期",
	u"时间",
	u"附着成功次数2G",
	u"附着失败次数2G",
	u"用户原因附着失败次数2G",
	u"附着成功率2G",
	u"去除用户原因附着成功率"
	]
	

	if (param.selectperiod=='60'):
		sqlstring="""
select  
twog.fins_id,
objects.CO_NAME MMESGSN, 
to_char(twog.period_start_time,'yyyy/mm/dd') Sdate,
to_char(twog.period_start_time,'hh24') Stime, 
sum(SUCC_GPRS_ATTACH+SUCC_COMBINED_ATTACH) attachsucccount, 
sum(FAIL_GPRS_ATTACH_GEN+FAIL_COMB_ATTACH_GEN-FAIL_GPRS_ATTACH_DUE_MS_ERR-FAIL_GPRS_ATTACH_COLLISIONS) attachfailcount, 
sum(FAIL_GPRS_ATTACH_SIM_NOT_PROV+FAIL_GPRS_ATTACH_ILLEGAL_MS+FAIL_GPRS_ATTACH_ILLEGAL_ME+FAIL_GPRS_ATTACH_SER_NONSER_NA) userfailcount, 
decode(nvl((sum(SUCC_GPRS_ATTACH+FAIL_GPRS_ATTACH_GEN+SUCC_COMBINED_ATTACH+FAIL_COMB_ATTACH_GEN-FAIL_GPRS_ATTACH_DUE_MS_ERR-FAIL_GPRS_ATTACH_COLLISIONS)),0),0,0,(round((sum(SUCC_GPRS_ATTACH+SUCC_COMBINED_ATTACH)/(sum(SUCC_GPRS_ATTACH+FAIL_GPRS_ATTACH_GEN+SUCC_COMBINED_ATTACH+FAIL_COMB_ATTACH_GEN-FAIL_GPRS_ATTACH_DUE_MS_ERR-FAIL_GPRS_ATTACH_COLLISIONS))),4)*100)) attachratio,
decode(nvl((sum(SUCC_GPRS_ATTACH+FAIL_GPRS_ATTACH_GEN+SUCC_COMBINED_ATTACH+FAIL_COMB_ATTACH_GEN-FAIL_GPRS_ATTACH_DUE_MS_ERR-FAIL_GPRS_ATTACH_COLLISIONS-FAIL_GPRS_ATTACH_SIM_NOT_PROV-FAIL_GPRS_ATTACH_ILLEGAL_MS-FAIL_GPRS_ATTACH_ILLEGAL_ME-FAIL_GPRS_ATTACH_SER_NONSER_NA)),0),0,0,(round((sum(SUCC_GPRS_ATTACH+SUCC_COMBINED_ATTACH)/(sum(SUCC_GPRS_ATTACH+FAIL_GPRS_ATTACH_GEN+SUCC_COMBINED_ATTACH+FAIL_COMB_ATTACH_GEN-FAIL_GPRS_ATTACH_DUE_MS_ERR-FAIL_GPRS_ATTACH_COLLISIONS-FAIL_GPRS_ATTACH_SIM_NOT_PROV-FAIL_GPRS_ATTACH_ILLEGAL_MS-FAIL_GPRS_ATTACH_ILLEGAL_ME-FAIL_GPRS_ATTACH_SER_NONSER_NA))),4)*100)) nonusersuccratio
from 	PCOFNS_PS_GMMLR_CI3_RAW twog,  
			UTP_COMMON_OBJECTS objects 
where 
twog.FINS_ID=objects.CO_GID 
""" 

	else:
		sqlstring="""
select  
twog.fins_id,
objects.CO_NAME MMESGSN, 
to_char(twog.period_start_time,'yyyy/mm/dd') Sdate,
to_char(twog.period_start_time,'hh24:mi') Stime, 
sum(SUCC_GPRS_ATTACH+SUCC_COMBINED_ATTACH) attachsucccount, 
sum(FAIL_GPRS_ATTACH_GEN+FAIL_COMB_ATTACH_GEN-FAIL_GPRS_ATTACH_DUE_MS_ERR-FAIL_GPRS_ATTACH_COLLISIONS) attachfailcount, 
sum(FAIL_GPRS_ATTACH_SIM_NOT_PROV+FAIL_GPRS_ATTACH_ILLEGAL_MS+FAIL_GPRS_ATTACH_ILLEGAL_ME+FAIL_GPRS_ATTACH_SER_NONSER_NA) userfailcount, 
decode(nvl((sum(SUCC_GPRS_ATTACH+FAIL_GPRS_ATTACH_GEN+SUCC_COMBINED_ATTACH+FAIL_COMB_ATTACH_GEN-FAIL_GPRS_ATTACH_DUE_MS_ERR-FAIL_GPRS_ATTACH_COLLISIONS)),0),0,0,(round((sum(SUCC_GPRS_ATTACH+SUCC_COMBINED_ATTACH)/(sum(SUCC_GPRS_ATTACH+FAIL_GPRS_ATTACH_GEN+SUCC_COMBINED_ATTACH+FAIL_COMB_ATTACH_GEN-FAIL_GPRS_ATTACH_DUE_MS_ERR-FAIL_GPRS_ATTACH_COLLISIONS))),4)*100)) attachratio,
decode(nvl((sum(SUCC_GPRS_ATTACH+FAIL_GPRS_ATTACH_GEN+SUCC_COMBINED_ATTACH+FAIL_COMB_ATTACH_GEN-FAIL_GPRS_ATTACH_DUE_MS_ERR-FAIL_GPRS_ATTACH_COLLISIONS-FAIL_GPRS_ATTACH_SIM_NOT_PROV-FAIL_GPRS_ATTACH_ILLEGAL_MS-FAIL_GPRS_ATTACH_ILLEGAL_ME-FAIL_GPRS_ATTACH_SER_NONSER_NA)),0),0,0,(round((sum(SUCC_GPRS_ATTACH+SUCC_COMBINED_ATTACH)/(sum(SUCC_GPRS_ATTACH+FAIL_GPRS_ATTACH_GEN+SUCC_COMBINED_ATTACH+FAIL_COMB_ATTACH_GEN-FAIL_GPRS_ATTACH_DUE_MS_ERR-FAIL_GPRS_ATTACH_COLLISIONS-FAIL_GPRS_ATTACH_SIM_NOT_PROV-FAIL_GPRS_ATTACH_ILLEGAL_MS-FAIL_GPRS_ATTACH_ILLEGAL_ME-FAIL_GPRS_ATTACH_SER_NONSER_NA))),4)*100)) nonusersuccratio
from 	PCOFNS_PS_GMMLR_CI3_RAW twog,  
			UTP_COMMON_OBJECTS objects 
where 
twog.FINS_ID=objects.CO_GID 
"""
 
	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(twog.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(twog.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(twog.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(twog.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(twog.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(twog.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(twog.period_start_time,'yyyy/mm/dd'), to_char(twog.period_start_time,'hh24'), twog.fins_id, objects.co_name 
	order by objects.co_name,to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24:mi'), twog.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	#print sqlstring
	
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_2g_pdp(cursor,param):
# PDP activation 2G
	title=[
	u"设备ID",
	u"设备名称",
	u"日期",
	u"时间",
	u"PDP成功次数2G",
	u"PDP次数2G",
	u"PDP失败次数2G",
	u"PDP激活成功率2G",
	u"PDP去除用户原因激活成功率2G"
	]	
	if (param.selectperiod=='60'):
		sqlstring="""
select
twog.fins_id,
objects.co_name MMESGSN,
to_char(twog.period_start_time,'yyyy/mm/dd') Sdate,
to_char(twog.period_start_time,'hh24') Stime,
sum(SUCC_MO_PDP_CONTEXT_ACT) PdpSucc2g,
sum(SUCC_MO_PDP_CONTEXT_ACT+FAIL_MO_PDP_CONT_ACT_GEN) PdpAtt2g,
sum(FAIL_MO_PDP_ACT_MIS_UNK_APN+FAIL_MO_PDP_ACT_UNK_ADDR_TYPE+FAIL_MO_PDP_ACT_WRONG_PASSWORD+FAIL_MO_PDP_ACT_SERV_OPT_NS+FAIL_MO_PDP_ACT_REQ_SE_OP_NS) PdpFailUser2g,
decode(nvl((sum(SUCC_MO_PDP_CONTEXT_ACT+FAIL_MO_PDP_CONT_ACT_GEN)),0),0,0,(round((sum(SUCC_MO_PDP_CONTEXT_ACT)/(sum(SUCC_MO_PDP_CONTEXT_ACT+FAIL_MO_PDP_CONT_ACT_GEN))),4)*100)) PdpSR2g,
decode(nvl((sum(SUCC_MO_PDP_CONTEXT_ACT+FAIL_MO_PDP_CONT_ACT_GEN)),0),0,0,(round((sum(SUCC_MO_PDP_CONTEXT_ACT)/(sum(SUCC_MO_PDP_CONTEXT_ACT+FAIL_MO_PDP_CONT_ACT_GEN-(FAIL_MO_PDP_ACT_MIS_UNK_APN+FAIL_MO_PDP_ACT_UNK_ADDR_TYPE+FAIL_MO_PDP_ACT_WRONG_PASSWORD+FAIL_MO_PDP_ACT_SERV_OPT_NS+FAIL_MO_PDP_ACT_REQ_SE_OP_NS)))),4)*100)) PdpSR2g
from 	PCOFNS_PS_SMTM2_CI3_RAW twog, 
			UTP_COMMON_OBJECTS objects
where 
twog.fins_id=objects.co_gid 
"""
	else:
		sqlstring="""
select
twog.fins_id,
objects.co_name MMESGSN,
to_char(twog.period_start_time,'yyyy/mm/dd') Sdate,
to_char(twog.period_start_time,'hh24:mi') Stime,
sum(SUCC_MO_PDP_CONTEXT_ACT) PdpSucc2g,
sum(SUCC_MO_PDP_CONTEXT_ACT+FAIL_MO_PDP_CONT_ACT_GEN) PdpAtt2g,
sum(FAIL_MO_PDP_ACT_MIS_UNK_APN+FAIL_MO_PDP_ACT_UNK_ADDR_TYPE+FAIL_MO_PDP_ACT_WRONG_PASSWORD+FAIL_MO_PDP_ACT_SERV_OPT_NS+FAIL_MO_PDP_ACT_REQ_SE_OP_NS) PdpFailUser2g,
decode(nvl((sum(SUCC_MO_PDP_CONTEXT_ACT+FAIL_MO_PDP_CONT_ACT_GEN)),0),0,0,(round((sum(SUCC_MO_PDP_CONTEXT_ACT)/(sum(SUCC_MO_PDP_CONTEXT_ACT+FAIL_MO_PDP_CONT_ACT_GEN))),4)*100)) PdpSR2g,
decode(nvl((sum(SUCC_MO_PDP_CONTEXT_ACT+FAIL_MO_PDP_CONT_ACT_GEN)),0),0,0,(round((sum(SUCC_MO_PDP_CONTEXT_ACT)/(sum(SUCC_MO_PDP_CONTEXT_ACT+FAIL_MO_PDP_CONT_ACT_GEN-(FAIL_MO_PDP_ACT_MIS_UNK_APN+FAIL_MO_PDP_ACT_UNK_ADDR_TYPE+FAIL_MO_PDP_ACT_WRONG_PASSWORD+FAIL_MO_PDP_ACT_SERV_OPT_NS+FAIL_MO_PDP_ACT_REQ_SE_OP_NS)))),4)*100)) PdpSR2g
from 	PCOFNS_PS_SMTM2_CI3_RAW twog, 
			UTP_COMMON_OBJECTS objects
where 
twog.fins_id=objects.co_gid 
"""

	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(twog.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(twog.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(twog.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(twog.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(twog.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(twog.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(twog.period_start_time,'yyyy/mm/dd'), to_char(twog.period_start_time,'hh24'), twog.fins_id, objects.co_name 
	order by objects.co_name,to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24:mi'), twog.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
	
def mme_2g_rau(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'RAU INTRA成功次数2G',
	u'RAU INTRA尝试次数2G',
	u'RAU INTRA失败次数2G',
	u'RAU INTRA成功率2G',
	u'RAU INTER PAPU成功次数2G',
	u'RAU INTER SGSN成功次数2G',
	u'RAU INTER SGSN尝试次数2G',
	u'RAU INTER SGSN失败次数2G',
	u'RAU INTER SGSN成功率2G'
	]
	if (param.selectperiod=='60'):
		sqlstring="""
select 
twog.FINS_ID,
objects.CO_Name MMESGSN,
to_char(twog.period_start_time,'yyyy/mm/dd') Sdate,
to_char(twog.period_start_time,'hh24') Stime,
(sum(SUCC_INTRA_PAPU_RA_UPDAT+SUCC_INTRA_PAPU_RA_LA_UPDAT+SUCC_INTER_PAPU_RA_UPDAT+SUCC_INTER_PAPU_RA_LA_UPDAT)) RauIntraSgsnSucc2g,
(sum(SUCC_INTRA_PAPU_RA_UPDAT+FAIL_INTRA_PAPU_RAU_GEN+SUCC_INTRA_PAPU_RA_LA_UPDAT+FAIL_INTRA_PAPU_RA_LA_UP_GEN+SUCC_INTER_PAPU_RA_UPDAT+FAIL_INTER_PAPU_RAU_GEN+SUCC_INTER_PAPU_RA_LA_UPDAT+FAIL_INTER_PAPU_RA_LA_UP_GEN)) RauIntraSgsnAtt2g,
(sum(FAIL_INTRA_PAPU_RAU_GEN+FAIL_INTRA_PAPU_RA_LA_UP_GEN+ FAIL_INTER_PAPU_RAU_GEN+ FAIL_INTER_PAPU_RA_LA_UP_GEN)) RauIntraSgsnFail2g,
decode(nvl((sum(SUCC_INTRA_PAPU_RA_UPDAT+FAIL_INTRA_PAPU_RAU_GEN+SUCC_INTRA_PAPU_RA_LA_UPDAT+FAIL_INTRA_PAPU_RA_LA_UP_GEN+SUCC_INTER_PAPU_RA_UPDAT+FAIL_INTER_PAPU_RAU_GEN+SUCC_INTER_PAPU_RA_LA_UPDAT+FAIL_INTER_PAPU_RA_LA_UP_GEN)),0),0,0,(round(((sum(SUCC_INTRA_PAPU_RA_UPDAT+SUCC_INTRA_PAPU_RA_LA_UPDAT+SUCC_INTER_PAPU_RA_UPDAT+SUCC_INTER_PAPU_RA_LA_UPDAT))/(sum(SUCC_INTRA_PAPU_RA_UPDAT+FAIL_INTRA_PAPU_RAU_GEN+SUCC_INTRA_PAPU_RA_LA_UPDAT+FAIL_INTRA_PAPU_RA_LA_UP_GEN+SUCC_INTER_PAPU_RA_UPDAT+FAIL_INTER_PAPU_RAU_GEN+SUCC_INTER_PAPU_RA_LA_UPDAT+FAIL_INTER_PAPU_RA_LA_UP_GEN))),4)*100)) RauIntraSgsnSR2g,
(sum(succ_periodical_ra_updat+succ_periodic_ra_la_updat+inter_papu_ra_la_up_s_in_ps+intra_papu_ra_la_up_s_in_ps+periodic_ra_la_up_s_in_ps)) RauPerSucc2g,
(sum(SUCC_INTER_SGSN_RA_UPDAT+SUCC_INTER_SGSN_RA_LA_UPDAT+INTER_SGSN_RA_LA_UP_S_IN_PS)) RauInterSgsnSucc2g,
(sum(SUCC_INTER_SGSN_RA_UPDAT+FAIL_INTER_SGSN_RAU_GEN+SUCC_INTER_SGSN_RA_LA_UPDAT+FAIL_INTER_SGSN_RA_LA_UP_GEN+INTER_SGSN_RA_LA_UP_S_IN_PS)) RauInterSgsnAtt2g,
(sum(FAIL_INTER_SGSN_RAU_GEN+FAIL_INTER_SGSN_RA_LA_UP_GEN)) RauInterSgsnFail2g,
decode(nvl((sum(SUCC_INTER_SGSN_RA_UPDAT+FAIL_INTER_SGSN_RAU_GEN+SUCC_INTER_SGSN_RA_LA_UPDAT+FAIL_INTER_SGSN_RA_LA_UP_GEN+INTER_SGSN_RA_LA_UP_S_IN_PS)),0),0,0,(round(((sum(SUCC_INTER_SGSN_RA_UPDAT+SUCC_INTER_SGSN_RA_LA_UPDAT+INTER_SGSN_RA_LA_UP_S_IN_PS))/(sum(SUCC_INTER_SGSN_RA_UPDAT+FAIL_INTER_SGSN_RAU_GEN+SUCC_INTER_SGSN_RA_LA_UPDAT+FAIL_INTER_SGSN_RA_LA_UP_GEN+INTER_SGSN_RA_LA_UP_S_IN_PS))),4)*100)) RauInterSgsnSR2g
 from 	PCOFNS_PS_GMMLR_CI3_RAW twog,  
			UTP_COMMON_OBJECTS objects
where 
twog.FINS_ID=objects.CO_GID
"""
	else:
		sqlstring="""
select 
twog.FINS_ID,
objects.CO_Name MMESGSN,
to_char(twog.period_start_time,'yyyy/mm/dd') Sdate,
to_char(twog.period_start_time,'hh24:mi') Stime,
(sum(SUCC_INTRA_PAPU_RA_UPDAT+SUCC_INTRA_PAPU_RA_LA_UPDAT+SUCC_INTER_PAPU_RA_UPDAT+SUCC_INTER_PAPU_RA_LA_UPDAT)) RauIntraSgsnSucc2g,
(sum(SUCC_INTRA_PAPU_RA_UPDAT+FAIL_INTRA_PAPU_RAU_GEN+SUCC_INTRA_PAPU_RA_LA_UPDAT+FAIL_INTRA_PAPU_RA_LA_UP_GEN+SUCC_INTER_PAPU_RA_UPDAT+FAIL_INTER_PAPU_RAU_GEN+SUCC_INTER_PAPU_RA_LA_UPDAT+FAIL_INTER_PAPU_RA_LA_UP_GEN)) RauIntraSgsnAtt2g,
(sum(FAIL_INTRA_PAPU_RAU_GEN+FAIL_INTRA_PAPU_RA_LA_UP_GEN+ FAIL_INTER_PAPU_RAU_GEN+ FAIL_INTER_PAPU_RA_LA_UP_GEN)) RauIntraSgsnFail2g,
decode(nvl((sum(SUCC_INTRA_PAPU_RA_UPDAT+FAIL_INTRA_PAPU_RAU_GEN+SUCC_INTRA_PAPU_RA_LA_UPDAT+FAIL_INTRA_PAPU_RA_LA_UP_GEN+SUCC_INTER_PAPU_RA_UPDAT+FAIL_INTER_PAPU_RAU_GEN+SUCC_INTER_PAPU_RA_LA_UPDAT+FAIL_INTER_PAPU_RA_LA_UP_GEN)),0),0,0,(round(((sum(SUCC_INTRA_PAPU_RA_UPDAT+SUCC_INTRA_PAPU_RA_LA_UPDAT+SUCC_INTER_PAPU_RA_UPDAT+SUCC_INTER_PAPU_RA_LA_UPDAT))/(sum(SUCC_INTRA_PAPU_RA_UPDAT+FAIL_INTRA_PAPU_RAU_GEN+SUCC_INTRA_PAPU_RA_LA_UPDAT+FAIL_INTRA_PAPU_RA_LA_UP_GEN+SUCC_INTER_PAPU_RA_UPDAT+FAIL_INTER_PAPU_RAU_GEN+SUCC_INTER_PAPU_RA_LA_UPDAT+FAIL_INTER_PAPU_RA_LA_UP_GEN))),4)*100)) RauIntraSgsnSR2g,
(sum(succ_periodical_ra_updat+succ_periodic_ra_la_updat+inter_papu_ra_la_up_s_in_ps+intra_papu_ra_la_up_s_in_ps+periodic_ra_la_up_s_in_ps)) RauPerSucc2g,
(sum(SUCC_INTER_SGSN_RA_UPDAT+SUCC_INTER_SGSN_RA_LA_UPDAT+INTER_SGSN_RA_LA_UP_S_IN_PS)) RauInterSgsnSucc2g,
(sum(SUCC_INTER_SGSN_RA_UPDAT+FAIL_INTER_SGSN_RAU_GEN+SUCC_INTER_SGSN_RA_LA_UPDAT+FAIL_INTER_SGSN_RA_LA_UP_GEN+INTER_SGSN_RA_LA_UP_S_IN_PS)) RauInterSgsnAtt2g,
(sum(FAIL_INTER_SGSN_RAU_GEN+FAIL_INTER_SGSN_RA_LA_UP_GEN)) RauInterSgsnFail2g,
decode(nvl((sum(SUCC_INTER_SGSN_RA_UPDAT+FAIL_INTER_SGSN_RAU_GEN+SUCC_INTER_SGSN_RA_LA_UPDAT+FAIL_INTER_SGSN_RA_LA_UP_GEN+INTER_SGSN_RA_LA_UP_S_IN_PS)),0),0,0,(round(((sum(SUCC_INTER_SGSN_RA_UPDAT+SUCC_INTER_SGSN_RA_LA_UPDAT+INTER_SGSN_RA_LA_UP_S_IN_PS))/(sum(SUCC_INTER_SGSN_RA_UPDAT+FAIL_INTER_SGSN_RAU_GEN+SUCC_INTER_SGSN_RA_LA_UPDAT+FAIL_INTER_SGSN_RA_LA_UP_GEN+INTER_SGSN_RA_LA_UP_S_IN_PS))),4)*100)) RauInterSgsnSR2g
from 	PCOFNS_PS_GMMLR_CI3_RAW twog,  
			UTP_COMMON_OBJECTS objects
where 
twog.FINS_ID=objects.CO_GID
"""

	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(twog.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(twog.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(twog.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(twog.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(twog.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(twog.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(twog.period_start_time,'yyyy/mm/dd'), to_char(twog.period_start_time,'hh24'), twog.fins_id, objects.co_name 
	order by objects.co_name,to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24:mi'), twog.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)

def mme_2g_paging(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'Paging尝试次数2G',
	u'Paging成功次数2G',
	u'Paging成功率2G'
	]

	if (param.selectperiod=='60'):
		sqlstring="""
select
twog.fins_id,
objects.co_name MMESGSN,
to_char(twog.period_start_time,'yyyy/mm/dd') Sdate,
to_char(twog.period_start_time,'hh24') Stime,
sum(SGSN_LEVEL_PS_PAGINGS) pagingatt2g,
sum(SGSN_LEVEL_PS_PAGINGS- SGSN_LEVEL_UNSUCC_PS_PAG) pagingsucc2g,
decode(nvl((sum(SGSN_LEVEL_PS_PAGINGS)),0),0,0,(round((sum(SGSN_LEVEL_PS_PAGINGS- SGSN_LEVEL_UNSUCC_PS_PAG)/(sum(SGSN_LEVEL_PS_PAGINGS))),4)*100)) paging2gSR
from 	PCOFNS_PS_SGPA_FLEXINS_RAW twog,  
			UTP_COMMON_OBJECTS objects
where 
twog.fins_id=objects.co_gid
"""
	else:
		sqlstring="""
select
twog.fins_id,
objects.co_name MMESGSN,
to_char(twog.period_start_time,'yyyy/mm/dd') Sdate,
to_char(twog.period_start_time,'hh24:mi') Stime,
sum(SGSN_LEVEL_PS_PAGINGS) pagingatt2g,
sum(SGSN_LEVEL_PS_PAGINGS- SGSN_LEVEL_UNSUCC_PS_PAG) pagingsucc2g,
decode(nvl((sum(SGSN_LEVEL_PS_PAGINGS)),0),0,0,(round((sum(SGSN_LEVEL_PS_PAGINGS- SGSN_LEVEL_UNSUCC_PS_PAG)/(sum(SGSN_LEVEL_PS_PAGINGS))),4)*100)) paging2gSR
from 	PCOFNS_PS_SGPA_FLEXINS_RAW twog,  
			UTP_COMMON_OBJECTS objects
where 
twog.fins_id=objects.co_gid
"""
	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(twog.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(twog.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(twog.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(twog.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(twog.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(twog.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(twog.period_start_time,'yyyy/mm/dd'), to_char(twog.period_start_time,'hh24'), twog.fins_id, objects.co_name 
	order by objects.co_name,to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24:mi'), twog.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(twog.period_start_time,'yyyy/mm/dd'),to_char(twog.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_3g_attach(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'附着成功次数3G',
	u'附着尝试次数3G',
	u'用户原因失败次数3G',
	u'SRNS InterSGSN尝试次数3G',
	u'SRNS InterSGSN成功次数3G',
	u'SRNS IntraSGSN尝试次数3G',
	u'SRNS IntraSGSN成功次数3G',
	u'SRNS InterSGSN成功率3G',
	u'SRNS IntraSGSN成功率3G',
	u'SRNS 成功率3G',
	u'去除用户原因附着成功率3G'
	]

	if (param.selectperiod=='60'):
		sqlstring="""
select 
threeg.FINS_ID,
objects.CO_Name MMESGSN,
to_char(threeg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(threeg.period_start_time,'hh24') Stime,
(SUM(IU_SUCC_GPRS_ATTACH)+SUM(IU_SUCC_COMBINED_ATTACH)) AttachSucc3g,
(SUM(IU_SUCC_GPRS_ATTACH+IU_SUCC_COMBINED_ATTACH+IU_FAIL_GPRS_ATTACH+IU_FAIL_COMB_ATTACH_IN_PS-IU_FAIL_GPRS_ATTACH_MS_ERR-IU_FAIL_GPRS_ATTACH_COLLISIONS)) AttachAttempt3g,
(SUM(IU_FAIL_GPRS_ATTACH_3)+SUM(IU_FAIL_COMB_ATTACH_3)+SUM(IU_FAIL_GPRS_ATTACH_6)+SUM(IU_FAIL_COMB_ATTACH_6)+SUM(IU_FAIL_GPRS_ATTACH_7)+SUM(IU_FAIL_COMB_ATTACH_7)+SUM(IU_FAIL_GPRS_ATTACH_8)+SUM(IU_FAIL_COMB_ATTACH_8+IU_FAIL_GPRS_ATTACH_MS_ERR+IU_FAIL_GPRS_ATTACH_COLLISIONS)) AttachFailUser3g,
(SUM(IU_SUCC_INTER_SGSN_RE+IU_FAIL_INTER_SGSN_RE_RNC)) SRNS_INTERSGSN_ATTEMPTS,
(SUM(IU_SUCC_INTER_SGSN_RE)) SRNS_INTERSGSN_SUCC,
(SUM(IU_SUCC_INTRA_PAPU_RE+IU_FAIL_INTRA_PAPU_RE_SGSN+ IU_FAIL_INTRA_PAPU_RE_RNC+ IU_SUCC_INTER_PAPU_RE+ IU_FAIL_INTER_PAPU_RE_SGSN+ IU_FAIL_INTER_PAPU_RE_RNC)) SRNS_INTRASGSN_ATTEMPTS,
(SUM(IU_SUCC_INTRA_PAPU_RE+IU_SUCC_INTER_PAPU_RE)) SRNS_INTRASGSN_SUCC,
decode(nvl((sum(IU_SUCC_INTER_SGSN_RE+IU_FAIL_INTER_SGSN_RE_RNC)),0),0,0,(round((SUM(IU_SUCC_INTER_SGSN_RE))/((sum(IU_SUCC_INTER_SGSN_RE+IU_FAIL_INTER_SGSN_RE_RNC))),4)*100)) SRNS_INTERSGSN_SR,
decode(nvl((SUM(IU_SUCC_INTRA_PAPU_RE+IU_FAIL_INTRA_PAPU_RE_SGSN+ IU_FAIL_INTRA_PAPU_RE_RNC+ IU_SUCC_INTER_PAPU_RE+ IU_FAIL_INTER_PAPU_RE_SGSN+ IU_FAIL_INTER_PAPU_RE_RNC)),0),0,0,(round((SUM(IU_SUCC_INTRA_PAPU_RE+IU_SUCC_INTER_PAPU_RE))/((SUM(IU_SUCC_INTRA_PAPU_RE+IU_FAIL_INTRA_PAPU_RE_SGSN+ IU_FAIL_INTRA_PAPU_RE_RNC+ IU_SUCC_INTER_PAPU_RE+ IU_FAIL_INTER_PAPU_RE_SGSN+ IU_FAIL_INTER_PAPU_RE_RNC))),4)*100)) SRNS_INTRASGSN_SR,
decode(nvl((SUM(IU_SUCC_INTER_SGSN_RE+IU_FAIL_INTER_SGSN_RE_RNC)+SUM(IU_SUCC_INTRA_PAPU_RE+IU_FAIL_INTRA_PAPU_RE_SGSN+ IU_FAIL_INTRA_PAPU_RE_RNC+ IU_SUCC_INTER_PAPU_RE+ IU_FAIL_INTER_PAPU_RE_SGSN+ IU_FAIL_INTER_PAPU_RE_RNC)),0),0,0,(round((SUM(IU_SUCC_INTRA_PAPU_RE+IU_SUCC_INTER_PAPU_RE)+SUM(IU_SUCC_INTER_SGSN_RE))/((SUM(IU_SUCC_INTER_SGSN_RE+IU_FAIL_INTER_SGSN_RE_RNC)+SUM(IU_SUCC_INTRA_PAPU_RE+IU_FAIL_INTRA_PAPU_RE_SGSN+ IU_FAIL_INTRA_PAPU_RE_RNC+ IU_SUCC_INTER_PAPU_RE+ IU_FAIL_INTER_PAPU_RE_SGSN+ IU_FAIL_INTER_PAPU_RE_RNC))),4)*100)) SRNS_SR,
decode(nvl(SUM(IU_SUCC_GPRS_ATTACH+IU_SUCC_COMBINED_ATTACH+IU_FAIL_GPRS_ATTACH+IU_FAIL_COMB_ATTACH_IN_PS-IU_FAIL_GPRS_ATTACH_MS_ERR-IU_FAIL_GPRS_ATTACH_COLLISIONS-IU_FAIL_GPRS_ATTACH_3-IU_FAIL_COMB_ATTACH_3-IU_FAIL_GPRS_ATTACH_6-IU_FAIL_COMB_ATTACH_6-IU_FAIL_GPRS_ATTACH_7-IU_FAIL_COMB_ATTACH_7-IU_FAIL_GPRS_ATTACH_8-IU_FAIL_COMB_ATTACH_8),0),0,0,(round(SUM(IU_SUCC_GPRS_ATTACH+IU_SUCC_COMBINED_ATTACH)/((SUM(IU_SUCC_GPRS_ATTACH+IU_SUCC_COMBINED_ATTACH+IU_FAIL_GPRS_ATTACH+IU_FAIL_COMB_ATTACH_IN_PS-IU_FAIL_GPRS_ATTACH_MS_ERR-IU_FAIL_GPRS_ATTACH_COLLISIONS-IU_FAIL_GPRS_ATTACH_3-IU_FAIL_COMB_ATTACH_3-IU_FAIL_GPRS_ATTACH_6-IU_FAIL_COMB_ATTACH_6-IU_FAIL_GPRS_ATTACH_7-IU_FAIL_COMB_ATTACH_7-IU_FAIL_GPRS_ATTACH_8-IU_FAIL_COMB_ATTACH_8))),4)*100)) AttachSR3G
from 	PCOFNS_PS_IUMLR_SAC1_RAW threeg, 
			UTP_COMMON_OBJECTS objects
where 
threeg.FINS_ID=objects.CO_GID
"""
	else:
		sqlstring="""
select 
threeg.FINS_ID,
objects.CO_Name MMESGSN,
to_char(threeg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(threeg.period_start_time,'hh24:mi') Stime,
(SUM(IU_SUCC_GPRS_ATTACH)+SUM(IU_SUCC_COMBINED_ATTACH)) AttachSucc3g,
(SUM(IU_SUCC_GPRS_ATTACH+IU_SUCC_COMBINED_ATTACH+IU_FAIL_GPRS_ATTACH+IU_FAIL_COMB_ATTACH_IN_PS-IU_FAIL_GPRS_ATTACH_MS_ERR-IU_FAIL_GPRS_ATTACH_COLLISIONS)) AttachAttempt3g,
(SUM(IU_FAIL_GPRS_ATTACH_3)+SUM(IU_FAIL_COMB_ATTACH_3)+SUM(IU_FAIL_GPRS_ATTACH_6)+SUM(IU_FAIL_COMB_ATTACH_6)+SUM(IU_FAIL_GPRS_ATTACH_7)+SUM(IU_FAIL_COMB_ATTACH_7)+SUM(IU_FAIL_GPRS_ATTACH_8)+SUM(IU_FAIL_COMB_ATTACH_8+IU_FAIL_GPRS_ATTACH_MS_ERR+IU_FAIL_GPRS_ATTACH_COLLISIONS)) AttachFailUser3g,
(SUM(IU_SUCC_INTER_SGSN_RE+IU_FAIL_INTER_SGSN_RE_RNC)) SRNS_INTERSGSN_ATTEMPTS,
(SUM(IU_SUCC_INTER_SGSN_RE)) SRNS_INTERSGSN_SUCC,
(SUM(IU_SUCC_INTRA_PAPU_RE+IU_FAIL_INTRA_PAPU_RE_SGSN+ IU_FAIL_INTRA_PAPU_RE_RNC+ IU_SUCC_INTER_PAPU_RE+ IU_FAIL_INTER_PAPU_RE_SGSN+ IU_FAIL_INTER_PAPU_RE_RNC)) SRNS_INTRASGSN_ATTEMPTS,
(SUM(IU_SUCC_INTRA_PAPU_RE+IU_SUCC_INTER_PAPU_RE)) SRNS_INTRASGSN_SUCC,
decode(nvl((sum(IU_SUCC_INTER_SGSN_RE+IU_FAIL_INTER_SGSN_RE_RNC)),0),0,0,(round((SUM(IU_SUCC_INTER_SGSN_RE))/((sum(IU_SUCC_INTER_SGSN_RE+IU_FAIL_INTER_SGSN_RE_RNC))),4)*100)) SRNS_INTERSGSN_SR,
decode(nvl((SUM(IU_SUCC_INTRA_PAPU_RE+IU_FAIL_INTRA_PAPU_RE_SGSN+ IU_FAIL_INTRA_PAPU_RE_RNC+ IU_SUCC_INTER_PAPU_RE+ IU_FAIL_INTER_PAPU_RE_SGSN+ IU_FAIL_INTER_PAPU_RE_RNC)),0),0,0,(round((SUM(IU_SUCC_INTRA_PAPU_RE+IU_SUCC_INTER_PAPU_RE))/((SUM(IU_SUCC_INTRA_PAPU_RE+IU_FAIL_INTRA_PAPU_RE_SGSN+ IU_FAIL_INTRA_PAPU_RE_RNC+ IU_SUCC_INTER_PAPU_RE+ IU_FAIL_INTER_PAPU_RE_SGSN+ IU_FAIL_INTER_PAPU_RE_RNC))),4)*100)) SRNS_INTRASGSN_SR,
decode(nvl((SUM(IU_SUCC_INTER_SGSN_RE+IU_FAIL_INTER_SGSN_RE_RNC)+SUM(IU_SUCC_INTRA_PAPU_RE+IU_FAIL_INTRA_PAPU_RE_SGSN+ IU_FAIL_INTRA_PAPU_RE_RNC+ IU_SUCC_INTER_PAPU_RE+ IU_FAIL_INTER_PAPU_RE_SGSN+ IU_FAIL_INTER_PAPU_RE_RNC)),0),0,0,(round((SUM(IU_SUCC_INTRA_PAPU_RE+IU_SUCC_INTER_PAPU_RE)+SUM(IU_SUCC_INTER_SGSN_RE))/((SUM(IU_SUCC_INTER_SGSN_RE+IU_FAIL_INTER_SGSN_RE_RNC)+SUM(IU_SUCC_INTRA_PAPU_RE+IU_FAIL_INTRA_PAPU_RE_SGSN+ IU_FAIL_INTRA_PAPU_RE_RNC+ IU_SUCC_INTER_PAPU_RE+ IU_FAIL_INTER_PAPU_RE_SGSN+ IU_FAIL_INTER_PAPU_RE_RNC))),4)*100)) SRNS_SR,
decode(nvl(SUM(IU_SUCC_GPRS_ATTACH+IU_SUCC_COMBINED_ATTACH+IU_FAIL_GPRS_ATTACH+IU_FAIL_COMB_ATTACH_IN_PS-IU_FAIL_GPRS_ATTACH_MS_ERR-IU_FAIL_GPRS_ATTACH_COLLISIONS-IU_FAIL_GPRS_ATTACH_3-IU_FAIL_COMB_ATTACH_3-IU_FAIL_GPRS_ATTACH_6-IU_FAIL_COMB_ATTACH_6-IU_FAIL_GPRS_ATTACH_7-IU_FAIL_COMB_ATTACH_7-IU_FAIL_GPRS_ATTACH_8-IU_FAIL_COMB_ATTACH_8),0),0,0,(round(SUM(IU_SUCC_GPRS_ATTACH+IU_SUCC_COMBINED_ATTACH)/((SUM(IU_SUCC_GPRS_ATTACH+IU_SUCC_COMBINED_ATTACH+IU_FAIL_GPRS_ATTACH+IU_FAIL_COMB_ATTACH_IN_PS-IU_FAIL_GPRS_ATTACH_MS_ERR-IU_FAIL_GPRS_ATTACH_COLLISIONS-IU_FAIL_GPRS_ATTACH_3-IU_FAIL_COMB_ATTACH_3-IU_FAIL_GPRS_ATTACH_6-IU_FAIL_COMB_ATTACH_6-IU_FAIL_GPRS_ATTACH_7-IU_FAIL_COMB_ATTACH_7-IU_FAIL_GPRS_ATTACH_8-IU_FAIL_COMB_ATTACH_8))),4)*100)) AttachSR3G
from 	PCOFNS_PS_IUMLR_SAC1_RAW threeg, 
			UTP_COMMON_OBJECTS objects
where 
threeg.FINS_ID=objects.CO_GID
"""
	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(threeg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(threeg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(threeg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(threeg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(threeg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(threeg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(threeg.period_start_time,'yyyy/mm/dd'), to_char(threeg.period_start_time,'hh24'), threeg.fins_id, objects.co_name 
	order by objects.co_name,to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24:mi'), threeg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)

def mme_3g_pdp(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'PDP激活成功次数3G',
	u'PDP激活尝试次数3G',
	u'用户原因失败次数3G',
	u'去原因PDP成功率3G'
	]

	if (param.selectperiod=='60'):
		sqlstring="""
select
threeg.fins_id,
objects.CO_NAME MMESGSN,
to_char(threeg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(threeg.period_start_time,'hh24') Stime,
sum(IU_SUCC_MO_PDP_CON_ACT) PdpSucc3g,
sum(IU_SUCC_MO_PDP_CON_ACT+IU_FAIL_MO_PDP_CON_ACT) PdpAtt3g,
sum(IU_FAIL_MO_PDP_ACT_27+IU_FAIL_MO_PDP_ACT_28+IU_FAIL_MO_PDP_ACT_29+IU_FAIL_MO_PDP_ACT_32+IU_FAIL_MO_PDP_ACT_33) PdpFailUser3g,
decode(nvl((sum(IU_SUCC_MO_PDP_CON_ACT+IU_FAIL_MO_PDP_CON_ACT)),0),0,0,(round((sum(IU_SUCC_MO_PDP_CON_ACT)/(sum(IU_SUCC_MO_PDP_CON_ACT+IU_FAIL_MO_PDP_CON_ACT-(IU_FAIL_MO_PDP_ACT_27+IU_FAIL_MO_PDP_ACT_28+IU_FAIL_MO_PDP_ACT_29+IU_FAIL_MO_PDP_ACT_32+IU_FAIL_MO_PDP_ACT_33)))),4)*100)) PdpSR3g
from 	PCOFNS_PS_IUSM2_SAC1_RAW threeg,
			UTP_COMMON_OBJECTS objects
where 
threeg.fins_id=objects.co_gid
"""
	else:
		sqlstring="""
select
threeg.fins_id,
objects.CO_NAME MMESGSN,
to_char(threeg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(threeg.period_start_time,'hh24:mi') Stime,
sum(IU_SUCC_MO_PDP_CON_ACT) PdpSucc3g,
sum(IU_SUCC_MO_PDP_CON_ACT+IU_FAIL_MO_PDP_CON_ACT) PdpAtt3g,
sum(IU_FAIL_MO_PDP_ACT_27+IU_FAIL_MO_PDP_ACT_28+IU_FAIL_MO_PDP_ACT_29+IU_FAIL_MO_PDP_ACT_32+IU_FAIL_MO_PDP_ACT_33) PdpFailUser3g,
decode(nvl((sum(IU_SUCC_MO_PDP_CON_ACT+IU_FAIL_MO_PDP_CON_ACT)),0),0,0,(round((sum(IU_SUCC_MO_PDP_CON_ACT)/(sum(IU_SUCC_MO_PDP_CON_ACT+IU_FAIL_MO_PDP_CON_ACT-(IU_FAIL_MO_PDP_ACT_27+IU_FAIL_MO_PDP_ACT_28+IU_FAIL_MO_PDP_ACT_29+IU_FAIL_MO_PDP_ACT_32+IU_FAIL_MO_PDP_ACT_33)))),4)*100)) PdpSR3g
from 	PCOFNS_PS_IUSM2_SAC1_RAW threeg,
			UTP_COMMON_OBJECTS objects
where 
threeg.fins_id=objects.co_gid
"""
	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(threeg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(threeg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(threeg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(threeg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(threeg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(threeg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(threeg.period_start_time,'yyyy/mm/dd'), to_char(threeg.period_start_time,'hh24'), threeg.fins_id, objects.co_name 
	order by objects.co_name,to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24:mi'), threeg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_3g_rau(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'RAU INTRA成功次数3G',
	u'RAU INTRA失败次数3G',
	u'RAU INTRA成功率3G',
	u'RAU INTER成功次数3G',
	u'RAU INTER失败次数3G',
	u'RAU INTER成功率3G'
	]

	if (param.selectperiod=='60'):
		sqlstring="""
select 
threeg.fins_ID,
objects.co_Name MMESGSN,
to_char(threeg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(threeg.period_start_time,'hh24') Stime,
(sum(IU_SUCC_IN_INTRA_PAPU_RA_UPD+IU_SUCC_IN_INTER_PAPU_RA_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD+IU_SUCC_COMB_INTER_PAPU_UPD_PS)) RauIntraSgsnSucc3g,
(sum(IU_FAIL_IN_INTRA_PAPU_RA_UPD+IU_FAIL_IN_INTER_PAPU_RA_UPD+IU_FAIL_COMB_INTRA_PAPU_UPD_PS+IU_FAIL_COMB_INTER_PAPU_UPD_PS)) RauIntraSgsnFail3g,
decode(nvl((sum(IU_SUCC_IN_INTRA_PAPU_RA_UPD+IU_FAIL_IN_INTRA_PAPU_RA_UPD+IU_SUCC_IN_INTER_PAPU_RA_UPD+IU_FAIL_IN_INTER_PAPU_RA_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD+IU_FAIL_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD+IU_FAIL_COMB_INTER_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD_PS)),0),0,0,(round(((sum(IU_SUCC_IN_INTRA_PAPU_RA_UPD+IU_SUCC_IN_INTER_PAPU_RA_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD+IU_SUCC_COMB_INTER_PAPU_UPD_PS))/(sum(IU_SUCC_IN_INTRA_PAPU_RA_UPD+IU_FAIL_IN_INTRA_PAPU_RA_UPD+IU_SUCC_IN_INTER_PAPU_RA_UPD+IU_FAIL_IN_INTER_PAPU_RA_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD+IU_FAIL_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD+IU_FAIL_COMB_INTER_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD_PS))),4)*100)) RauIntraSgsnSR3g,
(sum(IU_SUCC_IN_INTER_SGSN_RA_UPD+ IU_SUCC_OG_INTER_SGSN_RA_UPD+IU_SUCC_COMB_INTER_SGSN_UPD+IU_SUCC_COMB_INTER_SGSN_UPD_PS)) RauInterSgsnSucc3g,
(sum(IU_FAIL_IN_INTER_SGSN_RA_UPD+IU_FAIL_OG_INTER_SGSN_RA_UPD+IU_FAIL_COMB_INTER_SGSN_UPD_PS)) RauInterSgsnFail3g,
decode(nvl((sum(IU_SUCC_IN_INTER_SGSN_RA_UPD+IU_FAIL_IN_INTER_SGSN_RA_UPD+IU_SUCC_OG_INTER_SGSN_RA_UPD+IU_FAIL_OG_INTER_SGSN_RA_UPD+IU_SUCC_COMB_INTER_SGSN_UPD+IU_FAIL_COMB_INTER_SGSN_UPD_PS+IU_SUCC_COMB_INTER_SGSN_UPD_PS)),0),0,0,(round(((sum(IU_SUCC_IN_INTER_SGSN_RA_UPD+ IU_SUCC_OG_INTER_SGSN_RA_UPD+IU_SUCC_COMB_INTER_SGSN_UPD+IU_SUCC_COMB_INTER_SGSN_UPD_PS))/(sum(IU_SUCC_IN_INTER_SGSN_RA_UPD+IU_FAIL_IN_INTER_SGSN_RA_UPD+IU_SUCC_OG_INTER_SGSN_RA_UPD+IU_FAIL_OG_INTER_SGSN_RA_UPD+IU_SUCC_COMB_INTER_SGSN_UPD+IU_FAIL_COMB_INTER_SGSN_UPD_PS+IU_SUCC_COMB_INTER_SGSN_UPD_PS))),4)*100)) RauInterSgsnSR3g
from 	PCOFNS_PS_IUMLR_SAC1_RAW threeg, 
			UTP_COMMON_OBJECTS objects
where 
threeg.fins_ID=objects.co_gid
"""
	else:
		sqlstring="""
select 
threeg.fins_ID,
objects.co_Name MMESGSN,
to_char(threeg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(threeg.period_start_time,'hh24:mi') Stime,
(sum(IU_SUCC_IN_INTRA_PAPU_RA_UPD+IU_SUCC_IN_INTER_PAPU_RA_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD+IU_SUCC_COMB_INTER_PAPU_UPD_PS)) RauIntraSgsnSucc3g,
(sum(IU_FAIL_IN_INTRA_PAPU_RA_UPD+IU_FAIL_IN_INTER_PAPU_RA_UPD+IU_FAIL_COMB_INTRA_PAPU_UPD_PS+IU_FAIL_COMB_INTER_PAPU_UPD_PS)) RauIntraSgsnFail3g,
decode(nvl((sum(IU_SUCC_IN_INTRA_PAPU_RA_UPD+IU_FAIL_IN_INTRA_PAPU_RA_UPD+IU_SUCC_IN_INTER_PAPU_RA_UPD+IU_FAIL_IN_INTER_PAPU_RA_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD+IU_FAIL_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD+IU_FAIL_COMB_INTER_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD_PS)),0),0,0,(round(((sum(IU_SUCC_IN_INTRA_PAPU_RA_UPD+IU_SUCC_IN_INTER_PAPU_RA_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD+IU_SUCC_COMB_INTER_PAPU_UPD_PS))/(sum(IU_SUCC_IN_INTRA_PAPU_RA_UPD+IU_FAIL_IN_INTRA_PAPU_RA_UPD+IU_SUCC_IN_INTER_PAPU_RA_UPD+IU_FAIL_IN_INTER_PAPU_RA_UPD+IU_SUCC_COMB_INTRA_PAPU_UPD+IU_FAIL_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTRA_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD+IU_FAIL_COMB_INTER_PAPU_UPD_PS+IU_SUCC_COMB_INTER_PAPU_UPD_PS))),4)*100)) RauIntraSgsnSR3g,
(sum(IU_SUCC_IN_INTER_SGSN_RA_UPD+ IU_SUCC_OG_INTER_SGSN_RA_UPD+IU_SUCC_COMB_INTER_SGSN_UPD+IU_SUCC_COMB_INTER_SGSN_UPD_PS)) RauInterSgsnSucc3g,
(sum(IU_FAIL_IN_INTER_SGSN_RA_UPD+IU_FAIL_OG_INTER_SGSN_RA_UPD+IU_FAIL_COMB_INTER_SGSN_UPD_PS)) RauInterSgsnFail3g,
decode(nvl((sum(IU_SUCC_IN_INTER_SGSN_RA_UPD+IU_FAIL_IN_INTER_SGSN_RA_UPD+IU_SUCC_OG_INTER_SGSN_RA_UPD+IU_FAIL_OG_INTER_SGSN_RA_UPD+IU_SUCC_COMB_INTER_SGSN_UPD+IU_FAIL_COMB_INTER_SGSN_UPD_PS+IU_SUCC_COMB_INTER_SGSN_UPD_PS)),0),0,0,(round(((sum(IU_SUCC_IN_INTER_SGSN_RA_UPD+ IU_SUCC_OG_INTER_SGSN_RA_UPD+IU_SUCC_COMB_INTER_SGSN_UPD+IU_SUCC_COMB_INTER_SGSN_UPD_PS))/(sum(IU_SUCC_IN_INTER_SGSN_RA_UPD+IU_FAIL_IN_INTER_SGSN_RA_UPD+IU_SUCC_OG_INTER_SGSN_RA_UPD+IU_FAIL_OG_INTER_SGSN_RA_UPD+IU_SUCC_COMB_INTER_SGSN_UPD+IU_FAIL_COMB_INTER_SGSN_UPD_PS+IU_SUCC_COMB_INTER_SGSN_UPD_PS))),4)*100)) RauInterSgsnSR3g
from 	PCOFNS_PS_IUMLR_SAC1_RAW threeg, 
			UTP_COMMON_OBJECTS objects
where 
threeg.fins_ID=objects.co_gid
"""
	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(threeg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(threeg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(threeg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(threeg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(threeg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(threeg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(threeg.period_start_time,'yyyy/mm/dd'), to_char(threeg.period_start_time,'hh24'), threeg.fins_id, objects.co_name 
	order by objects.co_name,to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24:mi'), threeg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_3g_paging(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'Paging尝试次数3G',
	u'Paging成功次数3G',
	u'Paging成功率3G'
	]
	if (param.selectperiod=='60'):
		sqlstring="""
select
threeg.fins_ID,
objects.co_Name MMESGSN,
to_char(threeg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(threeg.period_start_time,'hh24') Stime,
sum(SGSN_LEVEL_IU_PS_PAGINGS) pagingatt3g,
sum(SGSN_LEVEL_IU_PS_PAGINGS- SGSN_LEVEL_UNSUCC_IU_PS_PAG) pagingsucc3g,
decode(nvl((sum(SGSN_LEVEL_IU_PS_PAGINGS)),0),0,0,(round((sum(SGSN_LEVEL_IU_PS_PAGINGS- SGSN_LEVEL_UNSUCC_IU_PS_PAG)/(sum(SGSN_LEVEL_IU_PS_PAGINGS))),4)*100)) paging3gSR
from 	PCOFNS_PS_IUSP_FLEXINS_RAW threeg,  
			UTP_COMMON_OBJECTS objects
where 
threeg.fins_id=objects.co_gid
"""
	else:
		sqlstring="""
select
threeg.fins_ID,
objects.co_Name MMESGSN,
to_char(threeg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(threeg.period_start_time,'hh24:mi') Stime,
sum(SGSN_LEVEL_IU_PS_PAGINGS) pagingatt3g,
sum(SGSN_LEVEL_IU_PS_PAGINGS- SGSN_LEVEL_UNSUCC_IU_PS_PAG) pagingsucc3g,
decode(nvl((sum(SGSN_LEVEL_IU_PS_PAGINGS)),0),0,0,(round((sum(SGSN_LEVEL_IU_PS_PAGINGS- SGSN_LEVEL_UNSUCC_IU_PS_PAG)/(sum(SGSN_LEVEL_IU_PS_PAGINGS))),4)*100)) paging3gSR
from 	PCOFNS_PS_IUSP_FLEXINS_RAW threeg,  
			UTP_COMMON_OBJECTS objects
where 
threeg.fins_id=objects.co_gid
"""
	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(threeg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(threeg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(threeg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(threeg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(threeg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(threeg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(threeg.period_start_time,'yyyy/mm/dd'), to_char(threeg.period_start_time,'hh24'), threeg.fins_id, objects.co_name 
	order by objects.co_name,to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24:mi'), threeg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_users(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'用户数2G',
	u'用户数3G',
	u'平均用户数2G+3G',
	u'最大用户数2G+3G',
	u'最大附着容量2G+3G',
	u'用户数4G IDLE',
	u'用户数4G CONN',
	u'用户总数4G',
	u'OVERLOAD_CONTROL_DROP_PROC'
	]
	if (param.selectperiod=='60'):
		sqlstring="""
select
threeg.fins_ID,
objects.co_Name MMESGSN,
to_char(threeg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(threeg.period_start_time,'hh24') Stime,
decode(nvl((max(threeg.AVG_ATTACH_GB_USERS_DEN)),0),0,0,(round((sum(threeg.AVG_ATTACH_GB_USERS_SUM)/max(threeg.AVG_ATTACH_GB_USERS_DEN)/round(count(threeg.AVG_ATTACH_GB_USERS_DEN)/16,0)),0))) AttachUsers2g,
decode(nvl((max(threeg.AVG_ATTACH_IU_USERS_DEN)),0),0,0,(round((sum(threeg.AVG_ATTACH_IU_USERS_SUM)/max(threeg.AVG_ATTACH_GB_USERS_DEN)/round(count(threeg.AVG_ATTACH_GB_USERS_DEN)/16,0)),0))) AttachUsers3g,
decode(nvl((max(threeg.AVG_ATTACH_GB_USERS_DEN)),0),0,0,(round((sum(threeg.AVG_ATTACH_GB_USERS_SUM)/max(threeg.AVG_ATTACH_GB_USERS_DEN)/round(count(threeg.AVG_ATTACH_GB_USERS_DEN)/16,0)),0)))+decode(nvl((max(threeg.AVG_ATTACH_IU_USERS_DEN)),0),0,0,(round((sum(threeg.AVG_ATTACH_IU_USERS_SUM)/max(threeg.AVG_ATTACH_GB_USERS_DEN)/round(count(threeg.AVG_ATTACH_GB_USERS_DEN)/16,0)),0))) AttachUsers23g,
round(sum(PEAK_ATTACH_USERS_GB_IU)/round(count(threeg.AVG_ATTACH_GB_USERS_DEN)/16,0),0) peakuser23g,
round(round(max(PEAK_ATTACH_USERS_GB_IU),0)*100/2000000,2) peakpercent,
decode(nvl((sum(EPS_ECM_IDLE_DENOM)),0),0,0,(round((sum(EPS_ECM_IDLE_SUM)/(sum(EPS_ECM_IDLE_DENOM))),0))) NbrSub_EcmIdle,
decode(nvl((sum(EPS_ECM_CONN_DENOM)),0),0,0,(round((sum(EPS_ECM_CONN_SUM)/(sum(EPS_ECM_CONN_DENOM))),0))) NbrSub_EcmConnected,
decode(nvl((sum(EPS_ECM_IDLE_DENOM)),0),0,0,(round((sum(EPS_ECM_IDLE_SUM)/(sum(EPS_ECM_IDLE_DENOM))),0)))+decode(nvl((sum(EPS_ECM_CONN_DENOM)),0),0,0,(round((sum(EPS_ECM_CONN_SUM)/(sum(EPS_ECM_CONN_DENOM))),0))) NbrSub_4g,
sum(OVERLOAD_CONTROL_DROP_PROC) dropproc
from 	PCOFNS_PS_PAUS_PAPU_RAW threeg,  
		  PCOFNS_PS_UMLM_FLEXINS_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
threeg.fins_ID=objects.co_gid and fourg.fins_ID=objects.co_gid
and threeg.period_start_time=fourg.period_start_time
"""
	else:
		sqlstring="""
select
threeg.fins_ID,
objects.co_Name MMESGSN,
to_char(threeg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(threeg.period_start_time,'hh24:mi') Stime,
decode(nvl((sum(threeg.AVG_ATTACH_GB_USERS_DEN)),0),0,0,(round((sum(threeg.AVG_ATTACH_GB_USERS_SUM)/max(threeg.AVG_ATTACH_GB_USERS_DEN)),0))) AttachUsers2g,
decode(nvl((sum(threeg.AVG_ATTACH_IU_USERS_DEN)),0),0,0,(round((sum(threeg.AVG_ATTACH_IU_USERS_SUM)/max(threeg.AVG_ATTACH_IU_USERS_DEN)),0))) AttachUsers3g,
decode(nvl((sum(threeg.AVG_ATTACH_GB_USERS_DEN)),0),0,0,(round((sum(threeg.AVG_ATTACH_GB_USERS_SUM)/max(threeg.AVG_ATTACH_GB_USERS_DEN)),0)))+decode(nvl((sum(threeg.AVG_ATTACH_IU_USERS_DEN)),0),0,0,(round((sum(threeg.AVG_ATTACH_IU_USERS_SUM)/max(threeg.AVG_ATTACH_IU_USERS_DEN)),0))) AttachUsers23g,
round(sum(PEAK_ATTACH_USERS_GB_IU),0) peakuser23g,
round(round(sum(PEAK_ATTACH_USERS_GB_IU)/1,0)*100/2000000,2) peakpercent,
decode(nvl((sum(EPS_ECM_IDLE_DENOM)),0),0,0,(round((sum(EPS_ECM_IDLE_SUM)/(sum(EPS_ECM_IDLE_DENOM))),0))) NbrSub_EcmIdle,
decode(nvl((sum(EPS_ECM_CONN_DENOM)),0),0,0,(round((sum(EPS_ECM_CONN_SUM)/(sum(EPS_ECM_CONN_DENOM))),0))) NbrSub_EcmConnected,
decode(nvl((sum(EPS_ECM_IDLE_DENOM)),0),0,0,(round((sum(EPS_ECM_IDLE_SUM)/(sum(EPS_ECM_IDLE_DENOM))),0)))+decode(nvl((sum(EPS_ECM_CONN_DENOM)),0),0,0,(round((sum(EPS_ECM_CONN_SUM)/(sum(EPS_ECM_CONN_DENOM))),0))) NbrSub_4g,
sum(OVERLOAD_CONTROL_DROP_PROC) dropproc
from 	PCOFNS_PS_PAUS_PAPU_RAW threeg,  
		  PCOFNS_PS_UMLM_FLEXINS_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
threeg.fins_ID=objects.co_gid and fourg.fins_ID=objects.co_gid
and threeg.period_start_time=fourg.period_start_time
"""

	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(threeg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(threeg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(threeg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(threeg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(threeg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(threeg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(threeg.period_start_time,'yyyy/mm/dd'), to_char(threeg.period_start_time,'hh24'), threeg.fins_id, objects.co_name 
	order by objects.co_name,to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24:mi'), threeg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(threeg.period_start_time,'yyyy/mm/dd'),to_char(threeg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_4g_attach(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'TAC',
	u'附着次数4G',
	u'附着成功次数',
	u'附着失败次数',
	u'附着失败无效UE',
	u'附着失败无效ME',
	u'附着失败EPS Service not allow',
	u'附着失败Service not allowed',
	u'附着成功率4G',
	u'去附着次数',
	u'服务请求成功次数',
	u'服务请求失败次数',
	u'服务请求成功率',
	u'IntraMME X2成功次数',
	u'IntraMME X2次数',
	u'IntraMME InterENB X2切换成功率',
	u'IntraMME S1成功次数',
	u'IntraMME S1次数',
	u'IntraMME InterENB S1切换成功率',
	u'OutMME s1切换成功率',
	u'OutMME s1切换成功次数',
	u'OutMME s1切换失败次数',
	u'In MME切换成功率',
	u'InMME s1切换SGW不变成功次数',
	u'InMME s1切换SGW改变成功次数',
	u'InMME s1切换失败次数'
	]

	if (param.selectperiod=='60'):
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
'ALL' elementtype,
sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL) allattach,
sum(EPS_ATTACH_SUCC) succ,
sum(EPS_ATTACH_FAIL) FailedEpsAttach,
sum(EPS_ATTACH_NAS_03_FAIL) EPS_ATTACH_NAS_03_FAIL,
sum(EPS_ATTACH_NAS_06_FAIL) EPS_ATTACH_NAS_06_FAIL,
sum(EPS_ATTACH_NAS_07_FAIL)  EPS_ATTACH_NAS_07_FAIL,
sum(EPS_ATTACH_NAS_08_FAIL) EPS_ATTACH_NAS_08_FAIL,
decode(nvl((sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL)),0),0,0,(round((sum(EPS_ATTACH_SUCC)/(sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL))),4)*100)) EPSAttach_SR,
sum(EPS_DETACH) EPS_DETACH,
sum(EPS_SERVICE_REQUEST_SUCC) SRSUCC,
sum(EPS_SERVICE_REQUEST_FAIL) SRFAIL,
decode(nvl((sum(EPS_SERVICE_REQUEST_SUCC+EPS_SERVICE_REQUEST_FAIL)),0),0,0,(round((sum(EPS_SERVICE_REQUEST_SUCC)/(sum(EPS_SERVICE_REQUEST_SUCC+EPS_SERVICE_REQUEST_FAIL))),4)*100)) SER_REQ_SR,
sum(EPS_PATH_SWITCH_X2_SUCC) intrammex2succ,
sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL) intrammex2att,
decode(nvl((sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL)),0),0,100,(round((sum(EPS_PATH_SWITCH_X2_SUCC)/(sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL))),4)*100)) IntraMme_InterEnbX2_SR,
sum(EPS_S1HO_SUCC) intrammes1succ,
sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL) intrammes1att,
decode(nvl((sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL)),0),0,100,(round((sum(EPS_S1HO_SUCC)/(sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL))),4)*100)) IntraMme_InterEnbS1_SR,
decode(nvl((sum(INTERMME_S1HO_OUT_SUCC+INTERMME_S1HO_OUT_FAIL)),0),0,0,(round((sum(INTERMME_S1HO_OUT_SUCC)/(sum(INTERMME_S1HO_OUT_SUCC+INTERMME_S1HO_OUT_FAIL))),4)*100)) Out_InterMme_Ho_SR,
sum(INTERMME_S1HO_OUT_SUCC) INTERMME_S1HO_OUT_SUCC,
sum(INTERMME_S1HO_OUT_FAIL) INTERMME_S1HO_OUT_FAIL,
decode(nvl((sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC+INTERMME_S1HO_IN_FAIL)),0),0,0,(round((sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC)/(sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC+INTERMME_S1HO_IN_FAIL))),4)*100)) Inc_InterMme_HO_SR,
sum(INTERMME_S1HO_WO_SGW_CHG_SUCC) INTERMME_S1HO_WO_SGW_CHG_SUCC,
sum(INTERMME_S1HO_SGW_CHG_IN_SUCC) INTERMME_S1HO_SGW_CHG_IN_SUCC,
sum(INTERMME_S1HO_IN_FAIL) INTERMME_S1HO_IN_FAIL
from 	PCOFNS_PS_MMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID
"""
		else:
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
ta_id elementtype,
sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL) allattach,
sum(EPS_ATTACH_SUCC) succ,
sum(EPS_ATTACH_FAIL) FailedEpsAttach,
sum(EPS_ATTACH_NAS_03_FAIL) EPS_ATTACH_NAS_03_FAIL,
sum(EPS_ATTACH_NAS_06_FAIL) EPS_ATTACH_NAS_06_FAIL,
sum(EPS_ATTACH_NAS_07_FAIL)  EPS_ATTACH_NAS_07_FAIL,
sum(EPS_ATTACH_NAS_08_FAIL) EPS_ATTACH_NAS_08_FAIL,
decode(nvl((sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL)),0),0,0,(round((sum(EPS_ATTACH_SUCC)/(sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL))),4)*100)) EPSAttach_SR,
sum(EPS_DETACH) EPS_DETACH,
sum(EPS_SERVICE_REQUEST_SUCC) SRSUCC,
sum(EPS_SERVICE_REQUEST_FAIL) SRFAIL,
decode(nvl((sum(EPS_SERVICE_REQUEST_SUCC+EPS_SERVICE_REQUEST_FAIL)),0),0,0,(round((sum(EPS_SERVICE_REQUEST_SUCC)/(sum(EPS_SERVICE_REQUEST_SUCC+EPS_SERVICE_REQUEST_FAIL))),4)*100)) SER_REQ_SR,
sum(EPS_PATH_SWITCH_X2_SUCC) intrammex2succ,
sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL) intrammex2att,
decode(nvl((sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL)),0),0,100,(round((sum(EPS_PATH_SWITCH_X2_SUCC)/(sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL))),4)*100)) IntraMme_InterEnbX2_SR,
sum(EPS_S1HO_SUCC) intrammes1succ,
sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL) intrammes1att,
decode(nvl((sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL)),0),0,100,(round((sum(EPS_S1HO_SUCC)/(sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL))),4)*100)) IntraMme_InterEnbS1_SR,
decode(nvl((sum(INTERMME_S1HO_OUT_SUCC+INTERMME_S1HO_OUT_FAIL)),0),0,0,(round((sum(INTERMME_S1HO_OUT_SUCC)/(sum(INTERMME_S1HO_OUT_SUCC+INTERMME_S1HO_OUT_FAIL))),4)*100)) Out_InterMme_Ho_SR,
sum(INTERMME_S1HO_OUT_SUCC) INTERMME_S1HO_OUT_SUCC,
sum(INTERMME_S1HO_OUT_FAIL) INTERMME_S1HO_OUT_FAIL,
decode(nvl((sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC+INTERMME_S1HO_IN_FAIL)),0),0,0,(round((sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC)/(sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC+INTERMME_S1HO_IN_FAIL))),4)*100)) Inc_InterMme_HO_SR,
sum(INTERMME_S1HO_WO_SGW_CHG_SUCC) INTERMME_S1HO_WO_SGW_CHG_SUCC,
sum(INTERMME_S1HO_SGW_CHG_IN_SUCC) INTERMME_S1HO_SGW_CHG_IN_SUCC,
sum(INTERMME_S1HO_IN_FAIL) INTERMME_S1HO_IN_FAIL
from 	PCOFNS_PS_MMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID and EPS_ATTACH_SUCC+EPS_ATTACH_FAIL>0
"""
	else:
		if (param.selectmmeelement=='MMESGSN'):	
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
'ALL' elementtype,
sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL) allattach,
sum(EPS_ATTACH_SUCC) succ,
sum(EPS_ATTACH_FAIL) FailedEpsAttach,
sum(EPS_ATTACH_NAS_03_FAIL) EPS_ATTACH_NAS_03_FAIL,
sum(EPS_ATTACH_NAS_06_FAIL) EPS_ATTACH_NAS_06_FAIL,
sum(EPS_ATTACH_NAS_07_FAIL)  EPS_ATTACH_NAS_07_FAIL,
sum(EPS_ATTACH_NAS_08_FAIL) EPS_ATTACH_NAS_08_FAIL,
decode(nvl((sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL)),0),0,0,(round((sum(EPS_ATTACH_SUCC)/(sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL))),4)*100)) EPSAttach_SR,
sum(EPS_DETACH) EPS_DETACH,
sum(EPS_SERVICE_REQUEST_SUCC) SRSUCC,
sum(EPS_SERVICE_REQUEST_FAIL) SRFAIL,
decode(nvl((sum(EPS_SERVICE_REQUEST_SUCC+EPS_SERVICE_REQUEST_FAIL)),0),0,0,(round((sum(EPS_SERVICE_REQUEST_SUCC)/(sum(EPS_SERVICE_REQUEST_SUCC+EPS_SERVICE_REQUEST_FAIL))),4)*100)) SER_REQ_SR,
sum(EPS_PATH_SWITCH_X2_SUCC) intrammex2succ,
sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL) intrammex2att,
decode(nvl((sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL)),0),0,100,(round((sum(EPS_PATH_SWITCH_X2_SUCC)/(sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL))),4)*100)) IntraMme_InterEnbX2_SR,
sum(EPS_S1HO_SUCC) intrammes1succ,
sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL) intrammes1att,
decode(nvl((sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL)),0),0,100,(round((sum(EPS_S1HO_SUCC)/(sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL))),4)*100)) IntraMme_InterEnbS1_SR,
decode(nvl((sum(INTERMME_S1HO_OUT_SUCC+INTERMME_S1HO_OUT_FAIL)),0),0,0,(round((sum(INTERMME_S1HO_OUT_SUCC)/(sum(INTERMME_S1HO_OUT_SUCC+INTERMME_S1HO_OUT_FAIL))),4)*100)) Out_InterMme_Ho_SR,
sum(INTERMME_S1HO_OUT_SUCC) INTERMME_S1HO_OUT_SUCC,
sum(INTERMME_S1HO_OUT_FAIL) INTERMME_S1HO_OUT_FAIL,
decode(nvl((sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC+INTERMME_S1HO_IN_FAIL)),0),0,0,(round((sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC)/(sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC+INTERMME_S1HO_IN_FAIL))),4)*100)) Inc_InterMme_HO_SR,
sum(INTERMME_S1HO_WO_SGW_CHG_SUCC) INTERMME_S1HO_WO_SGW_CHG_SUCC,
sum(INTERMME_S1HO_SGW_CHG_IN_SUCC) INTERMME_S1HO_SGW_CHG_IN_SUCC,
sum(INTERMME_S1HO_IN_FAIL) INTERMME_S1HO_IN_FAIL
from 	PCOFNS_PS_MMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID
"""
		else:
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
ta_id elementtype,
sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL) allattach,
sum(EPS_ATTACH_SUCC) succ,
sum(EPS_ATTACH_FAIL) FailedEpsAttach,
sum(EPS_ATTACH_NAS_03_FAIL) EPS_ATTACH_NAS_03_FAIL,
sum(EPS_ATTACH_NAS_06_FAIL) EPS_ATTACH_NAS_06_FAIL,
sum(EPS_ATTACH_NAS_07_FAIL)  EPS_ATTACH_NAS_07_FAIL,
sum(EPS_ATTACH_NAS_08_FAIL) EPS_ATTACH_NAS_08_FAIL,
decode(nvl((sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL)),0),0,0,(round((sum(EPS_ATTACH_SUCC)/(sum(EPS_ATTACH_SUCC+EPS_ATTACH_FAIL-EPS_ATTACH_NAS_03_FAIL-EPS_ATTACH_NAS_06_FAIL-EPS_ATTACH_NAS_07_FAIL-EPS_ATTACH_NAS_08_FAIL))),4)*100)) EPSAttach_SR,
sum(EPS_DETACH) EPS_DETACH,
sum(EPS_SERVICE_REQUEST_SUCC) SRSUCC,
sum(EPS_SERVICE_REQUEST_FAIL) SRFAIL,
decode(nvl((sum(EPS_SERVICE_REQUEST_SUCC+EPS_SERVICE_REQUEST_FAIL)),0),0,0,(round((sum(EPS_SERVICE_REQUEST_SUCC)/(sum(EPS_SERVICE_REQUEST_SUCC+EPS_SERVICE_REQUEST_FAIL))),4)*100)) SER_REQ_SR,
sum(EPS_PATH_SWITCH_X2_SUCC) intrammex2succ,
sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL) intrammex2att,
decode(nvl((sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL)),0),0,100,(round((sum(EPS_PATH_SWITCH_X2_SUCC)/(sum(EPS_PATH_SWITCH_X2_SUCC+EPS_PATH_SWITCH_X2_FAIL))),4)*100)) IntraMme_InterEnbX2_SR,
sum(EPS_S1HO_SUCC) intrammes1succ,
sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL) intrammes1att,
decode(nvl((sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL)),0),0,100,(round((sum(EPS_S1HO_SUCC)/(sum(EPS_S1HO_SUCC+EPS_S1HO_FAIL))),4)*100)) IntraMme_InterEnbS1_SR,
decode(nvl((sum(INTERMME_S1HO_OUT_SUCC+INTERMME_S1HO_OUT_FAIL)),0),0,0,(round((sum(INTERMME_S1HO_OUT_SUCC)/(sum(INTERMME_S1HO_OUT_SUCC+INTERMME_S1HO_OUT_FAIL))),4)*100)) Out_InterMme_Ho_SR,
sum(INTERMME_S1HO_OUT_SUCC) INTERMME_S1HO_OUT_SUCC,
sum(INTERMME_S1HO_OUT_FAIL) INTERMME_S1HO_OUT_FAIL,
decode(nvl((sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC+INTERMME_S1HO_IN_FAIL)),0),0,0,(round((sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC)/(sum(INTERMME_S1HO_WO_SGW_CHG_SUCC+INTERMME_S1HO_SGW_CHG_IN_SUCC+INTERMME_S1HO_IN_FAIL))),4)*100)) Inc_InterMme_HO_SR,
sum(INTERMME_S1HO_WO_SGW_CHG_SUCC) INTERMME_S1HO_WO_SGW_CHG_SUCC,
sum(INTERMME_S1HO_SGW_CHG_IN_SUCC) INTERMME_S1HO_SGW_CHG_IN_SUCC,
sum(INTERMME_S1HO_IN_FAIL) INTERMME_S1HO_IN_FAIL
from 	PCOFNS_PS_MMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID and EPS_ATTACH_SUCC+EPS_ATTACH_FAIL>0
"""

	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(fourg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name 
	order by objects.co_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
		else:
			sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name,ta_id 
	order by objects.co_name,ta_id,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
	else:
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
		else:
			sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name,ta_id 
	order by objects.CO_name,ta_id,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
		
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_4g_pdp(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'TAC',
	u'缺省承载建立成功率4G',
	u'激活缺省承载次数',
	u'激活缺省承载成功次数',
	u'缺省承载建立因MME失败',
	u'建立专有承载成功次数',
	u'建立专有承载次数',
	u'建立专有承载成功率',
	u'修改承载次数',
	u'修改承载成功次数',
	u'修改承载成功率',
	u's5s8 SGW承载建立成功次数',
	u's5s8 MME承载建立请求次数',
	u's5s8承载建立成功率',
	u's5s8 MME专有承载建立成功次数',
	u's5s8 MME专有承载建立请求次数',
	u's5s8专有承载建立成功率',
	u'PDN连接成功次数',
	u'PDN连接失败次数',
	u'PDN连接失败UE次数',
	u'PDN连接失败SGW次数',
	u'PDN连接失败MME次数',
	u'PDN连接失败ENB次数',
	u'PDN连接失败Coll次数',
	u'PDN连接失败其他次数',
	u'PDN连接成功率'
	]
	if (param.selectperiod=='60'):
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring="""
select 
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
'ALL' elementtype,
decode(nvl((sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL)),0),0,0,(round((sum(EPS_DEF_BEARER_ACT_SUCC)/(sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL))),4)*100)) ActDefault_EPS_Bearer_SR,
sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL) ActDefaultEpsBearerRequest,
sum(EPS_DEF_BEARER_ACT_SUCC) ActDefaultEpsBearerAccept,
sum(EPS_DEF_BEARER_ACT_MME_FAIL) EPS_DEF_BEARER_ACT_MME_FAIL,
sum(EPS_DDBEARE_CONF_BY_UE) ddsucc,
sum(EPS_DDBEARER_REQ_BY_MME) ddatt,
decode(nvl(sum(EPS_DDBEARER_REQ_BY_MME),0),0,0,round(sum(EPS_DDBEARE_CONF_BY_UE)/sum(EPS_DDBEARER_REQ_BY_MME)*100,2)) dd_succ_rate,
sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE) ModEpsBearerRequest,
sum(GW_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_SUCCESS) ModEpsBearerAccept,
decode(nvl(sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE),0),0,0,round(sum(GW_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_SUCCESS)/sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE)*100,2)) dd_succ_rate,
sum(EPS_DFBEARER_S5_S8_CONF_BY_SGW) s5s8succ,
sum(EPS_DFBEARER_S5_S8_REQ_BY_MME) s5s8att,
decode(nvl(sum(EPS_DFBEARER_S5_S8_REQ_BY_MME),0),0,0,round(sum(EPS_DFBEARER_S5_S8_CONF_BY_SGW)/sum(EPS_DFBEARER_S5_S8_REQ_BY_MME)*100,2)) s5s8_succ_rate,
sum(EPS_DDBEARER_S5_S8_CONF_BY_SGW) s5s8ddsucc,
sum(EPS_DDBEARER_S5_S8_REQ_BY_MME) s5s8ddatt,
decode(nvl(sum(EPS_DDBEARER_S5_S8_REQ_BY_MME),0),0,0,round(sum(EPS_DDBEARER_S5_S8_CONF_BY_SGW)/sum(EPS_DDBEARER_S5_S8_REQ_BY_MME)*100,2)) s5s8_dd_succ_rate,
sum(PDN_CONNECTIVITY_SUCCESSFUL) PdnSucc,
sum(PDN_CONNECTIVITY_FAILED) PdnFail,
sum(PDN_CONNECTIVITY_FAILED_UE) PdnFailUE,
sum(PDN_CONNECTIVITY_FAILED_SGW) PdnFailSGW,
sum(PDN_CONNECTIVITY_FAILED_MME) PdnFailMME,
sum(PDN_CONNECTIVITY_FAILED_ENB) PdnFailENB,
sum(PDN_CONNECT_FAILED_COLLISION) PdnFailColl,
sum(PDN_CONNECT_FAILED_UNSPECIFIED) PdnFailUnspec,
decode(nvl((sum(PDN_CONNECTIVITY_SUCCESSFUL+PDN_CONNECTIVITY_FAILED)),0),0,0,(round((sum(PDN_CONNECTIVITY_SUCCESSFUL)/sum(PDN_CONNECTIVITY_SUCCESSFUL+PDN_CONNECTIVITY_FAILED)),4)*100)) PDN_CONN_SR
from 	PCOFNS_PS_SMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID
"""
		else:
			sqlstring="""
select
fourg.fins_id id, 
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
ta_id elementtype,
decode(nvl((sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL)),0),0,0,(round((sum(EPS_DEF_BEARER_ACT_SUCC)/(sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL))),4)*100)) ActDefault_EPS_Bearer_SR,
sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL) ActDefaultEpsBearerRequest,
sum(EPS_DEF_BEARER_ACT_SUCC) ActDefaultEpsBearerAccept,
sum(EPS_DEF_BEARER_ACT_MME_FAIL) EPS_DEF_BEARER_ACT_MME_FAIL,
sum(EPS_DDBEARE_CONF_BY_UE) ddsucc,
sum(EPS_DDBEARER_REQ_BY_MME) ddatt,
decode(nvl(sum(EPS_DDBEARER_REQ_BY_MME),0),0,0,round(sum(EPS_DDBEARE_CONF_BY_UE)/sum(EPS_DDBEARER_REQ_BY_MME)*100,2)) dd_succ_rate,
sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE) ModEpsBearerRequest,
sum(GW_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_SUCCESS) ModEpsBearerAccept,
decode(nvl(sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE),0),0,0,round(sum(GW_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_SUCCESS)/sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE)*100,2)) dd_succ_rate,
sum(EPS_DFBEARER_S5_S8_CONF_BY_SGW) s5s8succ,
sum(EPS_DFBEARER_S5_S8_REQ_BY_MME) s5s8att,
decode(nvl(sum(EPS_DFBEARER_S5_S8_REQ_BY_MME),0),0,0,round(sum(EPS_DFBEARER_S5_S8_CONF_BY_SGW)/sum(EPS_DFBEARER_S5_S8_REQ_BY_MME)*100,2)) s5s8_succ_rate,
sum(EPS_DDBEARER_S5_S8_CONF_BY_SGW) s5s8ddsucc,
sum(EPS_DDBEARER_S5_S8_REQ_BY_MME) s5s8ddatt,
decode(nvl(sum(EPS_DDBEARER_S5_S8_REQ_BY_MME),0),0,0,round(sum(EPS_DDBEARER_S5_S8_CONF_BY_SGW)/sum(EPS_DDBEARER_S5_S8_REQ_BY_MME)*100,2)) s5s8_dd_succ_rate,
sum(PDN_CONNECTIVITY_SUCCESSFUL) PdnSucc,
sum(PDN_CONNECTIVITY_FAILED) PdnFail,
sum(PDN_CONNECTIVITY_FAILED_UE) PdnFailUE,
sum(PDN_CONNECTIVITY_FAILED_SGW) PdnFailSGW,
sum(PDN_CONNECTIVITY_FAILED_MME) PdnFailMME,
sum(PDN_CONNECTIVITY_FAILED_ENB) PdnFailENB,
sum(PDN_CONNECT_FAILED_COLLISION) PdnFailColl,
sum(PDN_CONNECT_FAILED_UNSPECIFIED) PdnFailUnspec,
decode(nvl((sum(PDN_CONNECTIVITY_SUCCESSFUL+PDN_CONNECTIVITY_FAILED)),0),0,0,(round((sum(PDN_CONNECTIVITY_SUCCESSFUL)/sum(PDN_CONNECTIVITY_SUCCESSFUL+PDN_CONNECTIVITY_FAILED)),4)*100)) PDN_CONN_SR
from 	PCOFNS_PS_SMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID and EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL>0
"""
	else:
		if (param.selectmmeelement=='MMESGSN'):	
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
'ALL' elementtype,
decode(nvl((sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL)),0),0,0,(round((sum(EPS_DEF_BEARER_ACT_SUCC)/(sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL))),4)*100)) ActDefault_EPS_Bearer_SR,
sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL) ActDefaultEpsBearerRequest,
sum(EPS_DEF_BEARER_ACT_SUCC) ActDefaultEpsBearerAccept,
sum(EPS_DEF_BEARER_ACT_MME_FAIL) EPS_DEF_BEARER_ACT_MME_FAIL,
sum(EPS_DDBEARE_CONF_BY_UE) ddsucc,
sum(EPS_DDBEARER_REQ_BY_MME) ddatt,
decode(nvl(sum(EPS_DDBEARER_REQ_BY_MME),0),0,0,round(sum(EPS_DDBEARE_CONF_BY_UE)/sum(EPS_DDBEARER_REQ_BY_MME)*100,2)) dd_succ_rate,
sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE) ModEpsBearerRequest,
sum(GW_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_SUCCESS) ModEpsBearerAccept,
decode(nvl(sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE),0),0,0,round(sum(GW_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_SUCCESS)/sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE)*100,2)) dd_succ_rate,
sum(EPS_DFBEARER_S5_S8_CONF_BY_SGW) s5s8succ,
sum(EPS_DFBEARER_S5_S8_REQ_BY_MME) s5s8att,
decode(nvl(sum(EPS_DFBEARER_S5_S8_REQ_BY_MME),0),0,0,round(sum(EPS_DFBEARER_S5_S8_CONF_BY_SGW)/sum(EPS_DFBEARER_S5_S8_REQ_BY_MME)*100,2)) s5s8_succ_rate,
sum(EPS_DDBEARER_S5_S8_CONF_BY_SGW) s5s8ddsucc,
sum(EPS_DDBEARER_S5_S8_REQ_BY_MME) s5s8ddatt,
decode(nvl(sum(EPS_DDBEARER_S5_S8_REQ_BY_MME),0),0,0,round(sum(EPS_DDBEARER_S5_S8_CONF_BY_SGW)/sum(EPS_DDBEARER_S5_S8_REQ_BY_MME)*100,2)) s5s8_dd_succ_rate,
sum(PDN_CONNECTIVITY_SUCCESSFUL) PdnSucc,
sum(PDN_CONNECTIVITY_FAILED) PdnFail,
sum(PDN_CONNECTIVITY_FAILED_UE) PdnFailUE,
sum(PDN_CONNECTIVITY_FAILED_SGW) PdnFailSGW,
sum(PDN_CONNECTIVITY_FAILED_MME) PdnFailMME,
sum(PDN_CONNECTIVITY_FAILED_ENB) PdnFailENB,
sum(PDN_CONNECT_FAILED_COLLISION) PdnFailColl,
sum(PDN_CONNECT_FAILED_UNSPECIFIED) PdnFailUnspec,
decode(nvl((sum(PDN_CONNECTIVITY_SUCCESSFUL+PDN_CONNECTIVITY_FAILED)),0),0,0,(round((sum(PDN_CONNECTIVITY_SUCCESSFUL)/sum(PDN_CONNECTIVITY_SUCCESSFUL+PDN_CONNECTIVITY_FAILED)),4)*100)) PDN_CONN_SR
from 	PCOFNS_PS_SMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID
"""
		else:
			sqlstring="""
select 
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
ta_id elementtype,
decode(nvl((sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL)),0),0,0,(round((sum(EPS_DEF_BEARER_ACT_SUCC)/(sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL))),4)*100)) ActDefault_EPS_Bearer_SR,
sum(EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL) ActDefaultEpsBearerRequest,
sum(EPS_DEF_BEARER_ACT_SUCC) ActDefaultEpsBearerAccept,
sum(EPS_DEF_BEARER_ACT_MME_FAIL) EPS_DEF_BEARER_ACT_MME_FAIL,
sum(EPS_DDBEARE_CONF_BY_UE) ddsucc,
sum(EPS_DDBEARER_REQ_BY_MME) ddatt,
decode(nvl(sum(EPS_DDBEARER_REQ_BY_MME),0),0,0,round(sum(EPS_DDBEARE_CONF_BY_UE)/sum(EPS_DDBEARER_REQ_BY_MME)*100,2)) dd_succ_rate,
sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE) ModEpsBearerRequest,
sum(GW_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_SUCCESS) ModEpsBearerAccept,
decode(nvl(sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE),0),0,0,round(sum(GW_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_SUCCESS)/sum(GW_INIT_BEARER_MOD_SUCCESS+GW_INIT_BEARER_MOD_FAILURE+HSS_INIT_BEARER_MOD_SUCCESS+HSS_INIT_BEARER_MOD_FAILURE)*100,2)) dd_succ_rate,
sum(EPS_DFBEARER_S5_S8_CONF_BY_SGW) s5s8succ,
sum(EPS_DFBEARER_S5_S8_REQ_BY_MME) s5s8att,
decode(nvl(sum(EPS_DFBEARER_S5_S8_REQ_BY_MME),0),0,0,round(sum(EPS_DFBEARER_S5_S8_CONF_BY_SGW)/sum(EPS_DFBEARER_S5_S8_REQ_BY_MME)*100,2)) s5s8_succ_rate,
sum(EPS_DDBEARER_S5_S8_CONF_BY_SGW) s5s8ddsucc,
sum(EPS_DDBEARER_S5_S8_REQ_BY_MME) s5s8ddatt,
decode(nvl(sum(EPS_DDBEARER_S5_S8_REQ_BY_MME),0),0,0,round(sum(EPS_DDBEARER_S5_S8_CONF_BY_SGW)/sum(EPS_DDBEARER_S5_S8_REQ_BY_MME)*100,2)) s5s8_dd_succ_rate,
sum(PDN_CONNECTIVITY_SUCCESSFUL) PdnSucc,
sum(PDN_CONNECTIVITY_FAILED) PdnFail,
sum(PDN_CONNECTIVITY_FAILED_UE) PdnFailUE,
sum(PDN_CONNECTIVITY_FAILED_SGW) PdnFailSGW,
sum(PDN_CONNECTIVITY_FAILED_MME) PdnFailMME,
sum(PDN_CONNECTIVITY_FAILED_ENB) PdnFailENB,
sum(PDN_CONNECT_FAILED_COLLISION) PdnFailColl,
sum(PDN_CONNECT_FAILED_UNSPECIFIED) PdnFailUnspec,
decode(nvl((sum(PDN_CONNECTIVITY_SUCCESSFUL+PDN_CONNECTIVITY_FAILED)),0),0,0,(round((sum(PDN_CONNECTIVITY_SUCCESSFUL)/sum(PDN_CONNECTIVITY_SUCCESSFUL+PDN_CONNECTIVITY_FAILED)),4)*100)) PDN_CONN_SR
from 	PCOFNS_PS_SMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID and EPS_DEF_BEARER_ACT_SUCC+EPS_DEF_BEARER_ACT_FAIL>0
"""

	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(fourg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name 
	order by objects.co_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
		else:
			sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name,ta_id 
	order by objects.co_name,ta_id,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
	else:
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
		else:
			sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name,ta_id 
	order by objects.CO_name,ta_id,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_4g_taupaging(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'TAC',
	u'InterMME SGW未切换TAU次数',
	u'InterMME TAU IN失败次数',
	u'InterMME SGW变更TAU次数',
	u'IntraMME SGW变更TAU成功次数',
	u'IntraMME SGW未TAU次数',
	u'IntraMME SGW未TAU成功次数',
	u'InterMME TAU成功率',
	u'TAU 次数',
	u'TAU成功次数',
	u'TAU成功率',
	u'跨系统TAU次数',
	u'跨系统TAU成功次数',
	u'跨系统TAU成功率',
	u'周期性TAU 次数',
	u'周期性TAU成功次数',
	u'周期性TAU成功率',
	u'一次寻呼成功次数',
	u'二次寻呼成功次数',
	u'寻呼次数',
	u'一次寻呼成功率',
	u'PAGING成功率',
	u'EPS PAGING VOLTE次数',
	u'EPS PAGING VOLTE成功次数',
	u'EPS PAGING VOLTE失败次数'
	]
	if (param.selectperiod=='60'):
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
'ALL' elementtype,
sum(INTERMME_TAU_WO_SGW_CHG_SUCC) two,
sum(INTERMME_TAU_IN_FAIL) three,
sum(EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC) five,
sum(INTRAMME_TAU_SGW_CHG_SUCC) six,
sum(INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL) seven,
sum(INTRATAU_WO_SGW_CHANGE_SUCC) eight,
decode(nvl(sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL),0),0,0,round((sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_WO_SGW_CHG_SUCC+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC)/sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL)*100),4)) tau_succ_rate,
sum(EPS_TAU_SUCC+EPS_TAU_FAIL) TAU_ALL,
sum(EPS_TAU_SUCC) TAU_SUCC,
decode(nvl((sum(EPS_TAU_SUCC+EPS_TAU_FAIL)),0),0,0,(round((sum(EPS_TAU_SUCC)/(sum(EPS_TAU_SUCC+EPS_TAU_FAIL))),4)*100)) TAU_SR,
sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL) INTER_SYS_TAU_ALL,
sum(EPS_INTER_TAU_OG_SUCC) INTER_SYS_TAU_SUCC,
decode(nvl((sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL)),0),0,0,(round((sum(EPS_INTER_TAU_OG_SUCC)/(sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL))),4)*100)) InterSystem_TAU_SR,
sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL) P_TAU_ALL,
sum(EPS_PERIODIC_TAU_SUCC) P_TAU_SUCC,
decode(nvl((sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL)),0),0,0,(round((sum(EPS_PERIODIC_TAU_SUCC)/(sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL))),4)*100)) P_TAU_SR,
sum(EPS_PAGING_1ST_ATTEMPT_SUCC) firstsucc,
sum(EPS_PAGING_SUCC-EPS_PAGING_1ST_ATTEMPT_SUCC) secondsucc,
sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL) page_att,
decode(nvl(sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL),0),0,0,round(sum(EPS_PAGING_1ST_ATTEMPT_SUCC)/sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL),4)*100) firstpagesucc_rate,
decode(nvl((sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL)),0),0,0,(round((sum(EPS_PAGING_SUCC)/(sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL))),4)*100)) PAGING_SR,
sum(EPS_PAGING_VOLTE_ATTEMPT) EPS_PAGING_VOLTE_ATTEMPT,
sum(EPS_PAGING_VOLTE_SUCC) EPS_PAGING_VOLTE_SUCC,
sum(EPS_PAGING_VOLTE_FAIL) EPS_PAGING_VOLTE_FAIL
from 	PCOFNS_PS_MMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID
"""
		else:
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
ta_id elementtype,
sum(INTERMME_TAU_WO_SGW_CHG_SUCC) two,
sum(INTERMME_TAU_IN_FAIL) three,
sum(EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC) five,
sum(INTRAMME_TAU_SGW_CHG_SUCC) six,
sum(INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL) seven,
sum(INTRATAU_WO_SGW_CHANGE_SUCC) eight,
decode(nvl(sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL),0),0,0,round((sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_WO_SGW_CHG_SUCC+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC)/sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL)*100),4)) tau_succ_rate,
sum(EPS_TAU_SUCC+EPS_TAU_FAIL) TAU_ALL,
sum(EPS_TAU_SUCC) TAU_SUCC,
decode(nvl((sum(EPS_TAU_SUCC+EPS_TAU_FAIL)),0),0,0,(round((sum(EPS_TAU_SUCC)/(sum(EPS_TAU_SUCC+EPS_TAU_FAIL))),4)*100)) TAU_SR,
sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL) INTER_SYS_TAU_ALL,
sum(EPS_INTER_TAU_OG_SUCC) INTER_SYS_TAU_SUCC,
decode(nvl((sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL)),0),0,0,(round((sum(EPS_INTER_TAU_OG_SUCC)/(sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL))),4)*100)) InterSystem_TAU_SR,
sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL) P_TAU_ALL,
sum(EPS_PERIODIC_TAU_SUCC) P_TAU_SUCC,
decode(nvl((sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL)),0),0,0,(round((sum(EPS_PERIODIC_TAU_SUCC)/(sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL))),4)*100)) P_TAU_SR,
sum(EPS_PAGING_1ST_ATTEMPT_SUCC) firstsucc,
sum(EPS_PAGING_SUCC-EPS_PAGING_1ST_ATTEMPT_SUCC) secondsucc,
sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL) page_att,
decode(nvl(sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL),0),0,0,round(sum(EPS_PAGING_1ST_ATTEMPT_SUCC)/sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL),4)*100) firstpagesucc_rate,
decode(nvl((sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL)),0),0,0,(round((sum(EPS_PAGING_SUCC)/(sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL))),4)*100)) PAGING_SR,
sum(EPS_PAGING_VOLTE_ATTEMPT) EPS_PAGING_VOLTE_ATTEMPT,
sum(EPS_PAGING_VOLTE_SUCC) EPS_PAGING_VOLTE_SUCC,
sum(EPS_PAGING_VOLTE_FAIL) EPS_PAGING_VOLTE_FAIL
from 	PCOFNS_PS_MMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID and EPS_ATTACH_SUCC+EPS_ATTACH_FAIL>0
"""
	else:
		if (param.selectmmeelement=='MMESGSN'):	
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
'ALL' elementtype,
sum(INTERMME_TAU_WO_SGW_CHG_SUCC) two,
sum(INTERMME_TAU_IN_FAIL) three,
sum(EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC) five,
sum(INTRAMME_TAU_SGW_CHG_SUCC) six,
sum(INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL) seven,
sum(INTRATAU_WO_SGW_CHANGE_SUCC) eight,
decode(nvl(sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL),0),0,0,round((sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_WO_SGW_CHG_SUCC+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC)/sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL)*100),4)) tau_succ_rate,
sum(EPS_TAU_SUCC+EPS_TAU_FAIL) TAU_ALL,
sum(EPS_TAU_SUCC) TAU_SUCC,
decode(nvl((sum(EPS_TAU_SUCC+EPS_TAU_FAIL)),0),0,0,(round((sum(EPS_TAU_SUCC)/(sum(EPS_TAU_SUCC+EPS_TAU_FAIL))),4)*100)) TAU_SR,
sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL) INTER_SYS_TAU_ALL,
sum(EPS_INTER_TAU_OG_SUCC) INTER_SYS_TAU_SUCC,
decode(nvl((sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL)),0),0,0,(round((sum(EPS_INTER_TAU_OG_SUCC)/(sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL))),4)*100)) InterSystem_TAU_SR,
sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL) P_TAU_ALL,
sum(EPS_PERIODIC_TAU_SUCC) P_TAU_SUCC,
decode(nvl((sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL)),0),0,0,(round((sum(EPS_PERIODIC_TAU_SUCC)/(sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL))),4)*100)) P_TAU_SR,
sum(EPS_PAGING_1ST_ATTEMPT_SUCC) firstsucc,
sum(EPS_PAGING_SUCC-EPS_PAGING_1ST_ATTEMPT_SUCC) secondsucc,
sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL) page_att,
decode(nvl(sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL),0),0,0,round(sum(EPS_PAGING_1ST_ATTEMPT_SUCC)/sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL),4)*100) firstpagesucc_rate,
decode(nvl((sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL)),0),0,0,(round((sum(EPS_PAGING_SUCC)/(sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL))),4)*100)) PAGING_SR,
sum(EPS_PAGING_VOLTE_ATTEMPT) EPS_PAGING_VOLTE_ATTEMPT,
sum(EPS_PAGING_VOLTE_SUCC) EPS_PAGING_VOLTE_SUCC,
sum(EPS_PAGING_VOLTE_FAIL) EPS_PAGING_VOLTE_FAIL
from 	PCOFNS_PS_MMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID
"""
		else:
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
ta_id elementtype,
sum(INTERMME_TAU_WO_SGW_CHG_SUCC) two,
sum(INTERMME_TAU_IN_FAIL) three,
sum(EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC) five,
sum(INTRAMME_TAU_SGW_CHG_SUCC) six,
sum(INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL) seven,
sum(INTRATAU_WO_SGW_CHANGE_SUCC) eight,
decode(nvl(sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL),0),0,0,round((sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_WO_SGW_CHG_SUCC+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC)/sum(INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+INTERMME_TAU_WO_SGW_CHG_SUCC+INTERMME_TAU_IN_FAIL+EPS_TAU_FAIL-INTRATAU_WO_SGW_CHANGE_FAIL+INTRAMME_TAU_SGW_CHG_SUCC+INTRATAU_WO_SGW_CHANGE_SUCC+INTRATAU_WO_SGW_CHANGE_FAIL)*100),4)) tau_succ_rate,
sum(EPS_TAU_SUCC+EPS_TAU_FAIL) TAU_ALL,
sum(EPS_TAU_SUCC) TAU_SUCC,
decode(nvl((sum(EPS_TAU_SUCC+EPS_TAU_FAIL)),0),0,0,(round((sum(EPS_TAU_SUCC)/(sum(EPS_TAU_SUCC+EPS_TAU_FAIL))),4)*100)) TAU_SR,
sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL) INTER_SYS_TAU_ALL,
sum(EPS_INTER_TAU_OG_SUCC) INTER_SYS_TAU_SUCC,
decode(nvl((sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL)),0),0,0,(round((sum(EPS_INTER_TAU_OG_SUCC)/(sum(EPS_INTER_TAU_OG_SUCC+EPS_INTER_TAU_OG_FAIL))),4)*100)) InterSystem_TAU_SR,
sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL) P_TAU_ALL,
sum(EPS_PERIODIC_TAU_SUCC) P_TAU_SUCC,
decode(nvl((sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL)),0),0,0,(round((sum(EPS_PERIODIC_TAU_SUCC)/(sum(EPS_PERIODIC_TAU_SUCC+EPS_PERIODIC_TAU_FAIL))),4)*100)) P_TAU_SR,
sum(EPS_PAGING_1ST_ATTEMPT_SUCC) firstsucc,
sum(EPS_PAGING_SUCC-EPS_PAGING_1ST_ATTEMPT_SUCC) secondsucc,
sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL) page_att,
decode(nvl(sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL),0),0,0,round(sum(EPS_PAGING_1ST_ATTEMPT_SUCC)/sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL),4)*100) firstpagesucc_rate,
decode(nvl((sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL)),0),0,0,(round((sum(EPS_PAGING_SUCC)/(sum(EPS_PAGING_SUCC+EPS_PAGING_FAIL))),4)*100)) PAGING_SR,
sum(EPS_PAGING_VOLTE_ATTEMPT) EPS_PAGING_VOLTE_ATTEMPT,
sum(EPS_PAGING_VOLTE_SUCC) EPS_PAGING_VOLTE_SUCC,
sum(EPS_PAGING_VOLTE_FAIL) EPS_PAGING_VOLTE_FAIL
from 	PCOFNS_PS_MMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID and EPS_ATTACH_SUCC+EPS_ATTACH_FAIL>0
"""

	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(fourg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name 
	order by objects.co_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
		else:
			sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name,ta_id 
	order by objects.co_name,ta_id,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
	else:
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
		else:
			sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name,ta_id 
	order by objects.CO_name,ta_id,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_cpu(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'MME CPU Type',
	u'MME CPU平均负荷',
	u'MME CPU峰值负荷',
	u'MME WO板卡数'
	]

	if (param.selectperiod=='60'):
		sqlstring="""
select
cpuload.fins_ID,
objects.co_Name MMESGSN,
cpuload.cu,
to_char(cpuload.period_start_time,'yyyy/mm/dd') Sdate,
to_char(cpuload.period_start_time,'hh24') Stime,
decode(nvl((sum(cpuload.AVE_LOAD_RATE_DEN)/15),0),0,0,(round(sum(cpuload.AVE_LOAD_RATE_SUM/15)/(sum(cpuload.AVE_LOAD_RATE_DEN)/15),2))) avecpuload,
max(cpuload.PEAK_LOAD_RATE_OF_OBJECT),
sum(cpuload.AVE_LOAD_RATE_DEN)/60
from 	PCOFNS_PS_LOAD_INDEX_RAW cpuload,  
		  UTP_COMMON_OBJECTS objects
where 
cpuload.fins_ID=objects.co_gid and cpuload.object_state=0
"""
	else:
		sqlstring="""
select
cpuload.fins_ID,
objects.co_Name MMESGSN,
CPULOAD.CU,
to_char(cpuload.period_start_time,'yyyy/mm/dd') Sdate,
to_char(cpuload.period_start_time,'hh24:mi') Stime,
decode(nvl((sum(cpuload.AVE_LOAD_RATE_DEN)/15),0),0,0,(round(sum(cpuload.AVE_LOAD_RATE_SUM/15)/(sum(cpuload.AVE_LOAD_RATE_DEN)/15),2))) avecpuload,
max(cpuload.PEAK_LOAD_RATE_OF_OBJECT),
sum(cpuload.AVE_LOAD_RATE_DEN)/15
from 	PCOFNS_PS_LOAD_INDEX_RAW cpuload,  
		  UTP_COMMON_OBJECTS objects
where 
cpuload.fins_ID=objects.co_gid and cpuload.object_state=0
"""
	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(cpuload.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(cpuload.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(cpuload.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(cpuload.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(cpuload.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(cpuload.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(cpuload.period_start_time,'yyyy/mm/dd'), to_char(cpuload.period_start_time,'hh24'), cpuload.fins_id, objects.co_name ,cpuload.CU
	order by objects.co_name,to_char(cpuload.period_start_time,'yyyy/mm/dd'),to_char(cpuload.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(cpuload.period_start_time,'yyyy/mm/dd'),to_char(cpuload.period_start_time,'hh24:mi'), cpuload.fins_ID, objects.co_name ,cpuload.CU
	order by objects.CO_name,to_char(cpuload.period_start_time,'yyyy/mm/dd'),to_char(cpuload.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1	
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		print 'mmecpu something error!'
		return (['error'],None)

def mme_4g_auth(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'ULR次数',
	u'ULR成功次数',
	u'ULR成功率',
	u'DNS查询次数',
	u'DNS成功次数',
	u'DNS成功率',
	u'鉴权成功次数',
	u'鉴权次数',
	u'鉴权失败UE Reject次数',
	u'鉴权失败MME Reject次数',
	u'鉴权成功率'
	]

	if (param.selectperiod=='60'):
		sqlstring="""
select
fourg.fins_ID,
objects.co_Name MMESGSN,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
sum(S6A_UPDATE_LOCATION_REQ_SENT) ULR_REQ,
sum(S6A_UPDATE_LOCATION_ANS_RCV) ULR_SUCC,
decode(nvl(sum(S6A_UPDATE_LOCATION_REQ_SENT),0),0,0,round(sum(S6A_UPDATE_LOCATION_ANS_RCV)/sum(S6A_UPDATE_LOCATION_REQ_SENT)*100,2)) ulr_succ_rate,
sum(DNS_MME_QUERY_ATTEMPTS) DNS_MME_QUERY_ATTEMPTS,
sum(DNS_MME_QUERY_SUCC) DNS_MME_QUERY_SUCC,
decode(nvl(sum(DNS_MME_QUERY_ATTEMPTS),0),0,0,round(sum(DNS_MME_QUERY_SUCC)/sum(DNS_MME_QUERY_ATTEMPTS)*100,2)) dns_succ_rate,
sum(EPS_AUTH_SUCC) auth_succ,
sum(EPS_AUTH_SUCC+EPS_AUTH_FAIL_BY_UE+EPS_AUTH_REJECT_BY_MME) auth_att,
sum(EPS_AUTH_FAIL_BY_UE) fail_ue,
sum(EPS_AUTH_REJECT_BY_MME) fail_mme,
decode(nvl(sum(EPS_AUTH_SUCC+EPS_AUTH_FAIL_BY_UE+EPS_AUTH_REJECT_BY_MME),0),0,0,(round((sum(EPS_AUTH_SUCC)/sum(EPS_AUTH_SUCC+EPS_AUTH_FAIL_BY_UE+EPS_AUTH_REJECT_BY_MME)),4)*100)) auth_succ_rate
from 	PCOFNS_PS_SMLM_FLEXINS_RAW fourg,
	    PCOFNS_PS_S6A_FLEXINS_RAW b,  
		PCOFNS_PS_EPDNS_FLEXINS_RAW c,  
		    UTP_COMMON_OBJECTS objects
where 
fourg.fins_ID=objects.co_gid and b.fins_id=objects.co_gid and c.fins_id=objects.co_gid
and fourg.period_start_time=b.period_start_time and fourg.period_start_time=c.period_start_time
"""
	else:
		sqlstring="""
select
fourg.fins_ID,
objects.co_Name MMESGSN,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
sum(S6A_UPDATE_LOCATION_REQ_SENT) ULR_REQ,
sum(S6A_UPDATE_LOCATION_ANS_RCV) ULR_SUCC,
decode(nvl(sum(S6A_UPDATE_LOCATION_REQ_SENT),0),0,0,round(sum(S6A_UPDATE_LOCATION_ANS_RCV)/sum(S6A_UPDATE_LOCATION_REQ_SENT)*100,2)) ulr_succ_rate,
sum(DNS_MME_QUERY_ATTEMPTS) DNS_MME_QUERY_ATTEMPTS,
sum(DNS_MME_QUERY_SUCC) DNS_MME_QUERY_SUCC,
decode(nvl(sum(DNS_MME_QUERY_ATTEMPTS),0),0,0,round(sum(DNS_MME_QUERY_SUCC)/sum(DNS_MME_QUERY_ATTEMPTS)*100,2)) dns_succ_rate,
sum(EPS_AUTH_SUCC) auth_succ,
sum(EPS_AUTH_SUCC+EPS_AUTH_FAIL_BY_UE+EPS_AUTH_REJECT_BY_MME) auth_att,
sum(EPS_AUTH_FAIL_BY_UE) fail_ue,
sum(EPS_AUTH_REJECT_BY_MME) fail_mme,
decode(nvl(sum(EPS_AUTH_SUCC+EPS_AUTH_FAIL_BY_UE+EPS_AUTH_REJECT_BY_MME),0),0,0,(round((sum(EPS_AUTH_SUCC)/sum(EPS_AUTH_SUCC+EPS_AUTH_FAIL_BY_UE+EPS_AUTH_REJECT_BY_MME)),4)*100)) auth_succ_rate
from 	PCOFNS_PS_SMLM_FLEXINS_RAW fourg,  
	    PCOFNS_PS_S6A_FLEXINS_RAW b,
		PCOFNS_PS_EPDNS_FLEXINS_RAW c,  
		    UTP_COMMON_OBJECTS objects
where 
fourg.fins_ID=objects.co_gid and b.fins_id=objects.co_gid and c.fins_id=objects.co_gid
and fourg.period_start_time=b.period_start_time and fourg.period_start_time=c.period_start_time
"""

	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(fourg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name 
	order by objects.co_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1	
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		print '4g something error!'
		return (['error'],None)
		
def mme_4g_csfb(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'联合附着成功次数EPS',
	u'联合附着失败次数EPS',
	u'联合附着成功率EPS',
	u'联合附着成功次数EPS only',
	u'联合附着成功次数EPS only',
	u'联合附着成功率EPS only',
	u'CSFB MO次数',
	u'CSFB MT次数',
	u'CSFB MO紧急次数',
	u'联合INTRAMME TAU成功次数',
	u'联合INTRAMME TAU失败次数',
	u'联合INTRAMME TAU成功率',
	u'联合INTRAMME TAU（IMSI attach）成功次数',
	u'联合INTRAMME TAU（IMSI attach）失败次数',
	u'联合INTRAMME TAU（IMSI attach）成功率',
	u'联合INTER SYSTEM TAU成功次数',
	u'联合INTER SYSTEM TAU失败次数',
	u'联合INTER SYSTEM TAU成功率'
	]
	if (param.selectperiod=='60'):
		sqlstring="""
select
fourg.fins_ID,
objects.co_Name MMESGSN,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
sum(EPS_COMBINED_ATTACH_SUCC) EPS_COMBINED_ATTACH_SUCC,
sum(EPS_CMBND_ATTACH_FAIL) EPS_CMBND_ATTACH_FAIL,
decode(nvl(sum(EPS_COMBINED_ATTACH_SUCC+EPS_CMBND_ATTACH_FAIL),0),0,0,round(sum(EPS_COMBINED_ATTACH_SUCC)/sum(EPS_COMBINED_ATTACH_SUCC+EPS_CMBND_ATTACH_FAIL)*100,2)) EPS_COMBINED_ATTACH_SUCC_RATE,
sum(EPS_CMBND_ATTACH_EPS_SUCC) EPS_CMBND_ATTACH_EPS_SUCC,
sum(EPS_CMBND_ATTACH_EPS_FAIL) EPS_CMBND_ATTACH_EPS_FAIL,
decode(nvl(sum(EPS_CMBND_ATTACH_EPS_SUCC+EPS_CMBND_ATTACH_EPS_FAIL),0),0,0,round(sum(EPS_CMBND_ATTACH_EPS_SUCC)/sum(EPS_CMBND_ATTACH_EPS_SUCC+EPS_CMBND_ATTACH_EPS_FAIL)*100,2)) EPS_CMBND_ATTACH_EPS_SUCC_RATE,
sum(ESR_MO_ATTEMPTS) ESR_MO_ATTEMPTS,
sum(ESR_MT_ATTEMPTS) ESR_MT_ATTEMPTS,
sum(ESR_MO_EMERGENCY_ATTEMPTS) ESR_MO_EMERGENCY_ATTEMPTS,
sum(EPS_CMB_INTRA_TAU_SUCC) EPS_CMB_INTRA_TAU_SUCC,
sum(EPS_CMB_INTRA_TAU_FAIL) EPS_CMB_INTRA_TAU_FAIL,
decode(nvl(sum(EPS_CMB_INTRA_TAU_SUCC+EPS_CMB_INTRA_TAU_FAIL),0),0,0,round(sum(EPS_CMB_INTRA_TAU_SUCC)/sum(EPS_CMB_INTRA_TAU_SUCC+EPS_CMB_INTRA_TAU_FAIL)*100,2)) EPS_CMB_INTRA_TAU_SUCC_RATE,
sum(EPS_CMB_INTRA_TAU_IMSI_ATT_SUC) EPS_CMB_INTRA_TAU_IMSI_ATT_SUC,
sum(EPS_CMB_INTRA_TAU_IMSI_ATT_FAI) EPS_CMB_INTRA_TAU_IMSI_ATT_FAI,
decode(nvl(sum(EPS_CMB_INTRA_TAU_IMSI_ATT_SUC+EPS_CMB_INTRA_TAU_IMSI_ATT_FAI),0),0,0,round(sum(EPS_CMB_INTRA_TAU_IMSI_ATT_SUC)/sum(EPS_CMB_INTRA_TAU_IMSI_ATT_SUC+EPS_CMB_INTRA_TAU_IMSI_ATT_FAI)*100,2)) EPS_CMB_INTRA_TAU_IMSI_RATE,
sum(EPS_CMB_INTER_TAU_SUCC) EPS_CMB_INTER_TAU_SUCC,
sum(EPS_CMB_INTER_TAU_FAIL) EPS_CMB_INTER_TAU_FAIL,
decode(nvl(sum(EPS_CMB_INTER_TAU_SUCC+EPS_CMB_INTER_TAU_FAIL),0),0,0,round(sum(EPS_CMB_INTER_TAU_SUCC)/sum(EPS_CMB_INTER_TAU_SUCC+EPS_CMB_INTER_TAU_FAIL)*100,2)) EPS_CMB_INTER_TAU_SUCC_RATE
from 	PCOFNS_PS_MMMT_TA_RAW fourg,  
		  UTP_COMMON_OBJECTS objects
where 
fourg.fins_ID=objects.co_gid 
"""
	else:
		sqlstring="""
select
fourg.fins_ID,
objects.co_Name MMESGSN,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
sum(EPS_COMBINED_ATTACH_SUCC) EPS_COMBINED_ATTACH_SUCC,
sum(EPS_CMBND_ATTACH_FAIL) EPS_CMBND_ATTACH_FAIL,
decode(nvl(sum(EPS_COMBINED_ATTACH_SUCC+EPS_CMBND_ATTACH_FAIL),0),0,0,round(sum(EPS_COMBINED_ATTACH_SUCC)/sum(EPS_COMBINED_ATTACH_SUCC+EPS_CMBND_ATTACH_FAIL)*100,2)) EPS_COMBINED_ATTACH_SUCC_RATE,
sum(EPS_CMBND_ATTACH_EPS_SUCC) EPS_CMBND_ATTACH_EPS_SUCC,
sum(EPS_CMBND_ATTACH_EPS_FAIL) EPS_CMBND_ATTACH_EPS_FAIL,
decode(nvl(sum(EPS_CMBND_ATTACH_EPS_SUCC+EPS_CMBND_ATTACH_EPS_FAIL),0),0,0,round(sum(EPS_CMBND_ATTACH_EPS_SUCC)/sum(EPS_CMBND_ATTACH_EPS_SUCC+EPS_CMBND_ATTACH_EPS_FAIL)*100,2)) EPS_CMBND_ATTACH_EPS_SUCC_RATE,
sum(ESR_MO_ATTEMPTS) ESR_MO_ATTEMPTS,
sum(ESR_MT_ATTEMPTS) ESR_MT_ATTEMPTS,
sum(ESR_MO_EMERGENCY_ATTEMPTS) ESR_MO_EMERGENCY_ATTEMPTS,
sum(EPS_CMB_INTRA_TAU_SUCC) EPS_CMB_INTRA_TAU_SUCC,
sum(EPS_CMB_INTRA_TAU_FAIL) EPS_CMB_INTRA_TAU_FAIL,
decode(nvl(sum(EPS_CMB_INTRA_TAU_SUCC+EPS_CMB_INTRA_TAU_FAIL),0),0,0,round(sum(EPS_CMB_INTRA_TAU_SUCC)/sum(EPS_CMB_INTRA_TAU_SUCC+EPS_CMB_INTRA_TAU_FAIL)*100,2)) EPS_CMB_INTRA_TAU_SUCC_RATE,
sum(EPS_CMB_INTRA_TAU_IMSI_ATT_SUC) EPS_CMB_INTRA_TAU_IMSI_ATT_SUC,
sum(EPS_CMB_INTRA_TAU_IMSI_ATT_FAI) EPS_CMB_INTRA_TAU_IMSI_ATT_FAI,
decode(nvl(sum(EPS_CMB_INTRA_TAU_IMSI_ATT_SUC+EPS_CMB_INTRA_TAU_IMSI_ATT_FAI),0),0,0,round(sum(EPS_CMB_INTRA_TAU_IMSI_ATT_SUC)/sum(EPS_CMB_INTRA_TAU_IMSI_ATT_SUC+EPS_CMB_INTRA_TAU_IMSI_ATT_FAI)*100,2)) EPS_CMB_INTRA_TAU_IMSI_RATE,
sum(EPS_CMB_INTER_TAU_SUCC) EPS_CMB_INTER_TAU_SUCC,
sum(EPS_CMB_INTER_TAU_FAIL) EPS_CMB_INTER_TAU_FAIL,
decode(nvl(sum(EPS_CMB_INTER_TAU_SUCC+EPS_CMB_INTER_TAU_FAIL),0),0,0,round(sum(EPS_CMB_INTER_TAU_SUCC)/sum(EPS_CMB_INTER_TAU_SUCC+EPS_CMB_INTER_TAU_FAIL)*100,2)) EPS_CMB_INTER_TAU_SUCC_RATE
from 	PCOFNS_PS_MMMT_TA_RAW fourg,
		  UTP_COMMON_OBJECTS objects
where 
fourg.fins_ID=objects.co_gid 
"""
	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(fourg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name 
	order by objects.co_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1	
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_4g_volte(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'TAC',
	u'IMS网络PDN连接请求次数',
	u'IMS网络PDN连接完成次数',
	u'IMS网络PDN连接成功率',
	u'语音业务专用承载激活请求次数',
	u'语音业务专用承载激活成功次数',
	u'语音业务专用承载激活成功率'
	]

	if (param.selectperiod=='60'):
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
'ALL' elementtype,
sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL) allvoltepdnatt,
sum(EPS_PDN_ACT_FOR_VOLTE_SUCC) voltepdnsucc,
decode(nvl((sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL)),0),0,0,(round((sum(EPS_PDN_ACT_FOR_VOLTE_SUCC)/(sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL))),4)*100)) voltepdn_SR,
sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL) ddvolteatt,
sum(EPS_DD_BEARER_VOLTE_ACT_SUCC) ddvoltesucc,
decode(nvl((sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL)),0),0,100,(round((sum(EPS_DD_BEARER_VOLTE_ACT_SUCC)/(sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL))),4)*100)) ddvolte_SR
from 	PCOFNS_PS_SMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID
"""
		else:
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
ta_id elementtype,
sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL) allvoltepdnatt,
sum(EPS_PDN_ACT_FOR_VOLTE_SUCC) voltepdnsucc,
decode(nvl((sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL)),0),0,0,(round((sum(EPS_PDN_ACT_FOR_VOLTE_SUCC)/(sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL))),4)*100)) voltepdn_SR,
sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL) ddvolteatt,
sum(EPS_DD_BEARER_VOLTE_ACT_SUCC) ddvoltesucc,
decode(nvl((sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL)),0),0,100,(round((sum(EPS_DD_BEARER_VOLTE_ACT_SUCC)/(sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL))),4)*100)) ddvolte_SR
from 	PCOFNS_PS_SMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID and EPS_DEF_BEARER_ACT_SUCC>0
"""
	else:
		if (param.selectmmeelement=='MMESGSN'):	
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
'ALL' elementtype,
sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL) allvoltepdnatt,
sum(EPS_PDN_ACT_FOR_VOLTE_SUCC) voltepdnsucc,
decode(nvl((sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL)),0),0,0,(round((sum(EPS_PDN_ACT_FOR_VOLTE_SUCC)/(sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL))),4)*100)) voltepdn_SR,
sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL) ddvolteatt,
sum(EPS_DD_BEARER_VOLTE_ACT_SUCC) ddvoltesucc,
decode(nvl((sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL)),0),0,100,(round((sum(EPS_DD_BEARER_VOLTE_ACT_SUCC)/(sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL))),4)*100)) ddvolte_SR
from 	PCOFNS_PS_SMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID
"""
		else:
			sqlstring="""
select
fourg.fins_id id,
objects.CO_NAME,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
ta_id elementtype,
sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL) allvoltepdnatt,
sum(EPS_PDN_ACT_FOR_VOLTE_SUCC) voltepdnsucc,
decode(nvl((sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL)),0),0,0,(round((sum(EPS_PDN_ACT_FOR_VOLTE_SUCC)/(sum(EPS_PDN_ACT_FOR_VOLTE_SUCC+EPS_PDN_ACT_FOR_VOLTE_FAIL))),4)*100)) voltepdn_SR,
sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL) ddvolteatt,
sum(EPS_DD_BEARER_VOLTE_ACT_SUCC) ddvoltesucc,
decode(nvl((sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL)),0),0,100,(round((sum(EPS_DD_BEARER_VOLTE_ACT_SUCC)/(sum(EPS_DD_BEARER_VOLTE_ACT_SUCC+EPS_DD_BEARER_VOLTE_ACT_FAIL))),4)*100)) ddvolte_SR
from 	PCOFNS_PS_SMMT_TA_RAW fourg,
			UTP_COMMON_OBJECTS objects
where 
fourg.FINS_ID=objects.CO_GID and EPS_DEF_BEARER_ACT_SUCC>0
"""
	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(fourg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name 
	order by objects.co_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
		else:
			sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name,ta_id 
	order by objects.co_name,ta_id,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
	else:
		if (param.selectmmeelement=='MMESGSN'):
			sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
		else:
			sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name,ta_id 
	order by objects.CO_name,ta_id,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)
		
def mme_4g_esrvcc(cursor,param):
	title=[
	u'设备ID',
	u'设备名称',
	u'日期',
	u'时间',
	u'SRVCC切换到2G成功次数',
	u'SRVCC切换到2G失败次数',
	u'SRVCC切换到2G取消次数',
	u'SRVCC切换成功率'
	]
	if (param.selectperiod=='60'):
		sqlstring="""
select
fourg.fins_ID,
objects.co_Name MMESGSN,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24') Stime,
sum(SRVCC_CS_HO_2G_SUCC) SRVCC_CS_HO_2G_SUCC,
sum(SRVCC_CS_HO_2G_FAIL) SRVCC_CS_HO_2G_FAIL,
sum(SRVCC_2G_CANCELLED) SRVCC_2G_CANCELLED,
decode(nvl(sum(SRVCC_CS_HO_2G_SUCC+SRVCC_CS_HO_2G_FAIL+SRVCC_2G_CANCELLED),0),0,0,round(sum(SRVCC_CS_HO_2G_SUCC)/sum(SRVCC_CS_HO_2G_SUCC+SRVCC_CS_HO_2G_FAIL+SRVCC_2G_CANCELLED)*100,2)) SRVCC_2G_SUCC_RATE
from 	PCOFNS_PS_UMLM_FLEXINS_RAW fourg,  
		  UTP_COMMON_OBJECTS objects
where 
fourg.fins_ID=objects.co_gid 
"""
	else:
		sqlstring="""
select
fourg.fins_ID,
objects.co_Name MMESGSN,
to_char(fourg.period_start_time,'yyyy/mm/dd') Sdate,
to_char(fourg.period_start_time,'hh24:mi') Stime,
sum(SRVCC_CS_HO_2G_SUCC) SRVCC_CS_HO_2G_SUCC,
sum(SRVCC_CS_HO_2G_FAIL) SRVCC_CS_HO_2G_FAIL,
sum(SRVCC_2G_CANCELLED) SRVCC_2G_CANCELLED,
decode(nvl(sum(SRVCC_CS_HO_2G_SUCC+SRVCC_CS_HO_2G_FAIL+SRVCC_2G_CANCELLED),0),0,0,round(sum(SRVCC_CS_HO_2G_SUCC)/sum(SRVCC_CS_HO_2G_SUCC+SRVCC_CS_HO_2G_FAIL+SRVCC_2G_CANCELLED)*100,2)) SRVCC_2G_SUCC_RATE
from 	PCOFNS_PS_UMLM_FLEXINS_RAW fourg,  
		  UTP_COMMON_OBJECTS objects
where 
fourg.fins_ID=objects.co_gid 
"""
	if (param.selectmmesgsn<>'all'):
		sqlstring=sqlstring+" and objects.co_name= \'"+param.selectmmesgsn+"\' " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and to_char(fourg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and to_char(fourg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')>=\'"+param.starttime+\
		" and to_char(fourg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
		"\' and to_char(fourg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=""" 
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'), to_char(fourg.period_start_time,'hh24'), fourg.fins_id, objects.co_name 
	order by objects.co_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24')
	"""
	else:
		sqlstring1="""
	group by to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi'), fourg.fins_ID, objects.co_name 
	order by objects.CO_name,to_char(fourg.period_start_time,'yyyy/mm/dd'),to_char(fourg.period_start_time,'hh24:mi')
	"""
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	try:
		cursor.execute(sqlstring)
		row=cursor.fetchall()
		return (title,row)
	except :
		#print 'something error!'
		return (['error'],None)