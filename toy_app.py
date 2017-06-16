from flask import Flask, Response, render_template, request
import requests
app = Flask(__name__)

# Set your apps client id and client secret here
CLIENT_ID = "CLIENT_ID_HERE"
CLIENT_SECRET = "CLIENT_SECRET_HERE"
API_URL = "API_URL_HERE"
HEADERS = {'X-IBM-Client-Secret': CLIENT_SECRET, 'X-IBM-Client-Id': CLIENT_ID}

MISSING_TOKEN_MSG = 'Access token is missing!'
INFO_TOKEN_MSG = 'Type in your access token and click send!'


def check_status(r):
    """
    Helper function to check the request status.
    We consider everything except 200 and 201 as an error in this example.
    """
    code = r.status_code

    error = None
    if code not in [200, 201]:
        error = True

    return error


@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
    """
    Accounts endpoint.
    This endpoint gets the list of accounts from the API.
    """
    url = "{}/accounts".format(API_URL)
    title = 'Accounts endpoint for account listing.'
    if request.method == 'POST':
        access_token = request.form.get('access_token')
        if not access_token:
            return render_template('accounts_template.html', warning=MISSING_TOKEN_MSG, title=title)
        else:
            HEADERS['Authorization'] = "Bearer {}".format(str(access_token))
            r = requests.get(url, headers=HEADERS)
            error = check_status(r)
            return render_template('accounts_template.html', response=r.json(), title=title, error=error)

    else:
        return render_template('accounts_template.html', info=INFO_TOKEN_MSG, title=title)


@app.route('/account/<account_id>', methods=['GET', 'POST'])
def account(account_id):
    """
    Account details endpoint.
    This endpoint gets the account details. from the given account_id.
    """
    url = "{}/accounts/{}".format(API_URL, account_id)
    title = 'Account enpoint for specific account information.'
    if request.method == 'POST':
        access_token = request.form.get('access_token')
        if not access_token:
            return render_template('account_template.html', warning=MISSING_TOKEN_MSG, title=title, account_id=account_id)
        else:
            HEADERS['Authorization'] = "Bearer {}".format(str(access_token))
            r = requests.get(url, headers=HEADERS)
            error = check_status(r)
            return render_template('account_template.html', response=r.json(), title=title, error=error, account_id=account_id)

    else:
        return render_template('account_template.html', info=INFO_TOKEN_MSG, title=title, account_id=account_id)


@app.route('/transactions/<account_id>', methods=['GET', 'POST'])
def transactions(account_id):
    """
    Transactions endpoint.
    This endpoint gets the list of transactions from given account_id.
    """
    url = "{}/accounts/{}/transactions".format(API_URL, account_id)
    title = 'Transactions endpoint for transaction listing.'
    if request.method == 'POST':
        access_token = request.form.get('access_token')
        if not access_token:
            return render_template('transactions_template.html', warning=MISSING_TOKEN_MSG, title=title, account_id=account_id)
        else:
            HEADERS['Authorization'] = "Bearer {}".format(str(access_token))
            r = requests.get(url, headers=HEADERS)
            error = check_status(r)
            return render_template('transactions_template.html', response=r.json(), title=title, error=error, account_id=account_id)

    else:
        return render_template('transactions_template.html', info=INFO_TOKEN_MSG, title=title, account_id=account_id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
