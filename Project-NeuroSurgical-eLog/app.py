#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Rishin Rahim Date : Mar 12 2014
# Added this comment for git test
import web
import sys
import json


urls = (
    '/', 'Index',
    '/admin','Admin',
    '/admincreateuser','Admin_cusr',
    '/admincus','Admincus',
    '/adminedituser','Admin_viewusr',
    '/adminlog','Admin_viewlog',
    '/admineditlog','Admin_editlog',
    '/admindellog','Admin_dellog',
    '/adminnotification','Admin_notif',
    '/adminnotification2','Admin_notif2',
    '/adminnotifyusr','Adminnotifyusr',
    '/adminsettings','Admin_settings',
    '/admindelsuc','Admindelsuc',
    '/surgeon','Surgeon',
    '/surgeonaddlog','Surg_Addlog',
    '/surgeonviewlog','SurgViewlog',
    '/surgeonviewlogexpand','Surg_expandview',
    '/surgeoneditlog','Surg_Editlog',
    '/surgeoneditlog2','Surg_Editlog2',
    '/surgeonsetting','Surg_settings',
    '/surgeonnotification','Surg_notif',
    '/surgeonsuccess','Surg_success',
    '/getsec','Getsec',
    '/getloc','Getloc',
    '/getsearch','Getsearch',
    '/getpro','Getpro',
    '/getcurrent','Getcurrent',
    '/editreq','Editreq',
    '/delreq','Delreq',
    '/editreqsuc','Editreqsuc',
    '/editdiag','Editdiag',
    '/editloc','Editloc',
    '/editpro','Editpro',
    '/editop','Editop',
    '/editsd','Editsd',
    '/headnurse','Headnurse',
    '/headalert','Headalert',
    '/headsetting','Headsetting',
    '/headalertsuc','Headalertsuc',
    '/logout','Logout'
    )


try:
    db=web.database(dbn='sqlite',db='log.db')
except:
    print 'Could not open database...'
    sys.exit()

#web.config.debug = False
app = web.application(urls, globals())
store = web.session.DBStore(db,'sessions')
session = web.session.Session(app, store)
render=web.template.render('templates/')

'''Start page
Users login to the page with a valid username and password.Invalid results to a failed attempt'''
class Index:
    def GET(self):
        session.logged_in=False
        return render.start(0)

    def POST(self):
        inp=web.input()
        users=db.select('users')
        for user in users:
                    if user.uname==inp.username and user.upwd==inp.password:
                        if user.urole==1:
                            session.logged_in=True
                            session.attr=user.uid
                            session.nam=user.name
                            session.count=1
                            raise web.seeother('/admin')
                        if user.urole==2:
                            session.logged_in=True
                            session.attr=user.uid
                            session.nam=user.name
                            session.count=2
                            raise web.seeother('/surgeon')
                        if user.urole==3:
                            session.logged_in=True
                            session.attr=user.uid
                            session.nam=user.name
                            session.count=3
                            raise web.seeother('/headnurse')  
        else:
                    return render.start(1)
'''Admisistrator Super user '''

class Admin:
    def GET(self):
        if session.logged_in==True and session.count==1:
            result1=db.query( "SELECT strftime('%d-%m-%Y %H:%M',lastlog) as l from users where uid=1")
            result2=db.query('select count(caseid) as a from caselog')
            result3=db.query('select count(urole) as b from userrole')
            result4=db.query('select count(uid) as c from users where urole=2')
            for user1 in result1:
                lastlog=user1.l
            for user2 in result2:
                caseno=user2.a
            for user3 in result3:
                utype=user3.b
            for user4 in result4:
                uno=user4.c
            alert=db.query("select count(rid) as r from request where status=0")
            for i in alert:
                    r=i.r
            db.query("update request set status=1 where status=0")
            return render.admin(lastlog,utype,uno,caseno,r)
        else:
            return render.ua2()

