from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    encrypted_password = Column(String, nullable=False)

    transactions = relationship('Transaction', back_populates='user')
    holdings = relationship('Holding', back_populates='user')

Index('idx_users_id', User.id)
Index('idx_username', User.username)
Index('idx_email', User.email)

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    symbol = Column(String, nullable=False)
    shares = Column(Integer, nullable=False)
    share_price = Column(Numeric, nullable=False)
    fee = Column(Numeric, nullable=False)
    transaction_date = Column(Date, nullable=False)

    user = relationship('User', back_populates='transactions')

Index('idx_transactions_id', Transaction.id)
Index('idx_user_id', Transaction.user_id)

class Holding(Base):
    __tablename__ = 'holdings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    symbol = Column(String, nullable=False)
    shares = Column(Integer, nullable=False, default=1)

    user = relationship('User', back_populates='holdings')

Index('idx_holdings_id', Holding.id)
Index('idx_user_id_holdings', Holding.user_id)
