@echo off
echo Fixing dependency conflicts...

:: Clear cache
pip cache purge

:: Install core packages first
pip install fastapi uvicorn[standard] pydantic pydantic-settings twilio

:: Install AI packages with compatible versions
pip install openai google-generativeai langchain
pip install transformers "huggingface-hub>=0.16.4,<0.18"
pip install sentence-transformers
pip install torch --index-url https://download.pytorch.org/whl/cpu

:: Install remaining packages
pip install Pillow opencv-python pytesseract pdf2image PyPDF2
pip install sqlalchemy asyncpg alembic redis pymongo
pip install celery flower
pip install python-dotenv python-multipart aiofiles httpx
pip install "python-jose[cryptography]" "passlib[bcrypt]" python-dateutil
pip install loguru sentry-sdk prometheus-client cryptography
pip install groq cohere ollama together
pip install chromadb faiss-cpu
pip install requests numpy pytz

echo.
echo Installation complete!
pause