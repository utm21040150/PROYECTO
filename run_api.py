
import uvicorn   # Servidor api


if __name__ == "__main__":

    uvicorn.run(
        "main:app",     
        host="127.0.0.1",  # Localhost
        port=8000,         # Puerto API
        reload=True        
    )


#pip install ----> uvicorn