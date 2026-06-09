QUERY_PROFILE_EUR = """
with 
q1 as (
--1)PROFILE OGOLNY
select
replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') as "Item"
,t5.pxtx50 as "Desc."
,t0.pgstun as "Sales Unit"
,t1.ppprcu as "Price Unit"
,t1.ppsalp as "MF"
,t2.ppsalp as "T"
,t3.ppsalp as "N"
,round(t3.ppsalp*1.15,(2)) as "AN"
,t4.ppsalp as "WD"
,round(t3.ppsalp*1.05,(2)) as "LN1"
,round(t3.ppsalp*1.075,(2)) as "LN2"
,round(t3.ppsalp*1.15,(2)) as "LN3"
,round(t3.ppsalp*1.3225,(2)) as "ANC"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t1.ppprdc=t0.pgprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end) and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end)  and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end)  and t4.pppril='{n}WD' and t4.pptodt=0
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D' and t0.pghstc='' and (t0.PGPPGR ='CPL' OR t0.pgpgrp='SS') and pgprcl in ('1','2') and t0.PGPPGR <>'XPL'
and pgprdc not like '%/9016%' and pgprdc not like '%/9006%' and pgprdc not like '%/8019%' and pgprdc not like '%/AN%' and pgprdc not like '%/LAN%' and pgprdc not like '%/9010%' and pgprdc not like '%/9005%' and pgprdc not like '%/INOX%' and pgprdc not like '%/ZN%' and pgprdc not like '%/WDZD01%'
and pgprfa in ('PMF','PRF')
and t0.pgprdc not like 'BL%'
and t0.PGPDGR <>'PRFAF'
and (t1.ppsalp<>0 or t2.ppsalp<>0 or t3.ppsalp <>0 or t4.ppsalp<>0)
),

q2 as (
--2)MAGAZYNOWKI
select
t0.pgprdc
,t5.pxtx50
,t0.pgstun as "Sales Unit"
,t1.ppprcu as "Price Unit"
,cast(null as int)
,case when t1.ppsalp is not null then t1.ppsalp else t2.ppsalp end
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t1.ppprdc=t0.pgprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=t0.pgprdc and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=t0.pgprdc and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=t0.pgprdc and t4.pppril='{n}WD' and t1.pptodt=0
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D' and t0.pghstc='' and (t0.PGPPGR ='CPL' OR t0.pgpgrp='SS') and pgprcl in ('1','2') and t0.PGPPGR <>'XPL'
and ( pgprdc like '%/9016%' or pgprdc like '%/9006%' or pgprdc like '%/8019%' or pgprdc like '%/9010%' or pgprdc like '%/9005%' or pgprdc like '%/WDZD01%' or pgprdc like '%/7016MT%')
and pgprfa in ('PMF','PRF','PP')
and t0.pgprdc not like 'BL%'
and t0.PGPDGR <>'PRFAF'
and (t1.ppsalp<>0 or t2.ppsalp<>0 or t3.ppsalp <>0 or t4.ppsalp<>0)
),

q3 as (
--3)ANODY
select
t0.pgprdc
,t5.pxtx50
,t0.pgstun as "Sales Unit"
,t1.ppprcu as "Price Unit"
,cast(null as int)
,cast(null as int)
,cast(null as int)
,case when t1.ppsalp is not null then t1.ppsalp else t2.ppsalp end
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t1.ppprdc=t0.pgprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=t0.pgprdc and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=t0.pgprdc and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=t0.pgprdc and t4.pppril='{n}WD' and t1.pptodt=0
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D' and t0.pghstc='' and (t0.PGPPGR ='CPL' OR t0.pgpgrp='SS') and pgprcl in ('1','2') and t0.PGPPGR <>'XPL'
and (pgprdc like '%/AN%' or pgprdc like '%/LAN%')
and pgprfa in ('PMF','PRF','PP')
and t0.pgprdc not like 'BL%'
and t0.PGPDGR <>'PRFAF'
and (t1.ppsalp<>0 or t2.ppsalp<>0 or t3.ppsalp <>0 or t4.ppsalp<>0)
),

q4 as (
--4)INOXY I OCYNKI
select
t0.pgprdc
,t5.pxtx50
,t0.pgstun as "Sales Unit"
,t1.ppprcu as "Price Unit"
,case when t1.ppsalp is not null then t1.ppsalp else t2.ppsalp end
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
,cast(null as int)
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t1.ppprdc=t0.pgprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=t0.pgprdc and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=t0.pgprdc and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=t0.pgprdc and t4.pppril='{n}WD' and t1.pptodt=0
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D' and t0.pghstc='' and (t0.PGPPGR ='CPL' OR t0.pgpgrp='SS') and pgprcl in ('1','2') and t0.PGPPGR <>'XPL'
and (pgprdc like '%/INOX%' or pgprdc like '%/ZN%')
and pgprfa in ('PMF','PRF','PP')
and t0.pgprdc not like 'BL%'
and t0.PGPDGR <>'PRFAF'
and (t1.ppsalp<>0 or t2.ppsalp<>0 or t3.ppsalp <>0 or t4.ppsalp<>0)
)

select * from q1
union
select * from q2
union
select * from q3
union
select * from q4
order by 1
"""

