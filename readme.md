a Python client for the OpenBTS NodeManager,
providing access to components in the OpenBTS application suite:
SMQueue, SIPAuthServe, and OpenBTS itself.


### requirements
* OpenBTS 5.0 public alpha (tested on `11465a2`)
* Python 2.7


### installation

```shell
$ pip install openbts
```


### usage

```python
# read a config value from a running OpenBTS instance
import openbts
openbts_connection = openbts.components.OpenBTS()
response = openbts_connection.read_config('GSM.Radio.Band')
print response.data['value']
# 900

# update a config value
response = openbts_connection.update_config('GSM.Identity.MCC', 672)
print response.code
# 204
```


### license
MIT


### releases
* 0.0.2 - config reading and updating for the OpenBTS component
* 0.0.1 - barebones setup for pypi


### resources
* see the [OpenBTS 4.0 manual](http://openbts.org/site/wp-content/uploads/2014/07/OpenBTS-4.0-Manual.pdf)
* and the [NodeManager source](https://github.com/RangeNetworks/NodeManager) from Range


### testing
run unit tests with `nose`:

```shell
$ nosetests --detailed-errors
```

We have quite a few similar unit tests between components.
Many could be written against `openbts.core.BaseComponent`, as the components
all inherit from this single class.  But it seems better to individually
inspect the functionality of each class in `openbts.components`. Anyway,
onward..

Running the integration tests requires one to have a live OpenBTS instance
running on the same machine.  The test will modify real system parameters,
so run it with caution, or better yet, run it against a system not in prod.

```shell
$ python integration_test.py
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

bump the versions in `setup.py` and in this file, then run:

```shell
$ git tag 0.0.1 -m 'openbts-python v0.0.1'
$ git push origin master --tags
$ python setup.py sdist upload -r pypi
```
