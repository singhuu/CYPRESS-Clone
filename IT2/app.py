'''CPS406: Iteration 2/3, CYPRESSv1
Group 49: Ming Zhu Kong, Khushdip Nijjar, Shantanu Singh, Aston Wright

1. Run app.py
2. localhost:5000 in browser to access

*For remote access, on same network*
3. If local host, cmd -> ipconfig for ipv4 address
4. In remote browser -> http://<host ipv4 address>:5000/
'''

#micro web framework in python
from flask import Flask, render_template, session, g, request, redirect, url_for

'''additional modules for database implementation and database password encryption down the line'''
# from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'cps406'.encode('utf-8')

'''hi, no touchy pls'''
'''------------------------------'''
# list of all existing security questions, in order with indice
SECURITY_QUESTIONS = ["What is your mother's maiden name?", "What is the name of your elementary school?", "What the name of your first pet?", "What was your first car?", "What is the name of the town you were born?"]
# for password recovery only
RECOVERY_QUESTION = ""
RECOVERY_ANS = ""
PASS_RECOVERY = ""
# for registration only
BUILD_USER = ""
'''------------------------------'''


### For Implementation with SQL database down the line ###

# the database file
DATABASE = './cypressdb.db'

# connect to the database
def get_db():
    # if there is a database, use it
    db = getattr(g, '_database', None)
    if db is None:
        # otherwise, create a database to use
        db = g._database = sqlite3.connect(DATABASE)
    return db

# given some query, executes and returns the result
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# given some query, executes and writes to db
def write_db(query, args=()):
    db = get_db()
    try:
        cur = db.execute(query, args)
        db.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        return str(e)

# write to database (multiple records)
def write_db_many(query, values=()):
    db = get_db()
    try:
        cur = db.executemany(query, values)
        db.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        return str(e)


### START OF FLASK METHODS ###

# call function when Flask shuts down
# tear down the database connection when Flask shuts down
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # close the database if connected
        db.close()

@app.route('/', methods=['GET','POST'])
# start by asking for login credentials, when there is no active session
@app.route('/login', methods=['GET','POST'])

# WIP LOGIN (For registered users only, no distinction between user and admin for now.)
def login():
    error = ''
    confirmation = ''
    if request.method == 'POST':
        sql = 'select full_name, email, password, address_line_1, address_line_2, postal_code, phone_number from user_info where email=\'' + request.form['email'] + '\''
        try:
            user = query_db(sql)[0]
        except IndexError:
            error = 'Account does not exist! Please try again.'
            return render_template('login.html', error=error)

        if (user[1] == request.form['email']) and (user[2] == request.form['password']):
            session['user'] = {'email': user[1], 'fullname': user[0], 'user_password': user[2], 'address_line_1': user[3], 'address_line_2': user[4], 'postal_code': user[5], 'phone_number': user[6]}
            return render_template('home.html', error=error)
        else:
            error = 'Incorrect password, please try again.'
    elif 'user' in session:
        return render_template('home.html', error=error)
    elif len(request.args) > 0 and request.args.get('f') == 'register':
        confirmation = 'Security answers set successfully! Please log in to access CYPRESS.'
    elif len(request.args) > 0 and request.args.get('f') == 'failed':
        confirmation = 'Failed to set security questions. Please log in to access CYPRESS.'

    return render_template('login.html', error=error, confirmation=confirmation)

    #missing: error counter (3 failed login attempts) + ban timer (1hr) 

