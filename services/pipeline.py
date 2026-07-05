from agents.language_agent import normalize_report
from agents.verification_agent import verify_report
from agents.safety_agent import analyze_safety
from agents.resource_finder_agent import find_resources
from agents.memory_agent import add_record


def run_full_pipeline(report: dict):

    # 1. Normalize
    normalized = normalize_report(report)

    # 2. Verification
    verified = verify_report(normalized.model_dump())

    # 3. Safety
    safety = analyze_safety(verified.model_dump())

    # 4. Resources
    resources = find_resources(safety.model_dump())

    # 5. Memory store
    add_record({
        "location": normalized.location,
        "emergency_type": safety.emergency_type,
        "priority": safety.priority,
        "confidence_score": verified.confidence_score
    })

    return {
        "normalized": normalized.model_dump(),
        "verification": verified.model_dump(),
        "safety": safety.model_dump(),
        "resources": resources.model_dump()
    }