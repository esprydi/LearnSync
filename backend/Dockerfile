# Gunakan base image Python yang ringan
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Copy file requirements.txt
COPY requirements.txt .

# Install semua dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh file backend ke dalam container
COPY . .

# Hugging Face Spaces secara default menggunakan port 7860
ENV PORT=7860
EXPOSE 7860

# Jalankan server FastAPI
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 7860"]
