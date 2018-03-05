from app import app

#route decorator tells flask the url to trigger
@app.route('/')
def index():
    return "Hello, Kenya!"

