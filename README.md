# netconf-sim
NETCONF Simulator



This is a work in progress, most responses are currently hardcoded.

SERVER
======

An RSA key is required in order to run, although currently the only check is that the key is provided and the username is the same

To produce the RSA private/public key pair, run the ssh-keygen command.

To Run:
./netconf-sim.py -k <rsa_key> -u <alex>






Docker
======
To build docker image:

sudo docker build -t <username>/netconf-sim .
e.g.
sudo docker build -t mcguinnessa/netconf-sim .


Run Docker
sudo docker run -p 1831:1831 --rm --name netconf-sim --rm -e PORT=1830 -e RSA_PRIVATE_KEY=./paramiko_rsa -e USER=alex -d mcguinnessa/netconf-sim



CLIENT
======
To run client:
./netconf-client.py -p 1830 -u <username> -h <hostname> -t <timeout> -l debug

The timeout is the time the client will wait for a response

