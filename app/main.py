from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.api.routes import auth, services, applications, users, payment


app = FastAPI(
    title="CivicEase API",
    description="All-in-One Citizen & Government Services API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(payment.router, prefix="/api")


Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "app": "CivicEase",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
