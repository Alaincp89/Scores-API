from fastapi import FastAPI, HTTPException, Form, Header, Depends
from model.usuario_conexion import UsuarioConexion
from schema.users_schema import PartnerCodeRequest, ScoreRequest, LogoutRequest
import jwt
import datetime

SECRET_KEY = "S3cure$K3yWith!@#Numerical1234Values"

conexion = UsuarioConexion()

app = FastAPI()

@app.post("/generate-token/")
async def generate_token(
    username: str = Form(...),
    password: str = Form(...),
    grant_type: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...)
):    
    client_aut = conexion.read_client_authentication(username, password, grant_type, client_id, client_secret)  
    if client_aut:
        # Generar el token JWT
        payload = {
            "client_aut": client_aut,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expira en 1 hora
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")       
        conexion.update_or_insert_token(username, token)
        return {"authtoken": token}
    else:
        raise HTTPException(status_code=401, detail="Bad credentials")
    
@app.post("/User/login/")
def validate_users(
    partner_code: PartnerCodeRequest,
    Authorization: str = Header(...),
    Username: str = Header(...),
    password: str = Header(...),
    
):
    validate_user = conexion.read_validate_users(partner_code.partner_code, Authorization, Username, password)
    
    if validate_user:
        return {
                "authtoken": Authorization, 
                "expires": "Wed Apr 12 16:00:41 GMT 2023", 
                "code": "2000", 
                "status": "Success", 
                "message": "OK"           
            }
    else:
        raise HTTPException(status_code=401, detail="Bad credentials")
    
@app.post("/Scores/")
def score_client(
    request: ScoreRequest,
    Client: str = Header(...),
    ClientId: str = Header(...)
):
    validate_score = conexion.read_score_client(request.authtoken, request.phone_no)
    if validate_score:
        return {
            "responseCode": 200,
            "message": "OK",
            "transactionId": "0001",
            "data": {
                "msisdn": "664b5a38394d6675613434536957673732664d6b35773d3d",
                "credit_score": validate_score,
                "created_on": "2022-01-21",
                "updated_on": "2023-09-25",
                "status": "2000",
                "message": "Fetched Customer Score"
            }
        }    
    else:
        raise HTTPException(status_code=401, detail="No scores found")

@app.post("/User/logout/")
def logout_users(request: LogoutRequest):
    result = conexion.read_logout_users(request.partner_code, request.username)
    
    if result:
        return { 
            "code": "2000", 
            "status": "Success", 
            "message": "OK"           
        }
    else:
        raise HTTPException(status_code=401, detail="Bad credentials")