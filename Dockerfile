FROM node:lts-slim AS builder

WORKDIR /app
COPY ./client/package*.json ./
RUN npm ci
COPY ./client .
RUN npm run build

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app/dist ./bundle
COPY ./server/requirements.txt .
RUN pip install -r requirements.txt
COPY ./server .
CMD [ "uvicorn", "src.main:app", "--port", "8000"]