'''Add user '''

class Admin_cusr:
    def GET(self):
         if session.logged_in==True and session.count==1:
             return render.admincreateuser()
         return render.ua2()
    def POST(self):
        inp=web.input()
        if inp.username=='' or inp.password=='' or inp.name=='' or inp.role=='':
            raise web.seeother('/admincreateuser')
        elif inp.password==inp.cpwd:
            users=db.select('users')
            una=db.select('users')
            for un in una:
                if un.name==inp.name:
                    raise web.seeother('/admincreateuser')
            for user in users:
                if user.uname==inp.username:
                    raise web.seeother('/admincreateuser')
            result=db.insert('users',uname=inp.username,upwd=inp.password,name=inp.name,urole=inp.role)
            raise web.seeother('/admincus')
        else:
            raise web.seeother('/admincreateuser')

class Admincus:
    def GET(self):
        if session.logged_in==True and session.count==1:
             return render.admincus()
        return render.ua2()
        

'''Edit/Delete USER'''

class Admin_viewusr:
    def GET(self):
        if session.logged_in==True and session.count==1:
            data=db.query('select * from (select * from users join userrole where users.urole=userrole.urole) where urole!=1 ;')
            data1=db.query('select * from (select * from users join userrole where users.urole=userrole.urole) where urole!=1 ;')
            return render.adminedituser(data,data1)
        return render.ua2()
    
    def POST(self):
        inp=web.input()
        if inp.edituser!=0:
            if inp.submit=='Delete':
                myvar=dict(t=inp.edituser)
                print inp.edituser
                result=db.query('DELETE FROM users WHERE name=$t',myvar)
                web.seeother('/adminedituser')
            else:
                if inp.flag=='':
                    web.seeother('/adminedituser')
                else:
                    if inp.editoption=='1':
                        var2 =dict(t1=inp.flag,t2=inp.edituser)
                        result=db.query("update users set uname=$t1 where name=$t2",var2)
                    elif inp.editoption=='2':
                        var2 =dict(t1=inp.flag,t2=inp.edituser)
                        result=db.query("update users set upwd=$t1 where name=$t2",var2)
                    elif inp.editoption=='3':
                        var2 =dict(t1=inp.flag,t2=inp.edituser)
                        result=db.query("update users set name=$t1 where name=$t2",var2)
                    web.seeother('/adminedituser')

'''View/Search Log'''

class Admin_viewlog:
    def GET(self):
        if session.logged_in==True and session.count==1:
            result=db.query("SELECT * FROM caselog ORDER BY caseid DESC")
            return render.adminlog(result)
        else:
            return render.ua2()
    def POST(self):
        inp=web.input()
        key=inp.search.split(',')
        l=[]
        cid=db.query("select caseid from caselog")
        for user in cid:
            l.append(user.caseid)
        for i in range(0,len(key)):
            myvar=dict(t="%"+key[i]+"%",t2=key[i],t1=l)
            cid=db.query("select caseid from (select * from caselog where caseid IN $t1) where date like $t2 or time like $t or psid like $t collate nocase or faid like $t collate nocase or said like $t collate nocase or spid like $t2 collate nocase or fdiag like $t collate nocase or floc like $t collate nocase or fpro like $t collate nocase or opid like $t collate nocase or sdid like $t collate nocase or scrub like $t collate nocase or anst like $t collate nocase or pname like $t collate nocase or page=$t2 or psex like $t2 collate nocase or hospid=$t2 order by caseid desc ",myvar)
            l=[]
            for user in cid:
                l.append(user.caseid)
        var=dict(t=l)
        result=db.query("select * from caselog where caseid in $t",var)
        return render.adminlog(result)

