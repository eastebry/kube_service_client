# Kubernetes Service Account Client
This is a simple example of how you can use the kuberentes default service account credentials to run code inside container.

This was all hacked together as an example, so I wouldn't recommend reusing this code for anything serious.

Fist, drop the token and ca.crt into the appropriate place in the secrets directory.

To run in docker:
```
docker run --rm -it \
  -v $(PWD):/tmp:ro \
  -v $(PWD)/secrets:/var/run/secrets:ro \
  python:2.7 sh /tmp/setup.sh

root@2e4be3ece9aa:# python /tmp/kube_service_client.py
```