#WIP REGISTER (For new users only, no distinction between user and admin accounts for now.)
# NO password encryption
@app.route('/register', methods=['GET','POST'])
def register():
    error = ''
    global BUILD_USER
    register_passed = False
    if request.method == 'POST':
        if 'email' in request.form:
            # missing: check for secure password
            # missing: check for proper phone number(?) (need some kind of standard format)
            if request.form['address-2'] == '':
                sql = ('insert into user_info (full_name, email, password, address_line_1, postal_code, phone_number) values (\'' +
                        request.form['fullname'] + '\',\'' + request.form['email'] + '\',\'' +
                        request.form['password'] + '\',\'' + request.form['address-1'] + '\', \'' + request.form['postal'] + '\',\'' + request.form['phone-number'] + '\')')
            else:
                sql = ('insert into user_info (full_name, email, password, address_line_1, address_line_2, postal_code, phone_number) values (\'' +
                        request.form['fullname'] + '\',\'' + request.form['email'] + '\',\'' +
                        request.form['password'] + '\',\'' + request.form['address-1'] + '\',\'' +
                        request.form['address-2'] + '\',\'' + request.form['postal'] + '\',\'' + request.form['phone-number'] + '\')')
            msg = write_db(sql)

            if type(msg) == int:
                register_passed = True
                BUILD_USER = request.form['email']
                render_template('register.html', error=error, register_passed=register_passed)
                # return redirect(url_for('login', f='register'))
            elif 'constraint failed' in msg and 'user_info.email' in msg:
                error = 'An existing account is associated with the email provided. If you have forgotten your password, please recover your password.'
            else:
                error = 'An unknown error has occured, please contact the site admin.'
        else:
            # set security questions, give option to skip for now
            sql = ('update user_info set security_question_1 =\'' + request.form['security1'] + '\', security_answer_1 =\'' + 
                    request.form['security_answer_1'] + '\', security_question_2 =\'' + request.form['security2'] + '\', security_answer_2 =\'' +
                    request.form['security_answer_2'] + '\', security_question_3 =\'' + request.form['security3'] + '\', security_answer_3 =\'' + request.form['security_answer_3'] + '\' where email=\'' + BUILD_USER + '\'')
            msg = write_db(sql)
            BUILD_USER = ""
            if type(msg) == int:
                return redirect(url_for('login', f='register'))

    return render_template('register.html', title='CYPRESS- Register', error = error, register_passed=register_passed)


@app.route('/logout')
def logout():
    #insert modal to confirm logout
	session.pop('user', None)
	return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET','POST'])
def forgot_password():
    error = ''
    question = ""
    wrong_ans = ""
    found_email = False
    success = False
    global RECOVERY_ANS
    global PASS_RECOVERY
    global RECOVERY_QUESTION
    # pick a question to ask the user for authentication
    # assuming that the user has chosen and answered 3 security questions after registration
    choose_1 = random.randint(1,3)
    question_number = "security_question_" + str(choose_1)
    answer_number = "security_answer_" + str(choose_1)

    if request.method == 'POST':
        if 'email' in request.form:
            sql_q = 'select ' + question_number + ' from user_info where email=\'' + request.form['email'] + '\''
            sql_a = 'select ' + answer_number + ' from user_info where email=\'' + request.form['email'] + '\''
            try:
                user_security_q = query_db(sql_q)[0]
                user_security_a = query_db(sql_a)[0]
                RECOVERY_QUESTION = SECURITY_QUESTIONS[int(user_security_q[0]-1)]
                RECOVERY_ANS = user_security_a[0]
                PASS_RECOVERY = query_db('select password from user_info where email=\'' + request.form['email'] + '\'')[0][0]
                found_email = True
            except IndexError:
                error = 'The email provided is not associated with a CYPRESS account! Please try again.'
                return render_template('forgot_password.html', error=error, question=RECOVERY_QUESTION, found=found_email, success=success, wrong_ans=wrong_ans)

        else:
            if request.form['security_a'].lower() == RECOVERY_ANS.lower():
                # USER SUCCESSFULLY AUTHENTICATED SECURITY QUESTION!
                # PROCEED TO EMAIL THEM THEIR PASSWORD
                # <------------here----------->

                # <-----------to here--------->
                success = True
                RECOVERY_QUESTION = ""
                RECOVERY_ANS = ''
                PASS_RECOVERY = ''
            else:
                wrong_ans = 'Incorrect security answer, please try again.'
                found_email = True
                return render_template('forgot_password.html', error=error, question=RECOVERY_QUESTION, found=found_email, success=success, wrong_ans=wrong_ans)



    return render_template('forgot_password.html', title='CYPRESS- Forgot Password', error=error, question=RECOVERY_QUESTION, found=found_email, success=success, wrong_ans=wrong_ans)

@app.route('/home')
def home():
    if len(session) == 0:
        return render_template('login.html', error=error)

    return render_template('home.html')