'''Admin edit log'''
class Admin_editlog:
    def GET(self):
        if session.logged_in==True and session.count==1:
            result=db.query("select * from caselog order by caseid DESC")
            return render.admineditlog(0,result)
        else:
            return render.ua2()
    def POST(self):
        inp=web.input()
        var1=dict(t2=inp.caseid)
        if inp.caseid=='':
            raise web.seeother('/admineditlog')
        else:
            var1=dict(t2=inp.caseid)
            result=db.query('select * from caselog where caseid=$t2',var1)
            if not result:
                return render.admineditlog(1,result)
            return render.admineditlog(0,result)
        
 
class Admin_dellog:
    def POST(self):
        inp=web.input()
        var1=dict(t2=inp.caseid)
        result=db.query('Delete from caselog where caseid=$t2',var1)
        raise web.seeother('/admindelsuc')
            
  
class Admindelsuc:
    def GET(self):
        return render.admindelsuc()

'''Admin Notification'''

'''/adminnotification','Admin_notif'''

class Admin_notif:
    def GET(self):
        if session.logged_in==True and session.count==1:
            result=db.query("select aid,uname,date,time,strftime('%d-%m-%Y',logdate)as l from alert2 order by logdate desc")
            return render.adminnotification(result)
        else:
            return render.ua2()
    def POST(self):
        myvar=dict(t=session.nam)
        db.query(" DELETE FROM alert2",myvar)
        web.seeother('/adminnotification')
        


class Admin_notif2:
    def GET(self):
        if session.logged_in==True and session.count==1:
            result=db.query("select rid,name,reason,strftime('%d-%m-%Y',logdate)as l,caseid from request order by logdate desc")
            return render.adminnotification2(result)
        else:
            return render.ua2()
    def POST(self):
        myvar=dict(t=session.nam)
        db.query(" DELETE FROM request",myvar)
        web.seeother('/adminnotification2')
        
'''Account Settings'''
class Admin_settings:
    def GET(self):
        if session.logged_in==True and session.count==1:
            return render.adminsettings(0)
        else:
            return render.ua2()
    def POST(self):
        inp=web.input()
        result=db.select('users',where="urole=1")
        i=0
        for user in result:
            if user.upwd==inp.cpassword:
                i=1
        if i!=0:
            myvar=dict(t1=inp.password)
            result=db.query("update users set upwd=$t1 where urole=1",myvar)
            return render.adminsettings(1)
        else:
            return render.adminsettings(2)
'''---------------------------------------------Surgeon---------------------------------------------------'''

'''surgeon Home page'''

class Surgeon:
        def GET(self):
            if session.logged_in==True and session.count==2:
                myvar=dict(t=session.nam)
                alert=db.query("select count(aid) as c from alert where status=0 and uname=$t",myvar)
                for i in alert:
                    a=i.c
                result2=db.query("update alert set status=1 where status=0")
                result=db.query("SELECT * FROM caselog ORDER BY caseid DESC")
                return render.surgeon(a,session.nam,result)
            else:
                return render.ua2()

        def POST(self):
                inp=web.input()
                key=inp.search.split(',')
                l=[]
                cid=db.query("select caseid from caselog")
                for user in cid:
                    l.append(user.caseid)
                for i in range(0,len(key)):
                    myvar=dict(t="%"+key[i]+"%",t2=key[i],t1=l)
                    cid=db.query("select caseid from (select * from caselog where caseid IN $t1) where date like $t2 or time like $t or psid like $t collate nocase or faid like $t collate nocase or said like $t collate nocase or spid like $t2 collate nocase or fdiag like $t collate nocase or floc like $t collate nocase or fpro like $t collate nocase or opid like $t collate nocase or sdid like $t collate nocase or scrub like $t collate nocase or anst like $t collate nocase or pname like $t collate nocase or page=$t2 or psex like $t2 collate nocase or hospid=$t2 order by caseid desc ",myvar)
                    l=[]
                    for user in cid:
                        l.append(user.caseid)
                var=dict(t=l)
                result=db.query("select * from caselog where caseid in $t",var)          
                return render.surgeon(0,session.nam,result)

