import random

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import prometheus_client
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

head_count = prometheus_client.Counter(
    "head_count",
    "Number of heads"
)

tails_count = prometheus_client.Counter(
    "tails_count",
    "Number of tails"
)

total_flips = prometheus_client.Counter(
    "total_flips",
    "Total number of flips"
)

@app.get("/flip-coins")
async def flip_coins(times=None):
    if times is None or not times.isdigit():
        raise HTTPException(status_code=400, detail="Invalid input")
    times_as_int = int(times)

    heads = 0
    for _ in range(times_as_int):
        heads += random.randint(0, 1)
    
    tails = times_as_int - heads

    head_count.inc(heads)
    tails_count.inc(tails)
    total_flips.inc(times_as_int)

    return {
        "heads": heads,
        "tails": tails
    }

@app.get("/metrics")
async def metrics():
    return Response(prometheus_client.generate_latest())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)