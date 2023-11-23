import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


DATABASEURI = "postgresql://postgres:ZLY0802kk.@35.193.93.151/postgres"


engine = create_engine(DATABASEURI)

#

conn = engine.connect()


conn.execute(text("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);"""))
conn.execute(text("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');"""))


conn.commit() 

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass



@app.route('/')
def index():
    conn = engine.connect()
    result = conn.execute(text("SELECT id, issue, description FROM reports"))
    reports = result.fetchall()
    conn.close()
    print(result)
    return render_template('index.html', reports=reports)

@app.route('/add', methods=['POST'])
def add_report():
    issue = request.form['issue']
    description = request.form['description']
    conn = engine.connect()
    conn.execute(text("INSERT INTO reports (issue, description) VALUES (:issue, :description)"),
                 {'issue': issue, 'description': description})
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:report_id>')
def edit_report(report_id):
    conn = engine.connect()
    result = conn.execute(text("SELECT id, issue, description FROM reports WHERE id = :id"), {'id': report_id})
    report = result.fetchone()
    conn.close()
    return render_template('edit_report.html', report=report)

@app.route('/update/<int:report_id>', methods=['POST'])
def update_report(report_id):
    issue = request.form['issue']
    description = request.form['description']
    conn = engine.connect()
    conn.execute(text("UPDATE reports SET issue = :issue, description = :description WHERE id = :id"),
                 {'issue': issue, 'description': description, 'id': report_id})
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    conn = engine.connect()
    conn.execute(text("DELETE FROM reports WHERE id = :id"), {'id': report_id})
    conn.commit()
    conn.close()
    return redirect('/')



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()