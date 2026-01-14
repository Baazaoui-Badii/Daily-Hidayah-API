import logging
import random
import sys
import time
from typing import List, Dict

from fastapi import FastAPI, Response
from prometheus_client import generate_latest, Counter, CONTENT_TYPE_LATEST

# Configure JSON logging
logger = logging.getLogger("daily-hidayah-api")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI(title="Daily Hidayah API")

# Metrics
REQUEST_COUNT = Counter("http_requests_total", "Total app HTTP requests", ["method", "endpoint", "status"])

# Data
guidance_list: List[Dict[str, str]] = [
    {"type": "ayah", "content": "Verily, with hardship comes ease. (94:6)", "source": "Quran 94:6"},
    {"type": "ayah", "content": "Allah does not burden a soul beyond that it can bear. (2:286)", "source": "Quran 2:286"},
    {"type": "hadith", "content": "The best among you are those who have the best manners and character.", "source": "Sahih Bukhari"},
    {"type": "hadith", "content": "None of you will have faith till he wishes for his (Muslim) brother what he likes for himself.", "source": "Sahih Bukhari"},
    {"type": "ayah", "content": "So remember Me; I will remember you. (2:152)", "source": "Quran 2:152"},
]

@app.middleware("http")
async def log_requests(request, call_next):
    method = request.method
    endpoint = request.url.path
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    status_code = response.status_code
    
    logger.info(f"Method={method} Endpoint={endpoint} Status={status_code} Latency={process_time:.4f}s")
    
    # Update metrics
    if endpoint != "/metrics": # Avoid tracking metrics scraping itself excessively if desired, or keep it.
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()
        
    return response

@app.get("/guidance")
def get_guidance():
    """Returns a random Ayah or Hadith."""
    item = random.choice(guidance_list)
    return item

@app.get("/metrics")
def metrics():
    """Exposes Prometheus metrics."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def root():
    return {"message": "Welcome to Daily Hidayah API. Visit /guidance for inspiration."}
