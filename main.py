from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Alldata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Items = db.Column(db.String(100), unique=False)
    Prices = db.Column(db.Integer, unique=False)
    Total = db.Column(db.Integer, unique=False,default=0)
    def __repr__(self):
        return f'{self.Items} - {self.Prices}'


@app.route('/',methods=["GET","POST"])
def home():
    if request.method == "POST":
        item = request.form.get('item')
        price = request.form.get('price')
        if not item or not price:
            return redirect('/') 
        data = Alldata(Items=item, Prices=price)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('home'))
    
    # Query all data and calculate total price
    maindata = Alldata.query.all()
    total_price = sum([data.Prices for data in maindata])  # Summing the prices
    
    return render_template('index.html', maindata=maindata, total_price=total_price)


@app.route('/delete/<int:id>')
def delete(id):
    data = Alldata.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)