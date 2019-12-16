
# Running Echo Web Service

Run the following commands:

```
cd resthooks
./run_docker.sh
```

This will run a sample rest hooks django application, and will expose an "echo" service that can be used as a test hook endpoint:

http://localhost:8000/api/echo/

Note that you can run the above on play with docker (https://labs.play-with-docker.com/) or play with von (http://play-with-von.vonx.io/) to expose a public endpoint for the echo service.