'''Add log'''

class Surg_Addlog:
    def GET(self):
        if session.logged_in==True and session.count==2:
           myvar=dict(t=session.attr)
           result=db.select('users',myvar,where='uid=$t')            
           surgeon1=db.select('users',what='name',where='urole=2')
           surgeon2=db.select('users',what='name',where='urole=2')
           surgeon3=db.select('users',what='name',where='urole=2')
           surgeon4=db.select('users',what='name',where='urole=2')
           scrub1=db.select('users',what='name',where='urole=5')
           scrub2=db.select('users',what='name',where='urole=5')
           anst=db.select('users',what='name',where='urole=4')
           result1=db.select('location',where='lparent=0') 
           result2=db.select('diagnosis',where='dparent=0')
           result3=db.select('operative')
           result4=db.select('side')
           result5=db.select('procedure',where='pcparent=0')
           return render.surgeonaddlog(result,result1,result2,result3,result4,result5,surgeon1,surgeon2,surgeon3,surgeon4,anst,scrub1,scrub2)
        else:
            return render.ua2()
    def POST(self):
        inp=web.input(primaryl=[],secl=[],terl=[],qual=[],primaryd=[],secd=[],terd=[],quad=[],primaryp=[],secp=[],terp=[],quap=[])
        if inp.anst=='' or inp.scrub=='' or inp.hospid=='' or inp.pname=='' or inp.page=='' or inp.secd=='' or inp.terd=='' or inp.quad=='' or inp.secl=='' or inp.terl=='' or inp.qual=='' or inp.secp=='' or inp.terp=='' or inp.quap=='' or inp.psid=='' or inp.faid=='' or inp.said=='' or inp.spid=='' or inp.date=='':
            raise web.seeother('/surgeonaddlog')
        else:
            pl,sl,tl,ql=','.join(inp.primaryl),','.join(inp.secl),','.join(inp.terl),','.join(inp.qual)
            pd,sd,td,qd=','.join(inp.primaryd),','.join(inp.secd),','.join(inp.terd),','.join(inp.quad)
            pp,sp,tp,qp=','.join(inp.primaryp),','.join(inp.secp),','.join(inp.terp),','.join(inp.quap)
            fdia=qd
            flo=ql
            fpr=qp
            if qd=="None":
                fdia=td
            if td=="None":
                fdia=sd
            if sd=="None":
                fdia=pd
            if ql=="None":
                flo=tl
            if tl=="None":
                flo=sl
            if sl=="None":
                flo=pl
            if qp=="None":
                fpr=tp
            if tp=="None":
                fpr=sp
            if sp=="None":
                fpr=pp
            duplicate=False
            myvar=dict(t1=inp.hospid,t2=inp.date,t3=inp.time)
            check=db.query("select caseid from caselog where hospid=$t1 AND date=$t2 AND time=$t3",myvar)
            if not check:
                result=db.insert('caselog',uid=session.attr,hospid=inp.hospid,pname=inp.pname,page=inp.page,psex=inp.pgender,pdiag=pd,sdiag=sd,tdiag=td,qdiag=qd,fdiag=fdia,ploc=pl,sloc=sl,tloc=tl,qloc=ql,floc=flo,ppro=pp,spro=sp,tpro=tp,qpro=qp,fpro=fpr,opid=inp.opid,sdid=inp.sdid,psid=inp.psid,faid=inp.faid,said=inp.said,spid=inp.spid,anst=inp.anst,scrub=inp.scrub,date=inp.date,time=inp.time)
                myvar=dict(t=result)
                result2=db.query("update caselog set logtime=(select datetime(current_timestamp, 'localtime')) where caseid=$t",myvar);
                raise web.seeother('/surgeonsuccess')
            else:
                raise web.seeother('/surgeonaddlog')
class Surg_success:
    def GET(self):
        return render.surgeonsuccess(session.nam)
        
        
