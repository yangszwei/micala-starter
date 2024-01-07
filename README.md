# micala-starter

## Usage

You can start the Docker Compose project with zero configuration by running:

```shell
$ docker compose up -d
```

Mongo Express is available at http://localhost:8081, and Kibana at http://localhost:5601.

## Credentials

| Service | Username | Password |
|---------|----------|----------|
| MongoDB | root     | root     |

## Activating the Micala user

There is a helper script that helps you activate the Micala user after registering. You can run it with:

```shell
$ ./scripts/activate-user.sh <your-username>
```

on macOS and Linux, or

```shell
$ ./scripts/activate-user.bat <your-username>
```

on Windows.

## Caveats

- Kibana may take a few minutes to start up, you can check if the status is `healthy` by running `docker compose ps`.
- The user activation script for Windows is untested. File an issue if you encounter any problems.
