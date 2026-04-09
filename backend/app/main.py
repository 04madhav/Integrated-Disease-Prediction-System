from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers.prediction import router as prediction_router
from backend.app.routers.recommendation import router as recommendation_router

app = FastAPI(
    title="Disease Prediction System API",
    description="A multi-model API for predicting cardiometabolic risk factors (Heart, Stroke, Diabetes, CKD) and a combined CHRI score.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Disease Prediction System API",
        "docs": "/docs"
    }

# Include routers
app.include_router(prediction_router, tags=["Predictions"])
app.include_router(recommendation_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
