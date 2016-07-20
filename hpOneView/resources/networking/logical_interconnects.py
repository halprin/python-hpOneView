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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

__title__ = 'Logical Interconnects'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class LogicalInterconnects(object):

    URI = '/rest/logical-interconnects'
    FIRMWARE_PATH = "/firmware"
    LOCATIONS_PATH = "/locations/interconnects"
    locations_uri = "{uri}{locations}".format(uri=URI, locations=LOCATIONS_PATH)

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of logical interconnects based on optional sorting and filtering, and constrained by start
        and count parameters.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all the items.
                The actual number of items in the response may differ from the requested
                count if the sum of start and count exceed the total number of items, or
                if returning the requested number of items would take too long.
            filter:
                A general filter/query string to narrow the list of items returned. The
                default is no filter - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time, with the oldest entry first.

        Returns:
            list: A list of logical interconnects

        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets a logical interconnect by ID or by uri

        Args:
            id_or_uri: Could be either the logical interconnect id or the logical interconnect uri

        Returns:
            dict: The logical interconnect
        """
        return self._client.get(id_or_uri)

    def get_by_name(self, name):
        """
        Gets a logical interconnect by name.

        Args:
            name: Name of the logical interconnect

        Returns: Logical Interconnect
        """
        logical_interconnects = self._client.get_all()
        result = [x for x in logical_interconnects if x['name'] == name]
        return result[0] if result else None

    def update_compliance(self, id_or_uri, timeout=-1):
        """
        Returns logical interconnects to a consistent state. The current logical interconnect state is
        compared to the associated logical interconnect group.

        Any differences identified are corrected, bringing the logical interconnect back to a consistent
        state. Changes are asynchronously applied to all managed interconnects. Note that if the changes detected
        involve differences in the interconnect map between the logical interconnect group and the logical interconnect,
        the process of bringing the logical interconnect back to a consistent state may involve automatically removing
        existing interconnects from management and/or adding new interconnects for management.

        Args:
            id_or_uri: Could be either the resource id or the resource uri
            timeout: Timeout in seconds. Wait task completion by default. The timeout do not abort the operation
                in OneView, just stop waiting its completion.

        Returns: Logical Interconnect
        """
        uri = self._client.build_uri(id_or_uri) + "/compliance"
        return self._client.update_with_zero_body(uri, timeout=timeout)

    def update_ethernet_settings(self, id_or_uri, configuration, force=False, timeout=-1):
        """
        Updates the Ethernet interconnect settings for the logical interconnect.

        Args:
            id_or_uri: Could be either the resource id or the resource uri
            configuration:  Ethernet interconnect settings.
            force: If set to true the operation completes despite any problems with network connectivity or errors
                on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait task completion by default. The timeout do not abort the operation
                in OneView, just stop waiting its completion.

        Returns: Logical Interconnect
        """
        uri = self._client.build_uri(id_or_uri) + "/ethernetSettings"
        return self._client.update(configuration, uri=uri, force=force, timeout=timeout)

    def update_internal_networks(self, id_or_uri, network_uri_list, force=False, timeout=-1):
        """
        Updates internal networks on the logical interconnect.

        Args:
            id_or_uri: Could be either the resource id or the resource uri
            network_uri_list: List of Ethernet network uris.
            force: If set to true the operation completes despite any problems with network connectivity or errors
                on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait task completion by default. The timeout do not abort the operation
                in OneView, just stop waiting its completion.

        Returns: Logical Interconnect
        """
        uri = self._client.build_uri(id_or_uri) + "/internalNetworks"
        return self._client.update(network_uri_list, uri=uri, force=force, timeout=timeout)

    def get_internal_vlans(self, id_or_uri):
        """
        Gets the internal VLAN IDs for the provisioned networks on a logical interconnect.

        Args:
            id_or_uri: Could be either the logical interconnect group id or the logical interconnect group uri

        Returns:
            dict: Collection of URIs

        """
        uri = self._client.build_uri(id_or_uri) + "/internalVlans"
        return self._client.get_collection(uri)

    def update_settings(self, id_or_uri, settings, force=False, timeout=-1):
        """
        Updates interconnect settings on the logical interconnect. Changes to interconnect settings are asynchronously
        applied to all managed interconnects.

        Args:
            id_or_uri: Could be either the resource id or the resource uri
            settings: Interconnect settings
            force: If set to true the operation completes despite any problems with network connectivity or errors
                on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait task completion by default. The timeout do not abort the operation
                in OneView, just stop waiting its completion.

        Returns: Logical Interconnect
        """
        data = settings.copy()
        if 'type' not in data:
            data['type'] = 'InterconnectSettingsV3'
        if 'ethernetSettings' in data and 'type' not in data['ethernetSettings']:
            data['ethernetSettings']['type'] = 'EthernetInterconnectSettingsV3'

        uri = self._client.build_uri(id_or_uri) + "/settings"
        return self._client.update(data, uri=uri, force=force, timeout=timeout)

    def update_configuration(self, id_or_uri, timeout=-1):
        """
        Asynchronously applies or re-applies the logical interconnect configuration to all managed interconnects.

        Args:
            id_or_uri: Could be either the resource id or the resource uri
            timeout: Timeout in seconds. Wait task completion by default. The timeout do not abort the operation
                in OneView, just stop waiting its completion.

        Returns: Logical Interconnect
        """
        uri = self._client.build_uri(id_or_uri) + "/configuration"
        return self._client.update_with_zero_body(uri=uri, timeout=timeout)

    def get_unassigned_uplink_ports(self, id_or_uri):
        """
        Gets a collection of uplink ports from the member interconnects which are eligible for assignment to an
        analyzer port. To be eligible a port must be a valid uplink, must not be a member of an existing uplink set
        and must not currently be used for stacking.

        Args:
            id_or_uri: Could be either the logical interconnect group id or the logical interconnect group uri

        Returns:
            dict: Collection of uplink ports
        """
        uri = self._client.build_uri(id_or_uri) + "/unassignedUplinkPortsForPortMonitor"
        return self._client.get_collection(uri)

    def get_telemetry_configuration(self, telemetry_configuration_uri):
        """
        Gets the telemetry configuration of a logical interconnect.

        Args:
            telemetry_configuration_uri: Telemetry Configuration URI

        Returns:
            dict: Telemetry configuration

        """
        return self._client.get(telemetry_configuration_uri)

    def create_interconnect(self, location_entries, timeout=-1):
        """
        Creates an interconnect at the given location.

        WARN: It does not create the LOGICAL INTERCONNECT itself.
        It will fail if no interconnect is already present on the specified position.

        Args:
            location_entries: dictionary with location entries
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout do not abort the operation
                in OneView, just stop waiting its completion.

        Returns: Created interconnect.
        """
        return self._client.create(location_entries, uri=self.locations_uri, timeout=timeout)

    def delete_interconnect(self, enclosure_uri, bay, timeout=-1):
        """
        Deletes an interconnect from a location.

        WARN: This won't delete the LOGICAL INTERCONNECT itself, and may cause inconsistency between the enclosure
        and Logical Interconnect Group.

        Args:
            enclosure_uri: URI of the Enclosure
            bay: Bay
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout do not abort the operation
                in OneView, just stop waiting its completion.

        Returns: bool: indicating if the interconnect was successfully deleted.
        """
        uri = "{locations_uri}?location=Enclosure:{enclosure_uri},Bay:{bay}".format(locations_uri=self.locations_uri,
                                                                                    enclosure_uri=enclosure_uri,
                                                                                    bay=bay)
        return self._client.delete(uri, timeout=timeout)

    def get_firmware(self, id_or_uri):
        """
        Gets the installed firmware for a logical interconnect.

        Args:
            id_or_uri: Could be either the logical interconnect id or the logical interconnect uri

        Returns:
            dict: LIFirmware
        """
        firmware_uri = self.__build_firmware_uri(id_or_uri)
        return self._client.get(firmware_uri)

    def install_firmware(self, firmware_information, id_or_uri):
        """
        Installs firmware to a logical interconnect. The three operations that are supported for the firmware
        update are Stage (uploads firmware to the interconnect), Activate (installs firmware on the interconnect)
        and Update (which does a Stage and Activate in a sequential manner).

        Returns:
            dict:
        """
        firmware_uri = self.__build_firmware_uri(id_or_uri)
        return self._client.update(firmware_information, firmware_uri)

    def __build_firmware_uri(self, id_or_uri):
        return self._client.build_uri(id_or_uri) + self.FIRMWARE_PATH
