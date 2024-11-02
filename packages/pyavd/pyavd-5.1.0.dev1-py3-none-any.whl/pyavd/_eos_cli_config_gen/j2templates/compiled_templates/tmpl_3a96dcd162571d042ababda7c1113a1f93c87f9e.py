from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-isis.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_isis = resolve('router_isis')
    l_0_spf_interval_cli = resolve('spf_interval_cli')
    l_0_wait_hold_interval_unit = resolve('wait_hold_interval_unit')
    l_0_isis_auth_cli = resolve('isis_auth_cli')
    l_0_both_key_ids = resolve('both_key_ids')
    l_0_lu_cli = resolve('lu_cli')
    l_0_ti_lfa_cli = resolve('ti_lfa_cli')
    l_0_ti_lfa_srlg_cli = resolve('ti_lfa_srlg_cli')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.filters['indent']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'indent' found.")
    try:
        t_4 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'instance')):
        pass
        yield '!\nrouter isis '
        yield str(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'instance'))
        yield '\n'
        if t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'net')):
            pass
            yield '   net '
            yield str(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'net'))
            yield '\n'
        if t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'router_id')):
            pass
            yield '   router-id ipv4 '
            yield str(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'router_id'))
            yield '\n'
        if t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'is_type')):
            pass
            yield '   is-type '
            yield str(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'is_type'))
            yield '\n'
        if t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'log_adjacency_changes'), True):
            pass
            yield '   log-adjacency-changes\n'
        elif t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'log_adjacency_changes'), False):
            pass
            yield '   no log-adjacency-changes\n'
        if t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'mpls_ldp_sync_default'), True):
            pass
            yield '   mpls ldp sync default\n'
        for l_1_redistribute_route in t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'redistribute_routes'), 'source_protocol'):
            l_1_redistribute_route_cli = resolve('redistribute_route_cli')
            _loop_vars = {}
            pass
            if t_4(environment.getattr(l_1_redistribute_route, 'source_protocol')):
                pass
                l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'isis'):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' instance', ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'ospf'):
                    pass
                    if t_4(environment.getattr(l_1_redistribute_route, 'include_leaked'), True):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (not t_4(environment.getattr(l_1_redistribute_route, 'ospf_route_type'))):
                        pass
                        continue
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'ospfv3'):
                    pass
                    if (not t_4(environment.getattr(l_1_redistribute_route, 'ospf_route_type'))):
                        pass
                        continue
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['static', 'connected']):
                    pass
                    if t_4(environment.getattr(l_1_redistribute_route, 'include_leaked'), True):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if t_4(environment.getattr(l_1_redistribute_route, 'route_map')):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                yield '   '
                yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                yield '\n'
        l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'timers'), 'local_convergence'), 'protected_prefixes'), True):
            pass
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'timers'), 'local_convergence'), 'delay')):
                pass
                yield '   timers local-convergence-delay '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'timers'), 'local_convergence'), 'delay'))
                yield ' protected-prefixes\n'
            else:
                pass
                yield '   timers local-convergence-delay protected-prefixes\n'
        if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'enabled')):
            pass
            yield '   set-overload-bit\n'
        if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup')):
            pass
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup'), 'delay')):
                pass
                yield '   set-overload-bit on-startup '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup'), 'delay'))
                yield '\n'
            elif t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup'), 'wait_for_bgp'), 'enabled'), True):
                pass
                if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup'), 'wait_for_bgp'), 'timeout')):
                    pass
                    yield '   set-overload-bit on-startup wait-for-bgp timeout '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup'), 'wait_for_bgp'), 'timeout'))
                    yield '\n'
                else:
                    pass
                    yield '   set-overload-bit on-startup wait-for-bgp\n'
        if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'advertise'), 'passive_only'), True):
            pass
            yield '   advertise passive-only\n'
        if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'interval')):
            pass
            l_0_spf_interval_cli = str_join(('spf-interval ', environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'interval'), ))
            context.vars['spf_interval_cli'] = l_0_spf_interval_cli
            context.exported_vars.add('spf_interval_cli')
            if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'interval_unit')):
                pass
                l_0_spf_interval_cli = str_join(((undefined(name='spf_interval_cli') if l_0_spf_interval_cli is missing else l_0_spf_interval_cli), ' ', environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'interval_unit'), ))
                context.vars['spf_interval_cli'] = l_0_spf_interval_cli
                context.exported_vars.add('spf_interval_cli')
                l_0_wait_hold_interval_unit = ' milliseconds'
                context.vars['wait_hold_interval_unit'] = l_0_wait_hold_interval_unit
                context.exported_vars.add('wait_hold_interval_unit')
            if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'wait_interval')):
                pass
                l_0_spf_interval_cli = str_join(((undefined(name='spf_interval_cli') if l_0_spf_interval_cli is missing else l_0_spf_interval_cli), ' ', environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'wait_interval'), t_1((undefined(name='wait_hold_interval_unit') if l_0_wait_hold_interval_unit is missing else l_0_wait_hold_interval_unit), ''), ))
                context.vars['spf_interval_cli'] = l_0_spf_interval_cli
                context.exported_vars.add('spf_interval_cli')
                if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'hold_interval')):
                    pass
                    l_0_spf_interval_cli = str_join(((undefined(name='spf_interval_cli') if l_0_spf_interval_cli is missing else l_0_spf_interval_cli), ' ', environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'hold_interval'), t_1((undefined(name='wait_hold_interval_unit') if l_0_wait_hold_interval_unit is missing else l_0_wait_hold_interval_unit), ''), ))
                    context.vars['spf_interval_cli'] = l_0_spf_interval_cli
                    context.exported_vars.add('spf_interval_cli')
            yield '   '
            yield str((undefined(name='spf_interval_cli') if l_0_spf_interval_cli is missing else l_0_spf_interval_cli))
            yield '\n'
        if (t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode')) and (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode') in ['md5', 'text']) or ((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode') == 'sha') and t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'sha'), 'key_id')))) or (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode') == 'shared-secret') and t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'shared_secret'), 'profile'))) and t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'shared_secret'), 'algorithm'))))):
            pass
            l_0_isis_auth_cli = str_join(('authentication mode ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode'), ))
            context.vars['isis_auth_cli'] = l_0_isis_auth_cli
            context.exported_vars.add('isis_auth_cli')
            if (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode') == 'sha'):
                pass
                l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' key-id ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'sha'), 'key_id'), ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
            elif (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode') == 'shared-secret'):
                pass
                l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' profile ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'shared_secret'), 'profile'), ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
                l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' algorithm ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'shared_secret'), 'algorithm'), ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'rx_disabled'), True):
                pass
                l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' rx-disabled', ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
            yield '   '
            yield str((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli))
            yield '\n'
        else:
            pass
            if (t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode')) and (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode') in ['md5', 'text']) or ((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode') == 'sha') and t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'sha'), 'key_id')))) or (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode') == 'shared-secret') and t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'shared_secret'), 'profile'))) and t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'shared_secret'), 'algorithm'))))):
                pass
                l_0_isis_auth_cli = str_join(('authentication mode ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode'), ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
                if (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode') == 'sha'):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' key-id ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'sha'), 'key_id'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                elif (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode') == 'shared-secret'):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' profile ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'shared_secret'), 'profile'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' algorithm ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'shared_secret'), 'algorithm'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'rx_disabled'), True):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' rx-disabled', ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                yield '   '
                yield str((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli))
                yield ' level-1\n'
            if (t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode')) and (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode') in ['md5', 'text']) or ((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode') == 'sha') and t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'sha'), 'key_id')))) or (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode') == 'shared-secret') and t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'shared_secret'), 'profile'))) and t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'shared_secret'), 'algorithm'))))):
                pass
                l_0_isis_auth_cli = str_join(('authentication mode ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode'), ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
                if (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode') == 'sha'):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' key-id ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'sha'), 'key_id'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                elif (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode') == 'shared-secret'):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' profile ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'shared_secret'), 'profile'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' algorithm ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'shared_secret'), 'algorithm'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'rx_disabled'), True):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' rx-disabled', ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                yield '   '
                yield str((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli))
                yield ' level-2\n'
        if t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart')):
            pass
            if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 'enabled'), True):
                pass
                yield '   graceful-restart\n'
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 't2'), 'level_1_wait_time')):
                pass
                yield '   graceful-restart t2 level-1 '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 't2'), 'level_1_wait_time'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 't2'), 'level_2_wait_time')):
                pass
                yield '   graceful-restart t2 level-2 '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 't2'), 'level_2_wait_time'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 'restart_hold_time')):
                pass
                yield '   graceful-restart restart-hold-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 'restart_hold_time'))
                yield '\n'
        if t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication')):
            pass
            l_0_both_key_ids = []
            context.vars['both_key_ids'] = l_0_both_key_ids
            context.exported_vars.add('both_key_ids')
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key_ids')):
                pass
                for l_1_auth_key in t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key_ids'), 'id'):
                    _loop_vars = {}
                    pass
                    if (((t_4(environment.getattr(l_1_auth_key, 'id')) and t_4(environment.getattr(l_1_auth_key, 'algorithm'))) and t_4(environment.getattr(l_1_auth_key, 'key_type'))) and t_4(environment.getattr(l_1_auth_key, 'key'))):
                        pass
                        context.call(environment.getattr((undefined(name='both_key_ids') if l_0_both_key_ids is missing else l_0_both_key_ids), 'append'), environment.getattr(l_1_auth_key, 'id'), _loop_vars=_loop_vars)
                        if t_4(environment.getattr(l_1_auth_key, 'rfc_5310'), True):
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' rfc-5310 key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield '\n'
                        else:
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield '\n'
                l_1_auth_key = missing
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key_ids')):
                pass
                for l_1_auth_key in environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key_ids'):
                    _loop_vars = {}
                    pass
                    if ((((t_4(environment.getattr(l_1_auth_key, 'id')) and (environment.getattr(l_1_auth_key, 'id') not in (undefined(name='both_key_ids') if l_0_both_key_ids is missing else l_0_both_key_ids))) and t_4(environment.getattr(l_1_auth_key, 'algorithm'))) and t_4(environment.getattr(l_1_auth_key, 'key_type'))) and t_4(environment.getattr(l_1_auth_key, 'key'))):
                        pass
                        if t_4(environment.getattr(l_1_auth_key, 'rfc_5310'), True):
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' rfc-5310 key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield ' level-1\n'
                        else:
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield ' level-1\n'
                l_1_auth_key = missing
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key_ids')):
                pass
                for l_1_auth_key in environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key_ids'):
                    _loop_vars = {}
                    pass
                    if ((((t_4(environment.getattr(l_1_auth_key, 'id')) and (environment.getattr(l_1_auth_key, 'id') not in (undefined(name='both_key_ids') if l_0_both_key_ids is missing else l_0_both_key_ids))) and t_4(environment.getattr(l_1_auth_key, 'algorithm'))) and t_4(environment.getattr(l_1_auth_key, 'key_type'))) and t_4(environment.getattr(l_1_auth_key, 'key'))):
                        pass
                        if t_4(environment.getattr(l_1_auth_key, 'rfc_5310'), True):
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' rfc-5310 key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield ' level-2\n'
                        else:
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield ' level-2\n'
                l_1_auth_key = missing
            if (t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key_type')) and t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key'))):
                pass
                yield '   authentication key '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key_type'))
                yield ' '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key'))
                yield '\n'
            else:
                pass
                if (t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key_type')) and t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key'))):
                    pass
                    yield '   authentication key '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key_type'))
                    yield ' '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key'))
                    yield ' level-1\n'
                if (t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key_type')) and t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key'))):
                    pass
                    yield '   authentication key '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key_type'))
                    yield ' '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key'))
                    yield ' level-2\n'
        yield '   !\n'
        if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'enabled'), True):
            pass
            yield '   address-family ipv4 unicast\n'
            if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'maximum_paths')):
                pass
                yield '      maximum-paths '
                yield str(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'maximum_paths'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'tunnel_source_labeled_unicast'), 'enabled'), True):
                pass
                l_0_lu_cli = 'tunnel source-protocol bgp ipv4 labeled-unicast'
                context.vars['lu_cli'] = l_0_lu_cli
                context.exported_vars.add('lu_cli')
                if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'tunnel_source_labeled_unicast'), 'rcf')):
                    pass
                    l_0_lu_cli = str_join(((undefined(name='lu_cli') if l_0_lu_cli is missing else l_0_lu_cli), ' rcf ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'tunnel_source_labeled_unicast'), 'rcf'), ))
                    context.vars['lu_cli'] = l_0_lu_cli
                    context.exported_vars.add('lu_cli')
                yield '      '
                yield str((undefined(name='lu_cli') if l_0_lu_cli is missing else l_0_lu_cli))
                yield '\n'
            if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'bfd_all_interfaces'), True):
                pass
                yield '      bfd all-interfaces\n'
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'mode')):
                pass
                l_0_ti_lfa_cli = str_join(('fast-reroute ti-lfa mode ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'mode'), ))
                context.vars['ti_lfa_cli'] = l_0_ti_lfa_cli
                context.exported_vars.add('ti_lfa_cli')
                if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'level')):
                    pass
                    l_0_ti_lfa_cli = str_join(((undefined(name='ti_lfa_cli') if l_0_ti_lfa_cli is missing else l_0_ti_lfa_cli), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'level'), ))
                    context.vars['ti_lfa_cli'] = l_0_ti_lfa_cli
                    context.exported_vars.add('ti_lfa_cli')
                yield '      '
                yield str((undefined(name='ti_lfa_cli') if l_0_ti_lfa_cli is missing else l_0_ti_lfa_cli))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'srlg'), 'enable'), True):
                pass
                l_0_ti_lfa_srlg_cli = 'fast-reroute ti-lfa srlg'
                context.vars['ti_lfa_srlg_cli'] = l_0_ti_lfa_srlg_cli
                context.exported_vars.add('ti_lfa_srlg_cli')
                if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'srlg'), 'strict'), True):
                    pass
                    l_0_ti_lfa_srlg_cli = str_join(((undefined(name='ti_lfa_srlg_cli') if l_0_ti_lfa_srlg_cli is missing else l_0_ti_lfa_srlg_cli), ' strict', ))
                    context.vars['ti_lfa_srlg_cli'] = l_0_ti_lfa_srlg_cli
                    context.exported_vars.add('ti_lfa_srlg_cli')
                yield '      '
                yield str((undefined(name='ti_lfa_srlg_cli') if l_0_ti_lfa_srlg_cli is missing else l_0_ti_lfa_srlg_cli))
                yield '\n'
            yield '   !\n'
        if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'enabled'), True):
            pass
            yield '   address-family ipv6 unicast\n'
            if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'bfd_all_interfaces'), True):
                pass
                yield '      bfd all-interfaces\n'
            if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'maximum_paths')):
                pass
                yield '      maximum-paths '
                yield str(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'maximum_paths'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'mode')):
                pass
                l_0_ti_lfa_cli = str_join(('fast-reroute ti-lfa mode ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'mode'), ))
                context.vars['ti_lfa_cli'] = l_0_ti_lfa_cli
                context.exported_vars.add('ti_lfa_cli')
                if t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'level')):
                    pass
                    l_0_ti_lfa_cli = str_join(((undefined(name='ti_lfa_cli') if l_0_ti_lfa_cli is missing else l_0_ti_lfa_cli), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'level'), ))
                    context.vars['ti_lfa_cli'] = l_0_ti_lfa_cli
                    context.exported_vars.add('ti_lfa_cli')
                yield '      '
                yield str((undefined(name='ti_lfa_cli') if l_0_ti_lfa_cli is missing else l_0_ti_lfa_cli))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'srlg'), 'enable'), True):
                pass
                l_0_ti_lfa_srlg_cli = 'fast-reroute ti-lfa srlg'
                context.vars['ti_lfa_srlg_cli'] = l_0_ti_lfa_srlg_cli
                context.exported_vars.add('ti_lfa_srlg_cli')
                if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'srlg'), 'strict'), True):
                    pass
                    l_0_ti_lfa_srlg_cli = str_join(((undefined(name='ti_lfa_srlg_cli') if l_0_ti_lfa_srlg_cli is missing else l_0_ti_lfa_srlg_cli), ' strict', ))
                    context.vars['ti_lfa_srlg_cli'] = l_0_ti_lfa_srlg_cli
                    context.exported_vars.add('ti_lfa_srlg_cli')
                yield '      '
                yield str((undefined(name='ti_lfa_srlg_cli') if l_0_ti_lfa_srlg_cli is missing else l_0_ti_lfa_srlg_cli))
                yield '\n'
            yield '   !\n'
        if t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'segment_routing_mpls')):
            pass
            yield '   segment-routing mpls\n'
            if t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'segment_routing_mpls'), 'enabled'), True):
                pass
                yield '      no shutdown\n'
            elif t_4(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'segment_routing_mpls'), 'enabled'), False):
                pass
                yield '      shutdown\n'
            for l_1_prefix_segment in t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'segment_routing_mpls'), 'prefix_segments'), 'prefix'):
                _loop_vars = {}
                pass
                if (t_4(environment.getattr(l_1_prefix_segment, 'prefix')) and t_4(environment.getattr(l_1_prefix_segment, 'index'))):
                    pass
                    yield '      prefix-segment '
                    yield str(environment.getattr(l_1_prefix_segment, 'prefix'))
                    yield ' index '
                    yield str(environment.getattr(l_1_prefix_segment, 'index'))
                    yield '\n'
            l_1_prefix_segment = missing
        if t_4(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'eos_cli')):
            pass
            yield '   '
            yield str(t_3(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'eos_cli'), 3, False))
            yield '\n'

