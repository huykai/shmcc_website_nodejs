# -*- coding: utf-8 -*-

import sys
import os
import io
import json
import logging
import time
import datetime
import re

import cx_Oracle as oracle
from CMG_statis_new import *
import reportsuite_sql

runmode = "test"
(dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "cmgdb")
print "cmgdb parameter: ", dbuser,dbpasswd,dburl,dburlport,db_dbname
cmgdb = oracle.connect(dbuser, dbpasswd, dburl)
cmgdbcursor=cmgdb.cursor()

    
createtable_sqlstring = """
create global temporary table jf_M11_2097590963 on commit preserve rows as
  select
a.period_start_time,
        a.cmg_gid,
AVG(period_duration) period_duration,
        SUM(giGnDlBytes) giGnDlBytes,
        SUM(giGnDlPackets) giGnDlPackets,
        SUM(giGpDlBytes) giGpDlBytes,
        SUM(giGpDlPackets) giGpDlPackets,
        SUM(giS1uDlBytes) giS1uDlBytes,
        SUM(giS1uDlPackets) giS1uDlPackets,
        SUM(giS2aDlBytes) giS2aDlBytes,
        SUM(giS2aDlPackets) giS2aDlPackets,
        SUM(giS2bDlBytes) giS2bDlBytes,
        SUM(giS2bDlPackets) giS2bDlPackets,
        SUM(giS5uDlBytes) giS5uDlBytes,
        SUM(giS5uDlPackets) giS5uDlPackets,
        SUM(giS8uDlBytes) giS8uDlBytes,
        SUM(giS8uDlPackets) giS8uDlPackets,
        SUM(gnGiUlBytes) gnGiUlBytes,
        SUM(gnGiUlPackets) gnGiUlPackets,
        SUM(gpGiUlBytes) gpGiUlBytes,
        SUM(gpGiUlPackets) gpGiUlPackets,
        SUM(s1uGiUlBytes) s1uGiUlBytes,
        SUM(s1uGiUlPackets) s1uGiUlPackets,
        SUM(s2aGiUlBytes) s2aGiUlBytes,
        SUM(s2aGiUlPackets) s2aGiUlPackets,
        SUM(s2bGiUlBytes) s2bGiUlBytes,
        SUM(s2bGiUlPackets) s2bGiUlPackets,
        SUM(s5uGiUlBytes) s5uGiUlBytes,
        SUM(s5uGiUlPackets) s5uGiUlPackets,
        SUM(s8uGiUlBytes) s8uGiUlBytes,
        SUM(s8uGiUlPackets) s8uGiUlPackets
from
        (
select
          trunc( p.period_start_time, 'mi' ) period_start_time,
        "sam".co_gid sam_gid,
        "cmg".co_gid cmg_gid,
        p.epc_id epc_id,
        p.gpname_id gpname_id,
        p.group_id group_id,
        p.slot_id slot_id,
        p.mda_id mda_id,
          SUM(period_duration) period_duration,
        SUM(giGnDlBytes) giGnDlBytes,
        SUM(giGnDlPackets) giGnDlPackets,
        SUM(giGpDlBytes) giGpDlBytes,
        SUM(giGpDlPackets) giGpDlPackets,
        SUM(giS1uDlBytes) giS1uDlBytes,
        SUM(giS1uDlPackets) giS1uDlPackets,
        SUM(giS2aDlBytes) giS2aDlBytes,
        SUM(giS2aDlPackets) giS2aDlPackets,
        SUM(giS2bDlBytes) giS2bDlBytes,
        SUM(giS2bDlPackets) giS2bDlPackets,
        SUM(giS5uDlBytes) giS5uDlBytes,
        SUM(giS5uDlPackets) giS5uDlPackets,
        SUM(giS8uDlBytes) giS8uDlBytes,
        SUM(giS8uDlPackets) giS8uDlPackets,
        SUM(gnGiUlBytes) gnGiUlBytes,
        SUM(gnGiUlPackets) gnGiUlPackets,
        SUM(gpGiUlBytes) gpGiUlBytes,
        SUM(gpGiUlPackets) gpGiUlPackets,
        SUM(s1uGiUlBytes) s1uGiUlBytes,
        SUM(s1uGiUlPackets) s1uGiUlPackets,
        SUM(s2aGiUlBytes) s2aGiUlBytes,
        SUM(s2aGiUlPackets) s2aGiUlPackets,
        SUM(s2bGiUlBytes) s2bGiUlBytes,
        SUM(s2bGiUlPackets) s2bGiUlPackets,
        SUM(s5uGiUlBytes) s5uGiUlBytes,
        SUM(s5uGiUlPackets) s5uGiUlPackets,
        SUM(s8uGiUlBytes) s8uGiUlBytes,
        SUM(s8uGiUlPackets) s8uGiUlPackets
        from
          
            utp_common_objects "plmn",
            utp_common_objects "sam",
            utp_common_objects "cmg",
          epccmg_ps_m11_mda_raw p
        where
           "plmn".co_gid in ( '100000' ) 
          and period_start_time >= to_date('2019/01/19 00:00:00', 'yyyy/mm/dd hh24:mi:ss')
          and period_start_time < to_date('2019/01/20 00:00:00', 'yyyy/mm/dd hh24:mi:ss')
          and "plmn".co_oc_id = 16
          and "sam".co_gid = p.sam_id               
          and "sam".co_parent_gid = "plmn".co_gid
          and "sam".co_oc_id = 5273
          and "cmg".co_gid = p.cmg_id               
          and "cmg".co_parent_gid = "sam".co_gid
          and "cmg".co_oc_id = 5313
        group by
          trunc( p.period_start_time, 'mi' ),
        "sam".co_gid,
        "cmg".co_gid,
        p.epc_id,
        p.gpname_id,
        p.group_id,
        p.slot_id,
        p.mda_id
) a
group by
a.period_start_time,
        a.cmg_gid
"""
select_sqlstring = """
select
        M11.period_start_time period_start_time,
        nvl("sam".co_name, nvl("sam".co_object_instance, 'NN('||"sam".co_gid||')')) "SAM name",
        nvl("cmg".co_name, nvl("cmg".co_object_instance, 'NN('||"cmg".co_gid||')')) "CMG name",
        M11.cmg_gid, nvl("cmg".co_ext_dn, "cmg".co_dn) "DN",
        to_number((M11.giGnDlBytes+M11.giGpDlBytes)/(1024*1024)) cmg_364a,
        to_number((M11.gnGiUlBytes+M11.gpGiUlBytes)/(1024*1024)) cmg_363a,
        to_number((M11.giGnDlBytes+ M11.giGpDlBytes+ M11.gnGiUlBytes+ M11.gpGiUlBytes) / (1024*1024)) cmg_1a,
        to_number((M11.giS1uDlBytes+M11.giS5uDlBytes+M11.giS8uDlBytes)/(1024*1024)) cmg_366a,
        to_number((M11.s1uGiUlBytes+M11.s5uGiUlBytes+M11.s8uGiUlBytes)/(1024*1024)) cmg_365a,
        to_number((M11.giS1uDlBytes+ M11.giS5uDlBytes+ M11.giS8uDlBytes+ M11.s1uGiUlBytes+ M11.s5uGiUlBytes+ M11.s8uGiUlBytes) / (1024*1024)) cmg_2a,
        to_number((M11.giS1uDlBytes+M11.giS5uDlBytes+M11.giS8uDlBytes+M11.giGnDlBytes+M11.giGpDlBytes)/(1024*1024)) cmg_375a,
        to_number((M11.s1uGiUlBytes+M11.s5uGiUlBytes+M11.s8uGiUlBytes+M11.gnGiUlBytes+M11.gpGiUlBytes)/(1024*1024)) cmg_374a,
        to_number((M11.giS1uDlBytes+ M11.giS5uDlBytes+ M11.giS8uDlBytes+ M11.giGnDlBytes+ M11.giGpDlBytes+ M11.s1uGiUlBytes+ M11.s5uGiUlBytes+ M11.s8uGiUlBytes+ M11.gnGiUlBytes+ M11.gpGiUlBytes) / (1024*1024)) cmg_3a,
        to_number((M11.giS1uDlBytes)/(1024*1024)) cmg_9a,
        to_number((M11.s1uGiUlBytes)/(1024*1024)) cmg_8a,
        to_number((M11.giS1uDlBytes+M11.s1uGiUlBytes)/(1024*1024)) cmg_380a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.giS1uDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_45a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.s1uGiUlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_44a,
        to_number(decode( (M11.period_duration*60*(1024*1024)), 0, NULL, (8*(M11.s1uGiUlBytes+M11.giS1uDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_416a,
        to_number(M11.giS1uDlPackets) cmg_27a,
        to_number(M11.s1uGiUlPackets) cmg_26a,
        to_number(M11.s1uGiUlPackets+M11.giS1uDlPackets) cmg_417a,
        to_number((M11.giS5uDlBytes)/(1024*1024)) cmg_11a,
        to_number((M11.s5uGiUlBytes)/(1024*1024)) cmg_10a,
        to_number((M11.giS5uDlBytes+M11.s5uGiUlBytes)/(1024*1024)) cmg_381a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.giS5uDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_47a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.s5uGiUlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_46a,
        to_number(decode( (M11.period_duration*60*(1024*1024)), 0, NULL, (8*(M11.s5uGiUlBytes+M11.giS5uDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_418a,
        to_number(M11.giS5uDlPackets) cmg_29a,
        to_number(M11.s5uGiUlPackets) cmg_28a,
        to_number(M11.s5uGiUlPackets+M11.giS5uDlPackets) cmg_419a,
        to_number((M11.giS8uDlBytes)/(1024*1024)) cmg_13a,
        to_number((M11.s8uGiUlBytes)/(1024*1024)) cmg_12a,
        to_number((M11.giS8uDlBytes+M11.s8uGiUlBytes)/(1024*1024)) cmg_382a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.giS8uDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_49a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.s8uGiUlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_48a,
        to_number(decode( (M11.period_duration*60*(1024*1024)), 0, NULL, (8*(M11.s8uGiUlBytes+M11.giS8uDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_420a,
        to_number((M11.giS8uDlPackets)) cmg_31a,
        to_number(M11.s8uGiUlPackets) cmg_30a,
        to_number(M11.s8uGiUlPackets+M11.giS8uDlPackets) cmg_421a,
        to_number((M11.giGnDlBytes)/(1024*1024)) cmg_15a,
        to_number((M11.gnGiUlBytes)/(1024*1024)) cmg_14a,
        to_number((M11.giGnDlBytes+M11.gnGiUlBytes)/(1024*1024)) cmg_383a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.giGnDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_51a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.gnGiUlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_50a,
        to_number(decode( (M11.period_duration*60*(1024*1024)), 0, NULL, (8*(M11.gnGiUlBytes+M11.giGnDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_422a,
        to_number((M11.giGnDlPackets)) cmg_33a,
        to_number((M11.gnGiUlPackets)) cmg_32a,
        to_number(M11.gnGiUlPackets+M11.giGnDlPackets) cmg_423a,
        to_number((M11.giGpDlBytes)/(1024*1024)) cmg_17a,
        to_number((M11.gpGiUlBytes)/(1024*1024)) cmg_16a,
        to_number((M11.giGpDlBytes+M11.gpGiUlBytes)/(1024*1024)) cmg_384a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.giGpDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_53a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.gpGiUlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_52a,
        to_number(decode( (M11.period_duration*60*(1024*1024)), 0, NULL, (8*(M11.gpGiUlBytes+M11.giGpDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_424a,
        to_number((M11.giGpDlPackets)) cmg_35a,
        to_number((M11.gpGiUlPackets)) cmg_34a,
        to_number(M11.gpGiUlPackets+M11.giGpDlPackets) cmg_425a,
        to_number((M11.giS2aDlBytes)/(1024*1024)) cmg_19a,
        to_number((M11.s2aGiUlBytes)/(1024*1024)) cmg_18a,
        to_number((M11.giS2aDlBytes+M11.s2aGiUlBytes)/(1024*1024)) cmg_385a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.giS2aDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_55a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.s2aGiUlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_54a,
        to_number(decode( (M11.period_duration*60*(1024*1024)), 0, NULL, (8*(M11.s2aGiUlBytes+M11.giS2aDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_426a,
        to_number((M11.giS2aDlPackets)) cmg_37a,
        to_number((M11.s2aGiUlPackets)) cmg_36a,
        to_number(M11.s2aGiUlPackets+M11.giS2aDlPackets) cmg_427a,
        to_number((M11.giS2bDlBytes)/(1024*1024)) cmg_21a,
        to_number((M11.s2bGiUlBytes)/(1024*1024)) cmg_20a,
        to_number((M11.giS2bDlBytes+M11.s2bGiUlBytes)/(1024*1024)) cmg_386a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.giS2bDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_57a,
        to_number(decode( ((M11.period_duration*60*(1024*1024))),0,NULL, ((8*M11.s2bGiUlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_56a,
        to_number(decode( (M11.period_duration*60*(1024*1024)), 0, NULL, (8*(M11.s2bGiUlBytes+M11.giS2bDlBytes) / (M11.period_duration*60*(1024*1024))))) cmg_428a,
        to_number((M11.giS2bDlPackets)) cmg_39a,
        to_number((M11.s2bGiUlPackets)) cmg_38a,
        to_number(M11.s2bGiUlPackets+M11.giS2bDlPackets) cmg_429a
      from
        utp_common_objects "sam",
        utp_common_objects "cmg"
        ,
      jf_M11_2097590963 M11
      where
        "cmg".co_parent_gid = "sam".co_gid and
        M11.cmg_gid = "cmg".co_gid
      order by
      2,1,3,4
"""
trunctable_sqlstring = """
truncate table jf_M11_2097590963 drop storage
"""
droptable_sqlstring = """
drop table jf_M11_2097590963
"""

if __name__ == "__main__":
    print 'begin getconfig'
    if len(sys.argv) > 2:
        print sys.argv[1]
        print sys.argv[2]
    else:
        print 'please input your command parameter for runmode and database model name.'
        sys.exit()
    (username, passwd, url, urlport, db_name) = getdbconfig(sys.argv[1], sys.argv[2])
    print username
    print passwd
    print url
    print urlport
    print db_name

    #print sqlstring
    cmgdbcursor.execute(createtable_sqlstring)
    cmgdbcursor.execute(select_sqlstring)
    row=cmgdbcursor.fetchall()
    print row
    cmgdbcursor.execute(trunctable_sqlstring)
    cmgdbcursor.execute(droptable_sqlstring)
