#!/bin/bash

# Put the ip address of the kuberenetes api for your cluster here
HOST=FILL_ME_IN
echo "$HOST kubernetes" >> /etc/hosts
export KUBERNETES_SERVICE_HOST=kubernetes
export KUBERNETES_SERVICE_PORT=443
pip install kubernetes
bash