blocks = {}
debug_info = '7=43&9=46&10=48&11=51&13=53&14=56&16=58&17=61&19=63&21=66&24=69&27=72&28=76&29=78&30=80&31=82&32=84&33=86&34=88&36=90&37=92&39=93&40=95&41=97&42=99&44=100&45=102&46=104&47=106&50=108&51=110&53=113&56=116&57=118&58=121&63=126&66=129&67=131&68=134&69=136&70=138&71=141&77=146&80=149&81=151&82=154&83=156&84=159&86=162&87=164&88=167&89=169&92=173&94=175&100=177&101=180&102=182&103=185&104=187&105=190&107=193&108=195&110=199&112=203&118=205&119=208&120=210&121=213&122=215&123=218&125=221&126=223&128=227&130=229&136=231&137=234&138=236&139=239&140=241&141=244&143=247&144=249&146=253&149=255&150=257&153=260&154=263&156=265&157=268&159=270&160=273&163=275&164=277&165=280&166=282&167=285&171=287&172=288&173=291&175=302&180=311&181=313&182=316&187=318&188=321&190=332&195=341&196=343&197=346&202=348&203=351&205=362&210=371&211=374&213=380&214=383&216=387&217=390&222=395&224=398&225=401&227=403&228=405&229=408&230=410&232=414&234=416&237=419&238=421&239=424&240=426&242=430&244=432&245=434&246=437&247=439&249=443&253=446&255=449&258=452&259=455&261=457&262=459&263=462&264=464&266=468&268=470&269=472&270=475&271=477&273=481&277=484&279=487&281=490&284=493&285=496&286=499&290=504&291=507'