FROM python:3.6

# Expose the web service port
EXPOSE 5000

# Add our application to the image
COPY ./ /opt/app
WORKDIR /opt/app

# Install python dependencies
RUN pip install -r /opt/app/requirements.txt

# Start the app
CMD python3 app.py
