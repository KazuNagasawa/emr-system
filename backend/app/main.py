from fastapi import FastAPI
from sqlalchemy import text
from app.db import engine, Base

# ★ モデルをimportしないとテーブルが登録されない
from app.models.patient import Patient  # noqa

app = FastAPI(title="EMR API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # テーブル作成
        await conn.execute(text("SELECT 1"))
    print("✅ Database connected & tables created")


@app.get("/")
def root():
    return {"message": "EMR backend is running"}
