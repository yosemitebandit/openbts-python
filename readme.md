a Python client for the OpenBTS NodeManager,
providing access to OpenBTS, SMQueue, SIPAuthServe and NodeManager itself


### installation
    $ pip install openbts


### usage
these examples come from Ch10 of the OpenBTS 4.0 manual

    # read a config value from a running openbts instance
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
    response = sipauthserve_connection.create_subscriber()
    print response.status_code
    # 204


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