QUERY_AKCESORIA_EUR = """
with q1 as (
--1) AKCESORIA W SURÓWCE I LAKIERZE
select distinct
replace(case when locate('/',t0.pgprdc)>0 then substring(t0.pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') as "Numer kat."
,t5.pxtx50 as "Nazwa elementu"
,t0.pgstun as "Sales Unit"
,t1.ppprcu as "Price Unit"
,case when t7.srufn3=0 then 1 else t7.srufn3 end as "Il.Handl."
,t1.ppsalp as "Surowy"
,t2.ppsalp AS "T"
,t3.ppsalp AS "N"
,t4.ppsalp AS "WD"
,CAST(NULL AS DECIMAL(15,4)) as "Anoda"
,round(t3.ppsalp*1.05,(2)) as "LN1"
,round(t3.ppsalp*1.075,(2)) as "LN2"
,round(t3.ppsalp*1.15,(2)) as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t0.pgprdc=t1.ppprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t4.pppril='{n}WD' and t4.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D' and pghstc=''
and (t0.pgprdc like 'AC%' or t0.pgprdc like 'FAZE%' or t0.pgprdc like 'M1%' or t0.pgprdc like 'M2%' or t0.pgprdc like 'M3%' or t0.pgprdc like 'M4%' or t0.pgprdc like 'M5%' or t0.pgprdc like 'M6%' or t0.pgprdc like 'M7%' or t0.pgprdc like 'M8%' or t0.pgprdc like 'M9%' or t0.pgprdc like 'LWB%' or t0.pgprdc like 'LOB%' or t0.pgprdc like 'CMC%' or t0.pgprdc like 'LWC%' or t0.pgprdc like 'CAH%' or t0.pgprdc like 'PKDP%' or t0.pgprdc like 'GS1%' or t0.pgprdc like 'GS2%' or t0.pgprdc like 'GS3%' or t0.pgprdc like 'GS4%' or t0.pgprdc like 'GS5%' or t0.pgprdc like 'GS6%' or t0.pgprdc like 'GS7%' or t0.pgprdc like 'GS8%' or t0.pgprdc like 'GS9%' or t0.pgprdc like 'GS0%' or t0.pgprdc like 'AFT%' or t0.pgprdc like 'AFWL%' or t0.pgprdc like 'SLO%' or t0.pgprdc like 'SLD%' or t0.pgprdc like 'SLF%' or t0.pgprdc like 'SLI%' or t0.pgprdc like 'SLC%' or t0.pgprdc like 'ALI%')
and t0.pgprcl in ('1','2') and t0.pgppgr in ('CPL') and t0.PGPPGR <>'XPL'
and (t0.pgprdc like '%/MF%' or t0.pgprdc not like '%/%')
),

q2 as (
--2)AKCESORIA ANODOOWANE I LAN
select distinct
replace(t0.pgprdc,' ','') as "Numer kat."
,t5.pxtx50 as "Nazwa elementu"
,t0.pgstun as "Sales Unit"
,t1.ppprcu as "Price Unit"
,case when t7.srufn3=0 then 1 else t7.srufn3 end as "Il.Handl."
,CAST(NULL AS DECIMAL(15,4)) as "Surowy"
,CAST(NULL AS DECIMAL(15,4)) as "T"
,CAST(NULL AS DECIMAL(15,4)) as "N"
,CAST(NULL AS DECIMAL(15,4)) as "WD"
,case when t1.ppsalp<>0 then t1.ppsalp else (case when t2.ppsalp<>0 then t2.ppsalp else t3.ppsalp end) end as "Anoda"
,CAST(NULL AS DECIMAL(15,4)) as "LN1"
,CAST(NULL AS DECIMAL(15,4)) as "LN2"
,CAST(NULL AS DECIMAL(15,4)) as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t0.pgprdc=t1.ppprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=t0.pgprdc and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=t0.pgprdc and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D' and pghstc=''
and (t0.pgprdc like 'AC%' or t0.pgprdc like 'FAZE%' or t0.pgprdc like 'M1%' or t0.pgprdc like 'M2%' or t0.pgprdc like 'M3%' or t0.pgprdc like 'M4%' or t0.pgprdc like 'M5%' or t0.pgprdc like 'M6%' or t0.pgprdc like 'M7%' or t0.pgprdc like 'M8%' or t0.pgprdc like 'M9%' or t0.pgprdc like 'LWB%' or t0.pgprdc like 'LOB%' or t0.pgprdc like 'CMC%' or t0.pgprdc like 'LWC%' or t0.pgprdc like 'CAH%' or t0.pgprdc like 'PKDP%' or t0.pgprdc like 'GS1%' or t0.pgprdc like 'GS2%' or t0.pgprdc like 'GS3%' or t0.pgprdc like 'GS4%' or t0.pgprdc like 'GS5%' or t0.pgprdc like 'GS6%' or t0.pgprdc like 'GS7%' or t0.pgprdc like 'GS8%' or t0.pgprdc like 'GS9%' or t0.pgprdc like 'GS0%' or t0.pgprdc like 'AFT%' or t0.pgprdc like 'AFWL%' or t0.pgprdc like 'SLO%' or t0.pgprdc like 'SLD%' or t0.pgprdc like 'SLF%' or t0.pgprdc like 'SLI%' or t0.pgprdc like 'SLC%' or t0.pgprdc like 'ALI%')
and t0.pgprcl in ('1','2') and t0.pgppgr in ('CPL') and t0.PGPPGR <>'XPL'
and (t0.pgprdc like '%/AN%' or t0.pgprdc like '%/LAN%')
),

q3 as (
--3)AKCESORIA MAGAZYNOWE W RALU
select distinct
replace(t0.pgprdc,' ','') as "Numer kat."
,t5.pxtx50 as "Nazwa elementu"
,t0.pgstun as "Sales Unit"
,t1.ppprcu as "Price Unit"
,case when t7.srufn3=0 then 1 else t7.srufn3 end as "Il.Handl."
,CAST(NULL AS DECIMAL(15,4)) as "Surowy"
,t2.ppsalp AS "T"
,t3.ppsalp AS "N"
,t4.ppsalp AS "WD"
,CAST(NULL AS DECIMAL(15,4)) as "Anoda"
,CAST(NULL AS DECIMAL(15,4)) as "LN1"
,CAST(NULL AS DECIMAL(15,4)) as "LN2"
,CAST(NULL AS DECIMAL(15,4)) as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t0.pgprdc=t1.ppprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=t0.pgprdc and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=t0.pgprdc and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=t0.pgprdc and t4.pppril='{n}WD' and t4.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D' and pghstc=''
and (t0.pgprdc like 'AC%' or t0.pgprdc like 'FAZE%' or t0.pgprdc like 'M1%' or t0.pgprdc like 'M2%' or t0.pgprdc like 'M3%' or t0.pgprdc like 'M4%' or t0.pgprdc like 'M5%' or t0.pgprdc like 'M6%' or t0.pgprdc like 'M7%' or t0.pgprdc like 'M8%' or t0.pgprdc like 'M9%' or t0.pgprdc like 'LWB%' or t0.pgprdc like 'LOB%' or t0.pgprdc like 'CMC%' or t0.pgprdc like 'LWC%' or t0.pgprdc like 'CAH%' or t0.pgprdc like 'PKDP%' or t0.pgprdc like 'GS1%' or t0.pgprdc like 'GS2%' or t0.pgprdc like 'GS3%' or t0.pgprdc like 'GS4%' or t0.pgprdc like 'GS5%' or t0.pgprdc like 'GS6%' or t0.pgprdc like 'GS7%' or t0.pgprdc like 'GS8%' or t0.pgprdc like 'GS9%' or t0.pgprdc like 'GS0%' or t0.pgprdc like 'AFT%' or t0.pgprdc like 'AFWL%' or t0.pgprdc like 'SLO%' or t0.pgprdc like 'SLD%' or t0.pgprdc like 'SLF%' or t0.pgprdc like 'SLI%' or t0.pgprdc like 'SLC%' or t0.pgprdc like 'ALI%')
and t0.pgprcl in ('1','2') and t0.pgppgr in ('CPL') and t0.PGPPGR <>'XPL'
and (t0.pgprdc like '%/8019%' or t0.pgprdc like '%/9006%' or t0.pgprdc like '%/9016%' or t0.pgprdc like '%/3000%' or t0.pgprdc like '%/6041%' or t0.pgprdc like '%/7016%' or t0.pgprdc like '%/9005%' or t0.pgprdc like '%/9010%')
),

q4 as (
--4)AKCESORIA LAKIER NA ANODE
select distinct
replace(t0.pgprdc,' ','')
,t5.pxtx50
,t0.pgstun as "Sales Unit"
,t2.ppprcu as "Price Unit"
,case when t7.srufn3=0 then 1 else t7.srufn3 end as "Il.Handl."
,CAST(NULL AS DECIMAL(15,4)) as "Surowy"
,t2.ppsalp AS "T"
,t3.ppsalp AS "N"
,t4.ppsalp AS "WD"
,CAST(NULL AS DECIMAL(15,4)) as "Anoda"
,CAST(NULL AS DECIMAL(15,4)) as "LN1"
,CAST(NULL AS DECIMAL(15,4)) as "LN2"
,CAST(NULL AS DECIMAL(15,4)) as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t2 on t2.ppprdc=t0.pgprdc and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=t0.pgprdc and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=t0.pgprdc and t4.pppril='{n}WD' and t4.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join ali800cfap.mfitps t8 on t8.afprdc=t0.pgprdc
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.PGSTAT <>'D' and
t0.PGPPGR in ('CPL') and t0.PGPPGR <>'XPL'
and t8.afa7cd like '%/AN%'
and (t0.pgprdc like 'AC%' or t0.pgprdc like 'FAZE%' or t0.pgprdc like 'M1%' or t0.pgprdc like 'M2%' or t0.pgprdc like 'M3%' or t0.pgprdc like 'M4%' or t0.pgprdc like 'M5%' or t0.pgprdc like 'M6%' or t0.pgprdc like 'M7%' or t0.pgprdc like 'M8%' or t0.pgprdc like 'M9%' or t0.pgprdc like 'LWB%' or t0.pgprdc like 'LOB%' or t0.pgprdc like 'CMC%' or t0.pgprdc like 'LWC%' or t0.pgprdc like 'CAH%' or t0.pgprdc like 'PKDP%' or t0.pgprdc like 'GS1%' or t0.pgprdc like 'GS2%' or t0.pgprdc like 'GS3%' or t0.pgprdc like 'GS4%' or t0.pgprdc like 'GS5%' or t0.pgprdc like 'GS6%' or t0.pgprdc like 'GS7%' or t0.pgprdc like 'GS8%' or t0.pgprdc like 'GS9%' or t0.pgprdc like 'GS0%' or t0.pgprdc like 'AFT%' or t0.pgprdc like 'AFWL%' or t0.pgprdc like 'SLO%' or t0.pgprdc like 'SLD%' or t0.pgprdc like 'SLF%' or t0.pgprdc like 'SLI%' or t0.pgprdc like 'SLC%' or t0.pgprdc like 'ALI%')
and t0.pgprcl in ('3')
),

q5 as (
--5)AKCESORIA inox, ocynk itp.
select distinct
replace(t0.pgprdc,' ','') as "Numer kat."
,t5.pxtx50 as "Nazwa elementu"
,t0.pgstun as "Sales Unit"
,t1.ppprcu as "Price Unit"
,case when t7.srufn3=0 then 1 else t7.srufn3 end as "Il.Handl."
,case when t1.ppsalp<>0 then t1.ppsalp else (case when t2.ppsalp<>0 then t2.ppsalp else t3.ppsalp end) end as "Surowy"
,CAST(NULL AS DECIMAL(15,4)) as "T"
,CAST(NULL AS DECIMAL(15,4)) as "N"
,CAST(NULL AS DECIMAL(15,4)) as "WD"
,CAST(NULL AS DECIMAL(15,4)) as "Anoda"
,CAST(NULL AS DECIMAL(15,4)) as "LN1"
,CAST(NULL AS DECIMAL(15,4)) as "LN2"
,CAST(NULL AS DECIMAL(15,4)) as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t0.pgprdc=t1.ppprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=t0.pgprdc and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=t0.pgprdc and t3.pppril='{n}N' and t2.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D' and pghstc=''
and (t0.pgprdc like 'AC%' or t0.pgprdc like 'FAZE%' or t0.pgprdc like 'M1%' or t0.pgprdc like 'M2%' or t0.pgprdc like 'M3%' or t0.pgprdc like 'M4%' or t0.pgprdc like 'M5%' or t0.pgprdc like 'M6%' or t0.pgprdc like 'M7%' or t0.pgprdc like 'M8%' or t0.pgprdc like 'M9%' or t0.pgprdc like 'LWB%' or t0.pgprdc like 'LOB%' or t0.pgprdc like 'CMC%' or t0.pgprdc like 'LWC%' or t0.pgprdc like 'CAH%' or t0.pgprdc like 'PKDP%' or t0.pgprdc like 'GS1%' or t0.pgprdc like 'GS2%' or t0.pgprdc like 'GS3%' or t0.pgprdc like 'GS4%' or t0.pgprdc like 'GS5%' or t0.pgprdc like 'GS6%' or t0.pgprdc like 'GS7%' or t0.pgprdc like 'GS8%' or t0.pgprdc like 'GS9%' or t0.pgprdc like 'GS0%' or t0.pgprdc like 'AFT%' or t0.pgprdc like 'AFWL%' or t0.pgprdc like 'SLO%' or t0.pgprdc like 'SLD%' or t0.pgprdc like 'SLF%' or t0.pgprdc like 'SLI%' or t0.pgprdc like 'SLC%' or t0.pgprdc like 'ALI%')
and t0.pgprcl in ('1','2') and t0.pgppgr in ('CPL') and t0.PGPPGR <>'XPL'
and (t0.pgprdc like '%/INOX%' or t0.pgprdc like '%/ZN%' or t0.pgprdc like '%/IN%')
),

q6 as (
--6) AKCESORIA W SURÓWCE I LAKIERZE jesli MF jest zablokowany
select distinct
replace(case when locate('/',t0.pgprdc)>0 then substring(t0.pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') as "Numer kat."
,t5.pxtx50 as "Nazwa elementu"
,t0.pgstun as "Sales Unit"
,t2.ppprcu as "Price Unit"
,case when t7.srufn3=0 then 1 else t7.srufn3 end as "Il.Handl."
,CAST(NULL AS DECIMAL(15,4)) as "Surowy"
,t2.ppsalp AS "T"
,t3.ppsalp AS "N"
,t4.ppsalp AS "WD"
,CAST(NULL AS DECIMAL(15,4)) as "Anoda"
,CAST(NULL AS DECIMAL(15,4)) as "LN1"
,CAST(NULL AS DECIMAL(15,4)) as "LN2"
,CAST(NULL AS DECIMAL(15,4)) as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t2 on t2.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t4.pppril='{n}WD' and t4.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D'
and (t0.pgprdc like 'AC%' or t0.pgprdc like 'FAZE%' or t0.pgprdc like 'M1%' or t0.pgprdc like 'M2%' or t0.pgprdc like 'M3%' or t0.pgprdc like 'M4%' or t0.pgprdc like 'M5%' or t0.pgprdc like 'M6%' or t0.pgprdc like 'M7%' or t0.pgprdc like 'M8%' or t0.pgprdc like 'M9%' or t0.pgprdc like 'LWB%' or t0.pgprdc like 'LOB%' or t0.pgprdc like 'CMC%' or t0.pgprdc like 'LWC%' or t0.pgprdc like 'CAH%' or t0.pgprdc like 'PKDP%' or t0.pgprdc like 'GS1%' or t0.pgprdc like 'GS2%' or t0.pgprdc like 'GS3%' or t0.pgprdc like 'GS4%' or t0.pgprdc like 'GS5%' or t0.pgprdc like 'GS6%' or t0.pgprdc like 'GS7%' or t0.pgprdc like 'GS8%' or t0.pgprdc like 'GS9%' or t0.pgprdc like 'GS0%' or t0.pgprdc like 'AFT%' or t0.pgprdc like 'AFWL%' or t0.pgprdc like 'SLO%' or t0.pgprdc like 'SLD%' or t0.pgprdc like 'SLF%' or t0.pgprdc like 'SLI%' or t0.pgprdc like 'SLC%' or t0.pgprdc like 'ALI%')
and t0.pgprcl in ('1','2')
and (t0.pgprdc like '%/MF%' or t0.pgprdc not like '%/%')
and t0.pgpsna like '%TYLKO W LAKIERZE%'
)

select * from q1
union all
select * from q2
union all
select * from q3
union all
select * from q4
union all
select * from q5
union all
select * from q6
order by 1
"""

