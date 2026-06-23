from fastapi import FastAPI
from app.database import Base, engine
from app.routers.auth_router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",      # React
    "http://localhost:8081",      # Expo development server
    "exp://192.168.1.100:8081",   # Expo Go (optional)
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)


app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "API is running"
    }