'''Dynamic drop table'''
'''Diagnosis'''

class Getsec:
    def PUT(self):
        inp = web.input()
        s = inp.get('text', inp['text[]'])
        for user in db.select('diagnosis'):
            if user.dname==s:
                did=user.did
                break
        ret = [user.dname.encode('ascii', 'ignore')
               for user in db.select('diagnosis')
               if user.dparent == did]
        if not ret:
            ret = ['None']
        return json.dumps(ret)        

'''location'''
class Getloc:
    def PUT(self):
        inp = web.input()
        s = inp.get('text', inp['text[]'])
        for user in db.select('location'):
            if user.lname==s:
                lid=user.lid
                break
        ret = [user.lname.encode('ascii', 'ignore')
               for user in db.select('location')
               if user.lparent == lid]
        if not ret:
            ret = ['None']
        return json.dumps(ret)
    
'''procedure'''
class Getpro:
    def PUT(self):
        inp = web.input()
        s = inp.get('text', inp['text[]'])
        for user in db.select('procedure'):
            if user.pcname==s:
                pcid=user.pcid
                break
        ret = [user.pcname.encode('ascii', 'ignore')
               for user in db.select('procedure')
               if user.pcparent == pcid]
        if not ret:
            ret = ['None']
        return json.dumps(ret)
    

'''Surgeon Vew log Table format + Search the log book'''

class SurgViewlog:
    def GET(self):
        if session.logged_in==True and session.count==2:
            myvar=dict(t=session.attr,t1=session.nam)
            result=db.query("select * from caselog where uid=$t or psid=$t1 or faid=$t1 or said=$t1 or spid=$t1 ORDER BY caseid DESC",myvar);
            return render.surgeonviewlog(result,session.nam)
        else:
            return render.ua2()
    def POST(self):
        inp=web.input()
        var1=dict(t=session.attr,t1=session.nam)
        key=inp.search.split(',')
        l=[]
        cid=db.query("select * from caselog where uid=$t or psid=$t1 or faid=$t1 or said=$t1 or spid=$t1",var1)
        for user in cid:
            l.append(user.caseid)
        for i in range(0,len(key)):
            myvar=dict(t="%"+key[i]+"%",t2=key[i],t1=l)
            cid=db.query("select caseid from (select * from caselog where caseid IN $t1) where date like $t2 or time like $t or psid like $t collate nocase or faid like $t collate nocase or said like $t collate nocase or spid like $t2 collate nocase or fdiag like $t collate nocase or floc like $t collate nocase or fpro like $t collate nocase or opid like $t collate nocase or sdid like $t collate nocase or scrub like $t collate nocase or anst like $t collate nocase or pname like $t collate nocase or page=$t2 or psex like $t2 collate nocase or hospid=$t2 order by caseid desc ",myvar)
            l=[]
            for user in cid:
                l.append(user.caseid)
        var=dict(t=l)
        result=db.query("select * from caselog where caseid in $t",var)
        return render.surgeonviewlog(result,session.nam)
        
    
class Surg_expandview:
    def GET(self):
        if session.logged_in==True and session.count==2:
            myvar=dict(t=session.attr,t1=session.nam)
            result=db.query("select * from caselog where uid=$t or psid=$t1 or faid=$t1 or said=$t1 or spid=$t1 ORDER BY caseid DESC",myvar);                
            return render.surgeonviewlogexpand(result,session.nam)
        else:
            return render.ua2()

