from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base

class OrderType(str, enum.Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderSide(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(str, enum.Enum):
    NEW = "new"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Order details
    symbol = Column(String, nullable=False, index=True)
    side = Column(Enum(OrderSide), nullable=False)
    order_type = Column(Enum(OrderType), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float)  # For limit orders
    stop_price = Column(Float)  # For stop orders
    
    # Status and execution
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    filled_quantity = Column(Float, default=0.0)
    average_price = Column(Float)
    
    # Strategy and metadata
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    filled_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User")
    strategy = relationship("Strategy")
    trades = relationship("Trade", back_populates="order")

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    
    # Trade details
    symbol = Column(String, nullable=False, index=True)
    side = Column(Enum(OrderSide), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    
    # Financial details
    commission = Column(Float, default=0.0)
    total_value = Column(Float, nullable=False)  # quantity * price
    pnl = Column(Float, default=0.0)  # Realized P&L
    
    # Strategy and metadata
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    
    # Timestamps
    executed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    order = relationship("Order", back_populates="trades")
    strategy = relationship("Strategy")

class Position(Base):
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Position details
    symbol = Column(String, nullable=False, index=True)
    quantity = Column(Float, nullable=False)  # Positive for long, negative for short
    average_price = Column(Float, nullable=False)
    current_price = Column(Float)
    
    # Financial metrics
    market_value = Column(Float)
    unrealized_pnl = Column(Float, default=0.0)
    realized_pnl = Column(Float, default=0.0)
    
    # Risk management
    stop_loss = Column(Float)
    take_profit = Column(Float)
    
    # Timestamps
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User")
    
    @property
    def is_long(self):
        return self.quantity > 0
    
    @property
    def is_short(self):
        return self.quantity < 0
