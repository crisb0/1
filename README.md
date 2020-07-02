# random side project

## How to run
Requires:
- Docker
- gRPC
- npm
- python3

### Envoy Proxy
1. `cd envoy/`
2. Build Dockerfile `docker build -t envoy:v1 .'
3. `docker run -d --name proxy -p 9901:9901 -p 10000:10000 envoy:v1`

### Server (python)
1. `pip3 install -r requirements.txt`
2. Make sure protos are compiled ``
2. Run as module `python3 -m server.src.Server`

### Client (react, ts)
1. `cd client`
2. `npm install`
3. `npm start`


## data sources
- yahoo finance
