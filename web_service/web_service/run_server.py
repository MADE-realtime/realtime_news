import uvicorn
from handlers import app as handlers_app

if __name__ == '__main__':
    uvicorn.run(handlers_app, host="127.0.0.1", port=8000)
