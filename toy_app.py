from flask import Flask, Response, render_template, request
import requests, json, urllib
app = Flask(__name__)

# Set your apps client id and client secret here
CLIENT_ID = "CLIENT_ID_HERE"
CLIENT_SECRET = "CLIENT_SECRET_HERE"
API_URL = 'https://api.nordeaopenbanking.com/v1' # api url in the form https://api.url/v1

MISSING_TOKEN_MSG = 'Access token is missing!'
INFO_TOKEN_MSG = 'Type in your access token and click send!'

# Perform authentication
HEADERS ={}
HEADERS['Content-Type'] = 'application/x-www-form-urlencoded'
REDIRECT_URI = 'https://httpbin.org/anything'
access_url = '/authentication?state=%s&client_id=%s&redirect_uri=%s'
r = requests.get(API_URL + access_url % ('123', CLIENT_ID, urllib.quote(REDIRECT_URI, safe='')), headers=HEADERS)
data = json.loads(r.text)
code = data['args']['code']
HEADERS['X-IBM-Client-Secret'] = CLIENT_SECRET
HEADERS['X-IBM-Client-Id'] = CLIENT_ID
access_url = '/authentication/access_token?code=%s&redirect_uri=%s'
r = requests.post(API_URL + access_url % (code, urllib.quote(REDIRECT_URI, safe='')), headers=HEADERS)
if r.status_code == 200:
    auth_data = json.loads(r.text)
    access_token = auth_data['access_token']
    token_type = auth_data['token_type']
else:
    print 'Auth not successful'
    exit()

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


@app.route('/', methods=['GET'])
def accounts():
    """
    Accounts endpoint.
    This endpoint gets the list of accounts from the API.
    """
    API_URL = 'https://api.nordeaopenbanking.com/v2' # this is freaking ugly
    url = "{}/accounts".format(API_URL)
    title = 'Accounts endpoint for account listing.'
    HEADERS['Authorization'] = "Bearer {}".format(str(access_token))
    r = requests.get(url, headers=HEADERS)
    error = check_status(r)
    return render_template('accounts_template.html', response=r.json(), title=title, error=error)


@app.route('/account/<account_id>', methods=['GET'])
def account(account_id):
    """
    Account details endpoint.
    This endpoint gets the account details. from the given account_id.
    """
    API_URL = 'https://api.nordeaopenbanking.com/v2' # this is freaking ugly
    url = "{}/accounts/{}".format(API_URL, account_id)
    title = 'Account enpoint for specific account information.'
    HEADERS['Authorization'] = "Bearer {}".format(str(access_token))
    r = requests.get(url, headers=HEADERS)
    error = check_status(r)
    return render_template('account_template.html', response=r.json(), title=title, error=error, account_id=account_id)


@app.route('/transactions/<account_id>', methods=['GET'])
def transactions(account_id):
    """
    Transactions endpoint.
    This endpoint gets the list of transactions from given account_id.
    """
    API_URL = 'https://api.nordeaopenbanking.com/v2' # this is freaking ugly
    url = "{}/accounts/{}/transactions".format(API_URL, account_id)
    title = 'Transactions endpoint for transaction listing.'
    HEADERS['Authorization'] = "Bearer {}".format(str(access_token))
    r = requests.get(url, headers=HEADERS)
    error = check_status(r)
    return render_template('transactions_template.html', response=r.json(), title=title, error=error, account_id=account_id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
