# Trading Wallet - Investment Portfolio Manager

Trading Wallet is a web application developed in Python using the Flask framework and an SQLite3 database to manage user profiles and investment portfolios. The application allows users to register, log in, log out, view their profile, and manage their investment portfolio.

## Features

- Authentication / Authorization
- Account / Profile
- Night mode
- Internationalization

## Set Up

### Prerequisites
- [Docker](https://www.docker.com/) installed on your machine.

### Run

  ```bash
  git clone https://github.com/tu-usuario/trading-wallet.git
  cd trading-wallet
  docker-compose up
  ```

The Flask application will be accessible at [http://localhost:5001/](http://localhost:5001/).

To stop the application, press `Ctrl + C` in the terminal, and then run:
  ```bash
  docker-compose down
  ```

### Database
<img width="708" alt="database-trading-wallet" src="https://github.com/agustin-chavez/trading-wallet/assets/39955956/baa710e1-977b-434a-a0d2-d9e00c2e30ec">


## License

This project is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0). See the LICENSE file for more details.


