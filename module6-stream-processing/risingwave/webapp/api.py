from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

import psycopg2


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,   
)

db_connection_params = {
    'host': 'localhost',
    'database': 'dev',
    'user': 'root',
    'port': 4566,
}

def run_query(query):
    connection = psycopg2.connect(**db_connection_params)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

@app.get('/get_busiest_zones')
def get_busiest_zones():
    stmt = "select * from busiest_zones_1_min"
    return run_query(stmt)

@app.get('/get_longest_trips')
def get_longest_trips():
    stmt = 'stmt * from longest_trip_1_min'
    return run_query(stmt)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
