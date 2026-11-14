from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from .models import UserStatus


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    status: UserStatus = UserStatus.buyer

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    status: UserStatus
    created_date: datetime

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    category_name: str

class CategoryOut(CategoryCreate):
    id: int

    class Config:
        from_attributes = True


class StoreCreate(BaseModel):
    store_name: str
    category_id: int
    store_image: Optional[str] = None

class StoreOut(StoreCreate):
    id: int

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    store_id: int
    product_name: str
    price: float
    description: Optional[str] = None
    is_original: bool = True

class ProductOut(ProductCreate):
    id: int
    create_date: datetime

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    store_id: int
    user_id: int
    text: str
    stars: int = Field(..., ge=1, le=5)

class ReviewOut(ReviewCreate):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True


class CityCreateSchema(BaseModel):
    city_name: str

class CitySchema(CityCreateSchema):
    id: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    product_id: int
    user_id: int
    city_id: int
    quantity: int = 1

class OrderOut(OrderCreate):
    id: int
    total_price: float
    created_date: datetime

    class Config:
        from_attributes = True



UserCreateSchema = UserCreate
UserSchema = UserOut

CategoryCreateSchema = CategoryCreate
CategorySchema = CategoryOut

StoreCreateSchema = StoreCreate
StoreSchema = StoreOut

ProductCreateSchema = ProductCreate
ProductSchema = ProductOut

ReviewCreateSchema = ReviewCreate
ReviewSchema = ReviewOut

OrderCreateSchema = OrderCreate
OrderSchema = OrderOut