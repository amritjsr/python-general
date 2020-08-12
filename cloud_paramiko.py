import os
import re
from paramiko import SSHClient, AutoAddPolicy, SSHConfig, ProxyCommand, SFTP, util
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException
from time import sleep
import string, unicodedata
util.log_to_file('/tmp/paramiko.SSHClient.log', level=5)

PS1 = "[PARAMIKO_PROMPT]# "
DEMO_COMMAND = 'echo ">>$(id -u)<<"\n'
MAX_BUFFER = 65535
regexRC = re.compile('COMMAND_EXIT_CODE: [\d]+',re.DOTALL)

def clear_buffer(connection):
    buffer_str = None
    while True:
        if connection.channel.recv_ready(): buffer_str = connection.channel.recv(MAX_BUFFER); break
        else: sleep(0.1); continue
    return buffer_str

def wait_input_prompt(connection):
    while True:
        if connection.recv_ready(): break
        else: sleep(0.1); continue
    return

def extract_output(text):
    output = ''
    rc = None
    output_str = text.decode('ascii').replace('\t', '    ')
    rc = int((regexRC.findall(output_str)[-1]).strip('COMMAND_EXIT_CODE: '))
    if not re.search(r'^\[PARAMIKO_PROMPT\]\# ', output_str): output_str = PS1 + output_str
    output = re.findall(r'(?<=\[PARAMIKO_PROMPT\]\# )([\s\S]+?)(?=\[PARAMIKO_PROMPT\]\# )', output_str, re.MULTILINE)
    if len(output) >= 1:
        output = output[0]
    return output, rc


class remoteSshClient():
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(self, host = '127.0.0.1', user = None, passowrd = None):
        self.host = host
        self.user = user
        self.password = passowrd
        self.client = None
        self.scp = None
        self.vbcs_conn = None
        self.vbcs_user_shell = None
        self.vbcs_root_shell = None
        self.stdout = None
        self.stdin = None
        self.stderr = None
        
    def login(self, host, user, passowrd):
        self.host = host
        self.user = user
        self.password = passowrd
        return self._connect(self.host, self.user, self.password)

        pass
    def _connect(self, host, user, passowrd):
        """Open connection to remote host. """
        if self.vbcs_conn is None:
            try:
                self.client = SSHClient()
                self.client.load_system_host_keys()
                self.client.set_missing_host_key_policy(AutoAddPolicy())
                user_ssh_cfg_file = os.path.expanduser("~/.ssh/config")
                userSshConfig = SSHConfig()
                userSshConfig.parse(open(user_ssh_cfg_file))
                user_config = userSshConfig.lookup(self.host)
                self.client.connect(
                    self.host,
                    username=self.user,
                    password=self.password,
                    sock=ProxyCommand(user_config['proxycommand']),
                    timeout=10
                )
                self.vbcs_conn = self.client
            except AuthenticationException as error:
                print(f'Authentication failed: did you remember to create an SSH key? {error}')
                raise error
        return self.client

    def enter_user_shell(self):
        """
        This function is for getting the remote shell as normal user
        :return: A shell with user id
        """
        try:
            if self.vbcs_conn == None:
                print("Please logging into the server < login/_connect > Before before invoking user shell .....")
                return None
            self.vbcs_user_shell = self.vbcs_conn.invoke_shell(term='vt100')
            self.stdout = self.vbcs_user_shell.makefile('rb', MAX_BUFFER)
            self.stdin = self.vbcs_user_shell.makefile_stdin('wb', MAX_BUFFER)
            self.stderr = self.vbcs_user_shell.makefile_stderr('rb', MAX_BUFFER)
            self.vbcs_user_shell.send('export PS1="[PARAMIKO_PROMPT]# "' + '\n'); sleep(0.2)
            self.vbcs_user_shell.send('stty -echo; unalias -a' + '\n'); sleep(0.25)
            self.vbcs_user_shell.send(DEMO_COMMAND); sleep(0.5)

            clear_buffer(self.stdout)

        except ConnectionError as error:
            print(f'ConnectionError: did you remember to create an SSH key? {error}')
            raise error
        return self.vbcs_user_shell

    def _enter_root_shell(self, wait = 0):
        """
        This function is for getting the remote shell as root user
        :return: A shell with root id
        """

        try:
            tmp_shell = self.enter_user_shell()
            tmp_shell.send('pbrun root-policy -u root\n'); sleep(wait + 1)
            clear_buffer(self.stdout)

            tmp_shell.send(self.password + '\n'); sleep(wait + 0.5)
            clear_buffer(self.stdout)

            tmp_shell.send('export PS1="[PARAMIKO_PROMPT]# "' + '\n'); sleep(wait + 0.25)
            tmp_shell.send('stty -echo' + '\n'); sleep(0.25)
            clear_buffer(self.stdout)

            self.vbcs_root_shell = tmp_shell

        except ConnectionError as error:
            print(f'ConnectionError: did you remember to create an SSH key? {error}')
            raise error
        return self.vbcs_root_shell

    def enter_root_shell(self):
        retry = 0; shell = None
        while retry < 3:
            shell = self._enter_root_shell(wait=retry)
            output, rc = self.run_command('whoami')
            print("retry root shell : ", output)
            if output.strip('\r\n') == "root":
                break
            else: retry = retry + 1
        return shell

    def run_command(self, command):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        :type commands: List[str]
        """

        if self.vbcs_conn == None:
            print("Please invoke < _connect => enter_user_shell > Before running any command .....")
            return None, None
        if self.vbcs_user_shell == None:
            print("Please invoke < enter_user_shell > Before running any command .....")
            return None, None

        self.stdin.channel.send( command + '\necho COMMAND_EXIT_CODE: $?\n' )
        self.stdin.flush(); sleep(0.5)
        raw_output = b''
        while True:
            if self.stdout.channel.recv_ready():
                raw_output = raw_output + self.stdout.channel.recv(MAX_BUFFER) #).decode('ascii')
            if regexRC.search(raw_output.decode('ascii')): break
            else: sleep(0.1); continue

        output, rc = extract_output(raw_output)
            
        return output, rc

    def print_formated_output(self, output = None, rc = None):
        for line in output.split('\r\n'):
            print(line)
        if rc is not None:
            print('\n RETURN_CODE : %d', int(rc))
        return

    def _upload_single_file(self, file):
        """Upload a single file to a remote directory."""
        upload = None
        try:
            self.scp.put(
                file,
                recursive=True,
                remote_path=self.remote_path
            )
            upload = file
        except SCPException as error:
            print(error)
            raise error
        finally:
            print(f'Uploaded {file} to {self.remote_path}')
            return upload

    def download_file(self, file):
        """Download file from remote host."""
        self.conn = self._connect()
        self.scp.get(file)

    def disconnect(self):
        """Close ssh connection."""
        if self.client:
            self.client.close()
        if self.scp:
            self.scp.close()

    def bulk_upload(self, files):
        """
        Upload multiple files to a remote directory.

        :param files: List of paths to local files.
        :type files: List[str]
        """
        self.conn = self._connect()
        uploads = [self._upload_single_file(file) for file in files]
        print(f'Finished uploading {len(uploads)} files to {self.remote_path} on {self.host}')

    def exit_root_shell(self):
        """
        THis funtion for exiting from root shell
        :return: None
        """
        self.vbcs_root_shell.send('exit' + '\n')
        self.vbcs_root_shell = None
        return True

    def exit_user_shell(self):
        """
        THis funtion for exiting from root shell
        :return: None
        """
        self.vbcs_user_shell.send('exit' + '\n')
        self.vbcs_user_shell = None
        return True
