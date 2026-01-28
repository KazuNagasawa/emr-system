from fastapi import FastAPI
from sqlalchemy import text
from app.db import engine, Base

# ★ モデルをimportしないとテーブルが登録されない
from app.models.patient import Patient  # noqa

# ★ ルーター追加
from app.api import patient


app = FastAPI(title="EMR API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))  # ←追加
        await conn.run_sync(Base.metadata.create_all)  # テーブル作成
        await conn.execute(text("SELECT 1"))
    print("✅ Database connected & tables created")


@app.get("/")
def root():
    return {"message": "EMR backend is running"}

# =========================
#  APIルーター登録
# =========================
app.include_router(patient.router)