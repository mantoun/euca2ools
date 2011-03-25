# Software License Agreement (BSD License)
#
# Copyright (c) 20092011, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Neil Soman neil@eucalyptus.com
#         Mitch Garnaat mgarnaat@eucalyptus.com


import euca2ools.commands.eucacommand
from boto.roboto.param import Param

class Register(euca2ools.commands.eucacommand.EucaCommand):

    Description = 'Registers a manifest for use with the cloud.'
    Options = [Param(name='block_device_mapping',
                     short_name='b', long_name='block-device-mapping',
                     optional=True, ptype='string', cardinality='*',
                     doc="""Block device mapping for the instance(s).
                     Option may be used multiple times."""),
               Param(name='description',
                     short_name='d', long_name='description',
                     optional=True, ptype='string',
                     doc='Description of the image.'),
               Param(name='name', short_name='n', long_name='name',
                     optional=True, ptype='string',
                     doc='Name of the image.'),
               Param(name='architecture',
                     short_name='a', long_name='architecture',
                     optional=True, ptype='string', default='i386',
                     doc="""The architecture of the image.
                     Valid values are: i386 | x86_64"""),
               Param(name='kernel', long_name='kernel',
                     optional=True, ptype='string',
                     doc='The ID of the kernel associated with the image.'),
               Param(name='ramdisk', long_name='ramdisk',
                     optional=True, ptype='string',
                     doc='The ID of the ramdisk associated with the image.'),
               Param(name='root_device_name', long_name='root-device-name',
                     optional=True, ptype='string',
                     doc='The root device name (e.g., /dev/sda1, or xvda).'),
               Param(name='snapshot', short_name='s', long_name='snapshot',
                     optional=True, ptype='string',
                     doc='The snapshot ID to use as the root device.')]
    Args = [Param(name='image_location',
                  optional=False, ptype='string',
                  doc='path to the uploaded image (bucket/manifest).')]
               
    def main(self):
        image_location = self.arguments['image_location']
        block_device_map = self.options.get('block_device_mapping', [])
        description = self.options.get('description', None)
        image_name = self.options.get('name', None)
        architecture = self.options.get('architecture', 'i386')
        kernel = self.options.get('kernel', None)
        ramdisk = self.options.get('ramdisk', None)
        root_device_name = self.options.get('root_device_name', None)
        snapshot = self.options.get('snapshot', None)

        if self.snapshot:
            if not self.root_device_name:
                self.root_device_name = '/dev/sda1'
            self.block_device_map.append('%s=%s' % (self.root_device_name,
                                                    self.snapshot))
        if self.block_device_map:
            self.block_device_map = self.parse_block_device_args(self.block_device_map)
        conn = self.make_connection_cli()
        return self.make_request_cli(conn, 'register_image',
                                     name=self.image_name,
                                     description=self.description,
                                     image_location=self.image_location,
                                     architecture=self.architecture,
                                     kernel_id=self.kernel,
                                     ramdisk_id=self.ramdisk,
                                     root_device_name=self.root_device_name,
                                     block_device_map=self.block_device_map)

    def main_cli(self):
        image_id = self.main()
        if image_id:
            print 'IMAGE\t%s' % image_id
