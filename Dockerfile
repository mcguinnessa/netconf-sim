# ==== CONFIGURE =====
# Use a Node 16 base image
#FROM python:3.12.0b3-bookworm
#FROM python:3.13.0a1-bookworm
FROM python:3




# Set the working directory to /app inside the container
WORKDIR /app
# Copy app files

ENV PORT 830
ENV USER ""
ENV RSA_PRIVATE_KEY ""
ENV LOGLEVEL "info"
ENV TIMEOUT "30"

COPY requirements.txt requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

COPY . .

#EXPOSE ${PORT}
EXPOSE 1830

#CMD [ "python3", "./netconf-client.py", "-p", "1830", "-u", "alex", "-h", "barnes.home.lan", "-t", "30", "-l", "debug"]
#CMD [ "python3", "./netconf-sim.py", "-p", $PORT, "-u", "alex", "-k", "paramiko_rsa"]
#CMD [ "sh", "-c", "python3 ./netconf-sim.py -p ${PORT} -u ${USER} -k ${RSA_PRIVATE_KEY} -t 30 -l debug"]
CMD [ "sh", "-c", "python3 ./netconf-sim.py -p ${PORT} -u ${USER} -k ${RSA_PRIVATE_KEY} -t ${TIMEOUT} -l ${LOGLEVEL}"]




