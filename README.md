# Test for Giskard

The project consists of a simple front-end based on Vue 3, and a simple back-end based on Python Flask.

There is an extra module, Python Celery, to run some time-consumption work.

## Build and run using Docker (Recommend)

Run the following command to build and run the entire project:

```
docker-compose build
```

The command will pull the necessary Docker image(s), build front-end codes and install back-end dependencies into a Docker image.

Then, run the services defined by `docker-compose.yml` (You can also do it at once using this command.):

```
docker-compose up
```

There should three running containers:

- a backend with `backend` in its name;
- a Celery worker with `celery-worker` in its name;
- a Redis instance with `redis` in its name.

Finally, the single-page application is accessible at `http://localhost:5000`.

Upload the empire plan, so that we can try to find a way beating them without being captured (at our best).

You can change the `FALCON_STATUS_FILE` environment in `backend.env` to change the default millennium falcon status file. Notice that the relative path always uses the `backend/` directory as the start.

## DIY

The components can also be built and run manually. We explain what happens in each part.

### Front-end

Building the front-end should be the first step.

It is just executing `npm install` to install the deps, and `npm run build` to let Vite build and output the files.

According to our configuration, there are 3 files built and produced in the `backend` folder:

- an `index.html` file for the template, in `backend/`;
- an `index-*.js` file for the Vue 3 code, in `backend/static`;
- an `index-*.css` file for the stylesheet, in `backend/static`.

### Back-end

After building the front-end, we can prepare the back-end environment. Without explicit explanation, the operations are all by default in the `backend/` sub-directory.

#### Dependencies

Create a virtual environment if necessary, and install the dependencies:

```
pip install -r requirements.txt
```

This command will install both Celery and Flask properly.

#### Redis

It is recommended to run a Redis instance using Docker, exposing `6379` port to `localhost`:

```
docker run -d -p 6379:6379 redis
```

However, you can also run your own instance locally.

#### Run Celery worker

Make sure that your Redis instance is alive. Then, run the Celery worker to wait for tasks:

```
celery -A task worker
```

#### Run the backend!

Finally, run the backend:

```
python app.py <millennium-falcon-status-file>
```

And that's all. You can access the website at `http://localhost:5000`.

## Extra notices

All of the commands are those in `*.sh` in the project root.

The configurations are kind of different between running in `docker-compose` and manually run. But the patches are automatically done by our Docker-related files.
