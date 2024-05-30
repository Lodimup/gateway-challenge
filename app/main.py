from fastapi import FastAPI
from routers import ocrs
from services.env_man import ENVS

app = FastAPI(debug=ENVS["DEBUG"])
app.include_router(ocrs.router)


@app.get("/live")
def get_live():
    """
    Returns 200 {"status": "ok"} if the server is live
    """
    return {"status": "ok"}