@app.route('/create_report', methods=['GET', 'POST'])
def create_report():
    if request.method == "POST":
        # write new report to db
        # note: long_lat holds coordinates
        if request.json['additional'] == '':
            sql = ('insert into reports (long_lat, address, type_problem, report_author) values (\'' + request.json['loc'] + '\',\'' + request.json['address'] +
                    '\', \'' + request.json['issues'] + '\',\'' + session['user']['email'] + '\')')
        else:
            sql = ('insert into reports (long_lat, address, type_problem, additional_details, report_author) values (\'' + request.json['loc'] + '\',\'' + request.json['address'] +
                    '\', \'' + request.json['issues'] + '\',\'' + request.json['additional'] + '\',\'' + session['user']['email'] + '\')')
        # create new report
        print(sql)
        write_db(sql)
        # send confirmation
    return render_template('create_report.html')

@app.route('/edit_report', methods=['GET', 'POST'])
def edit_report():
    if request.method == 'POST':
        return redirect("/edit_report_details?id=" + request.form['select_report'])
    else:
        # get list of reports made by the session user
        sql = ('select id, address, type_problem, additional_details, suggested_action, status, solution from reports where report_author =\'' + session['user']['email'] + '\'')
        user_reports = query_db(sql)

        return render_template('edit_report.html', user_reports=user_reports)

@app.route('/edit_report_details', methods=['GET', 'POST'])
def edit_report_details():
    report_id = request.args.get('id')

    if request.method == 'POST':
        if 'add_suggestion' in request.form and request.form['add_suggestion'] != '':
            sql = ('select suggested_action from reports where id=\'' + report_id + '\'')
            suggestion_string = query_db(sql)[0][0]
            if suggestion_string is None or suggestion_string == '':
                suggestion_string = session['user']['fullname'] + ": " + request.form['add_suggestion']
            else:
                suggestion_string = suggestion_string + "," + session['user']['fullname'] + ": " + request.form['add_suggestion']
            sql = ('update reports set address=\'' + request.form['address'] + '\', type_problem=\'' + request.form['issue_type'] + '\', additional_details=\'' + request.form['additional'] + 
                    '\', suggested_action=\'' + suggestion_string + '\' where id =\'' + report_id + '\'')
        else:
            sql = ('update reports set address=\'' + request.form['address'] + '\', type_problem=\'' + request.form['issue_type'] + '\', additional_details=\'' + request.form['additional'] + 
                    '\' where id =\'' + report_id + '\'')
        write_db(sql)

    sql = ('select * from reports where id =\'' + report_id + '\'')
    selected_report = query_db(sql)[0]
    if selected_report[5] is not None:
        hold = selected_report[5].rstrip().split(',')
    else:
        hold = []

    return render_template('edit_report_details.html', selected_report=selected_report, hold_suggest=hold)

@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    if request.method == 'POST':
        return redirect("/edit_suggestions?id=" + request.form['select_report'])
    else:
        sql = ("select id, address, type_problem, additional_details, suggested_action from reports where status = 'inc'")
        open_reports = query_db(sql)
        return render_template('suggestions.html', open_reports=open_reports)

@app.route('/edit_suggestions', methods=['GET', 'POST'])
def edit_suggestions():
    report_id = request.args.get('id')

    if request.method == 'POST':
        sql = ('select suggested_action from reports where id=\'' + report_id + '\'')
        suggestion_string = query_db(sql)[0][0]
        if (suggestion_string is None) or (suggestion_string == ''):
            suggestion_string = session['user']['fullname'] + ": " + request.form['add_suggestion']
        else:
            suggestion_string = suggestion_string + "," + session['user']['fullname'] + ": " + request.form['add_suggestion']
        sql = ('update reports set suggested_action=\'' + suggestion_string + '\' where id =\'' + report_id + '\'')
        print(sql)
        write_db(sql)
        return render_template('suggestions.html')
    sql = ('select * from reports where id =\'' + report_id + '\'')
    selected_report = query_db(sql)[0]
    if selected_report[5] is not None:
        hold = selected_report[5].rstrip().split(',')
    else:
        hold = []

    return render_template('edit_suggestions.html', selected_report=selected_report, hold_suggest=hold)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/user_settings')
def user_settings():
    return render_template('user_settings.html')

