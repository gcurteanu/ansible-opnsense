from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_ip, is_network, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class DnsmasqHostV4(BaseModule):
    FIELD_ID = 'ip'
    CMDS = {
        'add': 'add_host',
        'del': 'del_host',
        'set': 'set_host',
        'search': 'search_host',
        'detail': 'get_host',
    }
    API_KEY_PATH = 'host'
    API_MOD = 'dnsmasq'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'mac', 'hostname', 'description', 'domain', 'local',
    ]
    FIELDS_TYPING = {
        'bool': ['local'],
        'select_opt_list': ['ip', 'mac'],
    }
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'hostname': 'host',
        'mac': 'hwaddr',
        'description': 'descr',
    }
    EXIST_ATTR = 'hostname'
    SEARCH_DETAIL_ALL = False


    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.hostname = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['mac']):
                self.m.fail_json(
                    "You need to provide a 'mac' if you want to create a reservation!"
                )

            if not is_ip(self.p['ip']):
                self.m.fail_json('The provided IP is invalid!')

        self._base_check()
