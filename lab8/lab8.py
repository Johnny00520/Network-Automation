#!/bin/env python3

import yaml
from jinja2 import Environment, FileSystemLoader

#Load Jinja2
file_loader = FileSystemLoader('/etc/ansible/roles/router/templates/')
ENV = Environment(loader = file_loader)


with open("/etc/ansible/roles/router/vars/routers.yaml") as y:
    
    host_obj = yaml.load(y)

    for i in range(1, 4):
        print(i)
        jinjaTemplate = ENV.get_template('r'+str(i)+'.j2')

        f = open('r'+str(i)+'.conf', 'w')    

        config = jinjaTemplate.render(config=host_obj)
        #print(config)

        f.write(config)
        f.close()








#item = {
#    'hostname': 'R1',
#    'loopbacks': [ {
#        'int': 'Loopback 1',
#        'IPv4addr': '10.0.0.1 255.255.255.255'
#    }],
#    'interfaces': [ {
    
#    }],
#    'ospf': ''
#}


