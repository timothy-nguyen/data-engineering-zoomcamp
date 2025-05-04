# To build: docker build -t test:pandas .
# -t tag an image (i.e. versioning)
# Then run: docker run -it test:pandas
FROM python:3.9
RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2
WORKDIR /app
COPY data_pipeline.py data_pipeline.py

# avoid Python command line when running container
# ENTRYPOINT ["bash"]

# run python script
ENTRYPOINT [ "python", "data_pipeline.py"]