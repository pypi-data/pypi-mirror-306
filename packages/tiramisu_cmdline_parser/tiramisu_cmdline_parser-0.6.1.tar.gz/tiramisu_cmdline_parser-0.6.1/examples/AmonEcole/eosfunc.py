import re, random, ipaddress
def get_version(*args, **kwargs):
    return u'2.6.2'


def is_instanciate(*args, **kwargs):
    return 'oui'


def calc_val(valeur):
    return valeur


def concat(*args, **kwargs):
    """ concatène deux valeurs """
    sortedkeys = list(kwargs.keys())
    sortedkeys.sort()
    sortedkwvalues = []
    for key in sortedkeys:
        if kwargs[key] == '' or kwargs[key] is None:
            return None
        sortedkwvalues.append(kwargs[key])
    if None in args:
        return None
    return "".join(args)+''.join(sortedkwvalues)


def auto_dns(*args, **kwargs):
    return []


def calc_multi_condition(param, match=None, mismatch=None, operator='AND',
                         default_match=None, default_mismatch=None,
                         eval_match='False', eval_mismatch='False',
                         **conditions):
    if operator not in ('AND', 'OR'):
        raise ValueError(_(u'Operator must be either "AND" or "OR"'))
    if eval_match not in ('True', 'False'):
        raise ValueError(_(u'eval_match must be either "True" or "False"'))
    if eval_mismatch not in ('True', 'False'):
        raise ValueError(_(u'eval_mismatch must be either "True" or "False"'))
    if match is None:
        if default_match is None:
            match = u'oui'
        else:
            if default_match == 'None':
                match = None
            else:
                match = default_match
    if mismatch is None:
        if default_mismatch is None:
            mismatch = u'non'
        else:
            if default_mismatch == 'None':
                mismatch = None
            else:
                mismatch = default_mismatch
    conditions_keys = list(conditions.keys())
    conditions_keys.sort()
    for condition in conditions_keys:
        if not condition.startswith('condition_'):
            raise ValueError(_(u'Condition keys must start with "condition".'))
    # si le paramètre est une liste...
    if param.startswith('['):
        param = eval(param)
    # si il faut évaluer le résultat à retourner...
    if eval_match == 'True':
        match = eval(match)
    if eval_mismatch == 'True':
        mismatch = eval(mismatch)
    if isinstance(param, list) and len(param) != len(conditions):
        raise ValueError(_(u'Conditions and parameters counts do not match in calc_multi_condition.'))
    for num in range(0, len(conditions)):
        key = conditions_keys[num]
        value = conditions[key]
        if not isinstance(param, list):
            if operator == 'AND' and value != param:
                return mismatch
            if operator == 'OR' and value == param:
                return match
        else:
            if operator == 'AND' and value != param[num]:
                return mismatch
            if operator == 'OR' and value == param[num]:
                return match
    if operator == 'AND':
        return match
    else:
        return mismatch


auto_copy_val = calc_val


def activate_master_only_web_app(*args, **kwargs):
    return 'oui'


def calc_val_first_value(*args, **kwargs):
    if args == tuple():
        return None
    return args[0]


def valid_entier(*args, **kwargs):
    return True


def list_cdrom_devices(*args, **kwargs):
    return 'cdrom'


def cdrom_minormajor(*args, **kwargs):
    return 0


def calc_free_PE(*args, **kwargs):
    return 0


def enable_lv_creation(*args, **kwargs):
    return "oui"


def get_lv_names(*args, **kwargs):
    return "lvm"


def calc_multi_val(*args, **kwargs):
    res = []
    for arg in args:
        if arg is None:
            if kwargs.get('allow_none', u'False') == u'True':
                continue
            else:
                return []
        # gestion des valeurs multi
        if isinstance(arg, list):
            for ev_arg in arg:
                if ev_arg is not None and ev_arg not in res:
                    res.append(ev_arg)
        else:
            res.append(arg)
    return res


def check_partitioning_auto_extend(*args, **kwargs):
    return 'non'


def check_free_space(*args, **kwargs):
    return 0


def is_fs_type(*args, **kwargs):
    return "ext4"


def is_lv_name(*args, **kwargs):
    return "/etc"


def get_net_device(*args, **kwargs):
    return 'eth' + str(args[0])


def list_len_gt(param, max_len=None, match=None, mismatch=None,
                default_match=None, default_mismatch=None,
                eval_match='False', eval_mismatch='False',):
    if match is None:
        if default_match is None:
            match = u'oui'
        else:
            if default_match == 'None':
                match = None
            else:
                match = default_match
    if mismatch is None:
        if default_mismatch is None:
            mismatch = u'non'
        else:
            if default_mismatch == 'None':
                mismatch = None
            else:
                mismatch = default_mismatch
    # si il faut évaluer le résultat à retourner...
    if eval_match == 'True':
        match = eval(match)
    if eval_mismatch == 'True':
        mismatch = eval(mismatch)
    if isinstance(param, list):
        if len(param) > int(max_len):
            return match
        else:
            return mismatch
    else:
        return mismatch


def get_zone_name_bridge(*args, **kwargs):
    return "non"


def get_zone_name(*args, **kwargs):
    return 'eth0'

def auto_eth(*args, **kwargs):
    if kwargs['parametre'] == kwargs['condition']:
        return "192.168.1.1"


def auto_netmask(*args, **kwargs):
    if kwargs['parametre'] == kwargs['condition']:
        return "255.255.255.0"


def calc_or_auto_network(*args, **kwargs):
    if kwargs['parametre'] == kwargs['condition']:
        return "192.168.1.0"
    return calc_network(kwargs['ip'], kwargs['netmask'])


def calc_or_auto_broadcast(*args, **kwargs):
    if kwargs['parametre'] == kwargs['condition']:
        return "192.168.1.255"


def auto_defaultgw_ip(*args, **kwargs):
    if args[0] != 'statique':
        return "192.168.1.254"


def calc_network(ip, netmask):
    if None not in (ip, netmask):
        try:
            return str(ipaddress.ip_interface('{}/{}'.format(ip, netmask)).network.network_address)
        except:
            return None


def calc_broadcast(ip, netmask):
    if None not in (ip, netmask):
        return str(ipaddress.ip_interface('{}/{}'.format(ip, netmask)).network.broadcast_address)


def calc_ssl_country_name(*args, **kwargs):
    return 'FR'


def valid_country(*args, **kwargs):
    return


def valid_regexp(data, exp_reg, err_msg=u"Invalid syntax"):
    if data == "":
        return True
    match = re.match(exp_reg, data)
    if match is None:
        raise ValueError(err_msg)
    else:
        return True


def gen_random(*args, **kwargs):
    return '4444444444444444444'


def check_name_uniq(value, values, index):
    values.pop(index)
    if value in values:
        raise ValueError('le nom {} est déjà attribué à une autre plage'.format(value))


def calc_classe(*args, **kwargs):
    return "24"


def calc_webredirection(*args, **kwargs):
    return "/toto"


def calc_container(mode_container, container_info, mode_zephir='non'):
    return container_info


def calc_libelle_annuaire(*args, **kwargs):
    return "LDAP label"


def valid_differ(data, value):
    if data == value:
        raise ValueError(u"Value must be different from {0}".format(value))


def device_type(*args, **kwargs):
    return 'b'


def random_int(vmin, vmax, exclude=None):
    values = list(range(int(vmin), int(vmax)+1))
    if exclude != None and exclude in values:
        values.remove(exclude)
    return random.choice(values)