class Surg_Editlog:
    def GET(self):
        if session.logged_in==True and session.count==2:
            myvar=dict(t=session.attr,t1=session.nam)
            session.caseid=0
            result=db.query("select caseid from caselog where uid=$t or psid=$t1 or faid=$t1 or said=$t1 or spid=$t1",myvar)
            return render.surgeoneditlog(list(result),session.nam)
        else:
            return render.ua2()
    def POST(self):
        inp=web.input()
        if inp.caseid=='':
                raise web.seeother('/surgeoneditlog')
        else:
            myvar=dict(t=session.attr,t1=session.nam,t2=inp.caseid)
            session.caseid=inp.caseid
            result22=db.query('select * from caselog where caseid=$t2',myvar)
            result=db.query("select caseid from caselog where uid=$t or psid=$t1 or faid=$t1 or said=$t1 or spid=$t1",myvar)
            loc=db.select('location',where='lparent=0')
            diag=db.select('diagnosis',where='dparent=0')
            opr=db.select('operative')
            side=db.select('side')
            proc=db.select('procedure',where='pcparent=0')
            return render.surgeoneditlog2(result22,list(result),loc,diag,proc,opr,side,session.nam)


            

class Surg_Editlog2:
    def GET(self):
        if session.logged_in==True and session.count==2:
            myvar=dict(t=session.attr,t1=session.nam,t2=session.caseid)
            result22=db.query('select * from caselog where caseid=$t2',myvar)
            result=db.query("select caseid from caselog where uid=$t or psid=$t1 or faid=$t1 or said=$t1 or spid=$t1",myvar)
            loc=db.select('location',where='lparent=0')
            diag=db.select('diagnosis',where='dparent=0')
            opr=db.select('operative')
            side=db.select('side')
            proc=db.select('procedure',where='pcparent=0')
            return render.surgeoneditlog2(result22,list(result),loc,diag,proc,opr,side,session.nam)
        else:
            return render.ua2()
    def POST(self):
        inp=web.input()
        if inp.edit=='Edit Log':
            myvar=dict(t=session.attr,t1=session.nam,t2=inp.caseid)
            session.caseid=inp.caseid
            result22=db.query('select * from caselog where caseid=$t2',myvar)
            result=db.query("select caseid from caselog where uid=$t or psid=$t1 or faid=$t1 or said=$t1 or spid=$t1",myvar)
            loc=db.select('location',where='lparent=0')
            diag=db.select('diagnosis',where='dparent=0')
            opr=db.select('operative')
            side=db.select('side')
            proc=db.select('procedure',where='pcparent=0')
            return render.surgeoneditlog2(result22,list(result),loc,diag,proc,opr,side,session.nam)
               
        else:
            if inp.reason=='' or inp.caseid=='':
                raise web.seeother('/surgeoneditlog')
            else:
                result=db.insert('request',name=session.nam,status=0,reason=inp.reason,caseid=inp.caseid)
                myvar=dict(t=result)
                result1=db.query("update request set logdate=(select datetime(current_timestamp, 'localtime')) where rid=$t",myvar)
                raise web.seeother('/editreqsuc')

class Delreq:
    def POST(self):
        inp=web.input()
        if inp.reason=='':
                raise web.seeother('/surgeoneditlog2')

        else:
                
                result=db.insert('request',name=session.nam,status=0,reason=inp.reason,caseid=session.caseid)
                myvar=dict(t=result)
                result1=db.query("update request set logdate=(select datetime(current_timestamp, 'localtime')) where rid=$t",myvar)
                raise web.seeother('/editreqsuc')
            

