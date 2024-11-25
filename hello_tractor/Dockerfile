FROM python:3.10-slim

WORKDIR /usr/

COPY requirements.txt .

# # create virtual environment
# RUN python3 -m venv /opt/venv 

# # activate virtual environment
# RUN /opt/venv/bin/pip install -r requirements.txt

# RUN pip install --upgrade pip
# # do pip install
RUN pip install -r --no-cache-dir requirements.txt
# RUN pip install gunicorn

COPY . .

CMD ["python", "manage.py", "runserver"]