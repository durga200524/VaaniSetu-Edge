from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.intelligence.edge_simulator import simulate_edge_constraints


router = APIRouter(
    prefix="/api/v1/edge",
    tags=["Edge Constraint Simulator"]
)


class EdgeSimulationRequest(BaseModel):

    available_ram_mb: float = Field(default=512, gt=0)

    cpu_cores: float = Field(default=2, gt=0)

    network_latency_ms: float = Field(default=100, ge=0)

    bandwidth_mbps: float = Field(default=10, ge=0)

    internet_available: bool = True


@router.post("/simulate")
async def simulate_edge(request: EdgeSimulationRequest):

    try:
        result = simulate_edge_constraints(
            available_ram_mb=request.available_ram_mb,
            cpu_cores=request.cpu_cores,
            network_latency_ms=request.network_latency_ms,
            bandwidth_mbps=request.bandwidth_mbps,
            internet_available=request.internet_available
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        print("EDGE SIMULATION ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="Edge simulation failed."
        )