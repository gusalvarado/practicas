from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.idea_expander_api import routes as idea_expander_api
from routes.health import router as health_router
from routes.upload_api import routes as upload_api

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
app.include_router(upload_api)
app.include_router(health_router)
app.include_router(idea_expander_api)