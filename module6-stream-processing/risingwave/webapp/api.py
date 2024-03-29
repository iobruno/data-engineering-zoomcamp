import psycopg2
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

db_connection_params = {
    "host": "localhost",
    "database": "dev",
    "user": "root",
    "port": 4566,
}


def run_query(query):
    connection = psycopg2.connect(**db_connection_params)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result


@app.get("/busiest_zones")
def get_busiest_zones():
    stmt = "select * from busiest_zones_1_min"
    return run_query(stmt)


@app.get("/longest_trips")
def get_longest_trips():
    stmt = "select * from longest_trip_1_min"
    return run_query(stmt)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
