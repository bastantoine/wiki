To mount files when building a Docker image, use the `RUN --mount` option.

Multiple type are possible:
1. `bind`
2. `secret`
3. `cache`
4. `tmpfs`
5. `ssh`

## `RUN --mount=type=bind`
Useful to mount regular file at build time while not needing a previous layer to copy them.

```Dockerfile
FROM ubuntu:latest

RUN --mount=type=bind,source=my-secret-file,target=/var/config/my-secret-file \
    cat /var/config/my-secret-file

RUN cat /var/config/my-secret-file
```

[\[src\]](https://docs.docker.com/reference/dockerfile/#run---mounttypebind)

## `RUN --mount=type=secret`

Secret mounts can be used to mount secret values, such as config files or env var needed to perform operations, while not having them available in the final image, as well as any intermediate layer built.

```Dockerfile
FROM ubuntu:latest

RUN --mount=type=secret,id=token,target=/var/config/my-secret-token \
	cat /var/config/my-secret-token

RUN cat /var/config/my-secret-token
```

```bash
docker build --secret id=token,src=./my-secret-token .
```

It is also possible to mount the secret from an environment variable:

```bash
docker build --secret id=token,env=MY_SECRET_TOKEN .
```

If the `id` of the secret is the same as the name of the environment variable, the `env` param can be omitted:
```Dockerfile
FROM ubuntu:latest

RUN --mount=type=secret,id=MY_SECRET_TOKEN,target=/var/config/my-secret-token \
	cat /var/config/my-secret-token

RUN cat /var/config/my-secret-token
```
```bash
docker build --secret id=MY_SECRET_TOKEN .
```

Secret mounts can also be mounted as environment variables:

```dockerfile
RUN --mount=type=secret,id=aws-key-id,env=AWS_ACCESS_KEY_ID \
    --mount=type=secret,id=aws-secret-key,env=AWS_SECRET_ACCESS_KEY \
    --mount=type=secret,id=aws-session-token,env=AWS_SESSION_TOKEN \
    aws s3 cp ...
```
[\[src\]](https://docs.docker.com/build/building/secrets/)

## `RUN --mount=type=cache`

Cache mount can be used to mount cache for package manager and compilers.

Cache mounts should only be used for better performance. The image should be able to be built without any file in the cache mount, as another build may overwrite the files or GC may clean it if more storage space is needed.

```dockerfile
FROM golang
RUN --mount=type=cache,target=/root/.cache/go-build \
	go build ...
```

```dockerfile
FROM ubuntu

RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
	--mount=type=cache,target=/var/lib/apt,sharing=locked \
	apt update && apt-get --no-install-recommends install -y gcc
```
[\[src\]](https://docs.docker.com/reference/dockerfile/#run---mounttypecache)
