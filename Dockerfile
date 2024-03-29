FROM python:3.9-alpine

ARG DJANGO_SECRET_KEY
ARG SPOTIPY_CLIENT_ID
ARG SPOTIPY_CLIENT_SECRET
ARG SPOTIPY_REDIRECT_URI

WORKDIR /app
COPY . .

ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ENV SPOTIPY_CLIENT_ID=${SPOTIPY_CLIENT_ID}
ENV SPOTIPY_CLIENT_SECRET=${SPOTIPY_CLIENT_SECRET}
ENV SPOTIPY_REDIRECT_URI=${SPOTIPY_REDIRECT_URI}

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# docker build --build-arg DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY --build-arg SPOTIPY_CLIENT_ID=$SPOTIPY_CLIENT_ID --build-arg SPOTIPY_CLIENT_SECRET=$SPOTIPY_CLIENT_SECRET -t test-backend .