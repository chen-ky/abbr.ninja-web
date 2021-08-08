# abbr.ninja Frontend

This is the frontend code for the link shortener on [abbr.ninja](https://abbr.ninja/).


Source code for:
* [API documentation](https://github.com/chen-ky/abbr.ninja-api-doc)
* API server

## Building the Container

`podman` was used to run and build the container but this should also work
for `docker`.

1. Clone this repository. `git clone https://github.com/chen-ky/abbr.ninja-web.git`
2. Change directory into the cloned repository. `cd abbr.ninja-web`
3. Build the container with the provided Dockerfile. `podman build -t <INSERT_CONTAINER_TAG_NAME> .`
4. Run the newly built container. `podman run -p 8080:8080 -e API_BASE_URL="<INSERT_URL_FOR_API_SERVER>" -d -t <INSERT_CONTAINER_TAG_NAME>"`
5. You should be able to go to [http://localhost:8080](http://localhost:8080) for the webpage.


## Environment Variables for Container

* `API_BASE_URL` **(Required)**: The URL endpoint for the API server for API calls. Example: `https://api.abbr.ninja/api/v1`
* `HOST` (Optional): IP address the server will listen on. Default: `0.0.0.0`
* `PORT` (Optional): Network port that the server will listen on. Default: `8080`

## Deployment Recommendation

* A nginx reverse proxy to this server is recommended since this server does not support configuration for TLS/SSL and for higher performance.
[How to Configure a Nginx HTTPs Reverse Proxy on Ubuntu Bionic - Scaleway](https://www.scaleway.com/en/docs/how-to-configure-nginx-reverse-proxy/)