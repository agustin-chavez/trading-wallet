# Trading Wallet - Investment Portfolio Manager

Trading Wallet is a web application developed in Python using the Flask framework and a SQLite3 database to manage user profiles and investment portfolios. 

### Run

```bash
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

export DEBUG="True"
export SQLALCHEMY_DATABASE_URI="sqlite:///site.db"
export SECRET_KEY="<SECRET_KEY_FOR_SESSIONS_SECURITY>"
export EMAIL_USER="<EMAIL_FOR_RESET_PASSWORD_SIMULATION>"
export EMAIL_PASS="<PASS_FOR_RESET_PASSWORD_SIMULATION>"

python run.py
```

Go to http://127.0.0.1:5000/

## How to generate a secret with the python interpreter

```python
import secrets

secrets.token_hex(16)
```

## Features

- Register, login and logout
- Flash messages
- Form validations
- Encrypted passwords
- See and update account username, email, password and profile picture
- 

### Database
<img width="708" alt="database-trading-wallet" src="https://github.com/agustin-chavez/trading-wallet/assets/39955956/baa710e1-977b-434a-a0d2-d9e00c2e30ec">


## License

This project is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0). See the LICENSE file for more details.


