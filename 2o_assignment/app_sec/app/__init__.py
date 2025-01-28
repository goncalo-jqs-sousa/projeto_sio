import os, stripe, json, hashlib, requests
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_bootstrap import Bootstrap
from .forms import LoginForm, RegisterForm, ChangePassForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from .db_models import db, User, Item
from itsdangerous import URLSafeTimedSerializer
from .funcs import mail, send_confirmation_email, fulfill_order
from dotenv import load_dotenv
from .admin.routes import admin
from zxcvbn import zxcvbn


load_dotenv()
app = Flask(__name__)
app.register_blueprint(admin)

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', "somesecretvalue") #os.environ["SECRET_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db" #os.environ["DB_URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_USERNAME'] = os.getenv('EMAIL', "") #os.environ["EMAIL"]
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD', 0) #os.environ["PASSWORD"]
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PORT'] = 587
##stripe.api_key =                  # Aplicar uma devida key para testar 


Bootstrap(app)
db.init_app(app)
mail.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@app.context_processor
def inject_now():
    """ sends datetime to templates as 'now' """
    return {'now': datetime.utcnow()}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def home():
    items = Item.query.all()
    return render_template("home.html", items=items)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user == None:
            flash(f'Email and/or Password incorrect.<br>Try with different credentials or <a href={url_for("register")}>Register now!</a>', "error")
            return redirect(url_for('login'))
        elif check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash(f'Email and/or Password incorrect.<br>Try with different credentials or <a href={url_for("register")}>Register now!</a>', "error")
            return redirect(url_for('login'))
    return render_template("login.html", form=form)

def check_password(password):
    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    hash_prefix = hashed_password[:5]
    hash_suffix = hashed_password[5:]

    url = f'https://api.pwnedpasswords.com/range/{hash_prefix}'
    response = requests.get(url)

    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == hash_suffix:
            return int(count)
        
    return 0

@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(f"User with email {user.email} already exists!!<br> <a href={url_for('login')}>Login now!</a>", "error")
            return redirect(url_for('register'))
        
        password = form.password.data
        password_strength = zxcvbn(password)
        pwned_count = check_password(password)
        
        if pwned_count > 0:
            flash("Password has been compromised in a data breach<br>Use a different password.", "error")
            return redirect(url_for('register'))
        
        if password_strength['score'] < 2:
            flash("Password is too weak<br>Use a moderate or stronger Password", "error")
            return redirect(url_for('register'))

        new_user = User(name=form.name.data,
                    email=form.email.data,
                    password=generate_password_hash(
                                form.password.data,
                                method='pbkdf2:sha256',
                                salt_length=8),
                    phone=form.phone.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Thanks for registering!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/change_pass", methods=['POST', 'GET'])
def change_pass():
    form = ChangePassForm()
    if form.validate_on_submit():		
        user = User.query.get(current_user.id)

        if check_password_hash(user.password, form.cur_password.data):
            password = form.new_password.data
            password_strength = zxcvbn(password)
            pwned_count = check_password(password)

            if pwned_count > 0:
                flash("Password has been compromised in a data breach<br>Use a different new password", "error")
                return redirect(url_for('change_pass'))

            if password_strength['score'] < 2:
                flash("Password is too weak<br>Use a moderate or stronger new Password", "error")
                return redirect(url_for('change_pass'))

            user.password = generate_password_hash(
                form.new_password.data,
                method='pbkdf2:sha256',
                salt_length=8)
            db.session.commit()

            flash('Password changed successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Invalid current password', "error")
            return redirect(url_for('change_pass'))

    return render_template("change_pass.html", form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=email).first()
    if user.email_confirmed:
        flash(f'Account already confirmed. Please login.', 'success')
    else:
        user.email_confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('Email address successfully confirmed!', 'success')
    return redirect(url_for('login'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/data")
@login_required
def data():
    return render_template('data.html')

@app.route("/delete")
@login_required
def delete():
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route("/resend")
@login_required
def resend():
    send_confirmation_email(current_user.email)
    logout_user()
    flash('Confirmation email sent successfully.', 'success')
    return redirect(url_for('login'))

@app.route("/add/<id>", methods=['POST'])
def add_to_cart(id):
    if not current_user.is_authenticated:
        flash(f'You must login first!<br> <a href={url_for("login")}>Login now!</a>', 'error')
        return redirect(url_for('login'))

    item = Item.query.get(id)
    if request.method == "POST":
        quantity = request.form["quantity"]
        current_user.add_to_cart(id, quantity)
        flash(f'''{item.name} successfully added to the <a href=cart>cart</a>''','success')
        return redirect(url_for('home'))

@app.route("/cart")
@login_required
def cart():
    price = 0
    price_ids = []
    items = []
    quantity = []
    for cart in current_user.cart:
        items.append(cart.item)
        quantity.append(cart.quantity)
        price_id_dict = {
            "price": cart.item.price_id,
            "quantity": cart.quantity,
            }
        price_ids.append(price_id_dict)
        price += cart.item.price*cart.quantity
    return render_template('cart.html', items=items, price=price, price_ids=price_ids, quantity=quantity)

@app.route('/orders')
@login_required
def orders():
    return render_template('orders.html', orders=current_user.orders)

@app.route("/remove/<id>/<quantity>")
@login_required
def remove(id, quantity):
    current_user.remove_from_cart(id, quantity)
    return redirect(url_for('cart'))

@app.route('/item/<int:id>')
def item(id):
    item = Item.query.get(id)
    return render_template('item.html', item=item)

@app.route('/search')
def search():
    query = request.args['query']
    search = "%{}%".format(query)
    items = Item.query.filter(Item.name.like(search)).all()
    return render_template('home.html', items=items, search=True, query=query)

# stripe stuffs
@app.route('/payment_success')
def payment_success():
    return render_template('success.html')

@app.route('/payment_failure')
def payment_failure():
    return render_template('failure.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = json.loads(request.form['price_ids'].replace("'", '"'))
    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=current_user.id,
            line_items=data,
            payment_method_types=[
              'card',
            ],
            mode='payment',
            success_url=url_for('payment_success', _external=True),
            cancel_url=url_for('payment_failure', _external=True),
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():

    if request.content_length > 1024*1024:
        print("Request too big!")
        abort(400)

    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    ENDPOINT_SECRET = os.environ.get('ENDPOINT_SECRET')
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return {}, 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return {}, 200

@app.route('/check_password_strength', methods=['POST'])
def check_password_strength():
    data = request.get_json()
    password = data.get('password')

    pwned_count = check_password(password)

    if pwned_count > 0:
        return jsonify({'error': 'Password is breached. Try another one'})
    else:
        return jsonify({'success': 'Password is secure'})