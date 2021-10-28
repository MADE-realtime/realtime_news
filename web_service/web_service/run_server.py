import uvicorn
from handlers import app as handlers_app

if __name__ == '__main__':
    uvicorn.run(handlers_app)
