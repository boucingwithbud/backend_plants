import fastapi
from fastapi.middleware.cors import CORSMiddleware
app = fastapi.FastAPI()
from prediction import router as prediction_router

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)