from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import List, Dict, Optional
import math
from src.graph_search import astar, NODES
from src.forecasting import simple_exponential_smoothing

app = FastAPI(title="AI Supply Chain Orchestration API")

# Schema Payload (Standardisasi JSON Request)
class ForecastData(BaseModel):
    gerai_name: str
    current_stock: int
    sales_history: List[int]

class RouteRequest(BaseModel):
    gudang_awal: str
    gerai_tujuan: Optional[str] = "AUTO"  # Jika AUTO, gunakan AI Forecasting
    data_gerai: Optional[List[ForecastData]] = None

@app.post("/api/v1/distribute")
async def optimize_distribution(payload: RouteRequest, response: Response):
    # CONTAINMENT UNIT 1: Try-Except Block & Validasi
    try:
        # Validasi Gudang
        if payload.gudang_awal not in NODES:
            raise KeyError(f"Gudang '{payload.gudang_awal}' tidak terdaftar di database graf.")

        target_gerai = payload.gerai_tujuan

        # ORCHESTRATION: AI 1 (Forecasting) -> AI 2 (A* Search)
        if target_gerai == "AUTO":
            if not payload.data_gerai:
                raise ValueError("Mode AUTO membutuhkan 'data_gerai' untuk diproses oleh sistem Forecasting.")
            
            kritis_gerai = None
            min_hari_tersisa = math.inf
            
            for gerai in payload.data_gerai:
                if gerai.gerai_name not in NODES:
                    raise KeyError(f"Gerai '{gerai.gerai_name}' tidak dikenal dalam graf.")
                
                prediksi_harian = simple_exponential_smoothing(gerai.sales_history)
                hari_tersisa = gerai.current_stock / prediksi_harian if prediksi_harian > 0 else math.inf
                
                if hari_tersisa < min_hari_tersisa:
                    min_hari_tersisa = hari_tersisa
                    kritis_gerai = gerai.gerai_name
            
            target_gerai = kritis_gerai

        # Validasi Tujuan Manual
        if target_gerai not in NODES:
            raise KeyError(f"Gerai tujuan '{target_gerai}' tidak terdaftar.")

        # Eksekusi A* Search dengan Heuristik Sweet Spot (Euclidean)
        route_result = astar(payload.gudang_awal, target_gerai)

        return {
            "status": "success",
            "code": 200,
            "message": "Orchestration & Routing sukses.",
            "data": {
                "target_gerai": target_gerai,
                "route_path": route_result["path"],
                "total_cost_km": route_result["cost"],
                "heuristic_used": "Euclidean (H1) - Sweet Spot"
            }
        }

    # HUMAN-READABLE ERROR MESSAGES
    except KeyError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "code": 400, "message": f"Data Tidak Ditemukan: {str(e)}"}
    except ValueError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "code": 400, "message": f"Input Tidak Valid: {str(e)}"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "error", "code": 500, "message": f"Server Crash Dicegah. Pesan error: {str(e)}"}