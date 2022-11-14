from dotenv import load_dotenv
import sqlite3
from werkzeug.exceptions import abort
from flask import Flask, request, render_template, url_for, flash, redirect
import os
import sys
sys.path.append('.')
sys.path.append('..')
sys.path.insert(1, '/scripts/')
from scripts.transaction_helpers import get_balance, make_transaction
import scripts.defaults as defs
load_dotenv()

wallet_1 = os.getenv('my_address_w1')
flask_secret_key = os.getenv('flask_secret_key')

app = Flask(__name__)
app.secret_key = flask_secret_key


# region index related
"""
def get_db_connection():
    # A function to create a sqlite db connection
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/index')
def index():
    #The main index page
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)
"""
# endregion


# region certificates related endpoints
@app.route('/certificates')
def certificates():
    """
    The main certificates page
    """
    return render_template('certificates.html')
# endregion


# region opt in related endpoints
@app.route('/optin')
def optin():
    """
    The main opt in page
    """
    return render_template('optin.html')
# endregion


# region wallet related endpoints
@app.route('/wallets', methods=['GET'])
def wallets():
    """
    The main wallets page
    """
    return render_template('wallets.html')


@app.route('/wallets/connect_to_wallets', methods=['GET'])
def connect_to_wallets():
    """
    The wallet connection creator
    """
    return render_template('wallets.html')
# endregion


# region Transaction related endpoints
@app.route('/transactions', methods=['GET'])
def transactions():
    """
    The main transactions page
    """
    account_balance = 0
    return render_template('transactions.html', balance=account_balance)


@app.route('/transactions/display_records', methods=['GET'])
def display_records():
    """
    The display records endpoint
    """
    account_balance = 0
    return render_template('transactions.html', balance=account_balance)


@app.route('/transactions/display_balance', methods=['GET', 'POST'])
def display_balance():
    """
    The display balance endpoint
    """
    account_balance = 0
    if request.method == "POST":
        print('In post')
        account = request.form.get("accountAddress")
        if not account:
            flash('Account address is required')
            return render_template('transactions.html',
                                   balance=account_balance)
        else:
            print(f"loading the balance of the account: '{account}'")
            # calling the get_balance function to get the balance of the given
            # account
            account_balance = get_balance(account)
            print(f"displaying the balance of the account: '{account}'")
            return render_template('transactions.html',
                                   balance=account_balance)
    print('In get')
    return render_template('transactions.html', balance=account_balance)


@app.route('/transactions/commit_transaction', methods=['GET', 'POST'])
def commit_transaction():
    """
    The make transactions endpoint
    """
    if request.method == "POST":
        print('In post')
        sender_address = request.form.get('fromAddress')
        receiver_address = request.form.get('toAddress')
        algo_amount = request.form.get('algo-amount')
        algo_amount = int(algo_amount)
        if not sender_address:
            flash('Sender account address is required')
            return render_template('transactions.html', balance=0)
        if not receiver_address:
            flash('Receiver account address is required')
            return render_template('transactions.html', balance=0)
        if not algo_amount:
            flash('Algo amount to send is required')
            return render_template('transactions.html', balance=0)

        print(f'sender address: {sender_address}\nreceiver address: '
              f'{receiver_address}\nalgo amount: {algo_amount}')
        pk = os.getenv('base_test_private_key')
        sent = make_transaction(pk, sender_address, receiver_address,
                                algo_amount)
        if sent:
            flash('Transaction successfully committed to the Algorand '
                  + 'blockchain')
            return render_template('transactions.html', balance=0)
        else:
            flash('Transaction failed, see log for more details')
            return render_template('transactions.html', balance=0)
# endregion


if __name__ == '__main__':
    app.debug = True
    app.run()
