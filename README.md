# docker-data-synchronizer

## Subject

Synchronizing / moving data between two servers

## Description

The service has two responsibilities:
- Synchronizing data from running machine to remote server
- Deleting old or unnecessary data

## Usage

### Docker

```
docker run \
    -e TRANSMISSION_API="http://transmission:9091/transmission/rpc" \
    -e DESTINATION_PATH=""
    -v ~/transmission/data/completed:/sync \
    -v ~/data-synchronizer/data:/data \
    data-synchronizer
```

### Docker compose

```
version: "3"
services:
    data-synchronizer:
        image: data-synchronizer
        container_name: data-synchronizer
        restart: unless-stopped
        environment:
          - TRANSMISSION_API=http://transmission:9091/transmission/rpc
          - DESTINATION_PATH=""
        volumes:
          - ~/transmission/data/completed:/sync
          - ~/data-synchronizer/data:/data
```

## Parameters

| Parameter | Function |
| :----: | --- |
| `TRANSMISSION_API` | Transmission's rpc api url |
| `DESTINATION_PATH` | Destination path (server). Format - USER@SERVER: |

## Versions

* **20.04.18:** - Initial Release.

## To Do

- Implement rsync command including providing ssh key for access