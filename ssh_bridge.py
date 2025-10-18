
import paramiko
import sys
import json

def run_command(hostname, username, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname, username=username, password=password)

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        client.close()
        return {'output': output, 'error': error}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(json.dumps({'error': 'Usage: python ssh_bridge.py <hostname> <username> <password> <command>'}))
        sys.exit(1)

    hostname = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    command = sys.argv[4]

    result = run_command(hostname, username, password, command)
    print(json.dumps(result))

