# To build: docker build -t test:pandas .
# -t tag an image (i.e. versioning)
# Then run: docker run -it test:pandas
FROM python:3.9
RUN pip install pandas
WORKDIR /app
COPY pipeline.py pipeline.py

# avoid Python command line when running container
# ENTRYPOINT [ "bash"]

# run python script
ENTRYPOINT [ "python", "pipeline.py"]