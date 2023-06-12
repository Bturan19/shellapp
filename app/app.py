from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from modules import data_processing, model
import os
import pandas as pd
from flask_table import Table, Col

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#UPLOAD_FOLDER = './uploads/'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

users = {'user1': {'password': 'password1'}, 'user2': {'password': 'password2'}}

class User(UserMixin):
  pass

@login_manager.user_loader
def user_loader(username):
  if username not in users:
    return
  user = User()
  user.id = username
  return user

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  username = request.form['username']
  password = request.form['password']
  if (username in users) and (password == users[username]['password']):
    user = User()
    user.id = username
    login_user(user)
    return redirect(url_for('home'))
  return 'Bad login'

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return 'Logged out'

# Define your table
class ItemTable(Table):
    classes = ['table', 'table-striped', 'table-hover']
    date = Col('Date')
    predicted_mean = Col('Predicted Mean')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
  if request.method == 'POST':
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    df_orig = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    train_new_model = 'train_new_model' in request.form
    
    if data_processing.check_data(df_orig):
      df = data_processing.process_data(df_orig)

      predictions = model.predict(df, train_new_model)

      # Convert datetime to string
      df_orig = df_orig.reset_index(drop=True)
      df_orig.set_index('Date', inplace=True)
      original_data = df_orig['Net Cashflow from Operations']
      original_data.index = original_data.index.strftime('%Y-%m-%d')
      original_data = original_data.to_dict()

      predictions.index = predictions.index.strftime('%Y-%m-%d')
      predictions *= 10000000
      print(predictions)
      
      # Create table with first and last five rows
      #items = predictions.iloc[list(range(5)) + list(range(-5, 0))].reset_index().to_dict(orient='records')
      items = predictions.reset_index().rename(columns={'index': 'date'}).iloc[list(range(5)) + list(range(-5, 0))].to_dict(orient='records')
      table = ItemTable(items)

      # Calculate summary statistics
      summary = predictions.describe()
      
      predictions = predictions.to_dict()

      return render_template('results.html', original_data=original_data, predictions=predictions, table=table, summary=summary)
    else:
      flash('Uploaded file format is not ok.')
      print("No good")
  return render_template('upload.html')




if __name__ == "__main__":
  #app.run(debug=True, host='0.0.0.0')
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
