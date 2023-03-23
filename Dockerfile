FROM nikolaik/python-nodejs:python3.10-nodejs18

COPY . /src
WORKDIR /src

ENV FALCON_STATUS_FILE=developer-test/examples/example1/millennium-falcon.json

# Build frontend
RUN ./build-frondend.sh

# Configure backend
RUN pip install -r backend/requirements.txt
# Patch redis hostname
RUN sed -i 's/localhost/redis/g' backend/task.py
# Patch flask debug mode and listen address
RUN sed -i "s/app.run(debug=True)/app.run(host=\"0.0.0.0\")/g" backend/app.py

EXPOSE 5000
CMD ./run-backend.sh $FALCON_STATUS_FILE
