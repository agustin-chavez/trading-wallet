# Trading Wallet - Investment Portfolio Manager

Trading Wallet is a web application developed in Python using the Flask framework and a SQLite3 database to manage user profiles and investment portfolios.
Minimalist UI developed with PicoCSS.

![Trading Wallet Diagram](trading-wallet-diagram.svg)


https://trading-wallet-production.up.railway.app/

### Run

```bash
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

export DEBUG="True"
export SQLALCHEMY_DATABASE_URI="sqlite:///trading-wallet.db"
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(16))")

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
- See all the stocks available in the market (integration with Yahoo Finance API)
- Buy stocks and sell your holdings
- Historical of transactions


<img width="1430" alt="home" src="https://github.com/agustin-chavez/trading-wallet/assets/39955956/324fb235-b815-4ef4-83f3-e762325d5436">

![regi](https://github.com/agustin-chavez/trading-wallet/assets/39955956/1a41cd28-0789-442c-ac65-c7027d08d0ab)

<img width="1430" alt="login" src="https://github.com/agustin-chavez/trading-wallet/assets/39955956/07ebca51-d66e-4cc4-ad0c-079ea7cd89cc">

<img width="1430" alt="account-error" src="https://github.com/agustin-chavez/trading-wallet/assets/39955956/7f78760a-fb63-4dc1-b0b2-1ea05c07e347">

<img width="1430" alt="account-success" src="https://github.com/agustin-chavez/trading-wallet/assets/39955956/1875e3fe-169b-40ec-ac1a-ee232b30e062">

<img width="1430" alt="market" src="https://github.com/agustin-chavez/trading-wallet/assets/39955956/970bd780-5f20-484e-a891-a138fba65921">

<img width="1430" alt="buy-error" src="https://github.com/agustin-chavez/trading-wallet/assets/39955956/d3ea94b9-3ae0-4bd2-b695-8c4cb1b401bb">

<img width="1430" alt="buy-success" src="https://github.com/agustin-chavez/trading-wallet/assets/39955956/519c51bb-1004-4ca4-a8e5-e807a0b3651c">

![trs](https://github.com/agustin-chavez/trading-wallet/assets/39955956/fd8e34b0-18ec-4cbb-89d5-1729e468e955)



## License

This project is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0). See the LICENSE file for more details.


