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

    return dot1x_status[0]['status']

def main():
    count = 0 
    # initialize The Norn
    nr = InitNornir()
    # filter The Norn
    nr = nr.filter(platform="cisco_ios")
    # run The Norn run commands
    dot1x_result = nr.run(task=get_dot1x_status)

    for host in dot1x_result:
        print(host)
        print(dot1x_result[host].result)

    
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
