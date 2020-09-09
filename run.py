import os
import uvicorn


if __name__ == "__main__":
    uvicorn.run("colonist_hud.routing:application", host="0.0.0.0", port=8000, log_level="info", ssl_keyfile=os.environ["COLONIST_SSL_KEY"], ssl_certfile=os.environ["COLONIST_SSL_CERT"])
