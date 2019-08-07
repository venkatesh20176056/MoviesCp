from flask import Flask, render_template, redirect, url_for, request, flash, Response, jsonify
from werkzeug import secure_filename
import pymysql
import datetime
global name
import inspect,os
import tablib
import codecs
import csv
import io
import json
import boto3

upload_folder='FILE_UPLOADS'
ALLOWED_EXTENSIONS	=set(['csv','tsv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.join(os.getcwd(),upload_folder)

conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
mycursor = conn.cursor()

name = ""
supr_usr = ""
dat1 = ()
s3 = boto3.resource('s3')




@app.route('/')
def index():
	return redirect(url_for('login'))

	
@app.route('/cms/login')
def login():
	return render_template("faqs-template.html", message = "Enter Username and Password")


@app.route('/cms/login',methods=['GET','POST'])
def authenticate():
	global name
	if(request.method == 'POST'):
		# username = str(request.form['Username'])
		username = str(request.form.get("Username"))
		password = str(request.form.get("Password"))
# request.form['Password']
		name = username

		conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
		mycursor = conn.cursor()
		mycursor.execute("select * from users where user_name='"+username+"' and password='"+password+"'")
		data = mycursor.fetchone()

		if data is None:
			return render_template("faqs-template.html", message = "Username or password is wrong") 
		else:
			return redirect(url_for('home'))


@app.route('/cms/signup')
def signup():
	return render_template("signup.html")


# @app.route('/cms/signup',methods=['GET','POST'])
# def add_user():
# 	if(request.method == 'POST'):
# 		name = str(request.form.get("Username"))
# 		pw = str(request.form.get("Password"))

# 		conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
# 		mycursor = conn.cursor()
# 		insert_stmt = ("INSERT INTO users( user_name, password) VALUES(%s,%s)")
# 		data = (name,pw)
	
# 		mycursor.execute(insert_stmt, data)
# 		conn.commit()
		
@app.route('/cms/home')
def home():	
	global dat1
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select super_user from users where user_name='"+name+"'")
	dat1 = mycursor.fetchone()
	print(dat1)
	return render_template("home.html", dat = dat1)


@app.route('/cms/home',methods=['GET','POST'])
def save_project():
	if (request.method == 'POST' and 'save-project' in request.form):
		
		name1 = str(request.form.get("Name"))
		description = str(request.form.get("Description"))
		purpose = str(request.form.get("Purpose"))
		teams = str(request.form.get("Teams"))
		currentDT = str(datetime.datetime.now())

		conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
		mycursor = conn.cursor()
		mycursor.execute("select count(project_id) from projects where admin='"+name+"';")
		get = mycursor.fetchone()
		print(get)
		if(get[0] == 0):
			pro = 1
		else:
			mycursor.execute("select max(project_id) from projects where admin='"+name+"';")
			get1 = mycursor.fetchone()
			print(get1)
			pro = get1[0]+1
		pro1 = int(pro)
		insert_stmt = ("INSERT INTO projects( admin, project_id, name, description, purpose, teams, time_stamp) VALUES(%s,%s,%s,%s,%s,%s,%s)")
		data = (name,pro1,name1,description,purpose,teams,currentDT)
		
		mycursor.execute(insert_stmt, data)
		conn.commit()
		
		return redirect(url_for('project'))


@app.route('/cms/projects')
def project():
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select project_id,name,description,purpose,teams,time_stamp from projects where admin='"+name+"';")
	total_data = mycursor.fetchall()
	return render_template("projects.html", data = total_data, dat = dat1)

@app.route('/cms/projects',methods=['GET','POST'])
def save_project1():
	if (request.method == 'POST' and 'save-project' in request.form):
		
		name1 = str(request.form.get("Name"))
		description = str(request.form.get("Description"))
		purpose = str(request.form.get("Purpose"))
		teams = str(request.form.get("Teams"))
		currentDT = str(datetime.datetime.now())

		conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
		mycursor = conn.cursor()
		mycursor.execute("select count(project_id) from projects where admin='"+name+"';")
		get = mycursor.fetchone()
		print(get)
		if(get[0] == 0):
			pro = 1
		else:
			mycursor.execute("select max(project_id) from projects where admin='"+name+"';")
			get1 = mycursor.fetchone()
			print(get1)
			pro = get1[0]+1
		pro1 = int(pro)
		insert_stmt = ("INSERT INTO projects( admin, project_id, name, description, purpose, teams, time_stamp) VALUES(%s,%s,%s,%s,%s,%s,%s)")
		data = (name,pro1,name1,description,purpose,teams,currentDT)
		
		mycursor.execute(insert_stmt, data)
		conn.commit()
		
		return redirect(url_for('project'))

@app.route('/cms/projects/<variable>')
def project_id(variable):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select * from projects where project_id="+variable+" and admin='"+name+"';")
	get_data = mycursor.fetchone()
	print(get_data)
	mycursor.execute("select count(config_id) from config_table where admin='"+name+"' and project_id="+variable+";")
	get1 = mycursor.fetchone()
	print(get1[0])
	get2 = get1[0]+1
	mycursor.execute("select * from config_table where admin='"+name+"' and project_id="+variable+";")
	get_data2 = mycursor.fetchall()
	return render_template("project_id.html", send = get_data, send2 = get2, data = get_data2, dat = dat1)	

@app.route('/cms/projects/<variable>/delete')
def delete_project(variable):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("delete from config_table where admin='"+name+"' and project_id="+variable+";")
	mycursor.execute("delete from projects where admin='"+name+"' and project_id="+variable+";")
	conn.commit()
	
	return redirect(url_for('project'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/cms/projects/<variable1>/config/<variable2>/details')
def config(variable1,variable2):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select * from config_table where admin='"+name+"' and project_id="+variable1+" and config_id="+variable2+";")
	get_data2 = mycursor.fetchone()
	return render_template("config_id.html",send = get_data2, dat = dat1)

@app.route('/cms/projects/<variable1>/config/<variable2>/delete')
def delete_config(variable1,variable2):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("delete from config_table where admin='"+name+"' and project_id="+variable1+" and config_id="+variable2+";")
	conn.commit()
	return redirect(url_for('project_id',variable=variable1))


@app.route('/cms/projects/<variable1>/config/<variable2>/show')
def show_csv(variable1,variable2):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select file_path from config_table where admin='"+name+"' and project_id="+variable1+" and config_id="+variable2+";")
	get = mycursor.fetchone()
	csvList = []
	with codecs.open(get[0], encoding='utf-8',errors='ignore') as f:
		readCSV = csv.reader(f, delimiter=',')
		i = 0
		for row in readCSV:
			csvList.insert(i,row)
			i += 1
	print(csvList)
	return render_template('index2.html', data=csvList, pid = variable1, cid = variable2, dat = dat1)

@app.route('/cms/projects/<variable1>/config/<variable2>/update_s3')
def update_s3(variable1,variable2):
	return render_template('update_s3.html', pid = variable1, cid = variable2, dat = dat1)

@app.route('/cms/projects/<variable1>/config/<variable2>/update_s3', methods=['GET', 'POST'])
def update_s3_file(variable1,variable2):
	if request.method == 'POST':
		bucket_name = str(request.form.get("Bucket_name"))
		Folder_name = str(request.form.get("Folder_name"))

		conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
		mycursor = conn.cursor()
		mycursor.execute("select file_path from config_table where admin='"+name+"' and project_id="+variable1+" and config_id="+variable2+";")
		get4 = mycursor.fetchone()
		fl_name = str(name)+"_"+str(variable1)+"_"+str(variable2)+str(get4[0][-4:])
		try:
			s3.Object(bucket_name,Folder_name + fl_name).upload_file(Filename=str(get4[0]))
			return render_template('update.html',message = "SUCCESSFULLY UPDATED TO S3", dat = dat1)
		except boto3.exceptions.S3UploadFailedError:
			return render_template('update.html',message = "INVALID BUCKET NAME / BUCKET DOESNOT EXIST", dat = dat1)

@app.route('/cms/projects/<variable1>/config/<variable2>/edit')
def edit_config_file(variable1,variable2):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select file_path from config_table where admin='"+name+"' and project_id="+variable1+" and config_id="+variable2+";")
	get = mycursor.fetchone()
	csvList = []
	with codecs.open(get[0], encoding='utf-8',errors='ignore') as f:
		readCSV = csv.reader(f, delimiter=',')
		i = 0
		for row in readCSV:
			csvList.insert(i,row)
			i += 1
	print(csvList)
	return render_template('index3.html', data=csvList, pid = variable1, cid = variable2, dat = dat1)


@app.route('/cms/projects/<variable1>/config/<variable2>/upload')
def upload(variable1,variable2):
	return render_template("upload.html", message= "select only CSV or TSV file", dat = dat1)
	
@app.route('/cms/projects/<variable1>/config/<variable2>/upload', methods=['GET', 'POST'])
def upload_file(variable1,variable2):
	if request.method == 'POST':
		flag1 = request.form.get("Name")
		flag2 = request.form.get("Description")
		flag3 = request.form.get("Maintainer")
		flag4 = request.form.getlist("select_ext")[0]
		flag5 = request.form.getlist("select_type")
		flag6 = request.form.get("Key")
		flag7 = request.form.get("Value")
		lst1 = flag6.split(',')
		lst2 = flag7.split(',')
		lst3 = []
		lst3.extend(lst1)
		lst3.extend(lst2)
		print(str(lst3)+"@@@@@@@@@@")

		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		
		myList = []
		strList = []
		i = 0
		num_of_lines = 0
		
		for line in file:
			num_of_lines = num_of_lines+1
			print(line)
			filename = secure_filename(file.filename)
			str1 = str(line, 'utf-8')
			str1.rstrip()
			print(str1)
			if(num_of_lines == 1 and filename[-3:] == 'csv'):
				lst = str1.split(',')
				lst[-1] = lst[-1].rstrip()
				print(str(lst)+"$$$$$$$$$$$")
				kv = 0
				if(all(x in lst for x in lst3)): 
					kv = 1


			if(num_of_lines == 1 and filename[-3:] == 'tsv'):
				lst = str1.split(',')
				lst[-1] = lst[-1].rstrip()
				print(str(lst)+"$$$$$$$$$$$")
				kv = 0
				if(all(x in lst for x in lst3)): 
					kv = 1

			if filename[-3:] == 'csv':
				str2 = str1.split(',')
				strList.insert(i,str2)
			if filename[-3:] == 'tsv':
				str2 = str1.split('	')
				strList.insert(i,str2)
			myList.insert(i,len(str2))
			i += 1
		print(num_of_lines)
		print(myList)
		j = 1
		for i in range (0,len(myList)-1):
			if(myList[i] == myList[i+1]):
				j += 1
		if j == len(myList):

			# print("** in allowed_file",allowed_file(file.filename))
			if file and allowed_file(file.filename) and kv == 1:
				filename = secure_filename(file.filename)
				# filename = str(variable1)+"_"+str(variable2)+"_"+filename
				print(filename)
				print(type(filename))

				get1 = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
				print(get1+"####")
				get2 = upload_folder
				get3 = filename
				
				# print(get4)
				fl_name = str(name)+"_"+str(variable1)+"_"+str(variable2)+str(filename[-4:])		
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(fl_name)))
				file_path = os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'])
				get4 = str(get1)+"/"+str(get2)+"/"+str(fl_name)
				# s3.Object('ml-stag-insurance-serving-artifacts',"CMS_FILES/" + fl_name).upload_file(Filename=get4)

				

				print(str(flag1)+"***"+str(flag2)+"***"+str(flag3)+"***"+str(flag4)+"***"+str(flag5)+"***"+str(flag6)+"***"+str(flag7)+"***")
				conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
				mycursor = conn.cursor()
				
				insert_stmt = ("INSERT INTO config_table( admin, project_id, config_id, name, description, maintainer, file_path, extension, file_type, key_columns, value_columns) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
				data = (name,variable1,variable2,flag1,flag2,flag3,get4,flag4,flag5,flag6,flag7)
				mycursor.execute(insert_stmt, data)
				conn.commit()	
				
				with open(os.path.join(file_path,fl_name), 'w') as csvFile:
					writer = csv.writer(csvFile)
					for row in strList:
						writer.writerow(row)
				return render_template("success.html", dat = dat1)
			else:
				return render_template("upload.html", message = "Enter correct KEY VALUE column names", dat = dat1)
		else:
			return render_template("upload.html", message = "you are trying to upload a INVALID FILE", dat = dat1)	


@app.route('/cms/projects/<variable1>/config/<variable2>/edit', methods=['GET','POST'])
def test(variable1,variable2):
	clicked = request.json
	print(type(clicked))
	for i in clicked:
		print(i)
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select file_path from config_table where admin='"+name+"' and project_id="+variable1+" and config_id="+variable2+";")
	get = mycursor.fetchone()
	print(get)
	with open(get[0], 'w') as writeFile:
		writer = csv.writer(writeFile)
		for i in clicked:
			print("#####")
			print(type(i))
			my_list = list(i)
			writer.writerow(my_list)
			print(my_list)
	return "over"


# **************ADMIN PANEL**************
@app.route('/cms/admin')
def admin():
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select user_name from users;")
	exec1 = mycursor.fetchall()

	return render_template("admin.html",send = exec1)

@app.route('/cms/admin/<nam>/projects')
def project_admin(nam):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select admin,project_id,name,description,purpose,teams,time_stamp from projects where admin='"+nam+"';")
	total_data = mycursor.fetchall()
	return render_template("projects_admin.html", data = total_data, dat = dat1, pro = nam)

@app.route('/cms/admin/<nam>/projects',methods=['GET','POST'])
def save_project2(nam):
	if (request.method == 'POST' and 'save-project' in request.form):
		
		name1 = str(request.form.get("Name"))
		description = str(request.form.get("Description"))
		purpose = str(request.form.get("Purpose"))
		teams = str(request.form.get("Teams"))
		currentDT = str(datetime.datetime.now())

		conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
		mycursor = conn.cursor()
		mycursor.execute("select count(project_id) from projects where admin='"+nam+"';")
		get = mycursor.fetchone()
		print(get)
		if(get[0] == 0):
			pro = 1
		else:
			mycursor.execute("select max(project_id) from projects where admin='"+nam+"';")
			get1 = mycursor.fetchone()
			print(get1)
			pro = get1[0]+1
		pro1 = int(pro)
		insert_stmt = ("INSERT INTO projects( admin, project_id, name, description, purpose, teams, time_stamp) VALUES(%s,%s,%s,%s,%s,%s,%s)")
		data = (nam,pro1,name1,description,purpose,teams,currentDT)
		
		mycursor.execute(insert_stmt, data)
		conn.commit()
		
		return redirect(url_for('project_admin',nam = nam))

@app.route('/cms/admin/<nam>/projects/<variable>')
def project_id_admin(nam,variable):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select * from projects where project_id="+variable+" and admin='"+nam+"';")
	get_data = mycursor.fetchone()
	print(get_data)
	mycursor.execute("select count(config_id) from config_table where admin='"+nam+"' and project_id="+variable+";")
	get1 = mycursor.fetchone()
	print(get1[0])
	get2 = get1[0]+1
	mycursor.execute("select * from config_table where admin='"+nam+"' and project_id="+variable+";")
	get_data2 = mycursor.fetchall()
	return render_template("project_id_admin.html", pro = nam, send = get_data, send2 = get2, data = get_data2, dat = dat1)

@app.route('/cms/admin/<nam>/projects/<variable1>/config/<variable2>/upload')
def upload_admin(nam,variable1,variable2):
	return render_template("upload_admin.html", message= "select only CSV or TSV file", dat = dat1)
	
@app.route('/cms/admin/<nam>/projects/<variable1>/config/<variable2>/upload', methods=['GET', 'POST'])
def upload_file_admin(nam,variable1,variable2):
	if request.method == 'POST':
		flag1 = request.form.get("Name")
		flag2 = request.form.get("Description")
		flag3 = request.form.get("Maintainer")
		flag4 = request.form.getlist("select_ext")[0]
		flag5 = request.form.getlist("select_type")
		flag6 = request.form.get("Key")
		flag7 = request.form.get("Value")
		lst1 = flag6.split(',')
		lst2 = flag7.split(',')
		lst3 = []
		lst3.extend(lst1)
		lst3.extend(lst2)
		print(str(lst3)+"@@@@@@@@@@")

		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		
		myList = []
		strList = []
		i = 0
		num_of_lines = 0
		
		for line in file:
			num_of_lines = num_of_lines+1
			print(line)
			filename = secure_filename(file.filename)
			str1 = str(line, 'utf-8')
			str1.rstrip()
			print(str1)
			if(num_of_lines == 1 and filename[-3:] == 'csv'):
				lst = str1.split(',')
				lst[-1] = lst[-1].rstrip()
				print(str(lst)+"$$$$$$$$$$$")
				kv = 0
				if(all(x in lst for x in lst3)): 
					kv = 1


			if(num_of_lines == 1 and filename[-3:] == 'tsv'):
				lst = str1.split(',')
				lst[-1] = lst[-1].rstrip()
				print(str(lst)+"$$$$$$$$$$$")
				kv = 0
				if(all(x in lst for x in lst3)): 
					kv = 1

			if filename[-3:] == 'csv':
				str2 = str1.split(',')
				strList.insert(i,str2)
			if filename[-3:] == 'tsv':
				str2 = str1.split('	')
				strList.insert(i,str2)
			myList.insert(i,len(str2))
			i += 1
		print(num_of_lines)
		print(myList)
		j = 1
		for i in range (0,len(myList)-1):
			if(myList[i] == myList[i+1]):
				j += 1
		if j == len(myList):

			# print("** in allowed_file",allowed_file(file.filename))
			if file and allowed_file(file.filename) and kv == 1:
				filename = secure_filename(file.filename)
				# filename = str(variable1)+"_"+str(variable2)+"_"+filename
				print(filename)
				print(type(filename))

				get1 = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
				print(get1+"####")
				get2 = upload_folder
				get3 = filename
				
				# print(get4)
				fl_name = str(nam)+"_"+str(variable1)+"_"+str(variable2)+str(filename[-4:])		
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(fl_name)))
				file_path = os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'])
				get4 = str(get1)+"/"+str(get2)+"/"+str(fl_name)
				# s3.Object('ml-stag-insurance-serving-artifacts',"CMS_FILES/" + fl_name).upload_file(Filename=get4)

				

				print(str(flag1)+"***"+str(flag2)+"***"+str(flag3)+"***"+str(flag4)+"***"+str(flag5)+"***"+str(flag6)+"***"+str(flag7)+"***")
				conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
				mycursor = conn.cursor()
				
				insert_stmt = ("INSERT INTO config_table( admin, project_id, config_id, name, description, maintainer, file_path, extension, file_type, key_columns, value_columns) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
				data = (nam,variable1,variable2,flag1,flag2,flag3,get4,flag4,flag5,flag6,flag7)
				mycursor.execute(insert_stmt, data)
				conn.commit()	
				
				with open(os.path.join(file_path,fl_name), 'w') as csvFile:
					writer = csv.writer(csvFile)
					for row in strList:
						writer.writerow(row)
				return render_template("success_admin.html", dat = dat1)
			else:
				return render_template("upload_admin.html", message = "Enter correct KEY VALUE column names", dat = dat1)
		else:
			return render_template("upload_admin.html", message = "you are trying to upload a INVALID FILE", dat = dat1)

@app.route('/cms/admin/<nam>/projects/<variable1>/config/<variable2>/details')
def config_admin(nam,variable1,variable2):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select * from config_table where admin='"+nam+"' and project_id="+variable1+" and config_id="+variable2+";")
	get_data2 = mycursor.fetchone()
	return render_template("config_id_admin.html", pro = nam, send = get_data2, dat = dat1)

@app.route('/cms/admin/<nam>/projects/<variable1>/config/<variable2>/show')
def show_csv_admin(nam,variable1,variable2):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select file_path from config_table where admin='"+nam+"' and project_id="+variable1+" and config_id="+variable2+";")
	get = mycursor.fetchone()
	csvList = []
	with codecs.open(get[0], encoding='utf-8',errors='ignore') as f:
		readCSV = csv.reader(f, delimiter=',')
		i = 0
		for row in readCSV:
			csvList.insert(i,row)
			i += 1
	print(csvList)
	return render_template('index2_admin.html', pro=nam, data=csvList, pid = variable1, cid = variable2, dat = dat1)

@app.route('/cms/admin/<nam>/projects/<variable1>/config/<variable2>/edit')
def edit_config_file_admin(nam,variable1,variable2):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select file_path from config_table where admin='"+nam+"' and project_id="+variable1+" and config_id="+variable2+";")
	get = mycursor.fetchone()
	csvList = []
	with codecs.open(get[0], encoding='utf-8',errors='ignore') as f:
		readCSV = csv.reader(f, delimiter=',')
		i = 0
		for row in readCSV:
			csvList.insert(i,row)
			i += 1
	print(csvList)
	return render_template('index3_admin.html', pro = nam, data=csvList, pid = variable1, cid = variable2, dat = dat1)

@app.route('/cms/admin/<nam>/projects/<variable1>/config/<variable2>/edit', methods=['GET','POST'])
def test_admin(nam,variable1,variable2):
	clicked = request.json
	print(type(clicked))
	for i in clicked:
		print(i)
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("select file_path from config_table where admin='"+nam+"' and project_id="+variable1+" and config_id="+variable2+";")
	get = mycursor.fetchone()
	print(get)
	with open(get[0], 'w') as writeFile:
		writer = csv.writer(writeFile)
		for i in clicked:
			print("#####")
			print(type(i))
			my_list = list(i)
			writer.writerow(my_list)
			print(my_list)
	return "over"

@app.route('/cms/admin/<nam>/projects/<variable1>/config/<variable2>/update_s3')
def update_s3_admin(nam,variable1,variable2):
	return render_template('update_s3_admin.html', pro = nam, pid = variable1, cid = variable2, dat = dat1)

@app.route('/cms/admin/<nam>/projects/<variable1>/config/<variable2>/update_s3', methods=['GET', 'POST'])
def update_s3_file_admin(nam,variable1,variable2):
	if request.method == 'POST':
		bucket_name = str(request.form.get("Bucket_name"))
		Folder_name = str(request.form.get("Folder_name"))

		conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
		mycursor = conn.cursor()
		mycursor.execute("select file_path from config_table where admin='"+nam+"' and project_id="+variable1+" and config_id="+variable2+";")
		get4 = mycursor.fetchone()
		fl_name = str(nam)+"_"+str(variable1)+"_"+str(variable2)+str(get4[0][-4:])
		try:
			s3.Object(bucket_name,Folder_name + fl_name).upload_file(Filename=str(get4[0]))
			return render_template('update_admin.html',message = "SUCCESSFULLY UPDATED TO S3", dat = dat1)
		except boto3.exceptions.S3UploadFailedError:
			return render_template('update_admin.html',message = "INVALID BUCKET NAME / BUCKET DOESNOT EXIST", dat = dat1)

@app.route('/cms/admin/<nam>/projects/<variable>/delete')
def delete_project_admin(nam,variable):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("delete from config_table where admin='"+nam+"' and project_id="+variable+";")
	mycursor.execute("delete from projects where admin='"+nam+"' and project_id="+variable+";")
	conn.commit()
	
	return redirect(url_for('project_admin',nam = nam))

@app.route('/cms/admin/<nam>/projects/<variable1>/config/<variable2>/delete')
def delete_config_admin(nam,variable1,variable2):
	conn = pymysql.connect(host="172.21.113.175", user="cms_control_panel", passwd="cms_control_panel@123", db="cms_control_panel_paytm")
	mycursor = conn.cursor()
	mycursor.execute("delete from config_table where admin='"+nam+"' and project_id="+variable1+" and config_id="+variable2+";")
	conn.commit()
	return redirect(url_for('project_id_admin', nam=nam, variable=variable1))

if __name__ == '__main__':
	app.run(debug = True)
