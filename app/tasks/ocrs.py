from scheduler import app


@app.task
def ocr(x, y):
    return x + y
