from flask import Flask, request, render_template, redirect, url_for, jsonify, Response, flash, session
import sqlite3


app = Flask(__name__)
app.secret_key = 'myfukinsecretkey'
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/pru', methods=['POST', 'GET'])
def pru():
  if request.method == 'POST':
        hola = 'si funciona'
        User = request.form.get('firstname')
        print(User, request)
  return render_template('indexlogin.html')
  
@app.route('/login', methods=['POST', 'GET'])
def login():
    # handle the POST request
    if request.method == 'POST':
        hola = 'si funciona'
        print(hola, request)
      
        User = request.form.get('user')
        password = request.form.get('contraseña')
        
        con = sqlite3.connect("example.db")
        cur = con.cursor()
          
        cur.execute("select * from UserIds")
        
        users = cur.fetchall()
        
        for rew in users:
            el_usuario = rew[0]
        
        if not el_usuario == User:
        
          cur.execute("select * from UserIds")
          
          cur.execute(f"INSERT INTO UserIds VALUES ('{User}', '{password}')")
          con.commit()
          
          flash('usuario agregado :)')
          
          
          return render_template('login.html', usuarios = users)
        
    # otherwise handle the GET request
    return render_template('login.html')

@app.route('/logout')
def logout():
  session['username'] = None
  return redirect(url_for('index'))


@app.route('/regist')
def regist():
    return render_template('regist.html')

@app.route('/app', methods=['GET','POST'])
def app1():
    
    # handle the POST request
    if request.method == 'POST':
        
        User = request.form.get('user')
        password = request.form.get('contraseña')
        
        try:     
            
            con = sqlite3.connect("example.db")
            cur = con.cursor()
      
            cur.execute(f"SELECT * FROM UserIds WHERE usuarios='{User}'")
            
            
            
            for rew in cur.fetchall():
                Usuario = rew[0]
                contraseña = rew[1]
            
            
            
            if Usuario == User and  contraseña == password:
              session['username'] = User
              
              flash(f'bienbenido {User} :)')
              
              con = sqlite3.connect("example.db")
              cur = con.cursor()
      
              user2 = cur.fetchall()
              
              con.close()
              
              return render_template('base.html', usuarios = user2 )
            else:
              sesion_error = render_template('sesion_error.html')
              return Response(sesion_error, status= 403 )
        except:
          message = '<h1>Usuario o contraseña incorrecta </h1>'
          return Response(message, status= 403 )
    
    try: 
         
         if session['username']:

           User = session['username']
           
           con = sqlite3.connect("example.db")
           cur = con.cursor()
          
           cur.execute("select * from UserIds")
       
           flash(f'bienbenido {User} :)')
          
           users = cur.fetchall()
           
           return render_template('base.html', usuarios = users)
    except:
         #return print('Error :v')
      return  redirect(url_for('login')) 
      
      #return re
      #return Response(re, status = 403)


@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/list')
def list():
   con = sqlite3.connect("example.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from UserIds")
   
   rows = cur.fetchall();
   return render_template("list_2.html",rows = rows)

       
@app.route('/json', methods=['POST'])
def json():
    request_data = request.get_json()

    language = None
    framework = None
    python_version = None
    example = None
    boolean_test = None

    if request_data:
        if 'language' in request_data:
            language = request_data['language']

        if 'framework' in request_data:
            framework = request_data['framework']

        if 'version_info' in request_data:
            if 'python' in request_data['version_info']:
                python_version = request_data['version_info']['python']

        if 'examples' in request_data:
            if (type(request_data['examples']) == list) and (len(request_data['examples']) > 0):
                example = request_data['examples'][0]

        if 'boolean_test' in request_data:
            boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)

@app.route('/query-example')
def query_example():
    language = request.args.get('language')

    framework = request.args['framework']

    return '''   
              <h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              '''.format(language, framework)

@app.errorhandler(404)
def not_found(error=None):
  error_page = render_template('Error.html')
  return Response(error_page, status = 404)
  
    
if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(threaded=True, debug=True,port=5000)