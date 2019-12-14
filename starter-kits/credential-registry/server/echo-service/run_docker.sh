docker build -t echo-app .
docker run -p 8000:8000 -it --rm --name echo-app echo-app bash start.sh