QUERY_BLACHY_EUR = """
with priceAnod as(
select  left(pgprdc, 5) item , round(ppsalp*1.15,(2)) priceC0, round(ppsalp*1.32,(2)) priceColor
from ali800cfap.sroprg
left join ali800cfap.sropps on left(pgprdc, 5)=ppprdc and pppril='{n}N' and pptodt=0
where pgprdc like '%A/MF%'
and pgprdc like 'BL%'  and pgstat <>'D'
),

q1 as (
--1)blachy mf+config
select distinct
replace(case when locate('/',t0.pgprdc)>0 then substring(t0.pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') as "Numer kat."
, t9.pxtx50 as "Nazwa elementu"
, t0.pgstun as "J.m."
, case when t7.srufn3=0 then 1 else t7.srufn3 end as "Il.Handl."
, t1.ppsalp as "Surowy"
, t2.ppsalp as "Typowy"
, t3.ppsalp as "Nietypowy"
, t8.priceC0 as "Anoda C0"
, t8.priceColor as "Anoda kolor"
, t4.ppsalp as "Wood"
,round(t3.ppsalp*1.05,(2)) as "LN1"
,round(t3.ppsalp*1.075,(2)) as "LN2"
,round(t3.ppsalp*1.15,(2)) as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t0.pgprdc=t1.ppprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t4.pppril='{n}WD' and t4.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join priceAnod t8 on replace(case when locate('/',t0.pgprdc)>0 then substring(t0.pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','')=t8.item
left join ali800cfap.sroprx t9 on t0.pgprdc=t9.pxprdc and t9.pxlang='EN' and t9.PXTLIN=1
where
t0.pgstat<>'D' and pghstc=''
and t0.pgprdc like 'BL%'
and t0.pgprcl in ('1','2') and t0.pgppgr in ('CPL')
and (t0.pgprdc like '%/MF%' or t0.pgprdc not like '%/%')
),

q2 as (
--2)blachy w anodzie
select distinct
replace(t0.pgprdc,' ','') as "Numer kat."
, t9.pxtx50 as "Nazwa elementu"
, t0.pgstun as "J.m."
, case when t7.srufn3=0 then 1 else t7.srufn3 end as "Il.Handl."
, '' as "Surowy"
, '' as "Typowy"
, '' as "Nietypowy"
, case when t1.ppsalp>0 then t1.ppsalp else (case when t2.ppsalp>0 then t2.ppsalp else t3.ppsalp end) end as "Anoda"
, '' as "Anoda color"
, '' as "Wood"
, '' as "LN1"
, '' as "LN2"
, '' as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t0.pgprdc=t1.ppprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t4.pppril='{n}WD' and t4.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join ali800cfap.sroprx t9 on t0.pgprdc=t9.pxprdc and t9.pxlang='EN' and t9.PXTLIN=1
where
t0.pgstat<>'D' and pghstc=''
and t0.pgprdc like 'BL%'
and t0.pgprcl in ('1','2') and t0.pgppgr in ('CPL')
and (t0.pgprdc like '%/AN%')
),

q3 as (
--3)blachy magazynowe
select distinct
replace(t0.pgprdc,' ','') as "Numer kat."
, t9.pxtx50 as "Nazwa elementu"
, t0.pgstun as "J.m."
, case when t7.srufn3=0 then 1 else t7.srufn3 end as "Il.Handl."
, '' as "Surowy"
, case when t1.ppsalp>0 then t1.ppsalp else (case when t2.ppsalp>0 then t2.ppsalp else t3.ppsalp end) end as "Typowy"
, '' as "Nietypowy"
, '' as "Anoda"
, '' as "Anoda color"
, '' as "Wood"
, '' as "LN1"
, '' as "LN2"
, '' as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t0.pgprdc=t1.ppprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t4.pppril='{n}WD' and t4.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join ali800cfap.sroprx t9 on t0.pgprdc=t9.pxprdc and t9.pxlang='EN' and t9.PXTLIN=1
where
t0.pgstat<>'D' and pghstc=''
and t0.pgprdc like 'BL%'
and t0.pgprcl in ('1','2') and t0.pgppgr in ('CPL')
and (t0.pgprdc like '%/8019%' or t0.pgprdc like '%/9006%' or t0.pgprdc like '%/9016%')
)

select * from q1
union all
select * from q2
union all
select * from q3
order by 1
"""

