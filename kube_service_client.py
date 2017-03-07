#!python
"""
Code for execing into containers running on kubenertes, given the service account token and ca.crt

Code mostly from: https://github.com/kubernetes-incubator/client-python/blob/dc35eee071fdde52bc6a55673a4cb11c1e583e5b/examples/exec.py

I didn't put too much effort into this, so its a little janky.
"""
import os
import sys
from kubernetes import client, config

class KubeServiceClient(object):

    def __init__(self):
        config.load_incluster_config()
        self.api = client.CoreV1Api()

    def list_pods(self):
        print("Listing pods with their IPs:")
        ret = self.api.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" %
                  (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


    def exec_in_pod(self, pod):
        # Calling exec interactively.
        exec_command = ['/bin/sh']
        resp = self.api.connect_get_namespaced_pod_exec(pod, 'default',
                                                   command=exec_command,
                                                   stderr=True, stdin=True,
                                                   stdout=True, tty=False,
                                                   _preload_content=False)
        while resp.is_open():
            resp.update(timeout=1)
            while resp.peek_stdout():
                sys.stdout.write(resp.read_stdout())
            while resp.peek_stderr():
                sys.stdout.write(resp.read_stderr())
            command = raw_input()
            resp.write_stdin(command + "\n")

def usage():
    print("""Usage:
    # List all the pods
    python service_access.py pods

    # Get a shell in the pods
    python service_access.py shell <POD>
    """)
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()

    client = KubeServiceClient()

    if sys.argv[1] == 'pods':
        client.list_pods()
    elif sys.argv[1] == 'shell':
        client.exec_in_pod(sys.argv[2])
    else:
        usage()
