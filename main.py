from dashboard import idea
from fastapi import FastAPI
import fastapi.middleware.cors import CORSMiddleware
from routes.idea_expander_api import routes as idea_expander_api

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
# app.include_router(other_router, prefix="/api")
app.include_router(idea_expander_api, prefix="/api")