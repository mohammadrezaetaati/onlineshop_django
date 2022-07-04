FROM python:3

WORKDIR /online_shop

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Required to install mysqlclient with Pip

# Install pipenv
COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# Copy the application files into the image
COPY . /online_shop/

CMD ["python3", "manage.py", "runserver"]
# Expose port 8000 on the container
EXPOSE 8000
