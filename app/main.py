from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.api.routes import auth
from app.api.routes import parts as parts_router
from app.api.routes import builds as builds_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PC Build Compatibility Checker", version="0.1.0",
              description="CRUD for parts and builds + /builds/{id}/validate.")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(parts_router.router)
app.include_router(builds_router.router)

@app.get("/", tags=["health"])
def health(): return {"status": "ok"}