QUERY_FORMATKI_EUR = """

--1)blachy mf+config
select distinct
replace(case when locate('/',t0.pgprdc)>0 then substring(t0.pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') as "Numer kat."
, t5.pxtx50 as "Nazwa elementu"
, t0.pgstun as "J.m."
, case when t7.srufn3=0 then 1 else t7.srufn3 end as "Il.Handl."
, t1.ppsalp as "Surowy"
, t2.ppsalp as "Typowy"
, t3.ppsalp as "Nietypowy"
, t4.ppsalp as "Wood"
,round(t3.ppsalp*1.05,(2)) as "LN1"
,round(t3.ppsalp*1.075,(2)) as "LN2"
,round(t3.ppsalp*1.15,(2)) as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t1 on t0.pgprdc=t1.ppprdc and t1.pppril='{n}MF' and t1.pptodt=0
left join ali800cfap.sropps t2 on t2.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t4.pppril='{n}WD' and t4.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D' and pghstc=''
and t0.pgpgrp='BL-F'
and t0.pgppgr in ('CPL')
and (t0.pgprdc like '%/MF%')

order by 1
"""

QUERY_MOSKITIERY_EUR = """

--6)MOSKITIERY
select distinct
replace(case when locate('/',t0.pgprdc)>0 then substring(t0.pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') as "Numer kat."
, t5.pxtx50 as "Nazwa elementu"
, t0.pgstun as "J.m."
, t2.ppsalp as "Typowy"
, t3.ppsalp as "Nietypowy"
, t4.ppsalp as "Wood"
,round(t3.ppsalp*1.05,(2)) as "LN1"
,round(t3.ppsalp*1.075,(2)) as "LN2"
,round(t3.ppsalp*1.15,(2)) as "LN3"
from ali800cfap.sroprg t0
left join ali800cfap.sropps t2 on t2.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t2.pppril='{n}T' and t2.pptodt=0
left join ali800cfap.sropps t3 on t3.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t3.pppril='{n}N' and t3.pptodt=0
left join ali800cfap.sropps t4 on t4.ppprdc=replace(case when locate('/',t0.pgprdc)>0 then substring(pgprdc,1,locate('/',t0.pgprdc)-1) else t0.pgprdc end,' ','') and t4.pppril='{n}WD' and t4.pptodt=0
left join ali800cfap.srosro t7 on t7.srsrom='AP1' and t7.srprdc=t0.pgprdc
left join ali800cfap.sroprx t5 on t0.pgprdc=t5.pxprdc and t5.pxlang='EN' and t5.PXTLIN=1
where
t0.pgstat<>'D' and pghstc=''
and t0.pgprdc like 'ACIS%'
and t0.pgprcl = '3' and t0.pgppgr in ('CPL')

order by 1
"""
