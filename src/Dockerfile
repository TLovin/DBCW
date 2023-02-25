# start by pulling the python image
FROM python:3.9-slim-buster

# RUN apt-get update && \
#     apt-get install -y default-libmysqlclient-dev && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    python-dev \
    build-essential


RUN pip3 install flask-mysqldb

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["view.py" ]