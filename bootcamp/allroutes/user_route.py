from enum import unique
import random,json,string,requests
from flask import flash, redirect, render_template, request, session, url_for,abort
from werkzeug.security import check_password_hash, generate_password_hash
from bootcamp import db, fins, form,mail,Message
from bootcamp.models import Book, Car, Cust,Pay, Serve


def refno():
    sample_xters=random.sample(string.digits,10)
    newname=''.join(sample_xters)
    return newname
        

@fins.errorhandler(404)
def mistake(error):
    return render_template('user/error.html',error=error),404       

@fins.route('/')
def home():
    return render_template('user/home.html')


@fins.route('/sign',methods=['GET','POST'])
def sign():
    up=form.Signup()
    if request.method =='GET':
     return render_template('user/signup.html',up=up)  
    else:
        #retrieve form data
        if up.validate_on_submit:
            fname=request.form.get('firstname')  
            lname=request.form.get('lastname')
            number=request.form.get('number')
            email=request.form.get('mail')
            uname=request.form.get('username')
            password=request.form.get('password')  
            conf=request.form.get('confword')
            converted=generate_password_hash(password)
            address=request.form.get('address')    
                
            if password==conf:
                    g=Cust(customer_name=fname  + ''  + lname,customer_mobile=number,customer_email=email,customer_username=uname,customer_password=converted,customer_address=address)
                    db.session.add(g)
                    db.session.commit()
                    session['user']=g.customer_id
                    Message()
                    msg=Message(subject="Testing Mail",sender="oyindaadesewa@gmail.com",
                    recipients=[email],body="Test Mail")
                    msg.html=f"<div><h2>Hello {uname}</h2><p>You are welcome to Automotive app.On this app,you can make appointments,orders,see your orders and so on.Thanks for joining the app</p></div>"
                    mail.send(msg)
                    return redirect('/dashboard')              
            else:
                    flash('Please make sure the password are the same')
                    return render_template('user/signup.html',up=up)  

        else:
                return render_template('user/signup.html',up=up)  


@fins.route('/login',methods=['GET','POST'])
def log():
    if request.method =='GET':
        return render_template('user/login.html')
    else:
        data1=request.form.get('username')
        data2=request.form.get('password')
        rec=db.session.query(Cust).filter(Cust.customer_email==data1).first()
        if rec:
            loggedin_user =rec.customer_id
            hashedpass =rec.customer_password
            check=check_password_hash(hashedpass,data2)
            if check:
             session['user']=loggedin_user
             return redirect ('/dashboard')
             
            else:
                flash('Invalid credentials') 
                return redirect(url_for('log'))
        else:
         flash('Invalid Credientials,please try to login again')
         return   redirect('/login')


@fins.route('/dashboard')
def prof():
    loggedin_user = session.get('user')
    if loggedin_user != None:
        data = db.session.query(Cust).get(loggedin_user)
        return render_template('user/dash.html',data=data)  
    else:
        return redirect('/login')

   
@fins.route('/logout')
def logout():
    return redirect('/login')
     
@fins.route('/appointment',methods=['GET','POST'])
def appointment():
         loggedin = session.get('user')
         if loggedin != None:
             if request.method =='GET':
                 return render_template('user/appointment.html')
             else:
                title=request.form.get('appoint')
                type=request.form.get('kind')
                ticket=request.form.get('tick')
                descript=request.form.get('reason')
                s=Book(booking_customer_id =loggedin,booking_title=title,booking_type=type,booking_ticket=ticket,booking_description=descript)
                db.session.add(s)
                db.session.commit()
                return redirect('/dashboard')
         else:
            return redirect('/login')    


@fins.route('/contact')
def contact():
    return render_template('user/contact-us.html')

@fins.route('/direction') 
def direct():
    return render_template('user/direction.html')


@fins.route('/orders')   
def orders():
        loggedin=session.get('user')
        if loggedin != None:
         use=db.session.query(Cust,Car).join(Car).filter(Cust.customer_id==loggedin).first()
         return render_template('user/orders.html',use=use)
        else:
            return redirect('/login') 


