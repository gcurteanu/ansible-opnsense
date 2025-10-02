#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/kea.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.dnsmasq import DnsmasqMain

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/dhcp.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/modules/dhcp.html'


def run_module():
    module_args = dict(
        ip=dict(
            type='str', required=True,
            description='IP address to offer to the client',
        ),
        mac=dict(
            type='str', required=False,
            description='MAC/Ether address of the client in question',
        ),
        hostname=dict(
            type='str', required=False,
            description='Offer a hostname to the client',
        ),
        domain=dict(
            type='str', required=False,
            description='Domain of the client',
        ),
        local=dict(
            type='bool', required=False, default=True,
            description='If set, this will configure this DNS server as authoritative; it will not forward queries to any upstream servers for this domain.',
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module_wrapper(DnsmasqHostV4(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
