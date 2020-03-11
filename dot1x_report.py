#!/usr/local/bin/python3
'''
This script is to create a report on switches with dot1x enabled
'''

import os, sys, time, json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pywaffle import Waffle
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from ttp import ttp
from pprint import pprint as pp


# Run show commands on each switch
def get_dot1x_status(task):

    print(f'{task.host}: checking dot1x status.')
    # run "show dot1x all" on each host
    sh_dot1x = task.run(
        task=netmiko_send_command,
        command_string="show dot1x all",
    )

    # TTP template for dot1x status
    dot1x_ttp_template = "Sysauthcontrol              {{ status }}"

    # magic TTP parsing
    parser = ttp(data=sh_dot1x.result, template=dot1x_ttp_template)
    parser.parse()
    dot1x_status = json.loads(parser.result(format='json')[0])

    print(dot1x_status[0]['status'])
    return dot1x_status[0]['status']

def main():
    enabled = 0 
    enabled_hosts = []
    disabled = 0 
    disabled_hosts = []
    errored = 0
    errored_hosts = []
    # initialize The Norn
    nr = InitNornir()
    # filter The Norn
    nr = nr.filter(platform="cisco_ios")
    # run The Norn run commands
    dot1x_result = nr.run(task=get_dot1x_status)

    for host in dot1x_result:
        
        if dot1x_result[host].result == 'Enabled':
            enabled += 1 
            enabled_hosts.append(host)
        elif dot1x_result[host].result == 'Disabled':
            disabled += 1 
            disabled_hosts.append(host)
        else:
            print(dot1x_result[host].result)
            errored += 1
            errored_hosts.append(host)

    print(f"Enabled: {enabled}")
    print(f"Disabled: {disabled}")
    print(f"Error: {errored}")
    print(f"\nFailed hosts:")
    pp(nr.data.failed_hosts)
    print(f"\nDisabled hosts:")
    pp(disabled_hosts)
    print(f"\nEnabled hosts:")
    pp(enabled_hosts)


    enabled = 10
    disabled = 550

    #col = int((enabled + disabled) ** 0.5)

    wafflez = plt.figure(
        FigureClass=Waffle,
        columns=30,
        #rows=rows,
        title={
            'label': 'dot1x deployment progress',
            'loc': 'left',
            'fontdict': {
                'fontsize': 25
            }
        },
        #plot_anchor='C',
        values={
            'switch stacks with\ndot1x enabled': enabled, 
            'switch stacks with\ndot1x disabled': disabled
        },
        legend={'loc': 'lower left','bbox_to_anchor': (0, -0.3),'ncol': 2},
        icons=['lock','lock-open'],
        font_size=10,
        colors=["#008000", "#F51B00"],
    )


    #pp = PdfPages('dot1x_report.pdf')
    #plt.savefig(pp, format='pdf')
    #pp.close()

    #plt.show(wafflez)


if __name__ == "__main__":
    main()
