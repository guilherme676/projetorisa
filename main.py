from fastapi import FastAPI
from routes.auth_routes import auth_router
from routes.agendamento import agendamento_router 
from routes.srv import srv_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(agendamento_router)
app.include_router(srv_router)

@app.get('/')
def root_route():
    return {
        'mensagem': 'Herwo World'
    }
