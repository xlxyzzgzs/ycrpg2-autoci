uvicorn \
--port 8000 \
--workers 1 \
--log-level error \
--reload --reload-dir . \
--host 127.0.0.1 \
main:app 