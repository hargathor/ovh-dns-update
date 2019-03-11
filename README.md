# ovh-dns-update
Small script to auto update an OVH dns when your public IP changes

# Configuration

Create your `ovh.conf` file with your application_key, application_secret and consumer_key in `/etc/ovh.conf`, `~/.ovh.conf` or in the same directory as the script 

```properties
[default]
; general configuration: default endpoint
endpoint=ovh-eu
; check other endpoint on ovh https://api.ovh.com/

[ovh-eu]
; configuration specific to 'ovh-eu' endpoint
application_key=your_application_key
application_secret=your_application_secret
; uncomment following line when writing a script application
; with a single consumer key.
consumer_key=your_consumer_key

````

# Usage

To properly launch this script using docker
```bash
$ docker run -it --rm --name ovh-dns-update -v /var/log/ovh.log:/var/log/ovh.log -v "$PWD":/opt/app -w /opt/app python:3 bash -c 'pip install -r requirements.txt; python ovh-dns-auto-update.py'
```

To launch it as a command line just install the dependencies using pip and launch it
```bash
$ pip install -r requirements.txt
$ sudo cp ovh-dns-auto-update.py /usr/local/bin
$ ovh-dns-auto-update.py
````

Created to be launched as a cron command. Here is an example for an hourly launch
```bash
# m h  dom mon dow   command
@hourly /usr/local/bin/ovh-dns-auto-update.py
````

or if you want to use docker
```bash
# m h  dom mon dow   command
@hourly /usr/bin/docker run --rm --name ovh-dns-update -v /var/log/ovh.log:/var/log/ovh.log -v /opt/ovh-dns-update:/opt/app -w /opt/app python:3 bash -c 'pip install -r requirements.txt; python ovh-dns-auto-update.py'
````
