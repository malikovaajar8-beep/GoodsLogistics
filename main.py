from fastapi import FastAPI
from mysite.database.db import Base, engine
from mysite.admin.setup import setup_admin
from mysite.api import user, category, store, product, review, city, order

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GoodsLogistic API")

setup_admin(app)

app.include_router(user.user_router)
app.include_router(category.category_router)
app.include_router(store.store_router)
app.include_router(product.product_router)
app.include_router(review.review_router)
app.include_router(city.city_router)
app.include_router(order.order_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)