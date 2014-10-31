a Python client for the OpenBTS NodeManager,
providing access to OpenBTS, SMQueue, SIPAuthServe and NodeManager itself


### installation

```shell
$ pip install openbts
```


### usage
these examples come from chapter 10 of the
[OpenBTS 4.0 manual](http://openbts.org/site/wp-content/uploads/2014/07/OpenBTS-4.0-Manual.pdf)

```python
# read a config value from a running OpenBTS instance
import openbts
openbts_connection = openbts.OpenBTS()
response = openbts_connection.read_config('GSM.Radio.Band')
print response.value
# 900

# set an SMQueue parameter
import openbts
smqueue_connection = openbts.SMQueue()
response = smqueue_connection.update_config('SIP.myIP2', '192.168.0.22')
print response.status
# ok

# create a new subscriber
import openbts
sipauthserve_connection = openbts.SIPAuthServe()
response = sipauthserve_connection.create_subscriber(name='matt', imsi='899', ki='+Z3m')
print response.status_code
# 204
```


### requirements
* OpenBTS 4.0
* Python 2.7


### resources
* see the [OpenBTS 4.0 manual](http://openbts.org/site/wp-content/uploads/2014/07/OpenBTS-4.0-Manual.pdf)
* and the [NodeManager source](https://github.com/RangeNetworks/NodeManager) from Range


### license
MIT


### releases
* 0.0.1 - barebones setup for pypi


### testing
test with `nose`:

```shell
$ nosetests --detailed-errors openbts/tests.py
```


### release process
you need a ~/.pypirc like this:

```
[distutils]
index-servers =
  pypi

[pypi]
repository: https://pypi.python.org/pypi
username: yosemitebandit
password: mhm
```

then run:

```shell
$ git tag 0.0.1 -m 'openbts-python v0.0.1'
$ git push origin master --tags
$ python setup.py sdist upload -r pypi
```