class Editreq:
    def POST(self):
        inp=web.input()
        if inp.changeto=='':
            raise web.seeother('/surgeoneditlog2')
        else:
            myvar=dict(t1=inp.changeto,t=session.caseid)
            if inp.editfield=='1':
                result=db.query('update caselog set date=$t1 where caseid=$t',myvar)
            if inp.editfield=='17':
                 result=db.query('update caselog set time=$t1 where caseid=$t',myvar)
            if inp.editfield=='2':
                result=db.query('update caselog set hospid=$t1 where caseid=$t',myvar)
            if inp.editfield=='3':
                print inp.changeto
                result=db.query('update caselog set pname=$t1 where caseid=$t',myvar)
            if inp.editfield=='4':
                result=db.query('update caselog set page=$t1 where caseid=$t',myvar)
            if inp.editfield=='5':
                result=db.query('update caselog set psex=$t1 where caseid=$t',myvar)
            if inp.editfield=='11':
                result=db.query('update caselog set psid=$t1 where caseid=$t',myvar)
            if inp.editfield=='12':
                result=db.query('update caselog set faid=$t1 where caseid=$t',myvar)
            if inp.editfield=='13':
                result=db.query('update caselog set said=$t1 where caseid=$t',myvar)
            if inp.editfield=='14':
                result=db.query('update caselog set spid=$t1 where caseid=$t',myvar)
            if inp.editfield=='15':
                result=db.query('update caselog set anst=$t1 where caseid=$t',myvar)
            if inp.editfield=='16':
                result=db.query('update caselog set scrub=$t1 where caseid=$t',myvar)        
            raise web.seeother('/surgeoneditlog2')

class Editdiag:
     def POST(self):
            inp=web.input(primaryd=[],secd=[],terd=[],quad=[])
            if inp.primaryd=='' or inp.secd=='' or inp.terd=='' or inp.quad=='':
                raise web.seeother('/surgeoneditlog2')
            else:
                pd,sd,td,qd=','.join(inp.primaryd),','.join(inp.secd),','.join(inp.terd),','.join(inp.quad)
                fdiag=qd
                if qd=="None":
                    fdiag=td
                if td=="None":
                    fdiag=sd
                if sd=="None":
                    fdiag=pd
                myvar=dict(t1=pd,t2=sd,t3=sd,t4=qd,t5=fdiag,t=session.caseid)
                result=db.query('update caselog set pdiag=$t1,sdiag=$t2,tdiag=$t3,qdiag=$t4,fdiag=$t5 where caseid=$t',myvar)
                raise web.seeother('/surgeoneditlog2')
            


class Editloc:    
    def POST(self):
                inp=web.input(primaryl=[],secl=[],terl=[],qual=[])
                if inp.primaryl=='' or inp.secl=='' or inp.terl=='' or inp.qual=='':
                    raise web.seeother('/surgeoneditlog2')
                else:
                    pl,sl,tl,ql=','.join(inp.primaryl),','.join(inp.secl),','.join(inp.terl),','.join(inp.qual)
                    flo=ql
                    if ql=="None":
                        flo=tl
                    if tl=="None":
                        flo=sl
                    if sl=="None":
                        flo=pl
                    myvar=dict(t1=pl,t2=sl,t3=tl,t4=ql,t5=flo,t=session.caseid)
                    result=db.query('update caselog set ploc=$t1,sloc=$t2,tloc=$t3,qloc=$t4,floc=$t5 where caseid=$t',myvar)
                    raise web.seeother('/surgeoneditlog2')
            
class Editop:
      def POST(self):
                inp=web.input()
                if inp.opid=='':
                    raise web.seeother('/surgeoneditlog2')
                else:
                    myvar=dict(t1=inp.opid,t=session.caseid)
                    result=db.query('update caselog set opid=$t1 where caseid=$t',myvar)
                    raise web.seeother('/surgeoneditlog2')
class Editsd:
    
    def POST(self):
            inp=web.input()
            if inp.sdid=='':
                raise web.seeother('/surgeoneditlog2')
            else:
                myvar=dict(t1=inp.sdid,t=session.caseid)
                result=db.query('update caselog set sdid=$t1 where caseid=$t',myvar)
                raise web.seeother('/surgeoneditlog2')
       
