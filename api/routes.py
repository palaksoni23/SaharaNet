from fastapi import APIRouter
from services.pipeline import run_full_pipeline

router = APIRouter()

@router.post("/analyze")
def analyze(report: dict):
    result = run_full_pipeline(report)

    return {
        "normalized": result["normalized"],
        "verification": result["verification"],
        "safety": result["safety"],
        "resources": result["resources"]
    }