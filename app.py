
from flask import Flask, render_template, request, redirect, url_for, session,flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# # Initialize data
# accounts = pd.DataFrame([],columns=['Adhar_Number', 'Data_of_Birth','Full_Name','Age','Email','TimeStamp'])
# accounts.to_csv('accounts.csv',index=False,header=True)

# transaction = pd.DataFrame([],columns = ['Adhar_Number', 'transaction_Type', 'Amount' ,'Timestamp'])
# transaction.to_csv('transaction.csv',header=True, index=False)

# balance= pd.DataFrame([], columns=['Adhar_Number', 'Amount','TimeStamp'])
# balance.to_csv('balance.csv',header=True, index=False)

# withdrawal = pd.DataFrame([], columns=['Adhar_Number', 'Amount','TimeStamp'])
# withdrawal.to_csv('withdrawal.csv',header=True,index=False)
try:
    accounts = pd.read_csv('accounts.csv')
    transactions = pd.read_csv('transactions.csv')
except FileNotFoundError:
    accounts = pd.DataFrame(columns=['Account_Number', 'Data_Of_Birth', 'Full_Name', 'Age','Email', 'password', 'balance','Timestamp'])
    transactions = pd.DataFrame(columns=['Account_Number', 'type', 'amount', 'timestamp'])



# Helper functions
def create_account(account_number,date_of_birth,full_name,age, email,password):
    global accounts
    if account_number not in accounts['Account_Number'].values:
        #accounts = accounts.append({'Account_Number': Account_Number, 'password': password, 'balance': 0}, ignore_index=True)
        accounts.loc[len(accounts)] = [account_number,date_of_birth,full_name,age, email,password, 0,pd.Timestamp.now()]
        accounts.to_csv('accounts.csv',index=False,header= True)
        return True
    return False

def get_user(account_number):
    global accounts
    accounts = pd.read_csv('accounts.csv')
    password = list(accounts.loc[accounts['Account_Number'] == account_number]['password'])[0]
    name = list(accounts.loc[accounts['Account_Number'] == account_number]['Full_Name'])[0]
    
    return password,name
    # return accounts[accounts['Account_Number'] == account_number].iloc[0]

def update_balance(account_number, amount, type):
    global accounts, transactions
    accounts = pd.read_csv('accounts.csv')
    transactions = pd.read_csv('transactions.csv')
    accounts.loc[accounts['Account_Number'] == account_number, 'balance'] += amount
    accounts.to_csv('accounts.csv',index=False,header= True)
    transactions.loc[len(transactions.index)] = [account_number,type,amount,pd.Timestamp.now()]
    transactions.to_csv('transactions.csv',index=False,header=True)
    # transactions = transactions.append({'Account_Number': account_number, 'type': type, 'amount': amount, 'timestamp': pd.Timestamp.now()}, ignore_index=True)

def get_balance(account_number):
    global accounts
    accounts = pd.read_csv('accounts.csv')
    balance = list(accounts.loc[accounts['Account_Number'] == account_number]['balance'])[0]
    print(balance)
    return balance

def get_transactions(account_number, limit=15):
    global transactions
    return transactions[transactions['Account_Number'] == account_number].tail(limit)




# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_number = int(request.form['accountnumber'])
        password = request.form['password']
        user,name = get_user(account_number)
        
        if str(user) == password:
            session['account_number'] = account_number
            session['name'] = name
            
            return redirect(url_for('account'))
        else:
            return "Please check your login credentials"
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        account_dict = request.form.to_dict()
        account_number= int(account_dict['AccountNumber'])
        date_of_birth = account_dict['DataofBirth']
        full_name = account_dict['FullName']
        age = account_dict['Age']
        email = account_dict['Email']
        password = account_dict['password']
        account = [account_number,date_of_birth,full_name,age, email,password]
        if create_account(account_number,date_of_birth,full_name,age, email,password):
            session['account_number'] = account_number
            return redirect(url_for('account'))
    else:
        flash('Please check your detials',"danger")
        return render_template('register.html')


@app.route('/account')

def account():
    if 'account_number' not in session:
        return redirect(url_for('login'))
    return render_template('account.html')

@app.route('/balance')
def balance():
    if 'account_number' not in session:
        return redirect(url_for('login'))
    balance = get_balance(session['account_number'])
    return f"Your current balance is: {balance}"
        


@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if 'account_number' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = float(request.form['amount'])
        update_balance(session['account_number'], amount, 'deposit')
        return redirect(url_for('balance'))
    return render_template('deposit.html')


@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'account_number' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = float(request.form['amount'])
        update_balance(session['account_number'], -amount, 'withdraw')
        return redirect(url_for('balance'))
    return render_template('withdraw.html')

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'account_number' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        receiver = int(request.form['receiver'])
        amount = int(request.form['amount'])
        
        if receiver in accounts['Account_Number'].values:
            update_balance(session['account_number'], -amount, 'transfer')
            update_balance(receiver, amount, 'transfer')
            return redirect(url_for('balance'))
    return render_template('transfer.html')

@app.route('/mini_statement')
def mini_statement():
    if 'account_number' not in session:
        return redirect(url_for('login'))
    transactions = get_transactions(session['account_number'])
    return transactions.to_html()

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5003,debug=True)
