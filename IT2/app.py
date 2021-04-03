'''CPS406: Iteration 2/3, CYPRESSv1
Group 49: Ming Zhu Kong, Khushdip Nijjar, Shantanu Singh, Aston Wright

1. Run app.py
2. localhost:5000 in browser to access
'''


#micro web framework in python
from flask import Flask, render_template, session, g, request, redirect, url_for

'''additional modules for database implementation and database password encryption down the line'''
# from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'cps406'.encode('utf-8')

### For Implementation with SQL database down the line ###

# the database file (TBA later)
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
        sql = 'select full_name, email, password from user_info where email=\'' + request.form['email'] + '\''
        try:
            user = query_db(sql)[0]
        except IndexError:
            error = 'Account does not exist! Please try again.'
            return render_template('login.html', error=error)

        if (user[1] == request.form['email']) and (user[2] == request.form['password']):
            session['user'] = {'email': request.form['email'], 'fullname': user[0]}
            return render_template('home.html', error=error)
        else:
            error = 'Incorrect email or password, please try again.'
    elif 'user' in session:
        return render_template('home.html', error=error)
    elif len(request.args) > 0 and request.args.get('f') == 'register':
        confirmation = 'Account created successfully! Please log in to access CYPRESS.'

    return render_template('login.html', error=error, confirmation=confirmation)

    #missing: error counter (3 failed login attempts) + ban timer (1hr) 

#WIP REGISTER (For new users only, no distinction between user and admin accounts for now.)
# NO password encryption
@app.route('/register', methods=['GET','POST'])
def register():
    error = ''
    if request.method == 'POST':
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
            return redirect(url_for('login', f='register'))
        elif 'constraint failed' in msg and 'user_info.email' in msg:
            error = 'An existing account is associated with the email provided. If you have forgotten your password, please recover your password.'
        else:
            error = 'An unknown error has occured, please contact the site admin.'
    
    return render_template('register.html', title='CYPRESS- Register', error = error)

@app.route('/logout')
def logout():
    #insert modal to confirm logout
	session.pop('user', None)
	return redirect(url_for('login'))

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html', title='CYPRESS- Forgot Password')

@app.route('/home')
def home():
    if len(session) == 0:
        return render_template('login.html', error=error)

    return render_template('home.html')

@app.route('/create_report')
def create_report():
    return render_template('create_report.html', title = 'CYPRESS- Create a Report')

@app.route('/edit_report')
def edit_report():
    return render_template('edit_report.html', title='CYPRESS- Edit Reports')

@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html', title='CYPRESS- Suggest Solutions')

@app.route('/faq')
def faq():
    return render_template('faq.html', title='CYPRESS- FAQ')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html', title='CYPRESS- Contact Us')

@app.route('/user_settings')
def user_settings():
    return render_template('user_settings.html', title='CYPRESS- User Settings')

@app.route('/tell_a_friend')
def tell_a_friend():
    return render_template('tell_a_friend.html',title='CYPRESS- Tell a Friend!')

# WIP For Tables
'''@app.route('/grades', methods=['GET', 'POST', 'DEL'])
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