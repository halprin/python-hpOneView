# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# An existent Logical Downlink ID is required to run this example
logical_downlink_id = '246c3202-f4c8-4c92-9266-5e7b01c0598e'

# Get logical downlink by id
try:
    print("Get logical downlink by id")
    log_downlink = oneview_client.logical_downlinks.get(logical_downlink_id)
    pprint(log_downlink)
except HPOneViewException as e:
    print(e.msg)

# Get logical downlink by id without Ethernet networks
try:
    print("Get logical downlink by id without Ethernet networks")
    log_downlink_without_ethernet = oneview_client.logical_downlinks.get_without_ethernet(logical_downlink_id)
    pprint(log_downlink_without_ethernet)
except HPOneViewException as e:
    print(e.msg)

# Get all logical downlinks
print("Get all logical downlinks")
log_downlinks = oneview_client.logical_downlinks.get_all()
pprint(log_downlinks)

# Get all sorting by name descending
print("Get all logical downlinks sorting by name")
log_downlinks_sorted = oneview_client.logical_downlinks.get_all(
    sort='name:descending')
pprint(log_downlinks_sorted)

# Get all logical downlinks without Ethernet
print("Get all logical downlinks without Ethernet")
log_downlinks_without_ethernet = oneview_client.logical_downlinks.get_all_without_ethernet()
pprint(log_downlinks_without_ethernet)
