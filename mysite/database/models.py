import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from .db import Base


class UserStatus(str, enum.Enum):
    buyer = "buyer"
    seller = "seller"
    manager = "manager"
    courier = "courier"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.buyer, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    reviews = relationship("Review", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), unique=True, nullable=False)

    stores = relationship("Store", back_populates="category")


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    store_image = Column(String, nullable=True)

    category = relationship("Category", back_populates="stores")
    products = relationship("Product", back_populates="store")
    reviews = relationship("Review", back_populates="store")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    product_name = Column(String(150), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    is_original = Column(Boolean, default=True)
    create_date = Column(DateTime, default=datetime.utcnow)

    store = relationship("Store", back_populates="products")
    orders = relationship("Order", back_populates="product")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)
    stars = Column(Integer, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    store = relationship("Store", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(100), unique=True, nullable=False)

    orders = relationship("Order", back_populates="city")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    total_price = Column(Float, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="orders")
    user = relationship("User", back_populates="orders")
    city = relationship("City", back_populates="orders")