@app.route('/tell_a_friend')
def tell_a_friend():
    return render_template('tell_a_friend.html')

# For Reference ONLY
@app.route('/grades', methods=['GET', 'POST', 'DEL'])
def grades():
    #pull the entire grades table
    student_grades = query_db('select * from grades')
    evals = [ eval[0] for eval in query_db('select distinct eval from grades') ]
    #show a different set of information if the user is an instructor
    if session['user']['type'] == 'Ins':
        remark_check = 'There are no remark requests at this moment.'
        get_remarks = query_db('select distinct * from remark')
        delete_msg = ''
        if get_remarks != None:
            remark_check = ''

        if request.method == 'POST' and request.form['remark'] == 'no':
            if request.form['eval-name'] in evals and request.form['username'] in [ entry[0] for entry in student_grades ]:
                sql = ('update grades set grade=\'' + request.form['grade'] + '\'' ' where username=\'' +
                    request.form['username'] + '\' and eval=\'' + request.form['eval-name'] + '\'')
            else:
                sql = ('insert into grades values (\'' +
                    request.form['username'] + '\',\'' + request.form['eval-name'] + '\',\'' +
                    request.form['grade'] + '\')')

            msg = write_db(sql)
            if type(msg) == int:
                return redirect(url_for('grades'))
            elif 'constraint failed' in msg:
                ins_err = 'Entry already exists!'
                return render_template('grades_instructor.html', student_grades = student_grades, evals = evals, remark_check = remark_check, get_remarks = get_remarks, ins_err=ins_err)
        elif request.method == 'POST' and request.form['remark'] == 'yes':
            sql = ('delete from remark where username=\'' +
                    request.form['username'] + '\' and eval=\'' + request.form['eval-name'] + '\' and reason=\'' +
                    request.form['reason'] + '\'')
            
            msg = write_db(sql)
            return redirect(url_for('grades'))

        return render_template('grades_instructor.html', student_grades = student_grades, evals = evals, remark_check = remark_check, get_remarks = get_remarks, ins_err='')
        
    #set of information for students
    else:
        send_message = ''
        table_builder = []
        for grade_entry in student_grades:
            if grade_entry[0] == session['user']['username']:
                table_builder.append(grade_entry)

        #remark submission
        if request.method == 'POST':
            sql = ('insert into remark values (\'' +
                    session['user']['username'] + '\',\'' + request.form['eval'] + '\',\'' + request.form['remark_request'] + '\')')
            msg = write_db(sql)
            app.logger.info(msg)
            send_message = 'Thank you for your request.'

        return render_template('grades.html', table_builder = table_builder, send_message = send_message)

'''
@app.route('/resources')
def res():
    return render_template('resources.html', title='Resources')

q_map = {1: 'What do you like about the instructor teaching?',
         2: 'What do you recommend the instructor to do to improve their teaching?',
         3: 'What do you like about the labs?',
         4: 'What do you recommend the lab instructors to do to improve their lab teaching?'}

@app.route('/feedback', methods=['GET','POST'])
def feedback():
    title = 'Feedback'
    ins_list = query_db('select username, firstname, lastname from user_info where user_type = \'Ins\'')

    if request.method == 'POST': #will only be used for students
        feedback_id = query_db('select max(feedback_id) from feedback')[0][0]

        ans_list = []
        for key in request.form:
            if key != 'ins' and request.form[key] != '':
                ans_list.append((request.form['ins'], feedback_id + 1, int(key), request.form[key]))

        write_db_many('insert into feedback values(?,?,?,?)', ans_list)

        return render_template('feedback.html', title=title, ins_list=ins_list, q_map=q_map, submitted=1)
    if session['user']['type'] == 'Ins':
        fb_list = query_db('select q_num, response from feedback where username=\'' + session['user']['username'] + '\'')
        fb_mapped = {}
        for entry in fb_list:
            if entry[0] in fb_mapped.keys():
                fb_mapped[entry[0]].append(entry[1])
            else:
                fb_mapped[entry[0]] = [entry[1]]

        return render_template('view_feedback.html', title=title, q_map=q_map, fb_list=fb_mapped)
    else:
        return render_template('feedback.html', title=title, ins_list=ins_list, q_map=q_map)
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') #allow for external devices to access