from fastapi import FastAPI
import random

app=FastAPI()

@app.get('/')
async def root():
    return {'example': 'This is an example', 'data':0}

@app.get('/random')
async def get_random():
    ran:int = random.randint(0,100)
    return {'random':ran, 'limit':100}