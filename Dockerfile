# ==== CONFIGURE =====
# Use a Node 16 base image
FROM python:3.12.0b3-bookworm

# Set the working directory to /app inside the container
WORKDIR /app
# Copy app files

ENV PORT 830
ENV USER ""
ENV RSA_PRIVATE_KEY ""

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE ${PORT}

#CMD [ "python3", "./netconf-client.py", "-p", "1830", "-u", "alex", "-h", "barnes.home.lan", "-t", "30", "-l", "debug"]
#CMD [ "python3", "./netconf-sim.py", "-p", $PORT, "-u", "alex", "-k", "paramiko_rsa"]
CMD [ "sh", "-c", "python3 ./netconf-sim.py -p ${PORT} -u ${USER} -k ${RSA_PRIVATE_KEY}"]




