from fastapi import FastAPI
import random

app = FastAPI()


@app.get('/api/random')
async def get_random():
    ran:int = random.randint(0,100)
    return {'random':ran, 'limit':100}


@app.get('/api/register')
async def post_register():
    return {'message': 'Register'}


@app.get('/api/unregister')
async def post_unregister():
    return {'message': 'Unregister'}


@app.get('/api/available-nodes-by-zone')
async def get_available_nodes_by_zone():
    return {'message': 'Available nodes by zone'}