docker build echo-app -f ../docker/echo-service/Dockerfile .
docker run -p 8000:8000 -it --rm --name echo-app echo-app sh start.sh