class Editpro:
    
    def POST(self):
            inp=web.input(primaryp=[],secp=[],terp=[],quap=[])
            if inp.primaryp=='' or inp.secp=='' or inp.terp=='' or inp.quap=='':
                raise web.seeother('/surgeoneditlog2')
            else:
                pp,sp,tp,qp=','.join(inp.primaryp),','.join(inp.secp),','.join(inp.terp),','.join(inp.quap)
                flo=qp
                if qp=="None":
                    flo=tp
                if tp=="None":
                    flo=sp
                if sp=="None":
                    flo=pp
                myvar=dict(t1=pp,t2=sp,t3=sp,t4=qp,t5=flo,t=session.caseid)
                result=db.query('update caselog set ppro=$t1,spro=$t2,tpro=$t3,qpro=$t4,fpro=$t5 where caseid=$t',myvar)
                raise web.seeother('/surgeoneditlog2')

class Editreqsuc:
    def GET(self):
        return render.editreqsuc(session.nam)



class Surg_settings:
    def GET(self):
        if session.logged_in==True and session.count==2:
            return render.surgeonsetting(0,session.nam)
        else:
            return render.ua2()
    def POST(self):
        inp=web.input()
        myvar=dict(t=session.attr)
        result=db.select('users',myvar,where="uid=$t")
        i=0
        for user in result:
            if user.upwd==inp.cpassword:
                i=1
        if i!=0:
            var2 = dict(t1=inp.password,t2=session.attr)
            result=db.query("update users set upwd=$t1 where uid=$t2",var2)
            return render.surgeonsetting(1,session.nam)
        else:
            return render.surgeonsetting(2,session.nam)

    
class Surg_notif:
    def GET(self):
        if session.logged_in==True and session.count==2:
            myvar=dict(t=session.nam)
            result=db.query("select aid,alert.uname,date,time,strftime('%d-%m-%Y',logdate)as l from alert where uname=$t order by logdate desc",myvar)
            return render.surgeonnotification(session.nam,result)
        else:
            return render.ua2()
    def POST(self):
        myvar=dict(t=session.nam)
        db.query(" DELETE FROM alert WHERE uname=$t",myvar)
        web.seeother('/surgeonnotification')

'''---------------------------------Head Nurse-----------------------------'''
class Headnurse:
        def GET(self):
            if session.logged_in==True and session.count==3:
                result=db.query("SELECT * FROM caselog ORDER BY caseid DESC")
                result1=db.query('select * from users where urole=2')
                return render.headnurse(result,result1)
            else:
                return render.ua2()
        def POST(self):
            inp=web.input()
            if inp.date=='':
                raise web.seeother('/headnurse')
            else:
                result1=db.insert('alert',uname=inp.name,date=inp.date,time=inp.time,status=0)
                result2=db.insert('alert2',uname=inp.name,date=inp.date,time=inp.time,status=0)
                myvar=dict(t=result1)
                result=db.query("update alert set logdate=(select datetime(current_timestamp, 'localtime')) where aid=$t",myvar);
                result3=db.query("update alert2 set logdate=(select datetime(current_timestamp, 'localtime')) where aid=$t",myvar);
                raise web.seeother('/headalertsuc')


class Headalertsuc:
    def GET(self):
        return render.headalertsuc()
        
class Headsetting:
    def GET(self):
        if session.logged_in==True and session.count==3:
            return render.headsetting(0)
        else:
            return render.ua2()
    def POST(self):
        inp=web.input()
        var=dict(t=session.attr)
        result=db.select('users',var,where="uid=$t")
        i=0
        for user in result:
            if user.upwd==inp.cpassword:
                i=1
        if i!=0:
            var2 = dict(t1=inp.password,t2=session.attr)
            result=db.query("update users set upwd=$t1 where uid=$t2",var2)
            return render.headsetting(1)
        else:
            return render.headsetting(2)

class Logout:
    def GET(self):
        myvar=dict(t=session.attr)
        result=db.query("update users set lastlog=(select datetime(current_timestamp, 'localtime')) where uid=$t",myvar);
        session.logged_in=False
        session.kill()
        raise web.seeother('/')

if __name__ == "__main__":
     app.run()

