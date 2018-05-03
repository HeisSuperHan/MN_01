#!/usr/bin/env python
#coding:utf8


from flask import Flask,request,escape,session,redirect,url_for,render_template,make_response
from flask import jsonify
import sqlite3
import json
import os
import time

app = Flask(__name__)

#用户注册表单数据过滤函数
def saferegister(req):
    not_safe = ['/','\\','*','#','$','^',')','(','+','-','%','!','~','?','[',']','{','}','<','>','=']
    email_need = ['@','.']
    email = req.form['email']
    password = req.form['password']
    repeate = req.form['repeate']
    if password == repeate:
        if email_need[0] in email:
            if email_need[1] in email:
                for x in not_safe:
                    if x in email:
                        return False
                        break
                    else:
                        if x in password:
                            return False
                            break
                        else:
                            return True
            else:
                return False
        else:
            return False


#用户登陆数据过滤函数
def safelogin(req):
    not_safe = ['/','\\','*','#','$','^',')','(','+','-','%','!','~','?','[',']','{','}','<','>','=']
    email_need = ['@','.']
    email = req.form['email']
    password = req.form['password']
    if email_need[0] in email:
        if email_need[1] in email:
            for x in not_safe:
                if x in email:
                    return False
                    break
                else:
                    if x in password:
                        return False
                        break
                    else:
                        return True
    else:
        return False



#user

@app.route('/')
def index():
    column = os.listdir('./database/admin@bigboss.com')
    all_article = []
    for x in column:
        for y in os.listdir('./database/admin@bigboss.com/'+x):
            all_article.append([y.split('_')[0],y])
    try:
        names = request.cookies['user']
        return render_template('v2_index.html',tab_active=column[0],tab=column[1:],all_article=all_article)
    except:
        return render_template('v2_index.html',tab_active=column[0],tab=column[1:],all_article=all_article)

@app.route('/login',methods=['GET','POST'])
def login():
    column = os.listdir('./database/admin@bigboss.com')
    all_article = {}
    for x in column:
        all_article[x] = []
        for y in os.listdir('./database/admin@bigboss.com/' + x):
            all_article[x].append(y)
    if request.method == 'POST':
        if safelogin(request):
            conn = sqlite3.connect('database/user_info/user_account.db')
            cursor = conn.cursor()
            sql = "select password from account where email=?"
            a = cursor.execute(sql,(request.form['email'],))
            b = a.fetchall()
            cursor.close()
            conn.close()
            if b[0][0] == request.form['password'] :
                resp = make_response(render_template('v2_index.html',tab_active=column[0],tab=column[1:],all_article=all_article))
                resp.set_cookie('user',request.form['email'])
                return resp
            else:
                return render_template('v2_login.html',content='账户错误1')
        else:
            return render_template('v2_login.html',content='请不要输入符号等特殊字符！')

    if request.method == 'GET':
        try:
            if request.cookies['Isregister'] == 'True':
                return render_template('v2_login.html',content='您已完成注册，请登录')    #这个页面这里会显示注册过后进行登陆的提示语
        except:
            try:
                if request.cookies['user']:
                    username = request.cookies['user']
                    return render_template('v2_user.html',name=username)
                else:
                    return render_template('v2_login.html')              #这里返回直接点击登陆后的登陆页面
            except:
                return render_template('v2_login.html')


@app.route('/logout')
def logout():
    resp = make_response(render_template('v2_index.html'))
    resp.set_cookie('user','',expires=0)
    return resp



@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if saferegister(request):
            conn = sqlite3.connect('database/user_info/user_account.db')
            cursor = conn.cursor()
            ifexist = cursor.execute('select * from account where email=?',(request.form['email'],))
            if ifexist == []:
                return render_template('v2_login.html',content='账户已存在，请登录')
            sql = 'insert into account values(?,?)'
            cursor.execute(sql,(request.form['email'],request.form['password']))
            conn.commit()
            cursor.close()
            conn.close()
            return render_template('v2_login.html',content='您已完成注册，请登录')
        else:
            resp = make_response(render_template('v2_register.html',content='设置密码请不要输入符号等特殊字符！'))
            resp.set_cookie('q3','qqwasas')
            return resp
    if request.method == 'GET':
        return render_template('v2_register.html')



@app.route('/resetpwd',methods=['GET','POST'])
def resetpwd():
    pass


@app.route('/v2_article/<article_id>',methods=['GET'])
def v2_article(article_id):
    try:
        name = request.cookies['user']
        with open('./database/admin@bigboss.com/'+article_id.split('_')[1]+'/'+article_id,'r') as f:
            content = f.read()
        return render_template('v2_article.html',title=article_id.split('_')[1] ,content=content,open='yes')
    except:
        with open('./database/admin@bigboss.com/'+article_id.split('_')[1]+'/'+article_id,'r') as f:
            content = f.read()
        return render_template('v2_article.html',title=article_id.split('_')[1],content=content,open='no')


# admin
# admin_email = 'admin@bigboss.com'  admin_password = 'xisbigboss'

@app.route('/admin',methods=['GET'])
def admin():
    admin_cookies = request.cookies['admin']
    if admin_cookies == 'xman_7590_acca':
        conn = sqlite3.connect('database/user_info/user_account.db')
        cursor = conn.cursor()
        sql = 'select * from account'
        member = len(cursor.execute(sql).fetchall())
        cursor.close()
        conn.close()
        all_article = []
        for x in os.listdir('./database/admin@bigboss.com'):
            for y in os.listdir('./database/admin@bigboss.com/'+x):
                all_article.append(y)
        article_number = len(all_article)
        column_list = os.listdir('./database/admin@bigboss.com')
        return render_template('admin_dashboard.html',name='admin',member=member,article_number=article_number,column_list=column_list)
    else:
        return 'error cookies'


