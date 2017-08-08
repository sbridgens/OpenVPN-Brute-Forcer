# OpenVPN-Brute-Forcer
A very simple Password brute forcer for openvpn.

This was made for the Pentestit.ru v11 labs to learn bruteforce techniques.

It was a very quick script to acheive an aim so no apologies for the code.

REQUIREMENTS:

Python of course.
Server.conf/ovpn from the comprimised server
openvpn username
CA cert from the comprimised server: include in the server.conf or seperated into a crt file then reference

NOTE: Use the attached server.conf and update the crt path with the extracted ca certificate or edit your own to match i.e: Remove the auth-user-path line, comment out the remote lines and move the ca certificate into a seperate file from the server.conf file then execute.


SCRIPT EXECUTION:
```bash
python brute_openvpn.py --host 192.168.101.10 --config /home/scripts/python/server.conf --user xxxxxx --passlist /usr/share/john/password.lst
```

RESULT:
```ruby
[+] SUCCESS! command = /usr/sbin/openvpn --remote 192.168.101.10 --config /home/scripts/python/server.conf --auth-user-pass /tmp/sb_test/tmp4HdLuM
[+] Password: ***REMOVED***
[+] VPN Process stopped and temp files removed
Terminated
```

Please feel free to update.
