from operator import mod
from flask import render_template,request,redirect,session,flash,make_response
from bootcamp import fins,form,db
from bootcamp.models import Book, Car, Cust, Pay


@fins.route('/admin',methods=['GET','POST']) 
def admin():
    if request.method=='GET':
     return render_template('admin/adminlogin.html')   
    else:
        log=request.form.get('username') 
        word=request.form.get('password')
        if log == 'wale@gmail.com' and word =='wale':
            return redirect ('/adminboard')
        else:
            flash('Sorry your credentials are incorrect')  
            return render_template('admin/adminlogin.html')    
       

@fins.route('/adminpage')   
def adminpage():
        tot=db.session.query(Cust).all()
        return render_template('admin/adminpage.html',tot=tot) 
  

@fins.route('/custorder')   
def custorder():
    tol=db.session.query(Cust,Car).join(Car).all()
    return render_template('admin/custorder.html',tol=tol)     



@fins.route('/report')   
def report():
    lot=db.session.query(Cust,Pay).join(Pay).all()
    return render_template('admin/pay.html',lot=lot)       
    

@fins.route('/adminboard')
def adminboard():
    all=db.session.query(Cust).count()
    tot=db.session.query(Car).count()
    return render_template('admin/adminboard.html',all=all,tot=tot)


 
@fins.route('/adminlogout')
def adminlogout():
    return redirect('/admin')






