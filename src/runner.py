import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "bot.asgi:app",
        host="localhost",
        log_level="debug",
        port=8000,
        reload=True,
        reload_dirs=["src"],
    )
