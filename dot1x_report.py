#!/usr/local/bin/python3
'''
This script is to create a report on switches with dot1x enabled
'''

import os, sys, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pywaffle import Waffle
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command


# Run show commands on each switch
def run_commands(task):
    print(f'{task.host}: running show comands.')
    # run "show version" on each host
    sh_dot1x = task.run(
        task=netmiko_send_command,
        command_string="show dot1x all",
        use_textfsm=True,
    )

    print(sh_dot1x.result)


def main():
  
    # initialize The Norn
    #nr = InitNornir()
    # filter The Norn
    #nr = nr.filter(platform="cisco_ios")
    # run The Norn run commands
    #nr.run(task=run_commands)
    
    enabled = 14
    disabled = 154

    rows = int((enabled + disabled) ** 0.5)

    wafflez = plt.figure(
        FigureClass=Waffle,
        
        rows=rows,
        title={
            'label': 'dot1x deployment progress',
            'loc': 'left',
            'fontdict': {
                'fontsize': 20
            }
        },
        #plot_anchor='C',
        values={
            'switch stacks with\ndot1x enabled': enabled, 
            'switch stacks with\ndot1x disabled': disabled
        },
        legend={'loc': 'lower left','bbox_to_anchor': (0, -0.3),'ncol': 2},
        icons=['lock','lock-open'],
        #font_size=25,
        colors=["#008000", "#F51B00"],
        rounding_rule='floor'
    )


    #pp = PdfPages('dot1x_report.pdf')
    #plt.savefig(pp, format='pdf')
    #pp.close()

    plt.show(wafflez)

if __name__ == "__main__":
    main()