@fins.route('/appoint')   
def appoint():
        loggedin=session.get('user')
        if loggedin != None:
         used=db.session.query(Cust,Book).join(Book).filter(Cust.customer_id==loggedin).first()
         return render_template('user/appoint.html',used=used)         



@fins.route('/transaction')   
def transaction():
        loggedin=session.get('user')
        if loggedin != None:
         t=db.session.query(Cust,Pay).join(Pay).filter(Cust.customer_id==loggedin).first()
         return render_template('user/trans.html',t=t)         

@fins.route('/order',methods=['POST','GET'])
def order():
        sin=form.Signup()
        loggedin=session.get('user')
        if loggedin != None:
            if request.method=='GET': 
                return render_template('user/order.html',up=sin)

            else:
                    numb=request.form.get('year')
                    typ=request.form.get('model')
                    company=request.form.get('veh')
                    des=request.form.get('describe')
                    x=Car(car_number=numb,car_company=company,car_type=typ,car_description=des,car_customer_id=loggedin)
                    db.session.add(x)
                    db.session.commit()
                    flash('Your order has been received and we will get back to you shortly')
                    ser=request.form.get('services')
                    pat=db.session.query(Serve).filter(Serve.service_name==ser).first()
                    return render_template('user/order.html',pat=pat)
                    # return redirect('/payment')

        else:
            return  render_template('user/login.html')



@fins.route('/payment',methods=['GET','POST'])
def paycash():
    if session.get('user') != None:
     if request.method=='GET':
      return render_template('user/cash.html')     
     else:
        id=session.get('user')
        amt=request.form.get('amount',0)
        ref=refno()
        session['trxref']=ref
        t=Pay(payment_customer_id=id,payment_amt=amt,payment_ref=ref,payment_status='Pending',payment_type='Card')
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('confirmpay'))   
    else:
        return redirect(url_for('log'))  


@fins.route('/confirmpay',methods=['GET','POST'])
def confirmpay():
    if session.get('user') != None and session.get('trxref') != None:
        ref = session.get('trxref')
        conf = db.session.query(Pay,Cust).join(Cust).filter(Pay.payment_ref==ref).first()

        if request.method=='GET':
            return render_template('user/confirm.html',conf=conf)  
        else:
            #connect to paystack endpoint
            amt = conf[0].payment_amt* 100
            email=conf[1].customer_email
            headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_653a4b603cd60508a25eee177829e3928ff7ea2b"}            
            data = {"reference": ref, "amount": amt,"email":email}
            response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))

            rsp = json.loads(response.text) 
            if rsp.get('status')==True:	
                payurl=rsp['data']['authorization_url']
                return redirect (payurl)
            else: 
                flash('An error occcurred during the connection,please try again ')
                return redirect(url_for('paycash'))    
    else:     
        return redirect(url_for('log'))  

  
@fins.route('/payconfirm') 
def payconfirm():
    loggedin=session.get('user')
    refsession = session.get('trxref')
    if loggedin and refsession:
         #receive response from Payment Company and inform user of the transaction status
        ref=request.args.get('reference')
        headers={'Authorization':'Bearer sk_test_653a4b603cd60508a25eee177829e3928ff7ea2b'}
        #urlverify = "https://api.paystack.co/transaction/verify/"+ref
        response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
        rsp =response.json()#in json format
        #return render_template('user/test.html',rsp=rsp)

        if rsp['data']['status'] =='success':
            # amt = rsp['data']['amount']
            # ipaddress = rsp['data']['ip_address']
            t = Pay.query.filter(Pay.payment_ref==refsession).first()
            t.payment_status = 'Paid'
            db.session.commit()
            return "Payment Was Successful"
            #return 'update database and redirect them to the feedback page'
        else:
            t = Pay.query.filter(Pay.payment_ref==refsession).first()
            t.payment_status = 'Failed'
            db.session.commit()
            return "Payment Failed"     
    else:
        abort(403)
