
import fire
from fire import *
from analysis_module import *
from global_module import *

urllib3.disable_warnings()

# inbound uses client address exclusions

# create EH API header


def inb_data_call(json_body, record_format_selection, time_selection):
    json_body['types'].append(EH_RECORD_TYPE_OPTS[record_format_selection])
    json_body['from'] = '-{0}h'.format(time_selection)

    # read the exclusions from config, create a new rule for each address, and append to the rules portion of the query
    # for interesting inbounds, we don't want local clients
    for addr in INBOUND_ADDR_EXCLUSIONS:
        rule_base = {"field": "clientAddr",
                     "operand": "{0}".format(addr),
                     "operator": "!="}

        json_body['filter']['rules'].append(rule_base)
    return json_body

# record_choice = input('Pick record type: (cifs, ldap, ssh, rdp, ssl, ftp, dns, smtp, tcp, http)\n')
# time_choice = input('Number of hours to go back in time:\n')

# direction_choice = input('Traffic direction (inbound/outbound):\n') this is for a CLI with main.
# it would branch to inbound or outbound. right now the exclusions are wrapped up in this module


def generate_in(record_choice, time_choice):
    print('inbound')
    direction_choice = 'inbound'
    json = inb_data_call(EH_CALL_BASE, record_choice, time_choice)
    get_intel_data(EH_API_ENDPOINT, EH_HEADER_INFO, json, direction_choice, record_choice)


if __name__ == '__main__':
    fire.Fire(generate_in)

