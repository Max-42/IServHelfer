FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app


ENV ISERV_HOST="deine-schule.de/iserv/"
ENV ISERV_USER="vorname.nachname"
ENV ISERV_PASSWORD="D€iN-S1cErEs-P4S5W0rT"
ENV DISCORD_WEBHOOK="https://discord.com/api/webhooks/XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


CMD [ "python", "./main.py" ]
