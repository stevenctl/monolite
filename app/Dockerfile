FROM python:3.6

# Expose the web service port
EXPOSE 5000

# Add our application to the image
COPY ../ /opt/cmk_ns
WORKDIR /opt/cmk_ns

# Install python dependencies
RUN pip install -r /opt/cmk_ns/requirements.txt

# Start the app
CMD python3 checkmk_not_shitty.py
