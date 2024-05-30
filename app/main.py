from routers import ocrs, auths, users
from services.env_man import ENVS


from fastapi import FastAPI

app = FastAPI(debug=ENVS["DEBUG"])
app.include_router(ocrs.router)
app.include_router(auths.router)
app.include_router(users.router)


@app.get("/live")
def get_live():
    """
    Returns 200 {"status": "ok"} if the server is live
    """
    return {"status": "ok"}