@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method == 'GET':
        try:
            admin_cookies = request.cookies['admin']
            if admin_cookies == 'xman_7590_acca':
                return redirect('/admin')
            else:
                return render_template('admin_login.html')
        except:
            return render_template('admin_login.html')
    if request.method == 'POST':
        admin_email = request.form['email']
        admin_password = request.form['password']
        if admin_email != 'admin@bigboss.com' or admin_password != 'xisbigboss':
            return render_template('admin_login.html',content='密码错误')
        else:
            conn = sqlite3.connect('database/user_info/user_account.db')
            cursor = conn.cursor()
            sql = 'select * from account'
            member = len(cursor.execute(sql).fetchall())
            cursor.close()
            conn.close()
            all_article = []
            for x in os.listdir('./database/admin@bigboss.com'):
                for y in os.listdir('./database/admin@bigboss.com/' + x):
                    all_article.append(y)
            article_number = len(all_article)
            column_list = os.listdir('./database/admin@bigboss.com')
            resp = make_response(render_template('admin_dashboard.html',name='admin',member=member,article_number=article_number,column_list=column_list))
            resp.set_cookie('admin', 'xman_7590_acca')
            return resp



@app.route('/admin_logout',methods=['GET'])
def admin_logout():
    resp = make_response(render_template('admin_login.html'))
    resp.set_cookie('admin', '', expires=0)
    return resp


# 增加栏目
@app.route('/add_column',methods=['POST'])
def add_column():
    admin_path = './database/admin@bigboss.com/'
    try:
        admin_cookies = request.cookies['admin']
        if admin_cookies == 'xman_7590_acca':
            column = request.form['add_column']
            os.mkdir(admin_path+column)
            return render_template('admin_board.html')
        else:
            return 'error cookies'
    except:
        return redirect('admin')


@app.route('/delete_column/<column_id>',methods=['GET'])
def delete_column(column_id):
    try:
        admin_cookies = request.cookies['admin']
        if admin_cookies == 'xman_7590_acca':
            column_path = './database/admin@bigboss.com/'+column_id
            os.removedirs(column_path)
            return redirect('/admin')
        else:
            return 'error cookies'
    except:return 'no cookies'

@app.route('/add_article',methods=['POST'])      #ajax
def add_article():
    if request.method == 'POST':
        article_title = request.form['article_title']
        article_content = request.form['article_content']
        select_column = request.form['select_column']
        user_article_path = './database/admin@bigboss.com/'+select_column+'/'
        article_file = article_title+'_'+select_column+'_'+str(time.time())
        with open(user_article_path+article_file,'w')as f:
            f.write(article_content)
            f.close()
        return redirect('/article_list/1')
    else:
        return redirect('/')


@app.route('/update_article/<article_id>',methods=['POST'])
def update_article(article_id):
    try:
        select_column = article_id.split('_')[1]
        user_article_path = './database/admin@bigboss.com/' + select_column + '/'
        with open(user_article_path+article_id,'w')as f:
            f.write(request.form['data'])
        return 'ok!'
    except:
        return 'no cookies , no way'



@app.route('/article_list/<page>',methods=['GET'])
def article_list(page):
    try:
        page = int(page)
        user_article_path = './database/admin@bigboss.com/'
        column_list = [x for x in os.listdir(user_article_path)]
        article_list = []
        for z in column_list:
            for p in os.listdir(user_article_path+z):
                article_list.append(p)
        result = sorted([[float(y.split('_')[2]),[y.split('_')[0],y]] for y in article_list],reverse=True)
        if page<1:
            return 'error page'
        if page == 1:
            return render_template('article_list.html',previous=1,next=page+1,article_lists=result[:20],name='admin')
        if page>1:
            page1 = (page - 1)*20
            page2 = (page + 1)*20
            return render_template('article_list.html', previous=page - 1, next=page + 1, article_lists=result[page1:page2],name='admin')
    except:
        return 'no cookies , no way'


@app.route('/article_detail/<article_id>',methods=['GET'])
def article_detail(article_id):
    user_article_path = './database/admin@bigboss.com/'+article_id.split('_')[1]+'/'
    article_title = article_id.split('_')[0]
    article_timestamp = article_id.split('_')[2]
    article_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(article_timestamp)))
    if os.path.exists(user_article_path+article_id):
        with open(user_article_path+article_id,'r') as f:
            content = f.read()
        return render_template('article_detail.html',title=article_title,content=content,name='admin',article_id=article_id,article_time=article_time)
    else:
        return render_template('article_detail.html',title=article_title,content='内容不存在',name='admin')


@app.route('/delete_article/<article_id>',methods=['GET'])
def delete_article(article_id):
    try:
        user_article_path = './database/admin@bigboss.com/'+article_id.split('_')[1]+'/'
        if os.path.exists(user_article_path+article_id):
            os.remove(user_article_path+article_id)
            return redirect('/article_list/1')
        else:
            return 'article not exist!'
    except:
        return 'no cookies , no way'


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'chunli'
    app.run(host='0.0.0.0',debug=True)