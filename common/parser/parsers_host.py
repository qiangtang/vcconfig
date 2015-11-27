import ConfigParser
from common import operations
from common import utils


def _get_vc():
    cf = ConfigParser.ConfigParser()
    cf.read(utils.CONFIG_FILE_PATH)
    vc_ip = cf.get(utils.VC_SECTION, 'vc_ip')
    vc_user = cf.get(utils.VC_SECTION, 'vc_user')
    vc_pwd = cf.get(utils.VC_SECTION, 'vc_pwd')
    return operations.get_vcenter(vc_ip, vc_user, vc_pwd)


def config_service(args):
    vc = _get_vc()
    operations.cfg_esxi_service(vc, args.hosts, args.service, args.action)


def config_service_parser(subparsers):
    parser = subparsers.add_parser(
        'host-service',
        help='Start/stop service on target host.'
    )
    parser.add_argument(
        '--host',
        action='store',
        required=True,
        help='Target host list. Support single ip/fqdn or ip-range. '
             'Separated by comma',
        dest='hosts'
    )
    parser.add_argument(
        '--action',
        action='store',
        required=True,
        help='Action for the service. start/stop',
        choices=['start', 'stop'],
        dest='action'
    )
    parser.add_argument(
        '--service',
        action='store',
        required=True,
        help='Service to be config',
        choices=utils.SERVICES,
        dest='service'
    )
    parser.set_defaults(func=config_service)


def config_rule(args):
    vc = _get_vc()
    operations.cfg_esxi_fw_rule(vc, args.hosts, args.rule, args.action)


def config_rule_parser(subparsers):
    parser = subparsers.add_parser(
        'host-rule',
        help='Enable/disable firewall rule on target host.'
    )
    parser.add_argument(
        '--host',
        action='store',
        required=True,
        help='Target host list. Support single ip/fqdn or ip-range. '
             'Separated by comma',
        dest='hosts'
    )
    parser.add_argument(
        '--action',
        action='store',
        required=True,
        help='Action for the rule. enable/disable',
        choices=['enable', 'disable'],
        dest='action'
    )
    parser.add_argument(
        '--rule',
        action='store',
        required=True,
        help='Rule to be config',
        choices=utils.RULES,
        dest='rule'
    )
    parser.set_defaults(func=config_rule)


def maintenance(args):
    vc = _get_vc()
    hosts = operations.get_host_list(args.hosts)
    for host_name in hosts:
        host = vc.get_host_by_name(host_name)
        host.maintenance(args.action)


def maintenance_parser(subparsers):
    parser = subparsers.add_parser(
        'host-maintain',
        help='Enter/exit maintenance mode on target host.'
    )
    parser.add_argument(
        '--host',
        action='store',
        required=True,
        help='Target host list. Support single ip/fqdn or ip-range. '
             'Separated by comma',
        dest='hosts'
    )
    parser.add_argument(
        '--action',
        action='store',
        required=True,
        help='Action for the host. enter/exit',
        choices=['enter', 'exit'],
        dest='action'
    )
    parser.set_defaults(func=maintenance)


def config_vmotion(args):
    vc = _get_vc()
    operations.cfg_esxi_vmotion(vc, args.hosts, args.nic)


def config_vmotion_parser(subparsers):
    parser = subparsers.add_parser(
        'host-vmotion',
        help='Enable vMotion on target host.'
    )
    parser.add_argument(
        '--host',
        action='store',
        required=True,
        help='Target host list. Support single ip/fqdn or ip-range. '
             'Separated by comma',
        dest='hosts'
    )
    parser.add_argument(
        '--nic-num',
        action='store',
        type=int,
        help='[Optional] Virtual Nic number used for vMotion. 0 by default.',
        default=0,
        dest='nic'
    )
    parser.set_defaults(func=config_vmotion)


def config_autostart(args):
    vc = _get_vc()
    operations.cfg_autostart(vc, args.host, args.vms)


def config_autostart_parser(subparsers):
    parser = subparsers.add_parser(
        'host-autostart',
        help='Config auto start for VMs on the target host.'
    )
    parser.add_argument(
        '--host',
        action='store',
        required=True,
        help='Target host which the vms on',
        dest='host'
    )
    parser.add_argument(
        '--vm',
        action='store',
        required=True,
        help='Name list of VM to enable auto start func. First position '
             'with first priority. Separated by comma',
        dest='vms'
    )
    parser.set_defaults(func=config_autostart)