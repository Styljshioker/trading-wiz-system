"""
Database setup and connection
"""
import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trading_wiz.db")

# SQLAlchemy setup
engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database connection for async operations
database = databases.Database(DATABASE_URL)

# Metadata for table creation
metadata = sqlalchemy.MetaData()

# Table definitions
users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(50), unique=True, nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(100), unique=True, nullable=False),
    sqlalchemy.Column("hashed_password", sqlalchemy.String(128), nullable=False),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),
)

portfolios_table = sqlalchemy.Table(
    "portfolios",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("total_value", sqlalchemy.Float, default=0.0),
    sqlalchemy.Column("cash_balance", sqlalchemy.Float, default=0.0),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

positions_table = sqlalchemy.Table(
    "positions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("portfolio_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("portfolios.id"), nullable=False),
    sqlalchemy.Column("symbol", sqlalchemy.String(20), nullable=False),
    sqlalchemy.Column("quantity", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("average_price", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("current_price", sqlalchemy.Float),
    sqlalchemy.Column("market_value", sqlalchemy.Float),
    sqlalchemy.Column("unrealized_pnl", sqlalchemy.Float),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),
)

trades_table = sqlalchemy.Table(
    "trades",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("portfolio_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("portfolios.id"), nullable=False),
    sqlalchemy.Column("symbol", sqlalchemy.String(20), nullable=False),
    sqlalchemy.Column("side", sqlalchemy.String(10), nullable=False),  # 'buy' or 'sell'
    sqlalchemy.Column("quantity", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("commission", sqlalchemy.Float, default=0.0),
    sqlalchemy.Column("total_amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("status", sqlalchemy.String(20), default="pending"),
    sqlalchemy.Column("order_id", sqlalchemy.String(50)),
    sqlalchemy.Column("executed_at", sqlalchemy.DateTime),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

trading_strategies_table = sqlalchemy.Table(
    "trading_strategies",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("strategy_type", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("parameters", sqlalchemy.JSON),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=True),
    sqlalchemy.Column("performance_metrics", sqlalchemy.JSON),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

# Create tables
def create_tables():
    metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
