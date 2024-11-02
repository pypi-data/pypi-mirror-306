from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-bgp.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_bgp = resolve('router_bgp')
    l_0_distance_cli = resolve('distance_cli')
    l_0_rr_preserve_attributes_cli = resolve('rr_preserve_attributes_cli')
    l_0_paths_cli = resolve('paths_cli')
    l_0_redistribute_var = resolve('redistribute_var')
    l_0_redistribute_conn = resolve('redistribute_conn')
    l_0_redistribute_isis = resolve('redistribute_isis')
    l_0_redistribute_ospf = resolve('redistribute_ospf')
    l_0_redistribute_ospf_match = resolve('redistribute_ospf_match')
    l_0_redistribute_ospfv3 = resolve('redistribute_ospfv3')
    l_0_redistribute_ospfv3_match = resolve('redistribute_ospfv3_match')
    l_0_redistribute_static = resolve('redistribute_static')
    l_0_redistribute_rip = resolve('redistribute_rip')
    l_0_redistribute_host = resolve('redistribute_host')
    l_0_redistribute_dynamic = resolve('redistribute_dynamic')
    l_0_redistribute_bgp = resolve('redistribute_bgp')
    l_0_redistribute_user = resolve('redistribute_user')
    l_0_evpn_neighbor_default_encap_cli = resolve('evpn_neighbor_default_encap_cli')
    l_0_evpn_mpls_resolution_ribs = resolve('evpn_mpls_resolution_ribs')
    l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli = resolve('evpn_neighbor_default_nhs_received_evpn_routes_cli')
    l_0_hostflap_detection_cli = resolve('hostflap_detection_cli')
    l_0_layer2_cli = resolve('layer2_cli')
    l_0_v4_bgp_lu_resolution_ribs = resolve('v4_bgp_lu_resolution_ribs')
    l_0_redistribute_dhcp = resolve('redistribute_dhcp')
    l_0_path_selection_roles = resolve('path_selection_roles')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.hide_passwords']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.hide_passwords' found.")
    try:
        t_3 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_4 = environment.filters['indent']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'indent' found.")
    try:
        t_5 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_6 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    try:
        t_7 = environment.tests['defined']
    except KeyError:
        @internalcode
        def t_7(*unused):
            raise TemplateRuntimeError("No test named 'defined' found.")
    try:
        t_8 = environment.tests['number']
    except KeyError:
        @internalcode
        def t_8(*unused):
            raise TemplateRuntimeError("No test named 'number' found.")
    pass
    if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as')):
        pass
        yield '!\nrouter bgp '
        yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as'))
        yield '\n'
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as_notation')):
            pass
            yield '   bgp asn notation '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as_notation'))
            yield '\n'
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'router_id')):
            pass
            yield '   router-id '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'router_id'))
            yield '\n'
        if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'updates'), 'wait_for_convergence'), True):
            pass
            yield '   update wait-for-convergence\n'
        if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'updates'), 'wait_install'), True):
            pass
            yield '   update wait-install\n'
        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast'), True):
            pass
            yield '   bgp default ipv4-unicast\n'
        elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast'), False):
            pass
            yield '   no bgp default ipv4-unicast\n'
        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast_transport_ipv6'), True):
            pass
            yield '   bgp default ipv4-unicast transport ipv6\n'
        elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast_transport_ipv6'), False):
            pass
            yield '   no bgp default ipv4-unicast transport ipv6\n'
        if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'external_routes')):
            pass
            l_0_distance_cli = str_join(('distance bgp ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'external_routes'), ))
            context.vars['distance_cli'] = l_0_distance_cli
            context.exported_vars.add('distance_cli')
            if (t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'internal_routes')) and t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'local_routes'))):
                pass
                l_0_distance_cli = str_join(((undefined(name='distance_cli') if l_0_distance_cli is missing else l_0_distance_cli), ' ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'internal_routes'), ' ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'local_routes'), ))
                context.vars['distance_cli'] = l_0_distance_cli
                context.exported_vars.add('distance_cli')
            yield '   '
            yield str((undefined(name='distance_cli') if l_0_distance_cli is missing else l_0_distance_cli))
            yield '\n'
        if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'enabled'), True):
            pass
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'restart_time')):
                pass
                yield '   graceful-restart restart-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'restart_time'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'stalepath_time')):
                pass
                yield '   graceful-restart stalepath-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'stalepath_time'))
                yield '\n'
            yield '   graceful-restart\n'
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_cluster_id')):
            pass
            yield '   bgp cluster-id '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_cluster_id'))
            yield '\n'
        if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'enabled'), False):
            pass
            yield '   no graceful-restart-helper\n'
        elif t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'enabled'), True):
            pass
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'restart_time')):
                pass
                yield '   graceful-restart-helper restart-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'restart_time'))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'long_lived'), True):
                pass
                yield '   graceful-restart-helper long-lived\n'
        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'route_reflector_preserve_attributes'), 'enabled'), True):
            pass
            l_0_rr_preserve_attributes_cli = 'bgp route-reflector preserve-attributes'
            context.vars['rr_preserve_attributes_cli'] = l_0_rr_preserve_attributes_cli
            context.exported_vars.add('rr_preserve_attributes_cli')
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'route_reflector_preserve_attributes'), 'always'), True):
                pass
                l_0_rr_preserve_attributes_cli = str_join(((undefined(name='rr_preserve_attributes_cli') if l_0_rr_preserve_attributes_cli is missing else l_0_rr_preserve_attributes_cli), ' always', ))
                context.vars['rr_preserve_attributes_cli'] = l_0_rr_preserve_attributes_cli
                context.exported_vars.add('rr_preserve_attributes_cli')
            yield '   '
            yield str((undefined(name='rr_preserve_attributes_cli') if l_0_rr_preserve_attributes_cli is missing else l_0_rr_preserve_attributes_cli))
            yield '\n'
        if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'paths')):
            pass
            l_0_paths_cli = str_join(('maximum-paths ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'paths'), ))
            context.vars['paths_cli'] = l_0_paths_cli
            context.exported_vars.add('paths_cli')
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'ecmp')):
                pass
                l_0_paths_cli = str_join(((undefined(name='paths_cli') if l_0_paths_cli is missing else l_0_paths_cli), ' ecmp ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'ecmp'), ))
                context.vars['paths_cli'] = l_0_paths_cli
                context.exported_vars.add('paths_cli')
            yield '   '
            yield str((undefined(name='paths_cli') if l_0_paths_cli is missing else l_0_paths_cli))
            yield '\n'
        for l_1_bgp_default in t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_defaults'), []):
            _loop_vars = {}
            pass
            yield '   '
            yield str(l_1_bgp_default)
            yield '\n'
        l_1_bgp_default = missing
        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'receive'), True):
            pass
            yield '   bgp additional-paths receive\n'
        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'receive'), False):
            pass
            yield '   no bgp additional-paths receive\n'
        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'send')):
            pass
            if (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'send') == 'disabled'):
                pass
                yield '   no bgp additional-paths send\n'
            elif (t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'send') == 'ecmp')):
                pass
                yield '   bgp additional-paths send ecmp limit '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'send_limit'))
                yield '\n'
            elif (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'send') == 'limit'):
                pass
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'send_limit')):
                    pass
                    yield '   bgp additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'send_limit'))
                    yield '\n'
            else:
                pass
                yield '   bgp additional-paths send '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'additional_paths'), 'send'))
                yield '\n'
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges')):
            pass
            def t_9(fiter):
                for l_1_listen_range in fiter:
                    if ((t_6(environment.getattr(l_1_listen_range, 'peer_group')) and t_6(environment.getattr(l_1_listen_range, 'prefix'))) and (t_6(environment.getattr(l_1_listen_range, 'peer_filter')) or t_6(environment.getattr(l_1_listen_range, 'remote_as')))):
                        yield l_1_listen_range
            for l_1_listen_range in t_9(t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges'), 'peer_group')):
                l_1_listen_range_cli = missing
                _loop_vars = {}
                pass
                l_1_listen_range_cli = str_join(('bgp listen range ', environment.getattr(l_1_listen_range, 'prefix'), ))
                _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                if t_6(environment.getattr(l_1_listen_range, 'peer_id_include_router_id'), True):
                    pass
                    l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' peer-id include router-id', ))
                    _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' peer-group ', environment.getattr(l_1_listen_range, 'peer_group'), ))
                _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                if t_6(environment.getattr(l_1_listen_range, 'peer_filter')):
                    pass
                    l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' peer-filter ', environment.getattr(l_1_listen_range, 'peer_filter'), ))
                    _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                elif t_6(environment.getattr(l_1_listen_range, 'remote_as')):
                    pass
                    l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' remote-as ', environment.getattr(l_1_listen_range, 'remote_as'), ))
                    _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                yield '   '
                yield str((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli))
                yield '\n'
            l_1_listen_range = l_1_listen_range_cli = missing
        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'bestpath'), 'd_path'), True):
            pass
            yield '   bgp bestpath d-path\n'
        for l_1_peer_group in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), 'name'):
            l_1_remove_private_as_cli = resolve('remove_private_as_cli')
            l_1_allowas_in_cli = resolve('allowas_in_cli')
            l_1_neighbor_rib_in_pre_policy_retain_cli = resolve('neighbor_rib_in_pre_policy_retain_cli')
            l_1_hide_passwords = resolve('hide_passwords')
            l_1_default_originate_cli = resolve('default_originate_cli')
            l_1_maximum_routes_cli = resolve('maximum_routes_cli')
            l_1_link_bandwidth_cli = resolve('link_bandwidth_cli')
            l_1_remove_private_as_ingress_cli = resolve('remove_private_as_ingress_cli')
            _loop_vars = {}
            pass
            yield '   neighbor '
            yield str(environment.getattr(l_1_peer_group, 'name'))
            yield ' peer group\n'
            if t_6(environment.getattr(l_1_peer_group, 'remote_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' remote-as '
                yield str(environment.getattr(l_1_peer_group, 'remote_as'))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'next_hop_self'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' next-hop-self\n'
            if t_6(environment.getattr(l_1_peer_group, 'next_hop_unchanged'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' next-hop-unchanged\n'
            if t_6(environment.getattr(l_1_peer_group, 'shutdown'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' shutdown\n'
            if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled'), True):
                pass
                l_1_remove_private_as_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' remove-private-as', ))
                _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'all'), True):
                    pass
                    l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' all', ))
                    _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                    if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'replace_as'), True):
                        pass
                        l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' replace-as', ))
                        _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                yield '   '
                yield str((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' remove-private-as\n'
            if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'as_path'), 'prepend_own_disabled'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' as-path prepend-own disabled\n'
            if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'as_path'), 'remote_as_replace_out'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' as-path remote-as replace out\n'
            if t_6(environment.getattr(l_1_peer_group, 'local_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' local-as '
                yield str(environment.getattr(l_1_peer_group, 'local_as'))
                yield ' no-prepend replace-as\n'
            if t_6(environment.getattr(l_1_peer_group, 'weight')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' weight '
                yield str(environment.getattr(l_1_peer_group, 'weight'))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'passive'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' passive\n'
            if t_6(environment.getattr(l_1_peer_group, 'update_source')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' update-source '
                yield str(environment.getattr(l_1_peer_group, 'update_source'))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'bfd'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' bfd\n'
                if ((t_6(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'interval')) and t_6(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'min_rx'))) and t_6(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'multiplier'))):
                    pass
                    yield '   neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' bfd interval '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'interval'))
                    yield ' min-rx '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'min_rx'))
                    yield ' multiplier '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'multiplier'))
                    yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'description')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' description '
                yield str(environment.getattr(l_1_peer_group, 'description'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'enabled'), True):
                pass
                l_1_allowas_in_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' allowas-in', ))
                _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'times')):
                    pass
                    l_1_allowas_in_cli = str_join(((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli), ' ', environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'times'), ))
                    _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                yield '   '
                yield str((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled'), True):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'all'), True):
                    pass
                    l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli), ' all', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled'), False):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('no neighbor ', environment.getattr(l_1_peer_group, 'name'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'ebgp_multihop')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' ebgp-multihop '
                yield str(environment.getattr(l_1_peer_group, 'ebgp_multihop'))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'ttl_maximum_hops')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' ttl maximum-hops '
                yield str(environment.getattr(l_1_peer_group, 'ttl_maximum_hops'))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'route_reflector_client'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' route-reflector-client\n'
            if t_6(environment.getattr(l_1_peer_group, 'session_tracker')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' session tracker '
                yield str(environment.getattr(l_1_peer_group, 'session_tracker'))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'timers')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' timers '
                yield str(environment.getattr(l_1_peer_group, 'timers'))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'route_map_in')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' route-map '
                yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                yield ' in\n'
            if t_6(environment.getattr(l_1_peer_group, 'route_map_out')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' route-map '
                yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                yield ' out\n'
            if t_6(environment.getattr(l_1_peer_group, 'password')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' password 7 '
                yield str(t_2(environment.getattr(l_1_peer_group, 'password'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
            if (t_6(environment.getattr(environment.getattr(l_1_peer_group, 'shared_secret'), 'profile')) and t_6(environment.getattr(environment.getattr(l_1_peer_group, 'shared_secret'), 'hash_algorithm'))):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' password shared-secret profile '
                yield str(environment.getattr(environment.getattr(l_1_peer_group, 'shared_secret'), 'profile'))
                yield ' algorithm '
                yield str(environment.getattr(environment.getattr(l_1_peer_group, 'shared_secret'), 'hash_algorithm'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'enabled'), True):
                pass
                l_1_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-originate', ))
                _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map')):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map'), ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'always'), True):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' always', ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                yield '   '
                yield str((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'send_community'), 'all'):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' send-community\n'
            elif t_6(environment.getattr(l_1_peer_group, 'send_community')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' send-community '
                yield str(environment.getattr(l_1_peer_group, 'send_community'))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'maximum_routes')):
                pass
                l_1_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' maximum-routes ', environment.getattr(l_1_peer_group, 'maximum_routes'), ))
                _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_6(environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit')):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-limit ', environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit'), ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_6(environment.getattr(l_1_peer_group, 'maximum_routes_warning_only'), True):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-only', ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                yield '   '
                yield str((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli))
                yield '\n'
            if t_6(environment.getattr(l_1_peer_group, 'missing_policy')):
                pass
                for l_2_direction in ['in', 'out']:
                    l_2_missing_policy_cli = resolve('missing_policy_cli')
                    l_2_dir = l_2_policy = missing
                    _loop_vars = {}
                    pass
                    l_2_dir = str_join(('direction_', l_2_direction, ))
                    _loop_vars['dir'] = l_2_dir
                    l_2_policy = environment.getitem(environment.getattr(l_1_peer_group, 'missing_policy'), (undefined(name='dir') if l_2_dir is missing else l_2_dir))
                    _loop_vars['policy'] = l_2_policy
                    if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action')):
                        pass
                        l_2_missing_policy_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' missing-policy address-family all', ))
                        _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        if ((t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True) or t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True)) or t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True)):
                            pass
                            l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' include', ))
                            _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' community-list', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' prefix-list', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' sub-route-map', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' direction ', l_2_direction, ' action ', environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action'), ))
                        _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        yield '   '
                        yield str((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli))
                        yield '\n'
                l_2_direction = l_2_dir = l_2_policy = l_2_missing_policy_cli = missing
            if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'enabled'), True):
                pass
                l_1_link_bandwidth_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' link-bandwidth', ))
                _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'default')):
                    pass
                    l_1_link_bandwidth_cli = str_join(((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli), ' default ', environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'default'), ))
                    _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                yield '   '
                yield str((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled'), True):
                pass
                l_1_remove_private_as_ingress_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' remove-private-as ingress', ))
                _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'replace_as'), True):
                    pass
                    l_1_remove_private_as_ingress_cli = str_join(((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli), ' replace-as', ))
                    _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                yield '   '
                yield str((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' remove-private-as ingress\n'
        l_1_peer_group = l_1_remove_private_as_cli = l_1_allowas_in_cli = l_1_neighbor_rib_in_pre_policy_retain_cli = l_1_hide_passwords = l_1_default_originate_cli = l_1_maximum_routes_cli = l_1_link_bandwidth_cli = l_1_remove_private_as_ingress_cli = missing
        for l_1_neighbor in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbors'), 'ip_address'):
            l_1_remove_private_as_cli = resolve('remove_private_as_cli')
            l_1_allowas_in_cli = resolve('allowas_in_cli')
            l_1_neighbor_rib_in_pre_policy_retain_cli = resolve('neighbor_rib_in_pre_policy_retain_cli')
            l_1_hide_passwords = resolve('hide_passwords')
            l_1_default_originate_cli = resolve('default_originate_cli')
            l_1_maximum_routes_cli = resolve('maximum_routes_cli')
            l_1_link_bandwidth_cli = resolve('link_bandwidth_cli')
            l_1_remove_private_as_ingress_cli = resolve('remove_private_as_ingress_cli')
            _loop_vars = {}
            pass
            if t_6(environment.getattr(l_1_neighbor, 'peer_group')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' peer group '
                yield str(environment.getattr(l_1_neighbor, 'peer_group'))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'remote_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' remote-as '
                yield str(environment.getattr(l_1_neighbor, 'remote_as'))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'next_hop_self'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' next-hop-self\n'
            if t_6(environment.getattr(l_1_neighbor, 'shutdown'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' shutdown\n'
            if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'enabled'), True):
                pass
                l_1_remove_private_as_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' remove-private-as', ))
                _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'all'), True):
                    pass
                    l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' all', ))
                    _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                    if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'replace_as'), True):
                        pass
                        l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' replace-as', ))
                        _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                yield '   '
                yield str((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' remove-private-as\n'
            if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'as_path'), 'prepend_own_disabled'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' as-path prepend-own disabled\n'
            if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'as_path'), 'remote_as_replace_out'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' as-path remote-as replace out\n'
            if t_6(environment.getattr(l_1_neighbor, 'local_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' local-as '
                yield str(environment.getattr(l_1_neighbor, 'local_as'))
                yield ' no-prepend replace-as\n'
            if t_6(environment.getattr(l_1_neighbor, 'weight')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' weight '
                yield str(environment.getattr(l_1_neighbor, 'weight'))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'passive'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' passive\n'
            if t_6(environment.getattr(l_1_neighbor, 'update_source')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' update-source '
                yield str(environment.getattr(l_1_neighbor, 'update_source'))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'bfd'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' bfd\n'
                if ((t_6(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'interval')) and t_6(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'min_rx'))) and t_6(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'multiplier'))):
                    pass
                    yield '   neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' bfd interval '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'interval'))
                    yield ' min-rx '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'min_rx'))
                    yield ' multiplier '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'multiplier'))
                    yield '\n'
            elif (t_6(environment.getattr(l_1_neighbor, 'bfd'), False) and t_6(environment.getattr(l_1_neighbor, 'peer_group'))):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' bfd\n'
            if t_6(environment.getattr(l_1_neighbor, 'description')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' description '
                yield str(environment.getattr(l_1_neighbor, 'description'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'enabled'), True):
                pass
                l_1_allowas_in_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' allowas-in', ))
                _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'times')):
                    pass
                    l_1_allowas_in_cli = str_join(((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli), ' ', environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'times'), ))
                    _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                yield '   '
                yield str((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), True):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'all'), True):
                    pass
                    l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli), ' all', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), False):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('no neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'ebgp_multihop')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' ebgp-multihop '
                yield str(environment.getattr(l_1_neighbor, 'ebgp_multihop'))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'ttl_maximum_hops')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' ttl maximum-hops '
                yield str(environment.getattr(l_1_neighbor, 'ttl_maximum_hops'))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'route_reflector_client'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-reflector-client\n'
            elif t_6(environment.getattr(l_1_neighbor, 'route_reflector_client'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-reflector-client\n'
            if t_6(environment.getattr(l_1_neighbor, 'session_tracker')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' session tracker '
                yield str(environment.getattr(l_1_neighbor, 'session_tracker'))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'timers')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' timers '
                yield str(environment.getattr(l_1_neighbor, 'timers'))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-map '
                yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                yield ' in\n'
            if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-map '
                yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                yield ' out\n'
            if (t_6(environment.getattr(environment.getattr(l_1_neighbor, 'shared_secret'), 'profile')) and t_6(environment.getattr(environment.getattr(l_1_neighbor, 'shared_secret'), 'hash_algorithm'))):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' password shared-secret profile '
                yield str(environment.getattr(environment.getattr(l_1_neighbor, 'shared_secret'), 'profile'))
                yield ' algorithm '
                yield str(environment.getattr(environment.getattr(l_1_neighbor, 'shared_secret'), 'hash_algorithm'))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'password')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' password 7 '
                yield str(t_2(environment.getattr(l_1_neighbor, 'password'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'enabled'), True):
                pass
                l_1_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-originate', ))
                _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map')):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map'), ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'always'), True):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' always', ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                yield '   '
                yield str((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'send_community'), 'all'):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' send-community\n'
            elif t_6(environment.getattr(l_1_neighbor, 'send_community')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' send-community '
                yield str(environment.getattr(l_1_neighbor, 'send_community'))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'maximum_routes')):
                pass
                l_1_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' maximum-routes ', environment.getattr(l_1_neighbor, 'maximum_routes'), ))
                _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_6(environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit')):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-limit ', environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit'), ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_6(environment.getattr(l_1_neighbor, 'maximum_routes_warning_only'), True):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-only', ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                yield '   '
                yield str((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli))
                yield '\n'
            if t_6(environment.getattr(l_1_neighbor, 'missing_policy')):
                pass
                for l_2_direction in ['in', 'out']:
                    l_2_missing_policy_cli = resolve('missing_policy_cli')
                    l_2_dir = l_2_policy = missing
                    _loop_vars = {}
                    pass
                    l_2_dir = str_join(('direction_', l_2_direction, ))
                    _loop_vars['dir'] = l_2_dir
                    l_2_policy = environment.getitem(environment.getattr(l_1_neighbor, 'missing_policy'), (undefined(name='dir') if l_2_dir is missing else l_2_dir))
                    _loop_vars['policy'] = l_2_policy
                    if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action')):
                        pass
                        l_2_missing_policy_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' missing-policy address-family all', ))
                        _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        if ((t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True) or t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True)) or t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True)):
                            pass
                            l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' include', ))
                            _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' community-list', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' prefix-list', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' sub-route-map', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' direction ', l_2_direction, ' action ', environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action'), ))
                        _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        yield '   '
                        yield str((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli))
                        yield '\n'
                l_2_direction = l_2_dir = l_2_policy = l_2_missing_policy_cli = missing
            if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'link_bandwidth'), 'enabled'), True):
                pass
                l_1_link_bandwidth_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' link-bandwidth', ))
                _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'link_bandwidth'), 'default')):
                    pass
                    l_1_link_bandwidth_cli = str_join(((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli), ' default ', environment.getattr(environment.getattr(l_1_neighbor, 'link_bandwidth'), 'default'), ))
                    _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                yield '   '
                yield str((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as_ingress'), 'enabled'), True):
                pass
                l_1_remove_private_as_ingress_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' remove-private-as ingress', ))
                _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as_ingress'), 'replace_as'), True):
                    pass
                    l_1_remove_private_as_ingress_cli = str_join(((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli), ' replace-as', ))
                    _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                yield '   '
                yield str((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as_ingress'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' remove-private-as ingress\n'
        l_1_neighbor = l_1_remove_private_as_cli = l_1_allowas_in_cli = l_1_neighbor_rib_in_pre_policy_retain_cli = l_1_hide_passwords = l_1_default_originate_cli = l_1_maximum_routes_cli = l_1_link_bandwidth_cli = l_1_remove_private_as_ingress_cli = missing
        if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'redistribute_internal'), True):
            pass
            yield '   bgp redistribute-internal\n'
        elif t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'redistribute_internal'), False):
            pass
            yield '   no bgp redistribute-internal\n'
        for l_1_aggregate_address in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'aggregate_addresses'), 'prefix'):
            l_1_aggregate_address_cli = missing
            _loop_vars = {}
            pass
            l_1_aggregate_address_cli = str_join(('aggregate-address ', environment.getattr(l_1_aggregate_address, 'prefix'), ))
            _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_6(environment.getattr(l_1_aggregate_address, 'as_set'), True):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' as-set', ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_6(environment.getattr(l_1_aggregate_address, 'summary_only'), True):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' summary-only', ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_6(environment.getattr(l_1_aggregate_address, 'attribute_map')):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' attribute-map ', environment.getattr(l_1_aggregate_address, 'attribute_map'), ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_6(environment.getattr(l_1_aggregate_address, 'match_map')):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' match-map ', environment.getattr(l_1_aggregate_address, 'match_map'), ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_6(environment.getattr(l_1_aggregate_address, 'advertise_only'), True):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' advertise-only', ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            yield '   '
            yield str((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli))
            yield '\n'
        l_1_aggregate_address = l_1_aggregate_address_cli = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'redistribute')):
            pass
            l_0_redistribute_var = environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'redistribute')
            context.vars['redistribute_var'] = l_0_redistribute_var
            context.exported_vars.add('redistribute_var')
            if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'enabled'), True):
                pass
                l_0_redistribute_conn = 'redistribute connected'
                context.vars['redistribute_conn'] = l_0_redistribute_conn
                context.exported_vars.add('redistribute_conn')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' include leaked', ))
                    context.vars['redistribute_conn'] = l_0_redistribute_conn
                    context.exported_vars.add('redistribute_conn')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'route_map')):
                    pass
                    l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'route_map'), ))
                    context.vars['redistribute_conn'] = l_0_redistribute_conn
                    context.exported_vars.add('redistribute_conn')
                elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'rcf')):
                    pass
                    l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'rcf'), ))
                    context.vars['redistribute_conn'] = l_0_redistribute_conn
                    context.exported_vars.add('redistribute_conn')
                yield '   '
                yield str((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'enabled'), True):
                pass
                l_0_redistribute_isis = 'redistribute isis'
                context.vars['redistribute_isis'] = l_0_redistribute_isis
                context.exported_vars.add('redistribute_isis')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'isis_level')):
                    pass
                    l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'isis_level'), ))
                    context.vars['redistribute_isis'] = l_0_redistribute_isis
                    context.exported_vars.add('redistribute_isis')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' include leaked', ))
                    context.vars['redistribute_isis'] = l_0_redistribute_isis
                    context.exported_vars.add('redistribute_isis')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'route_map')):
                    pass
                    l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'route_map'), ))
                    context.vars['redistribute_isis'] = l_0_redistribute_isis
                    context.exported_vars.add('redistribute_isis')
                elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'rcf')):
                    pass
                    l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'rcf'), ))
                    context.vars['redistribute_isis'] = l_0_redistribute_isis
                    context.exported_vars.add('redistribute_isis')
                yield '   '
                yield str((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'enabled'), True):
                pass
                l_0_redistribute_ospf = 'redistribute ospf'
                context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                context.exported_vars.add('redistribute_ospf')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' include leaked', ))
                    context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                    context.exported_vars.add('redistribute_ospf')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'route_map')):
                    pass
                    l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'route_map'), ))
                    context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                    context.exported_vars.add('redistribute_ospf')
                yield '   '
                yield str((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'enabled'), True):
                pass
                l_0_redistribute_ospf = 'redistribute ospf match internal'
                context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                context.exported_vars.add('redistribute_ospf')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' include leaked', ))
                    context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                    context.exported_vars.add('redistribute_ospf')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'route_map')):
                    pass
                    l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'route_map'), ))
                    context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                    context.exported_vars.add('redistribute_ospf')
                yield '   '
                yield str((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'enabled'), True):
                pass
                l_0_redistribute_ospf_match = 'redistribute ospf match external'
                context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                context.exported_vars.add('redistribute_ospf_match')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' include leaked', ))
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'route_map')):
                    pass
                    l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'route_map'), ))
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                yield '   '
                yield str((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'enabled'), True):
                pass
                l_0_redistribute_ospf_match = 'redistribute ospf match nssa-external'
                context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                context.exported_vars.add('redistribute_ospf_match')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type')):
                    pass
                    l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type'), ))
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' include leaked', ))
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map')):
                    pass
                    l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map'), ))
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                yield '   '
                yield str((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'enabled'), True):
                pass
                l_0_redistribute_ospfv3 = 'redistribute ospfv3'
                context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                context.exported_vars.add('redistribute_ospfv3')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' include leaked', ))
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'route_map')):
                    pass
                    l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'route_map'), ))
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                yield '   '
                yield str((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'enabled'), True):
                pass
                l_0_redistribute_ospfv3 = 'redistribute ospfv3 match internal'
                context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                context.exported_vars.add('redistribute_ospfv3')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' include leaked', ))
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map')):
                    pass
                    l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map'), ))
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                yield '   '
                yield str((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'enabled'), True):
                pass
                l_0_redistribute_ospfv3_match = 'redistribute ospfv3 match external'
                context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                context.exported_vars.add('redistribute_ospfv3_match')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' include leaked', ))
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'route_map')):
                    pass
                    l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'route_map'), ))
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                yield '   '
                yield str((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'enabled'), True):
                pass
                l_0_redistribute_ospfv3_match = 'redistribute ospfv3 match nssa-external'
                context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                context.exported_vars.add('redistribute_ospfv3_match')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type')):
                    pass
                    l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type'), ))
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' include leaked', ))
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map')):
                    pass
                    l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map'), ))
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                yield '   '
                yield str((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'enabled'), True):
                pass
                l_0_redistribute_static = 'redistribute static'
                context.vars['redistribute_static'] = l_0_redistribute_static
                context.exported_vars.add('redistribute_static')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'include_leaked'), True):
                    pass
                    l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' include leaked', ))
                    context.vars['redistribute_static'] = l_0_redistribute_static
                    context.exported_vars.add('redistribute_static')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'route_map')):
                    pass
                    l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'route_map'), ))
                    context.vars['redistribute_static'] = l_0_redistribute_static
                    context.exported_vars.add('redistribute_static')
                elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'rcf')):
                    pass
                    l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'rcf'), ))
                    context.vars['redistribute_static'] = l_0_redistribute_static
                    context.exported_vars.add('redistribute_static')
                yield '   '
                yield str((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'rip'), 'enabled'), True):
                pass
                l_0_redistribute_rip = 'redistribute rip'
                context.vars['redistribute_rip'] = l_0_redistribute_rip
                context.exported_vars.add('redistribute_rip')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'rip'), 'route_map')):
                    pass
                    l_0_redistribute_rip = str_join(((undefined(name='redistribute_rip') if l_0_redistribute_rip is missing else l_0_redistribute_rip), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'rip'), 'route_map'), ))
                    context.vars['redistribute_rip'] = l_0_redistribute_rip
                    context.exported_vars.add('redistribute_rip')
                yield '   '
                yield str((undefined(name='redistribute_rip') if l_0_redistribute_rip is missing else l_0_redistribute_rip))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'enabled'), True):
                pass
                l_0_redistribute_host = 'redistribute attached-host'
                context.vars['redistribute_host'] = l_0_redistribute_host
                context.exported_vars.add('redistribute_host')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'route_map')):
                    pass
                    l_0_redistribute_host = str_join(((undefined(name='redistribute_host') if l_0_redistribute_host is missing else l_0_redistribute_host), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'route_map'), ))
                    context.vars['redistribute_host'] = l_0_redistribute_host
                    context.exported_vars.add('redistribute_host')
                yield '   '
                yield str((undefined(name='redistribute_host') if l_0_redistribute_host is missing else l_0_redistribute_host))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'enabled'), True):
                pass
                l_0_redistribute_dynamic = 'redistribute dynamic'
                context.vars['redistribute_dynamic'] = l_0_redistribute_dynamic
                context.exported_vars.add('redistribute_dynamic')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'route_map')):
                    pass
                    l_0_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_0_redistribute_dynamic is missing else l_0_redistribute_dynamic), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'route_map'), ))
                    context.vars['redistribute_dynamic'] = l_0_redistribute_dynamic
                    context.exported_vars.add('redistribute_dynamic')
                elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'rcf')):
                    pass
                    l_0_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_0_redistribute_dynamic is missing else l_0_redistribute_dynamic), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'rcf'), ))
                    context.vars['redistribute_dynamic'] = l_0_redistribute_dynamic
                    context.exported_vars.add('redistribute_dynamic')
                yield '   '
                yield str((undefined(name='redistribute_dynamic') if l_0_redistribute_dynamic is missing else l_0_redistribute_dynamic))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'bgp'), 'enabled'), True):
                pass
                l_0_redistribute_bgp = 'redistribute bgp leaked'
                context.vars['redistribute_bgp'] = l_0_redistribute_bgp
                context.exported_vars.add('redistribute_bgp')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'bgp'), 'route_map')):
                    pass
                    l_0_redistribute_bgp = str_join(((undefined(name='redistribute_bgp') if l_0_redistribute_bgp is missing else l_0_redistribute_bgp), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'bgp'), 'route_map'), ))
                    context.vars['redistribute_bgp'] = l_0_redistribute_bgp
                    context.exported_vars.add('redistribute_bgp')
                yield '   '
                yield str((undefined(name='redistribute_bgp') if l_0_redistribute_bgp is missing else l_0_redistribute_bgp))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'user'), 'enabled'), True):
                pass
                l_0_redistribute_user = 'redistribute user'
                context.vars['redistribute_user'] = l_0_redistribute_user
                context.exported_vars.add('redistribute_user')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'user'), 'rcf')):
                    pass
                    l_0_redistribute_user = str_join(((undefined(name='redistribute_user') if l_0_redistribute_user is missing else l_0_redistribute_user), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'user'), 'rcf'), ))
                    context.vars['redistribute_user'] = l_0_redistribute_user
                    context.exported_vars.add('redistribute_user')
                yield '   '
                yield str((undefined(name='redistribute_user') if l_0_redistribute_user is missing else l_0_redistribute_user))
                yield '\n'
        elif t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'redistribute_routes')):
            pass
            for l_1_redistribute_route in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'redistribute_routes'), 'source_protocol'):
                l_1_redistribute_route_cli = missing
                _loop_vars = {}
                pass
                l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                    pass
                    if t_6(environment.getattr(l_1_redistribute_route, 'ospf_route_type')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'bgp'):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' leaked', ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif t_6(environment.getattr(l_1_redistribute_route, 'include_leaked'), True):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if t_6(environment.getattr(l_1_redistribute_route, 'route_map')):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                    pass
                    if t_6(environment.getattr(l_1_redistribute_route, 'rcf')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' rcf ', environment.getattr(l_1_redistribute_route, 'rcf'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                yield '   '
                yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                yield '\n'
            l_1_redistribute_route = l_1_redistribute_route_cli = missing
        for l_1_neighbor_interface in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbor_interfaces'), 'name'):
            _loop_vars = {}
            pass
            if (t_6(environment.getattr(l_1_neighbor_interface, 'peer_group')) and t_6(environment.getattr(l_1_neighbor_interface, 'remote_as'))):
                pass
                yield '   neighbor interface '
                yield str(environment.getattr(l_1_neighbor_interface, 'name'))
                yield ' peer-group '
                yield str(environment.getattr(l_1_neighbor_interface, 'peer_group'))
                yield ' remote-as '
                yield str(environment.getattr(l_1_neighbor_interface, 'remote_as'))
                yield '\n'
            elif (t_6(environment.getattr(l_1_neighbor_interface, 'peer_group')) and t_6(environment.getattr(l_1_neighbor_interface, 'peer_filter'))):
                pass
                yield '   neighbor interface '
                yield str(environment.getattr(l_1_neighbor_interface, 'name'))
                yield ' peer-group '
                yield str(environment.getattr(l_1_neighbor_interface, 'peer_group'))
                yield ' peer-filter '
                yield str(environment.getattr(l_1_neighbor_interface, 'peer_filter'))
                yield '\n'
        l_1_neighbor_interface = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlans')):
            pass
            for l_1_vlan in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlans')):
                _loop_vars = {}
                pass
                yield '   !\n   vlan '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield '\n'
                if t_6(environment.getattr(l_1_vlan, 'rd')):
                    pass
                    yield '      rd '
                    yield str(environment.getattr(l_1_vlan, 'rd'))
                    yield '\n'
                if (t_6(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'domain')) and t_6(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'rd'))):
                    pass
                    yield '      rd evpn domain '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'domain'))
                    yield ' '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'rd'))
                    yield '\n'
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'both')):
                    _loop_vars = {}
                    pass
                    yield '      route-target both '
                    yield str(l_2_route_target)
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import')):
                    _loop_vars = {}
                    pass
                    yield '      route-target import '
                    yield str(l_2_route_target)
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export')):
                    _loop_vars = {}
                    pass
                    yield '      route-target export '
                    yield str(l_2_route_target)
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_evpn_domains')):
                    _loop_vars = {}
                    pass
                    yield '      route-target import evpn domain '
                    yield str(environment.getattr(l_2_route_target, 'domain'))
                    yield ' '
                    yield str(environment.getattr(l_2_route_target, 'route_target'))
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export_evpn_domains')):
                    _loop_vars = {}
                    pass
                    yield '      route-target export evpn domain '
                    yield str(environment.getattr(l_2_route_target, 'domain'))
                    yield ' '
                    yield str(environment.getattr(l_2_route_target, 'route_target'))
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_export_evpn_domains')):
                    _loop_vars = {}
                    pass
                    yield '      route-target import export evpn domain '
                    yield str(environment.getattr(l_2_route_target, 'domain'))
                    yield ' '
                    yield str(environment.getattr(l_2_route_target, 'route_target'))
                    yield '\n'
                l_2_route_target = missing
                for l_2_redistribute_route in t_3(environment.getattr(l_1_vlan, 'redistribute_routes')):
                    _loop_vars = {}
                    pass
                    yield '      redistribute '
                    yield str(l_2_redistribute_route)
                    yield '\n'
                l_2_redistribute_route = missing
                for l_2_no_redistribute_route in t_3(environment.getattr(l_1_vlan, 'no_redistribute_routes')):
                    _loop_vars = {}
                    pass
                    yield '      no redistribute '
                    yield str(l_2_no_redistribute_route)
                    yield '\n'
                l_2_no_redistribute_route = missing
                if t_6(environment.getattr(l_1_vlan, 'eos_cli')):
                    pass
                    yield '      !\n      '
                    yield str(t_4(environment.getattr(l_1_vlan, 'eos_cli'), 6, False))
                    yield '\n'
            l_1_vlan = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vpws')):
            pass
            for l_1_vpws_service in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vpws'), 'name'):
                _loop_vars = {}
                pass
                yield '   !\n'
                if t_6(environment.getattr(l_1_vpws_service, 'name')):
                    pass
                    yield '   vpws '
                    yield str(environment.getattr(l_1_vpws_service, 'name'))
                    yield '\n'
                    if t_6(environment.getattr(l_1_vpws_service, 'rd')):
                        pass
                        yield '      rd '
                        yield str(environment.getattr(l_1_vpws_service, 'rd'))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(l_1_vpws_service, 'route_targets'), 'import_export')):
                        pass
                        yield '      route-target import export evpn '
                        yield str(environment.getattr(environment.getattr(l_1_vpws_service, 'route_targets'), 'import_export'))
                        yield '\n'
                    if t_6(environment.getattr(l_1_vpws_service, 'mpls_control_word'), True):
                        pass
                        yield '      mpls control-word\n'
                    if t_6(environment.getattr(l_1_vpws_service, 'label_flow'), True):
                        pass
                        yield '      label flow\n'
                    if t_6(environment.getattr(l_1_vpws_service, 'mtu')):
                        pass
                        yield '      mtu '
                        yield str(environment.getattr(l_1_vpws_service, 'mtu'))
                        yield '\n'
                    for l_2_pw in t_3(environment.getattr(l_1_vpws_service, 'pseudowires'), 'name'):
                        _loop_vars = {}
                        pass
                        if ((t_6(environment.getattr(l_2_pw, 'name')) and t_6(environment.getattr(l_2_pw, 'id_local'))) and t_6(environment.getattr(l_2_pw, 'id_remote'))):
                            pass
                            yield '      !\n      pseudowire '
                            yield str(environment.getattr(l_2_pw, 'name'))
                            yield '\n         evpn vpws id local '
                            yield str(environment.getattr(l_2_pw, 'id_local'))
                            yield ' remote '
                            yield str(environment.getattr(l_2_pw, 'id_remote'))
                            yield '\n'
                    l_2_pw = missing
            l_1_vpws_service = missing
        for l_1_vlan_aware_bundle in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlan_aware_bundles'), 'name'):
            _loop_vars = {}
            pass
            yield '   !\n   vlan-aware-bundle '
            yield str(environment.getattr(l_1_vlan_aware_bundle, 'name'))
            yield '\n'
            if t_6(environment.getattr(l_1_vlan_aware_bundle, 'rd')):
                pass
                yield '      rd '
                yield str(environment.getattr(l_1_vlan_aware_bundle, 'rd'))
                yield '\n'
            if (t_6(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'domain')) and t_6(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'rd'))):
                pass
                yield '      rd evpn domain '
                yield str(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'domain'))
                yield ' '
                yield str(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'rd'))
                yield '\n'
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'both')):
                _loop_vars = {}
                pass
                yield '      route-target both '
                yield str(l_2_route_target)
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import')):
                _loop_vars = {}
                pass
                yield '      route-target import '
                yield str(l_2_route_target)
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export')):
                _loop_vars = {}
                pass
                yield '      route-target export '
                yield str(l_2_route_target)
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_evpn_domains')):
                _loop_vars = {}
                pass
                yield '      route-target import evpn domain '
                yield str(environment.getattr(l_2_route_target, 'domain'))
                yield ' '
                yield str(environment.getattr(l_2_route_target, 'route_target'))
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export_evpn_domains')):
                _loop_vars = {}
                pass
                yield '      route-target export evpn domain '
                yield str(environment.getattr(l_2_route_target, 'domain'))
                yield ' '
                yield str(environment.getattr(l_2_route_target, 'route_target'))
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_export_evpn_domains')):
                _loop_vars = {}
                pass
                yield '      route-target import export evpn domain '
                yield str(environment.getattr(l_2_route_target, 'domain'))
                yield ' '
                yield str(environment.getattr(l_2_route_target, 'route_target'))
                yield '\n'
            l_2_route_target = missing
            for l_2_redistribute_route in t_3(environment.getattr(l_1_vlan_aware_bundle, 'redistribute_routes')):
                _loop_vars = {}
                pass
                yield '      redistribute '
                yield str(l_2_redistribute_route)
                yield '\n'
            l_2_redistribute_route = missing
            for l_2_no_redistribute_route in t_3(environment.getattr(l_1_vlan_aware_bundle, 'no_redistribute_routes')):
                _loop_vars = {}
                pass
                yield '      no redistribute '
                yield str(l_2_no_redistribute_route)
                yield '\n'
            l_2_no_redistribute_route = missing
            yield '      vlan '
            yield str(environment.getattr(l_1_vlan_aware_bundle, 'vlan'))
            yield '\n'
            if t_6(environment.getattr(l_1_vlan_aware_bundle, 'eos_cli')):
                pass
                yield '      !\n      '
                yield str(t_4(environment.getattr(l_1_vlan_aware_bundle, 'eos_cli'), 6, False))
                yield '\n'
        l_1_vlan_aware_bundle = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn')):
            pass
            yield '   !\n   address-family evpn\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'export_ethernet_segment_ip_mass_withdraw'), True):
                pass
                yield '      route export ethernet-segment ip mass-withdraw\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'import_ethernet_segment_ip_mass_withdraw'), True):
                pass
                yield '      route import ethernet-segment ip mass-withdraw\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp'), 'additional_paths'), 'send')):
                pass
                if (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp'), 'additional_paths'), 'send') == 'disabled'):
                    pass
                    yield '      no bgp additional-paths send\n'
                elif (t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp'), 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp'), 'additional_paths'), 'send') == 'ecmp')):
                    pass
                    yield '      bgp additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp'), 'additional_paths'), 'send_limit'))
                    yield '\n'
                elif (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp'), 'additional_paths'), 'send') == 'limit'):
                    pass
                    if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp'), 'additional_paths'), 'send_limit')):
                        pass
                        yield '      bgp additional-paths send limit '
                        yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp'), 'additional_paths'), 'send_limit'))
                        yield '\n'
                else:
                    pass
                    yield '      bgp additional-paths send '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp'), 'additional_paths'), 'send'))
                    yield '\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'any'), True):
                pass
                yield '      bgp additional-paths send any\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'backup'), True):
                pass
                yield '      bgp additional-paths send backup\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'ecmp'), True):
                pass
                yield '      bgp additional-paths send ecmp\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'limit')):
                pass
                yield '      bgp additional-paths send ecmp limit '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'limit'))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'limit')):
                pass
                yield '      bgp additional-paths send limit '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'limit'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_unchanged'), True):
                pass
                yield '      bgp next-hop-unchanged\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'encapsulation'), 'mpls'):
                pass
                l_0_evpn_neighbor_default_encap_cli = 'neighbor default encapsulation mpls'
                context.vars['evpn_neighbor_default_encap_cli'] = l_0_evpn_neighbor_default_encap_cli
                context.exported_vars.add('evpn_neighbor_default_encap_cli')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_source_interface')):
                    pass
                    l_0_evpn_neighbor_default_encap_cli = str_join(((undefined(name='evpn_neighbor_default_encap_cli') if l_0_evpn_neighbor_default_encap_cli is missing else l_0_evpn_neighbor_default_encap_cli), ' next-hop-self source-interface ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_source_interface'), ))
                    context.vars['evpn_neighbor_default_encap_cli'] = l_0_evpn_neighbor_default_encap_cli
                    context.exported_vars.add('evpn_neighbor_default_encap_cli')
                yield '      '
                yield str((undefined(name='evpn_neighbor_default_encap_cli') if l_0_evpn_neighbor_default_encap_cli is missing else l_0_evpn_neighbor_default_encap_cli))
                yield '\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'encapsulation'), 'path-selection'):
                pass
                yield '      neighbor default encapsulation path-selection\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_mpls_resolution_ribs')):
                pass
                l_0_evpn_mpls_resolution_ribs = []
                context.vars['evpn_mpls_resolution_ribs'] = l_0_evpn_mpls_resolution_ribs
                context.exported_vars.add('evpn_mpls_resolution_ribs')
                for l_1_rib in environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_mpls_resolution_ribs'):
                    _loop_vars = {}
                    pass
                    if t_6(environment.getattr(l_1_rib, 'rib_type'), 'tunnel-rib-colored'):
                        pass
                        context.call(environment.getattr((undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), 'append'), 'tunnel-rib colored system-colored-tunnel-rib', _loop_vars=_loop_vars)
                    elif (t_6(environment.getattr(l_1_rib, 'rib_type'), 'tunnel-rib') and t_6(environment.getattr(l_1_rib, 'rib_name'))):
                        pass
                        context.call(environment.getattr((undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), 'append'), str_join(('tunnel-rib ', environment.getattr(l_1_rib, 'rib_name'), )), _loop_vars=_loop_vars)
                    elif t_6(environment.getattr(l_1_rib, 'rib_type')):
                        pass
                        context.call(environment.getattr((undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), 'append'), environment.getattr(l_1_rib, 'rib_type'), _loop_vars=_loop_vars)
                l_1_rib = missing
                if (undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs):
                    pass
                    yield '      next-hop mpls resolution ribs '
                    yield str(t_5(context.eval_ctx, (undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), ' '))
                    yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups'), 'name'):
                l_1_peer_group_default_route_cli = resolve('peer_group_default_route_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_peer_group, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer_group, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'enabled'), True):
                    pass
                    l_1_peer_group_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-route', ))
                    _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    elif t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    yield '      '
                    yield str((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' additional-paths send\n'
                    elif (t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'ecmp')):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' additional-paths send ecmp limit '
                        yield str(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit'))
                        yield '\n'
                    elif (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'limit'):
                        pass
                        if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit')):
                            pass
                            yield '      neighbor '
                            yield str(environment.getattr(l_1_peer_group, 'name'))
                            yield ' additional-paths send limit '
                            yield str(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit'))
                            yield '\n'
                    else:
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' additional-paths send '
                        yield str(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'))
                        yield '\n'
                if t_6(environment.getattr(l_1_peer_group, 'encapsulation')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' encapsulation '
                    yield str(environment.getattr(l_1_peer_group, 'encapsulation'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer_group, 'domain_remote'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' domain remote\n'
            l_1_peer_group = l_1_peer_group_default_route_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbors'), 'ip_address'):
                l_1_neighbor_default_route_cli = resolve('neighbor_default_route_cli')
                l_1_encapsulation_cli = resolve('encapsulation_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'enabled'), True):
                    pass
                    l_1_neighbor_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-route', ))
                    _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    elif t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send\n'
                    elif (t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'ecmp')):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send ecmp limit '
                        yield str(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit'))
                        yield '\n'
                    elif (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'limit'):
                        pass
                        if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit')):
                            pass
                            yield '      neighbor '
                            yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                            yield ' additional-paths send limit '
                            yield str(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit'))
                            yield '\n'
                    else:
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send '
                        yield str(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'))
                        yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'encapsulation')):
                    pass
                    l_1_encapsulation_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' encapsulation ', environment.getattr(l_1_neighbor, 'encapsulation'), ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                    if ((environment.getattr(l_1_neighbor, 'encapsulation') == 'mpls') and t_6(environment.getattr(l_1_neighbor, 'next_hop_self_source_interface'))):
                        pass
                        l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' next-hop-self source-interface ', environment.getattr(l_1_neighbor, 'next_hop_self_source_interface'), ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                    yield '      '
                    yield str((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli))
                    yield '\n'
            l_1_neighbor = l_1_neighbor_default_route_cli = l_1_encapsulation_cli = missing
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'domain_identifier')):
                pass
                yield '      domain identifier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'domain_identifier'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'domain_identifier_remote')):
                pass
                yield '      domain identifier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'domain_identifier_remote'))
                yield ' remote\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop'), 'resolution_disabled'), True):
                pass
                yield '      next-hop resolution disabled\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '      route import match-failure action discard\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'enable'), True):
                pass
                l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli = 'neighbor default next-hop-self received-evpn-routes route-type ip-prefix'
                context.vars['evpn_neighbor_default_nhs_received_evpn_routes_cli'] = l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli
                context.exported_vars.add('evpn_neighbor_default_nhs_received_evpn_routes_cli')
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'inter_domain'), True):
                    pass
                    l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli = str_join(((undefined(name='evpn_neighbor_default_nhs_received_evpn_routes_cli') if l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli is missing else l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli), ' inter-domain', ))
                    context.vars['evpn_neighbor_default_nhs_received_evpn_routes_cli'] = l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli
                    context.exported_vars.add('evpn_neighbor_default_nhs_received_evpn_routes_cli')
                yield '      '
                yield str((undefined(name='evpn_neighbor_default_nhs_received_evpn_routes_cli') if l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli is missing else l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'enabled'), False):
                pass
                yield '      no host-flap detection\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'enabled'), True):
                pass
                l_0_hostflap_detection_cli = ''
                context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                context.exported_vars.add('hostflap_detection_cli')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'window')):
                    pass
                    l_0_hostflap_detection_cli = str_join(((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli), ' window ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'window'), ))
                    context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                    context.exported_vars.add('hostflap_detection_cli')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'threshold')):
                    pass
                    l_0_hostflap_detection_cli = str_join(((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli), ' threshold ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'threshold'), ))
                    context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                    context.exported_vars.add('hostflap_detection_cli')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'expiry_timeout')):
                    pass
                    l_0_hostflap_detection_cli = str_join(((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli), ' expiry timeout ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'expiry_timeout'), ' seconds', ))
                    context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                    context.exported_vars.add('hostflap_detection_cli')
                if ((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli) != ''):
                    pass
                    yield '      host-flap detection'
                    yield str((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli))
                    yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'layer_2_fec_in_place_update'), 'enabled'), True):
                pass
                l_0_layer2_cli = 'layer-2 fec in-place update'
                context.vars['layer2_cli'] = l_0_layer2_cli
                context.exported_vars.add('layer2_cli')
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'layer_2_fec_in_place_update'), 'timeout')):
                    pass
                    l_0_layer2_cli = str_join(((undefined(name='layer2_cli') if l_0_layer2_cli is missing else l_0_layer2_cli), ' timeout ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'layer_2_fec_in_place_update'), 'timeout'), ' seconds', ))
                    context.vars['layer2_cli'] = l_0_layer2_cli
                    context.exported_vars.add('layer2_cli')
                yield '      '
                yield str((undefined(name='layer2_cli') if l_0_layer2_cli is missing else l_0_layer2_cli))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'import_overlay_index_gateway'), True):
                pass
                yield '      route import overlay-index gateway\n'
            for l_1_segment in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_ethernet_segment'), 'domain'):
                _loop_vars = {}
                pass
                yield '      !\n      evpn ethernet-segment domain '
                yield str(environment.getattr(l_1_segment, 'domain'))
                yield '\n'
                if t_6(environment.getattr(l_1_segment, 'identifier')):
                    pass
                    yield '         identifier '
                    yield str(environment.getattr(l_1_segment, 'identifier'))
                    yield '\n'
                if t_6(environment.getattr(l_1_segment, 'route_target_import')):
                    pass
                    yield '         route-target import '
                    yield str(environment.getattr(l_1_segment, 'route_target_import'))
                    yield '\n'
            l_1_segment = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4')):
            pass
            yield '   !\n   address-family flow-spec ipv4\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6')):
            pass
            yield '   !\n   address-family flow-spec ipv6\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4')):
            pass
            yield '   !\n   address-family ipv4\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'install'), True):
                pass
                yield '      bgp additional-paths install\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'install_ecmp_primary'), True):
                pass
                yield '      bgp additional-paths install ecmp-primary\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send')):
                pass
                if (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send') == 'disabled'):
                    pass
                    yield '      no bgp additional-paths send\n'
                elif (t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send') == 'ecmp')):
                    pass
                    yield '      bgp additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send_limit'))
                    yield '\n'
                elif (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send') == 'limit'):
                    pass
                    if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send_limit')):
                        pass
                        yield '      bgp additional-paths send limit '
                        yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send_limit'))
                        yield '\n'
                else:
                    pass
                    yield '      bgp additional-paths send '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'))
                    yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'peer_groups'), 'name'):
                l_1_neighbor_default_originate_cli = resolve('neighbor_default_originate_cli')
                l_1_add_path_cli = resolve('add_path_cli')
                l_1_nexthop_v6_cli = resolve('nexthop_v6_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_peer_group, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer_group, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer_group, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer_group, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_peer_group, 'default_originate')):
                    pass
                    l_1_neighbor_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-originate', ))
                    _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map')):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map'), ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'always'), True):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' always', ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' additional-paths send\n'
                    else:
                        pass
                        if (t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'ecmp')):
                            pass
                            l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' additional-paths send ecmp limit ', environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        elif (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'limit'):
                            pass
                            if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit')):
                                pass
                                l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' additional-paths send limit ', environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit'), ))
                                _loop_vars['add_path_cli'] = l_1_add_path_cli
                        else:
                            pass
                            l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' additional-paths send ', environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        if (t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'prefix_list')) and t_6((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli))):
                            pass
                            l_1_add_path_cli = str_join(((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli), ' prefix-list ', environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'prefix_list'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        if t_6((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli)):
                            pass
                            yield '      '
                            yield str((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli))
                            yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'next_hop'), 'address_family_ipv6'), 'enabled'), True):
                    pass
                    l_1_nexthop_v6_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' next-hop address-family ipv6', ))
                    _loop_vars['nexthop_v6_cli'] = l_1_nexthop_v6_cli
                    if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'next_hop'), 'address_family_ipv6'), 'originate'), True):
                        pass
                        l_1_nexthop_v6_cli = str_join(((undefined(name='nexthop_v6_cli') if l_1_nexthop_v6_cli is missing else l_1_nexthop_v6_cli), ' originate', ))
                        _loop_vars['nexthop_v6_cli'] = l_1_nexthop_v6_cli
                    yield '      '
                    yield str((undefined(name='nexthop_v6_cli') if l_1_nexthop_v6_cli is missing else l_1_nexthop_v6_cli))
                    yield '\n'
            l_1_peer_group = l_1_neighbor_default_originate_cli = l_1_add_path_cli = l_1_nexthop_v6_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'neighbors'), 'ip_address'):
                l_1_neighbor_default_originate_cli = resolve('neighbor_default_originate_cli')
                l_1_add_path_cli = resolve('add_path_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_neighbor, 'default_originate')):
                    pass
                    l_1_neighbor_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-originate', ))
                    _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map')):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map'), ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'always'), True):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' always', ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send\n'
                    else:
                        pass
                        if (t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'ecmp')):
                            pass
                            l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' additional-paths send ecmp limit ', environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        elif (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'limit'):
                            pass
                            if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit')):
                                pass
                                l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' additional-paths send limit ', environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit'), ))
                                _loop_vars['add_path_cli'] = l_1_add_path_cli
                        else:
                            pass
                            l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' additional-paths send ', environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'prefix_list')):
                            pass
                            l_1_add_path_cli = str_join(((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli), ' prefix-list ', environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'prefix_list'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        if t_6((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli)):
                            pass
                            yield '      '
                            yield str((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli))
                            yield '\n'
            l_1_neighbor = l_1_neighbor_default_originate_cli = l_1_add_path_cli = missing
            for l_1_network in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'networks'), 'prefix'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_network, 'route_map')):
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_network, 'route_map'))
                    yield '\n'
                else:
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield '\n'
            l_1_network = missing
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'redistribute_internal'), True):
                pass
                yield '      bgp redistribute-internal\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'redistribute_internal'), False):
                pass
                yield '      no bgp redistribute-internal\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'redistribute')):
                pass
                l_0_redistribute_var = environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'redistribute')
                context.vars['redistribute_var'] = l_0_redistribute_var
                context.exported_vars.add('redistribute_var')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'enabled'), True):
                    pass
                    l_0_redistribute_host = 'redistribute attached-host'
                    context.vars['redistribute_host'] = l_0_redistribute_host
                    context.exported_vars.add('redistribute_host')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'route_map')):
                        pass
                        l_0_redistribute_host = str_join(((undefined(name='redistribute_host') if l_0_redistribute_host is missing else l_0_redistribute_host), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'route_map'), ))
                        context.vars['redistribute_host'] = l_0_redistribute_host
                        context.exported_vars.add('redistribute_host')
                    yield '      '
                    yield str((undefined(name='redistribute_host') if l_0_redistribute_host is missing else l_0_redistribute_host))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'bgp'), 'enabled'), True):
                    pass
                    l_0_redistribute_bgp = 'redistribute bgp leaked'
                    context.vars['redistribute_bgp'] = l_0_redistribute_bgp
                    context.exported_vars.add('redistribute_bgp')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'bgp'), 'route_map')):
                        pass
                        l_0_redistribute_bgp = str_join(((undefined(name='redistribute_bgp') if l_0_redistribute_bgp is missing else l_0_redistribute_bgp), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'bgp'), 'route_map'), ))
                        context.vars['redistribute_bgp'] = l_0_redistribute_bgp
                        context.exported_vars.add('redistribute_bgp')
                    yield '      '
                    yield str((undefined(name='redistribute_bgp') if l_0_redistribute_bgp is missing else l_0_redistribute_bgp))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'enabled'), True):
                    pass
                    l_0_redistribute_conn = 'redistribute connected'
                    context.vars['redistribute_conn'] = l_0_redistribute_conn
                    context.exported_vars.add('redistribute_conn')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' include leaked', ))
                        context.vars['redistribute_conn'] = l_0_redistribute_conn
                        context.exported_vars.add('redistribute_conn')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'route_map')):
                        pass
                        l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'route_map'), ))
                        context.vars['redistribute_conn'] = l_0_redistribute_conn
                        context.exported_vars.add('redistribute_conn')
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'rcf')):
                        pass
                        l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'rcf'), ))
                        context.vars['redistribute_conn'] = l_0_redistribute_conn
                        context.exported_vars.add('redistribute_conn')
                    yield '      '
                    yield str((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'enabled'), True):
                    pass
                    l_0_redistribute_dynamic = 'redistribute dynamic'
                    context.vars['redistribute_dynamic'] = l_0_redistribute_dynamic
                    context.exported_vars.add('redistribute_dynamic')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'route_map')):
                        pass
                        l_0_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_0_redistribute_dynamic is missing else l_0_redistribute_dynamic), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'route_map'), ))
                        context.vars['redistribute_dynamic'] = l_0_redistribute_dynamic
                        context.exported_vars.add('redistribute_dynamic')
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'rcf')):
                        pass
                        l_0_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_0_redistribute_dynamic is missing else l_0_redistribute_dynamic), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'rcf'), ))
                        context.vars['redistribute_dynamic'] = l_0_redistribute_dynamic
                        context.exported_vars.add('redistribute_dynamic')
                    yield '      '
                    yield str((undefined(name='redistribute_dynamic') if l_0_redistribute_dynamic is missing else l_0_redistribute_dynamic))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'user'), 'enabled'), True):
                    pass
                    l_0_redistribute_user = 'redistribute user'
                    context.vars['redistribute_user'] = l_0_redistribute_user
                    context.exported_vars.add('redistribute_user')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'user'), 'rcf')):
                        pass
                        l_0_redistribute_user = str_join(((undefined(name='redistribute_user') if l_0_redistribute_user is missing else l_0_redistribute_user), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'user'), 'rcf'), ))
                        context.vars['redistribute_user'] = l_0_redistribute_user
                        context.exported_vars.add('redistribute_user')
                    yield '      '
                    yield str((undefined(name='redistribute_user') if l_0_redistribute_user is missing else l_0_redistribute_user))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'enabled'), True):
                    pass
                    l_0_redistribute_isis = 'redistribute isis'
                    context.vars['redistribute_isis'] = l_0_redistribute_isis
                    context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'isis_level')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'isis_level'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' include leaked', ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'route_map')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'route_map'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'rcf')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'rcf'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    yield '      '
                    yield str((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf = 'redistribute ospf'
                    context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                    context.exported_vars.add('redistribute_ospf')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' include leaked', ))
                        context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                        context.exported_vars.add('redistribute_ospf')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'route_map')):
                        pass
                        l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'route_map'), ))
                        context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                        context.exported_vars.add('redistribute_ospf')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf = 'redistribute ospf match internal'
                    context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                    context.exported_vars.add('redistribute_ospf')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' include leaked', ))
                        context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                        context.exported_vars.add('redistribute_ospf')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'route_map')):
                        pass
                        l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'route_map'), ))
                        context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                        context.exported_vars.add('redistribute_ospf')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3 = 'redistribute ospfv3'
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' include leaked', ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'route_map'), ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3 = 'redistribute ospfv3 match internal'
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' include leaked', ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map'), ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3_match = 'redistribute ospfv3 match external'
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' include leaked', ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'route_map'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3_match = 'redistribute ospfv3 match nssa-external'
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' include leaked', ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf_match = 'redistribute ospf match external'
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' include leaked', ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'route_map'), ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf_match = 'redistribute ospf match nssa-external'
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type')):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type'), ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' include leaked', ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map'), ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'rip'), 'enabled'), True):
                    pass
                    l_0_redistribute_rip = 'redistribute rip'
                    context.vars['redistribute_rip'] = l_0_redistribute_rip
                    context.exported_vars.add('redistribute_rip')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'rip'), 'route_map')):
                        pass
                        l_0_redistribute_rip = str_join(((undefined(name='redistribute_rip') if l_0_redistribute_rip is missing else l_0_redistribute_rip), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'rip'), 'route_map'), ))
                        context.vars['redistribute_rip'] = l_0_redistribute_rip
                        context.exported_vars.add('redistribute_rip')
                    yield '      '
                    yield str((undefined(name='redistribute_rip') if l_0_redistribute_rip is missing else l_0_redistribute_rip))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'enabled'), True):
                    pass
                    l_0_redistribute_static = 'redistribute static'
                    context.vars['redistribute_static'] = l_0_redistribute_static
                    context.exported_vars.add('redistribute_static')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' include leaked', ))
                        context.vars['redistribute_static'] = l_0_redistribute_static
                        context.exported_vars.add('redistribute_static')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'route_map')):
                        pass
                        l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'route_map'), ))
                        context.vars['redistribute_static'] = l_0_redistribute_static
                        context.exported_vars.add('redistribute_static')
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'rcf')):
                        pass
                        l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'rcf'), ))
                        context.vars['redistribute_static'] = l_0_redistribute_static
                        context.exported_vars.add('redistribute_static')
                    yield '      '
                    yield str((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static))
                    yield '\n'
            elif t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'redistribute_routes')):
                pass
                for l_1_redistribute_route in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'redistribute_routes'), 'source_protocol'):
                    l_1_redistribute_route_cli = missing
                    _loop_vars = {}
                    pass
                    l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                        pass
                        if t_6(environment.getattr(l_1_redistribute_route, 'ospf_route_type')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'bgp'):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif (t_6(environment.getattr(l_1_redistribute_route, 'include_leaked'), True) and (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'ospf', 'ospfv3'])):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_6(environment.getattr(l_1_redistribute_route, 'route_map')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                        pass
                        if t_6(environment.getattr(l_1_redistribute_route, 'rcf')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' rcf ', environment.getattr(l_1_redistribute_route, 'rcf'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                    yield '\n'
                l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast')):
            pass
            yield '   !\n   address-family ipv4 labeled-unicast\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'update_wait_for_convergence'), True):
                pass
                yield '      update wait-for-convergence\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'missing_policy')):
                pass
                for l_1_direction in ['in', 'out']:
                    l_1_missing_policy_cli = resolve('missing_policy_cli')
                    l_1_dir = l_1_policy = missing
                    _loop_vars = {}
                    pass
                    l_1_dir = str_join(('direction_', l_1_direction, ))
                    _loop_vars['dir'] = l_1_dir
                    l_1_policy = environment.getitem(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'missing_policy'), (undefined(name='dir') if l_1_dir is missing else l_1_dir))
                    _loop_vars['policy'] = l_1_policy
                    if t_6(environment.getattr((undefined(name='policy') if l_1_policy is missing else l_1_policy), 'action')):
                        pass
                        l_1_missing_policy_cli = 'bgp missing-policy'
                        _loop_vars['missing_policy_cli'] = l_1_missing_policy_cli
                        if ((t_6(environment.getattr((undefined(name='policy') if l_1_policy is missing else l_1_policy), 'include_community_list'), True) or t_6(environment.getattr((undefined(name='policy') if l_1_policy is missing else l_1_policy), 'include_prefix_list'), True)) or t_6(environment.getattr((undefined(name='policy') if l_1_policy is missing else l_1_policy), 'include_sub_route_map'), True)):
                            pass
                            l_1_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_1_missing_policy_cli is missing else l_1_missing_policy_cli), ' include', ))
                            _loop_vars['missing_policy_cli'] = l_1_missing_policy_cli
                            if t_6(environment.getattr((undefined(name='policy') if l_1_policy is missing else l_1_policy), 'include_community_list'), True):
                                pass
                                l_1_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_1_missing_policy_cli is missing else l_1_missing_policy_cli), ' community-list', ))
                                _loop_vars['missing_policy_cli'] = l_1_missing_policy_cli
                            if t_6(environment.getattr((undefined(name='policy') if l_1_policy is missing else l_1_policy), 'include_prefix_list'), True):
                                pass
                                l_1_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_1_missing_policy_cli is missing else l_1_missing_policy_cli), ' prefix-list', ))
                                _loop_vars['missing_policy_cli'] = l_1_missing_policy_cli
                            if t_6(environment.getattr((undefined(name='policy') if l_1_policy is missing else l_1_policy), 'include_sub_route_map'), True):
                                pass
                                l_1_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_1_missing_policy_cli is missing else l_1_missing_policy_cli), ' sub-route-map', ))
                                _loop_vars['missing_policy_cli'] = l_1_missing_policy_cli
                        l_1_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_1_missing_policy_cli is missing else l_1_missing_policy_cli), ' direction ', l_1_direction, ' action ', environment.getattr((undefined(name='policy') if l_1_policy is missing else l_1_policy), 'action'), ))
                        _loop_vars['missing_policy_cli'] = l_1_missing_policy_cli
                        yield '      '
                        yield str((undefined(name='missing_policy_cli') if l_1_missing_policy_cli is missing else l_1_missing_policy_cli))
                        yield '\n'
                l_1_direction = l_1_dir = l_1_policy = l_1_missing_policy_cli = missing
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'additional_paths'), 'send')):
                pass
                if (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'additional_paths'), 'send') == 'disabled'):
                    pass
                    yield '      no bgp additional-paths send\n'
                elif (t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'additional_paths'), 'send') == 'ecmp')):
                    pass
                    yield '      bgp additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'additional_paths'), 'send_limit'))
                    yield '\n'
                elif (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'additional_paths'), 'send') == 'limit'):
                    pass
                    if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'additional_paths'), 'send_limit')):
                        pass
                        yield '      bgp additional-paths send limit '
                        yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'additional_paths'), 'send_limit'))
                        yield '\n'
                else:
                    pass
                    yield '      bgp additional-paths send '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'additional_paths'), 'send'))
                    yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'bgp'), 'next_hop_unchanged'), True):
                pass
                yield '      bgp next-hop-unchanged\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'neighbor_default'), 'next_hop_self'), True):
                pass
                yield '      neighbor default next-hop-self\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'next_hop_resolution_ribs')):
                pass
                l_0_v4_bgp_lu_resolution_ribs = []
                context.vars['v4_bgp_lu_resolution_ribs'] = l_0_v4_bgp_lu_resolution_ribs
                context.exported_vars.add('v4_bgp_lu_resolution_ribs')
                for l_1_rib in environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'next_hop_resolution_ribs'):
                    _loop_vars = {}
                    pass
                    if t_6(environment.getattr(l_1_rib, 'rib_type'), 'tunnel-rib-colored'):
                        pass
                        context.call(environment.getattr((undefined(name='v4_bgp_lu_resolution_ribs') if l_0_v4_bgp_lu_resolution_ribs is missing else l_0_v4_bgp_lu_resolution_ribs), 'append'), 'tunnel-rib colored system-colored-tunnel-rib', _loop_vars=_loop_vars)
                    elif t_6(environment.getattr(l_1_rib, 'rib_type'), 'tunnel-rib'):
                        pass
                        if t_6(environment.getattr(l_1_rib, 'rib_name')):
                            pass
                            context.call(environment.getattr((undefined(name='v4_bgp_lu_resolution_ribs') if l_0_v4_bgp_lu_resolution_ribs is missing else l_0_v4_bgp_lu_resolution_ribs), 'append'), str_join(('tunnel-rib ', environment.getattr(l_1_rib, 'rib_name'), )), _loop_vars=_loop_vars)
                    elif t_6(environment.getattr(l_1_rib, 'rib_type')):
                        pass
                        context.call(environment.getattr((undefined(name='v4_bgp_lu_resolution_ribs') if l_0_v4_bgp_lu_resolution_ribs is missing else l_0_v4_bgp_lu_resolution_ribs), 'append'), environment.getattr(l_1_rib, 'rib_type'), _loop_vars=_loop_vars)
                l_1_rib = missing
                if (undefined(name='v4_bgp_lu_resolution_ribs') if l_0_v4_bgp_lu_resolution_ribs is missing else l_0_v4_bgp_lu_resolution_ribs):
                    pass
                    yield '      next-hop resolution ribs '
                    yield str(t_5(context.eval_ctx, (undefined(name='v4_bgp_lu_resolution_ribs') if l_0_v4_bgp_lu_resolution_ribs is missing else l_0_v4_bgp_lu_resolution_ribs), ' '))
                    yield '\n'
            for l_1_peer in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'peer_groups'), 'name'):
                l_1_maximum_routes_cli = resolve('maximum_routes_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' activate\n'
                else:
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_peer, 'graceful_restart'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' graceful-restart\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer, 'graceful_restart_helper'), 'stale_route_map')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' graceful-restart-helper stale-route route-map '
                    yield str(environment.getattr(environment.getattr(l_1_peer, 'graceful_restart_helper'), 'stale_route_map'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_peer, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_peer, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_1_peer, 'name'))
                        yield ' additional-paths send\n'
                    elif (t_6(environment.getattr(environment.getattr(l_1_peer, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_1_peer, 'additional_paths'), 'send') == 'ecmp')):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer, 'name'))
                        yield ' additional-paths send ecmp limit '
                        yield str(environment.getattr(environment.getattr(l_1_peer, 'additional_paths'), 'send_limit'))
                        yield '\n'
                    elif (environment.getattr(environment.getattr(l_1_peer, 'additional_paths'), 'send') == 'limit'):
                        pass
                        if t_6(environment.getattr(environment.getattr(l_1_peer, 'additional_paths'), 'send_limit')):
                            pass
                            yield '      neighbor '
                            yield str(environment.getattr(l_1_peer, 'name'))
                            yield ' additional-paths send limit '
                            yield str(environment.getattr(environment.getattr(l_1_peer, 'additional_paths'), 'send_limit'))
                            yield '\n'
                    else:
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer, 'name'))
                        yield ' additional-paths send '
                        yield str(environment.getattr(environment.getattr(l_1_peer, 'additional_paths'), 'send'))
                        yield '\n'
                if t_6(environment.getattr(l_1_peer, 'next_hop_unchanged'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' next-hop-unchanged\n'
                if t_6(environment.getattr(l_1_peer, 'next_hop_self'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' next-hop-self\n'
                if t_6(environment.getattr(l_1_peer, 'next_hop_self_v4_mapped_v6_source_interface')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' next-hop-self v4-mapped-v6 source-interface '
                    yield str(environment.getattr(l_1_peer, 'next_hop_self_v4_mapped_v6_source_interface'))
                    yield '\n'
                elif t_6(environment.getattr(l_1_peer, 'next_hop_self_source_interface')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' next-hop-self source-interface '
                    yield str(environment.getattr(l_1_peer, 'next_hop_self_source_interface'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer, 'maximum_advertised_routes')):
                    pass
                    l_1_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_1_peer, 'name'), ' maximum-advertised-routes ', environment.getattr(l_1_peer, 'maximum_advertised_routes'), ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                    if t_6(environment.getattr(l_1_peer, 'maximum_advertised_routes_warning_limit')):
                        pass
                        l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-limit ', environment.getattr(l_1_peer, 'maximum_advertised_routes_warning_limit'), ))
                        _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                    yield '      '
                    yield str((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer, 'missing_policy')):
                    pass
                    for l_2_direction in ['in', 'out']:
                        l_2_missing_policy_cli = resolve('missing_policy_cli')
                        l_2_dir = l_2_policy = missing
                        _loop_vars = {}
                        pass
                        l_2_dir = str_join(('direction_', l_2_direction, ))
                        _loop_vars['dir'] = l_2_dir
                        l_2_policy = environment.getitem(environment.getattr(l_1_peer, 'missing_policy'), (undefined(name='dir') if l_2_dir is missing else l_2_dir))
                        _loop_vars['policy'] = l_2_policy
                        if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action')):
                            pass
                            l_2_missing_policy_cli = str_join(('neighbor ', environment.getattr(l_1_peer, 'name'), ' missing-policy', ))
                            _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if ((t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True) or t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True)) or t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True)):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' include', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                                if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True):
                                    pass
                                    l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' community-list', ))
                                    _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                                if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True):
                                    pass
                                    l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' prefix-list', ))
                                    _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                                if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True):
                                    pass
                                    l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' sub-route-map', ))
                                    _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' direction ', l_2_direction, ' action ', environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action'), ))
                            _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            yield '      '
                            yield str((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli))
                            yield '\n'
                    l_2_direction = l_2_dir = l_2_policy = l_2_missing_policy_cli = missing
                if t_6(environment.getattr(l_1_peer, 'aigp_session'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' aigp-session\n'
                if t_6(environment.getattr(l_1_peer, 'multi_path'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer, 'name'))
                    yield ' multi-path\n'
            l_1_peer = l_1_maximum_routes_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'neighbors'), 'ip_address'):
                l_1_maximum_routes_cli = resolve('maximum_routes_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                else:
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_neighbor, 'graceful_restart'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' graceful-restart\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'graceful_restart_helper'), 'stale_route_map')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' graceful-restart-helper stale-route route-map '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'graceful_restart_helper'), 'stale_route_map'))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send\n'
                    elif (t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'ecmp')):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send ecmp limit '
                        yield str(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit'))
                        yield '\n'
                    elif (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'limit'):
                        pass
                        if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit')):
                            pass
                            yield '      neighbor '
                            yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                            yield ' additional-paths send limit '
                            yield str(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit'))
                            yield '\n'
                    else:
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send '
                        yield str(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'))
                        yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'next_hop_unchanged'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' next-hop-unchanged\n'
                if t_6(environment.getattr(l_1_neighbor, 'next_hop_self'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' next-hop-self\n'
                if t_6(environment.getattr(l_1_neighbor, 'next_hop_self_v4_mapped_v6_source_interface')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' next-hop-self v4-mapped-v6 source-interface '
                    yield str(environment.getattr(l_1_neighbor, 'next_hop_self_v4_mapped_v6_source_interface'))
                    yield '\n'
                elif t_6(environment.getattr(l_1_neighbor, 'next_hop_self_source_interface')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' next-hop-self source-interface '
                    yield str(environment.getattr(l_1_neighbor, 'next_hop_self_source_interface'))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'maximum_advertised_routes')):
                    pass
                    l_1_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' maximum-advertised-routes ', environment.getattr(l_1_neighbor, 'maximum_advertised_routes'), ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                    if t_6(environment.getattr(l_1_neighbor, 'maximum_advertised_routes_warning_limit')):
                        pass
                        l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-limit ', environment.getattr(l_1_neighbor, 'maximum_advertised_routes_warning_limit'), ))
                        _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                    yield '      '
                    yield str((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'missing_policy')):
                    pass
                    for l_2_direction in ['in', 'out']:
                        l_2_missing_policy_cli = resolve('missing_policy_cli')
                        l_2_dir = l_2_policy = missing
                        _loop_vars = {}
                        pass
                        l_2_dir = str_join(('direction_', l_2_direction, ))
                        _loop_vars['dir'] = l_2_dir
                        l_2_policy = environment.getitem(environment.getattr(l_1_neighbor, 'missing_policy'), (undefined(name='dir') if l_2_dir is missing else l_2_dir))
                        _loop_vars['policy'] = l_2_policy
                        if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action')):
                            pass
                            l_2_missing_policy_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' missing-policy ', ))
                            _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if ((t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True) or t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True)) or t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True)):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' include', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                                if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True):
                                    pass
                                    l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' community-list', ))
                                    _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                                if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True):
                                    pass
                                    l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' prefix-list', ))
                                    _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                                if t_6(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True):
                                    pass
                                    l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' sub-route-map', ))
                                    _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' direction ', l_2_direction, ' action ', environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action'), ))
                            _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            yield '      '
                            yield str((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli))
                            yield '\n'
                    l_2_direction = l_2_dir = l_2_policy = l_2_missing_policy_cli = missing
                if t_6(environment.getattr(l_1_neighbor, 'aigp_session'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' aigp-session\n'
                if t_6(environment.getattr(l_1_neighbor, 'multi_path'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' multi-path\n'
            l_1_neighbor = l_1_maximum_routes_cli = missing
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'networks')):
                pass
                for l_1_network in environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'networks'):
                    l_1_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_1_network_cli = str_join(('network ', environment.getattr(l_1_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_1_network_cli
                    if t_6(environment.getattr(l_1_network, 'route_map')):
                        pass
                        l_1_network_cli = str_join(((undefined(name='network_cli') if l_1_network_cli is missing else l_1_network_cli), ' route-map ', environment.getattr(l_1_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_1_network_cli
                    yield '      '
                    yield str((undefined(name='network_cli') if l_1_network_cli is missing else l_1_network_cli))
                    yield '\n'
                l_1_network = l_1_network_cli = missing
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'next_hops')):
                pass
                for l_1_next_hop in environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'next_hops'):
                    l_1_next_hop_cli = missing
                    _loop_vars = {}
                    pass
                    l_1_next_hop_cli = str_join(('next-hop ', environment.getattr(l_1_next_hop, 'ip_address'), ' originate', ))
                    _loop_vars['next_hop_cli'] = l_1_next_hop_cli
                    if t_6(environment.getattr(l_1_next_hop, 'lfib_backup_ip_forwarding'), True):
                        pass
                        l_1_next_hop_cli = str_join(((undefined(name='next_hop_cli') if l_1_next_hop_cli is missing else l_1_next_hop_cli), ' lfib-backup ip-forwarding', ))
                        _loop_vars['next_hop_cli'] = l_1_next_hop_cli
                    yield '      '
                    yield str((undefined(name='next_hop_cli') if l_1_next_hop_cli is missing else l_1_next_hop_cli))
                    yield '\n'
                l_1_next_hop = l_1_next_hop_cli = missing
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'lfib_entry_installation_skipped'), True):
                pass
                yield '      lfib entry installation skipped\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'label_local_termination')):
                pass
                yield '      label local-termination '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'label_local_termination'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'graceful_restart'), True):
                pass
                yield '      graceful-restart\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'tunnel_source_protocols')):
                pass
                for l_1_tunnel_source_protocol in environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'tunnel_source_protocols'):
                    l_1_tunnel_source_protocol_cli = missing
                    _loop_vars = {}
                    pass
                    l_1_tunnel_source_protocol_cli = str_join(('tunnel source-protocol ', environment.getattr(l_1_tunnel_source_protocol, 'protocol'), ))
                    _loop_vars['tunnel_source_protocol_cli'] = l_1_tunnel_source_protocol_cli
                    if t_6(environment.getattr(l_1_tunnel_source_protocol, 'rcf')):
                        pass
                        l_1_tunnel_source_protocol_cli = str_join(((undefined(name='tunnel_source_protocol_cli') if l_1_tunnel_source_protocol_cli is missing else l_1_tunnel_source_protocol_cli), ' rcf ', environment.getattr(l_1_tunnel_source_protocol, 'rcf'), ))
                        _loop_vars['tunnel_source_protocol_cli'] = l_1_tunnel_source_protocol_cli
                    yield '      '
                    yield str((undefined(name='tunnel_source_protocol_cli') if l_1_tunnel_source_protocol_cli is missing else l_1_tunnel_source_protocol_cli))
                    yield '\n'
                l_1_tunnel_source_protocol = l_1_tunnel_source_protocol_cli = missing
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'aigp_session')):
                pass
                for l_1_aigp_session_type in ['ibgp', 'confederation', 'ebgp']:
                    _loop_vars = {}
                    pass
                    if t_6(environment.getitem(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_labeled_unicast'), 'aigp_session'), l_1_aigp_session_type), True):
                        pass
                        yield '      aigp-session '
                        yield str(l_1_aigp_session_type)
                        yield '\n'
                l_1_aigp_session_type = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast')):
            pass
            yield '   !\n   address-family ipv4 multicast\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'redistribute')):
                pass
                l_0_redistribute_var = environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'redistribute')
                context.vars['redistribute_var'] = l_0_redistribute_var
                context.exported_vars.add('redistribute_var')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'enabled'), True):
                    pass
                    l_0_redistribute_host = 'redistribute attached-host'
                    context.vars['redistribute_host'] = l_0_redistribute_host
                    context.exported_vars.add('redistribute_host')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'route_map')):
                        pass
                        l_0_redistribute_host = str_join(((undefined(name='redistribute_host') if l_0_redistribute_host is missing else l_0_redistribute_host), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'route_map'), ))
                        context.vars['redistribute_host'] = l_0_redistribute_host
                        context.exported_vars.add('redistribute_host')
                    yield '      '
                    yield str((undefined(name='redistribute_host') if l_0_redistribute_host is missing else l_0_redistribute_host))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'enabled'), True):
                    pass
                    l_0_redistribute_conn = 'redistribute connected'
                    context.vars['redistribute_conn'] = l_0_redistribute_conn
                    context.exported_vars.add('redistribute_conn')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'route_map')):
                        pass
                        l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'route_map'), ))
                        context.vars['redistribute_conn'] = l_0_redistribute_conn
                        context.exported_vars.add('redistribute_conn')
                    yield '      '
                    yield str((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'enabled'), True):
                    pass
                    l_0_redistribute_isis = 'redistribute isis'
                    context.vars['redistribute_isis'] = l_0_redistribute_isis
                    context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'isis_level')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'isis_level'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' include leaked', ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'route_map')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'route_map'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'rcf')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'rcf'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    yield '      '
                    yield str((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf = 'redistribute ospf'
                    context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                    context.exported_vars.add('redistribute_ospf')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'route_map')):
                        pass
                        l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'route_map'), ))
                        context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                        context.exported_vars.add('redistribute_ospf')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf = 'redistribute ospf match internal'
                    context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                    context.exported_vars.add('redistribute_ospf')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'route_map')):
                        pass
                        l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'route_map'), ))
                        context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                        context.exported_vars.add('redistribute_ospf')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3 = 'redistribute ospfv3'
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'route_map'), ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3 = 'redistribute ospfv3 match internal'
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map'), ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3_match = 'redistribute ospfv3 match external'
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'route_map'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3_match = 'redistribute ospfv3 match nssa-external'
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf_match = 'redistribute ospf match external'
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'route_map'), ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf_match = 'redistribute ospf match nssa-external'
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type')):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type'), ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map'), ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'enabled'), True):
                    pass
                    l_0_redistribute_static = 'redistribute static'
                    context.vars['redistribute_static'] = l_0_redistribute_static
                    context.exported_vars.add('redistribute_static')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'route_map')):
                        pass
                        l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'route_map'), ))
                        context.vars['redistribute_static'] = l_0_redistribute_static
                        context.exported_vars.add('redistribute_static')
                    yield '      '
                    yield str((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static))
                    yield '\n'
            elif t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'redistribute_routes')):
                pass
                for l_1_redistribute_route in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'redistribute_routes'), 'source_protocol'):
                    l_1_redistribute_route_cli = missing
                    _loop_vars = {}
                    pass
                    l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                        pass
                        if t_6(environment.getattr(l_1_redistribute_route, 'ospf_route_type')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (t_6(environment.getattr(l_1_redistribute_route, 'include_leaked'), True) and (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'isis')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_6(environment.getattr(l_1_redistribute_route, 'route_map')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif ((environment.getattr(l_1_redistribute_route, 'source_protocol') == 'isis') and t_6(environment.getattr(l_1_redistribute_route, 'rcf'))):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' rcf ', environment.getattr(l_1_redistribute_route, 'rcf'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                    yield '\n'
                l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te')):
            pass
            yield '   !\n   address-family ipv4 sr-te\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6')):
            pass
            yield '   !\n   address-family ipv6\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'install'), True):
                pass
                yield '      bgp additional-paths install\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'install_ecmp_primary'), True):
                pass
                yield '      bgp additional-paths install ecmp-primary\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send')):
                pass
                if (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send') == 'disabled'):
                    pass
                    yield '      no bgp additional-paths send\n'
                elif (t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send') == 'ecmp')):
                    pass
                    yield '      bgp additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send_limit'))
                    yield '\n'
                elif (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send') == 'limit'):
                    pass
                    if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send_limit')):
                        pass
                        yield '      bgp additional-paths send limit '
                        yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send_limit'))
                        yield '\n'
                else:
                    pass
                    yield '      bgp additional-paths send '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'))
                    yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'peer_groups'), 'name'):
                l_1_add_path_cli = resolve('add_path_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_peer_group, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer_group, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer_group, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer_group, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_out'))
                    yield ' out\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' additional-paths send\n'
                    else:
                        pass
                        if (t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'ecmp')):
                            pass
                            l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' additional-paths send ecmp limit ', environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        elif (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'limit'):
                            pass
                            if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit')):
                                pass
                                l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' additional-paths send limit ', environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit'), ))
                                _loop_vars['add_path_cli'] = l_1_add_path_cli
                        else:
                            pass
                            l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' additional-paths send ', environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'prefix_list')):
                            pass
                            l_1_add_path_cli = str_join(((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli), ' prefix-list ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'prefix_list'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        if t_6((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli)):
                            pass
                            yield '      '
                            yield str((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli))
                            yield '\n'
            l_1_peer_group = l_1_add_path_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'neighbors'), 'ip_address'):
                l_1_add_path_cli = resolve('add_path_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_out'))
                    yield ' out\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send\n'
                    else:
                        pass
                        if (t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'ecmp')):
                            pass
                            l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' additional-paths send ecmp limit ', environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        elif (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'limit'):
                            pass
                            if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit')):
                                pass
                                l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' additional-paths send limit ', environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit'), ))
                                _loop_vars['add_path_cli'] = l_1_add_path_cli
                        else:
                            pass
                            l_1_add_path_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' additional-paths send ', environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'prefix_list')):
                            pass
                            l_1_add_path_cli = str_join(((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli), ' prefix-list ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'prefix_list'), ))
                            _loop_vars['add_path_cli'] = l_1_add_path_cli
                        if t_6((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli)):
                            pass
                            yield '      '
                            yield str((undefined(name='add_path_cli') if l_1_add_path_cli is missing else l_1_add_path_cli))
                            yield '\n'
            l_1_neighbor = l_1_add_path_cli = missing
            for l_1_network in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'networks'), 'prefix'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_network, 'route_map')):
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_network, 'route_map'))
                    yield '\n'
                else:
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield '\n'
            l_1_network = missing
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'redistribute_internal'), True):
                pass
                yield '      bgp redistribute-internal\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'redistribute_internal'), False):
                pass
                yield '      no bgp redistribute-internal\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'redistribute')):
                pass
                l_0_redistribute_var = environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'redistribute')
                context.vars['redistribute_var'] = l_0_redistribute_var
                context.exported_vars.add('redistribute_var')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'enabled'), True):
                    pass
                    l_0_redistribute_host = 'redistribute attached-host'
                    context.vars['redistribute_host'] = l_0_redistribute_host
                    context.exported_vars.add('redistribute_host')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'route_map')):
                        pass
                        l_0_redistribute_host = str_join(((undefined(name='redistribute_host') if l_0_redistribute_host is missing else l_0_redistribute_host), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'attached_host'), 'route_map'), ))
                        context.vars['redistribute_host'] = l_0_redistribute_host
                        context.exported_vars.add('redistribute_host')
                    yield '      '
                    yield str((undefined(name='redistribute_host') if l_0_redistribute_host is missing else l_0_redistribute_host))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'bgp'), 'enabled'), True):
                    pass
                    l_0_redistribute_bgp = 'redistribute bgp leaked'
                    context.vars['redistribute_bgp'] = l_0_redistribute_bgp
                    context.exported_vars.add('redistribute_bgp')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'bgp'), 'route_map')):
                        pass
                        l_0_redistribute_bgp = str_join(((undefined(name='redistribute_bgp') if l_0_redistribute_bgp is missing else l_0_redistribute_bgp), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'bgp'), 'route_map'), ))
                        context.vars['redistribute_bgp'] = l_0_redistribute_bgp
                        context.exported_vars.add('redistribute_bgp')
                    yield '      '
                    yield str((undefined(name='redistribute_bgp') if l_0_redistribute_bgp is missing else l_0_redistribute_bgp))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dhcp'), 'enabled'), True):
                    pass
                    l_0_redistribute_dhcp = 'redistribute dhcp'
                    context.vars['redistribute_dhcp'] = l_0_redistribute_dhcp
                    context.exported_vars.add('redistribute_dhcp')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dhcp'), 'route_map')):
                        pass
                        l_0_redistribute_dhcp = str_join(((undefined(name='redistribute_dhcp') if l_0_redistribute_dhcp is missing else l_0_redistribute_dhcp), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dhcp'), 'route_map'), ))
                        context.vars['redistribute_dhcp'] = l_0_redistribute_dhcp
                        context.exported_vars.add('redistribute_dhcp')
                    yield '      '
                    yield str((undefined(name='redistribute_dhcp') if l_0_redistribute_dhcp is missing else l_0_redistribute_dhcp))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'enabled'), True):
                    pass
                    l_0_redistribute_conn = 'redistribute connected'
                    context.vars['redistribute_conn'] = l_0_redistribute_conn
                    context.exported_vars.add('redistribute_conn')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' include leaked', ))
                        context.vars['redistribute_conn'] = l_0_redistribute_conn
                        context.exported_vars.add('redistribute_conn')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'route_map')):
                        pass
                        l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'route_map'), ))
                        context.vars['redistribute_conn'] = l_0_redistribute_conn
                        context.exported_vars.add('redistribute_conn')
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'rcf')):
                        pass
                        l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'rcf'), ))
                        context.vars['redistribute_conn'] = l_0_redistribute_conn
                        context.exported_vars.add('redistribute_conn')
                    yield '      '
                    yield str((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'enabled'), True):
                    pass
                    l_0_redistribute_dynamic = 'redistribute dynamic'
                    context.vars['redistribute_dynamic'] = l_0_redistribute_dynamic
                    context.exported_vars.add('redistribute_dynamic')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'route_map')):
                        pass
                        l_0_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_0_redistribute_dynamic is missing else l_0_redistribute_dynamic), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'route_map'), ))
                        context.vars['redistribute_dynamic'] = l_0_redistribute_dynamic
                        context.exported_vars.add('redistribute_dynamic')
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'rcf')):
                        pass
                        l_0_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_0_redistribute_dynamic is missing else l_0_redistribute_dynamic), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'dynamic'), 'rcf'), ))
                        context.vars['redistribute_dynamic'] = l_0_redistribute_dynamic
                        context.exported_vars.add('redistribute_dynamic')
                    yield '      '
                    yield str((undefined(name='redistribute_dynamic') if l_0_redistribute_dynamic is missing else l_0_redistribute_dynamic))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'user'), 'enabled'), True):
                    pass
                    l_0_redistribute_user = 'redistribute user'
                    context.vars['redistribute_user'] = l_0_redistribute_user
                    context.exported_vars.add('redistribute_user')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'user'), 'rcf')):
                        pass
                        l_0_redistribute_user = str_join(((undefined(name='redistribute_user') if l_0_redistribute_user is missing else l_0_redistribute_user), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'user'), 'rcf'), ))
                        context.vars['redistribute_user'] = l_0_redistribute_user
                        context.exported_vars.add('redistribute_user')
                    yield '      '
                    yield str((undefined(name='redistribute_user') if l_0_redistribute_user is missing else l_0_redistribute_user))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'enabled'), True):
                    pass
                    l_0_redistribute_isis = 'redistribute isis'
                    context.vars['redistribute_isis'] = l_0_redistribute_isis
                    context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'isis_level')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'isis_level'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' include leaked', ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'route_map')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'route_map'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'rcf')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'rcf'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    yield '      '
                    yield str((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3 = 'redistribute ospfv3'
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' include leaked', ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'route_map'), ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3 = 'redistribute ospfv3 match internal'
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' include leaked', ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map'), ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3_match = 'redistribute ospfv3 match external'
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' include leaked', ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'route_map'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3_match = 'redistribute ospfv3 match nssa-external'
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' include leaked', ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'enabled'), True):
                    pass
                    l_0_redistribute_static = 'redistribute static'
                    context.vars['redistribute_static'] = l_0_redistribute_static
                    context.exported_vars.add('redistribute_static')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' include leaked', ))
                        context.vars['redistribute_static'] = l_0_redistribute_static
                        context.exported_vars.add('redistribute_static')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'route_map')):
                        pass
                        l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'route_map'), ))
                        context.vars['redistribute_static'] = l_0_redistribute_static
                        context.exported_vars.add('redistribute_static')
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'rcf')):
                        pass
                        l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'rcf'), ))
                        context.vars['redistribute_static'] = l_0_redistribute_static
                        context.exported_vars.add('redistribute_static')
                    yield '      '
                    yield str((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static))
                    yield '\n'
            elif t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'redistribute_routes')):
                pass
                for l_1_redistribute_route in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'redistribute_routes'), 'source_protocol'):
                    l_1_redistribute_route_cli = missing
                    _loop_vars = {}
                    pass
                    l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'ospfv3'):
                        pass
                        if t_6(environment.getattr(l_1_redistribute_route, 'ospf_route_type')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'bgp'):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif t_6(environment.getattr(l_1_redistribute_route, 'include_leaked'), True):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_6(environment.getattr(l_1_redistribute_route, 'route_map')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                        pass
                        if t_6(environment.getattr(l_1_redistribute_route, 'rcf')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' rcf ', environment.getattr(l_1_redistribute_route, 'rcf'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                    yield '\n'
                l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast')):
            pass
            yield '   !\n   address-family ipv6 multicast\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths receive\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
            for l_1_network in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'networks'), 'prefix'):
                l_1_network_cli = missing
                _loop_vars = {}
                pass
                l_1_network_cli = str_join(('network ', environment.getattr(l_1_network, 'prefix'), ))
                _loop_vars['network_cli'] = l_1_network_cli
                if t_6(environment.getattr(l_1_network, 'route_map')):
                    pass
                    l_1_network_cli = str_join(((undefined(name='network_cli') if l_1_network_cli is missing else l_1_network_cli), ' route-map ', environment.getattr(l_1_network, 'route_map'), ))
                    _loop_vars['network_cli'] = l_1_network_cli
                yield '      '
                yield str((undefined(name='network_cli') if l_1_network_cli is missing else l_1_network_cli))
                yield '\n'
            l_1_network = l_1_network_cli = missing
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'redistribute')):
                pass
                l_0_redistribute_var = environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'redistribute')
                context.vars['redistribute_var'] = l_0_redistribute_var
                context.exported_vars.add('redistribute_var')
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'enabled'), True):
                    pass
                    l_0_redistribute_conn = 'redistribute connected'
                    context.vars['redistribute_conn'] = l_0_redistribute_conn
                    context.exported_vars.add('redistribute_conn')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'route_map')):
                        pass
                        l_0_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'connected'), 'route_map'), ))
                        context.vars['redistribute_conn'] = l_0_redistribute_conn
                        context.exported_vars.add('redistribute_conn')
                    yield '      '
                    yield str((undefined(name='redistribute_conn') if l_0_redistribute_conn is missing else l_0_redistribute_conn))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'enabled'), True):
                    pass
                    l_0_redistribute_isis = 'redistribute isis'
                    context.vars['redistribute_isis'] = l_0_redistribute_isis
                    context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'isis_level')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'isis_level'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'include_leaked'), True):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' include leaked', ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'route_map')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'route_map'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'rcf')):
                        pass
                        l_0_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'isis'), 'rcf'), ))
                        context.vars['redistribute_isis'] = l_0_redistribute_isis
                        context.exported_vars.add('redistribute_isis')
                    yield '      '
                    yield str((undefined(name='redistribute_isis') if l_0_redistribute_isis is missing else l_0_redistribute_isis))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf = 'redistribute ospf'
                    context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                    context.exported_vars.add('redistribute_ospf')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'route_map')):
                        pass
                        l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'route_map'), ))
                        context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                        context.exported_vars.add('redistribute_ospf')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf = 'redistribute ospf match internal'
                    context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                    context.exported_vars.add('redistribute_ospf')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'route_map')):
                        pass
                        l_0_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_internal'), 'route_map'), ))
                        context.vars['redistribute_ospf'] = l_0_redistribute_ospf
                        context.exported_vars.add('redistribute_ospf')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf') if l_0_redistribute_ospf is missing else l_0_redistribute_ospf))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3 = 'redistribute ospfv3'
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'route_map'), ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3 = 'redistribute ospfv3 match internal'
                    context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                    context.exported_vars.add('redistribute_ospfv3')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map'), ))
                        context.vars['redistribute_ospfv3'] = l_0_redistribute_ospfv3
                        context.exported_vars.add('redistribute_ospfv3')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3') if l_0_redistribute_ospfv3 is missing else l_0_redistribute_ospfv3))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3_match = 'redistribute ospfv3 match external'
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_external'), 'route_map'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospfv3_match = 'redistribute ospfv3 match nssa-external'
                    context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                    context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map'), ))
                        context.vars['redistribute_ospfv3_match'] = l_0_redistribute_ospfv3_match
                        context.exported_vars.add('redistribute_ospfv3_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3_match') if l_0_redistribute_ospfv3_match is missing else l_0_redistribute_ospfv3_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf_match = 'redistribute ospf match external'
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_external'), 'route_map'), ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'enabled'), True):
                    pass
                    l_0_redistribute_ospf_match = 'redistribute ospf match nssa-external'
                    context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                    context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type')):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type'), ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map')):
                        pass
                        l_0_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map'), ))
                        context.vars['redistribute_ospf_match'] = l_0_redistribute_ospf_match
                        context.exported_vars.add('redistribute_ospf_match')
                    yield '      '
                    yield str((undefined(name='redistribute_ospf_match') if l_0_redistribute_ospf_match is missing else l_0_redistribute_ospf_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'enabled'), True):
                    pass
                    l_0_redistribute_static = 'redistribute static'
                    context.vars['redistribute_static'] = l_0_redistribute_static
                    context.exported_vars.add('redistribute_static')
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'route_map')):
                        pass
                        l_0_redistribute_static = str_join(((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_0_redistribute_var is missing else l_0_redistribute_var), 'static'), 'route_map'), ))
                        context.vars['redistribute_static'] = l_0_redistribute_static
                        context.exported_vars.add('redistribute_static')
                    yield '      '
                    yield str((undefined(name='redistribute_static') if l_0_redistribute_static is missing else l_0_redistribute_static))
                    yield '\n'
            elif t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'redistribute_routes')):
                pass
                for l_1_redistribute_route in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'redistribute_routes'), 'source_protocol'):
                    l_1_redistribute_route_cli = missing
                    _loop_vars = {}
                    pass
                    l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                        pass
                        if t_6(environment.getattr(l_1_redistribute_route, 'ospf_route_type')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_6(environment.getattr(l_1_redistribute_route, 'include_leaked'), True):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_6(environment.getattr(l_1_redistribute_route, 'route_map')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif ((environment.getattr(l_1_redistribute_route, 'source_protocol') == 'isis') and t_6(environment.getattr(l_1_redistribute_route, 'rcf'))):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' rcf ', environment.getattr(l_1_redistribute_route, 'rcf'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                    yield '\n'
                l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te')):
            pass
            yield '   !\n   address-family ipv6 sr-te\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state')):
            pass
            yield '   !\n   address-family link-state\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_out_action'))
                    yield '\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_out_action'))
                    yield '\n'
            l_1_neighbor = missing
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection')):
                pass
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'producer'), True):
                    pass
                    yield '      path-selection\n'
                if (t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'consumer'), True) or t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'propagator'), True)):
                    pass
                    l_0_path_selection_roles = 'path-selection role'
                    context.vars['path_selection_roles'] = l_0_path_selection_roles
                    context.exported_vars.add('path_selection_roles')
                    if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'consumer'), True):
                        pass
                        l_0_path_selection_roles = str_join(((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), ' consumer', ))
                        context.vars['path_selection_roles'] = l_0_path_selection_roles
                        context.exported_vars.add('path_selection_roles')
                    if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'propagator'), True):
                        pass
                        l_0_path_selection_roles = str_join(((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), ' propagator', ))
                        context.vars['path_selection_roles'] = l_0_path_selection_roles
                        context.exported_vars.add('path_selection_roles')
                    yield '      '
                    yield str((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles))
                    yield '\n'
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection')):
            pass
            yield '   !\n   address-family path-selection\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send')):
                pass
                if (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send') == 'disabled'):
                    pass
                    yield '      no bgp additional-paths send\n'
                elif (t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send') == 'ecmp')):
                    pass
                    yield '      bgp additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send_limit'))
                    yield '\n'
                elif (environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send') == 'limit'):
                    pass
                    if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send_limit')):
                        pass
                        yield '      bgp additional-paths send limit '
                        yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send_limit'))
                        yield '\n'
                else:
                    pass
                    yield '      bgp additional-paths send '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'))
                    yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' send\n'
                    elif (t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'ecmp')):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' additional-paths send ecmp limit '
                        yield str(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit'))
                        yield '\n'
                    elif (environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send') == 'limit'):
                        pass
                        if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit')):
                            pass
                            yield '      neighbor '
                            yield str(environment.getattr(l_1_peer_group, 'name'))
                            yield ' additional-paths send limit '
                            yield str(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send_limit'))
                            yield '\n'
                    else:
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' additional-paths send '
                        yield str(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'))
                        yield '\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send\n'
                    elif (t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'ecmp')):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send ecmp limit '
                        yield str(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit'))
                        yield '\n'
                    elif (environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send') == 'limit'):
                        pass
                        if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit')):
                            pass
                            yield '      neighbor '
                            yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                            yield ' additional-paths send limit '
                            yield str(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send_limit'))
                            yield '\n'
                    else:
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                        yield ' additional-paths send '
                        yield str(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'))
                        yield '\n'
            l_1_neighbor = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_rtc')):
            pass
            yield '   !\n   address-family rt-membership\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_rtc'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_7(environment.getattr(l_1_peer_group, 'default_route_target')):
                    pass
                    if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_route_target'), 'only'), True):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' default-route-target only\n'
                    else:
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' default-route-target\n'
                if t_7(environment.getattr(environment.getattr(l_1_peer_group, 'default_route_target'), 'encoding_origin_as_omit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' default-route-target encoding origin-as omit\n'
            l_1_peer_group = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4')):
            pass
            yield '   !\n   address-family vpn-ipv4\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'peer_groups'), 'name'):
                l_1_peer_group_default_route_cli = resolve('peer_group_default_route_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_peer_group, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer_group, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'enabled'), True):
                    pass
                    l_1_peer_group_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-route', ))
                    _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    elif t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    yield '      '
                    yield str((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli))
                    yield '\n'
            l_1_peer_group = l_1_peer_group_default_route_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbors'), 'ip_address'):
                l_1_neighbor_default_route_cli = resolve('neighbor_default_route_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'enabled'), True):
                    pass
                    l_1_neighbor_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-route', ))
                    _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    elif t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli))
                    yield '\n'
            l_1_neighbor = l_1_neighbor_default_route_cli = missing
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface')):
                pass
                yield '      neighbor default encapsulation mpls next-hop-self source-interface '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'domain_identifier')):
                pass
                yield '      domain identifier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'domain_identifier'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '      route import match-failure action discard\n'
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6')):
            pass
            yield '   !\n   address-family vpn-ipv6\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'peer_groups'), 'name'):
                l_1_peer_group_default_route_cli = resolve('peer_group_default_route_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_peer_group, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_peer_group, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'enabled'), True):
                    pass
                    l_1_peer_group_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-route', ))
                    _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    if t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    elif t_6(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    yield '      '
                    yield str((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli))
                    yield '\n'
            l_1_peer_group = l_1_peer_group_default_route_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbors'), 'ip_address'):
                l_1_neighbor_default_route_cli = resolve('neighbor_default_route_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_6(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_6(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'enabled'), True):
                    pass
                    l_1_neighbor_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-route', ))
                    _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    if t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    elif t_6(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli))
                    yield '\n'
            l_1_neighbor = l_1_neighbor_default_route_cli = missing
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface')):
                pass
                yield '      neighbor default encapsulation mpls next-hop-self source-interface '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'domain_identifier')):
                pass
                yield '      domain identifier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'domain_identifier'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '      route import match-failure action discard\n'
        for l_1_vrf in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
            l_1_paths_cli = l_0_paths_cli
            l_1_redistribute_var = l_0_redistribute_var
            l_1_redistribute_conn = l_0_redistribute_conn
            l_1_redistribute_isis = l_0_redistribute_isis
            l_1_redistribute_ospf = l_0_redistribute_ospf
            l_1_redistribute_ospf_match = l_0_redistribute_ospf_match
            l_1_redistribute_ospfv3 = l_0_redistribute_ospfv3
            l_1_redistribute_ospfv3_match = l_0_redistribute_ospfv3_match
            l_1_redistribute_static = l_0_redistribute_static
            l_1_redistribute_rip = l_0_redistribute_rip
            l_1_redistribute_host = l_0_redistribute_host
            l_1_redistribute_dynamic = l_0_redistribute_dynamic
            l_1_redistribute_bgp = l_0_redistribute_bgp
            l_1_redistribute_user = l_0_redistribute_user
            l_1_redistribute_dhcp = l_0_redistribute_dhcp
            _loop_vars = {}
            pass
            yield '   !\n   vrf '
            yield str(environment.getattr(l_1_vrf, 'name'))
            yield '\n'
            if t_6(environment.getattr(l_1_vrf, 'rd')):
                pass
                yield '      rd '
                yield str(environment.getattr(l_1_vrf, 'rd'))
                yield '\n'
            if t_6(environment.getattr(l_1_vrf, 'default_route_exports')):
                pass
                for l_2_default_route_export in t_3(environment.getattr(l_1_vrf, 'default_route_exports'), 'address_family'):
                    l_2_vrf_default_route_export_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_vrf_default_route_export_cli = str_join(('default-route export ', environment.getattr(l_2_default_route_export, 'address_family'), ))
                    _loop_vars['vrf_default_route_export_cli'] = l_2_vrf_default_route_export_cli
                    if t_6(environment.getattr(l_2_default_route_export, 'always'), True):
                        pass
                        l_2_vrf_default_route_export_cli = str_join(((undefined(name='vrf_default_route_export_cli') if l_2_vrf_default_route_export_cli is missing else l_2_vrf_default_route_export_cli), ' always', ))
                        _loop_vars['vrf_default_route_export_cli'] = l_2_vrf_default_route_export_cli
                    if t_6(environment.getattr(l_2_default_route_export, 'rcf')):
                        pass
                        l_2_vrf_default_route_export_cli = str_join(((undefined(name='vrf_default_route_export_cli') if l_2_vrf_default_route_export_cli is missing else l_2_vrf_default_route_export_cli), ' rcf ', environment.getattr(l_2_default_route_export, 'rcf'), ))
                        _loop_vars['vrf_default_route_export_cli'] = l_2_vrf_default_route_export_cli
                    elif t_6(environment.getattr(l_2_default_route_export, 'route_map')):
                        pass
                        l_2_vrf_default_route_export_cli = str_join(((undefined(name='vrf_default_route_export_cli') if l_2_vrf_default_route_export_cli is missing else l_2_vrf_default_route_export_cli), ' route-map ', environment.getattr(l_2_default_route_export, 'route_map'), ))
                        _loop_vars['vrf_default_route_export_cli'] = l_2_vrf_default_route_export_cli
                    yield '      '
                    yield str((undefined(name='vrf_default_route_export_cli') if l_2_vrf_default_route_export_cli is missing else l_2_vrf_default_route_export_cli))
                    yield '\n'
                l_2_default_route_export = l_2_vrf_default_route_export_cli = missing
            if t_6(environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'import')):
                pass
                for l_2_address_family in environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'import'):
                    _loop_vars = {}
                    pass
                    for l_3_route_target in environment.getattr(l_2_address_family, 'route_targets'):
                        _loop_vars = {}
                        pass
                        yield '      route-target import '
                        yield str(environment.getattr(l_2_address_family, 'address_family'))
                        yield ' '
                        yield str(l_3_route_target)
                        yield '\n'
                    l_3_route_target = missing
                    if (environment.getattr(l_2_address_family, 'address_family') in ['evpn', 'vpn-ipv4', 'vpn-ipv6']):
                        pass
                        if t_6(environment.getattr(l_2_address_family, 'rcf')):
                            pass
                            if (t_6(environment.getattr(l_2_address_family, 'vpn_route_filter_rcf')) and (environment.getattr(l_2_address_family, 'address_family') in ['vpn-ipv4', 'vpn-ipv6'])):
                                pass
                                yield '      route-target import '
                                yield str(environment.getattr(l_2_address_family, 'address_family'))
                                yield ' rcf '
                                yield str(environment.getattr(l_2_address_family, 'rcf'))
                                yield ' vpn-route filter-rcf '
                                yield str(environment.getattr(l_2_address_family, 'vpn_route_filter_rcf'))
                                yield '\n'
                            else:
                                pass
                                yield '      route-target import '
                                yield str(environment.getattr(l_2_address_family, 'address_family'))
                                yield ' rcf '
                                yield str(environment.getattr(l_2_address_family, 'rcf'))
                                yield '\n'
                        if t_6(environment.getattr(l_2_address_family, 'route_map')):
                            pass
                            yield '      route-target import '
                            yield str(environment.getattr(l_2_address_family, 'address_family'))
                            yield ' route-map '
                            yield str(environment.getattr(l_2_address_family, 'route_map'))
                            yield '\n'
                l_2_address_family = missing
            if t_6(environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'export')):
                pass
                for l_2_address_family in environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'export'):
                    _loop_vars = {}
                    pass
                    for l_3_route_target in environment.getattr(l_2_address_family, 'route_targets'):
                        _loop_vars = {}
                        pass
                        yield '      route-target export '
                        yield str(environment.getattr(l_2_address_family, 'address_family'))
                        yield ' '
                        yield str(l_3_route_target)
                        yield '\n'
                    l_3_route_target = missing
                    if (environment.getattr(l_2_address_family, 'address_family') in ['evpn', 'vpn-ipv4', 'vpn-ipv6']):
                        pass
                        if t_6(environment.getattr(l_2_address_family, 'rcf')):
                            pass
                            if (t_6(environment.getattr(l_2_address_family, 'vpn_route_filter_rcf')) and (environment.getattr(l_2_address_family, 'address_family') in ['vpn-ipv4', 'vpn-ipv6'])):
                                pass
                                yield '      route-target export '
                                yield str(environment.getattr(l_2_address_family, 'address_family'))
                                yield ' rcf '
                                yield str(environment.getattr(l_2_address_family, 'rcf'))
                                yield ' vpn-route filter-rcf '
                                yield str(environment.getattr(l_2_address_family, 'vpn_route_filter_rcf'))
                                yield '\n'
                            else:
                                pass
                                yield '      route-target export '
                                yield str(environment.getattr(l_2_address_family, 'address_family'))
                                yield ' rcf '
                                yield str(environment.getattr(l_2_address_family, 'rcf'))
                                yield '\n'
                        if t_6(environment.getattr(l_2_address_family, 'route_map')):
                            pass
                            yield '      route-target export '
                            yield str(environment.getattr(l_2_address_family, 'address_family'))
                            yield ' route-map '
                            yield str(environment.getattr(l_2_address_family, 'route_map'))
                            yield '\n'
                l_2_address_family = missing
            if t_6(environment.getattr(l_1_vrf, 'router_id')):
                pass
                yield '      router-id '
                yield str(environment.getattr(l_1_vrf, 'router_id'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(l_1_vrf, 'updates'), 'wait_for_convergence'), True):
                pass
                yield '      update wait-for-convergence\n'
            if t_6(environment.getattr(environment.getattr(l_1_vrf, 'updates'), 'wait_install'), True):
                pass
                yield '      update wait-install\n'
            if t_6(environment.getattr(l_1_vrf, 'timers')):
                pass
                yield '      timers bgp '
                yield str(environment.getattr(l_1_vrf, 'timers'))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(l_1_vrf, 'maximum_paths'), 'paths')):
                pass
                l_1_paths_cli = str_join(('maximum-paths ', environment.getattr(environment.getattr(l_1_vrf, 'maximum_paths'), 'paths'), ))
                _loop_vars['paths_cli'] = l_1_paths_cli
                if t_6(environment.getattr(environment.getattr(l_1_vrf, 'maximum_paths'), 'ecmp')):
                    pass
                    l_1_paths_cli = str_join(((undefined(name='paths_cli') if l_1_paths_cli is missing else l_1_paths_cli), ' ecmp ', environment.getattr(environment.getattr(l_1_vrf, 'maximum_paths'), 'ecmp'), ))
                    _loop_vars['paths_cli'] = l_1_paths_cli
                yield '      '
                yield str((undefined(name='paths_cli') if l_1_paths_cli is missing else l_1_paths_cli))
                yield '\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'install'), True):
                pass
                yield '      bgp additional-paths install\n'
            elif t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'install_ecmp_primary'), True):
                pass
                yield '      bgp additional-paths install ecmp-primary\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'send')):
                pass
                if (environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'send') == 'disabled'):
                    pass
                    yield '      no bgp additional-paths send\n'
                elif (t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'send') == 'ecmp')):
                    pass
                    yield '      bgp additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'send_limit'))
                    yield '\n'
                elif (environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'send') == 'limit'):
                    pass
                    if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'send_limit')):
                        pass
                        yield '      bgp additional-paths send limit '
                        yield str(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'send_limit'))
                        yield '\n'
                else:
                    pass
                    yield '      bgp additional-paths send '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'additional_paths'), 'send'))
                    yield '\n'
            if t_6(environment.getattr(l_1_vrf, 'listen_ranges')):
                pass
                def t_10(fiter):
                    for l_2_listen_range in fiter:
                        if ((t_6(environment.getattr(l_2_listen_range, 'peer_group')) and t_6(environment.getattr(l_2_listen_range, 'prefix'))) and (t_6(environment.getattr(l_2_listen_range, 'peer_filter')) or t_6(environment.getattr(l_2_listen_range, 'remote_as')))):
                            yield l_2_listen_range
                for l_2_listen_range in t_10(t_3(environment.getattr(l_1_vrf, 'listen_ranges'), 'peer_group')):
                    l_2_listen_range_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_listen_range_cli = str_join(('bgp listen range ', environment.getattr(l_2_listen_range, 'prefix'), ))
                    _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    if t_6(environment.getattr(l_2_listen_range, 'peer_id_include_router_id'), True):
                        pass
                        l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' peer-id include router-id', ))
                        _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' peer-group ', environment.getattr(l_2_listen_range, 'peer_group'), ))
                    _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    if t_6(environment.getattr(l_2_listen_range, 'peer_filter')):
                        pass
                        l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' peer-filter ', environment.getattr(l_2_listen_range, 'peer_filter'), ))
                        _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    elif t_6(environment.getattr(l_2_listen_range, 'remote_as')):
                        pass
                        l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' remote-as ', environment.getattr(l_2_listen_range, 'remote_as'), ))
                        _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    yield '      '
                    yield str((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli))
                    yield '\n'
                l_2_listen_range = l_2_listen_range_cli = missing
            for l_2_neighbor in t_3(environment.getattr(l_1_vrf, 'neighbors'), 'ip_address'):
                l_2_remove_private_as_cli = resolve('remove_private_as_cli')
                l_2_allowas_in_cli = resolve('allowas_in_cli')
                l_2_neighbor_rib_in_pre_policy_retain_cli = resolve('neighbor_rib_in_pre_policy_retain_cli')
                l_2_neighbor_ebgp_multihop_cli = resolve('neighbor_ebgp_multihop_cli')
                l_2_hide_passwords = resolve('hide_passwords')
                l_2_neighbor_default_originate_cli = resolve('neighbor_default_originate_cli')
                l_2_maximum_routes_cli = resolve('maximum_routes_cli')
                l_2_remove_private_as_ingress_cli = resolve('remove_private_as_ingress_cli')
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_2_neighbor, 'peer_group')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' peer group '
                    yield str(environment.getattr(l_2_neighbor, 'peer_group'))
                    yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'remote_as')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' remote-as '
                    yield str(environment.getattr(l_2_neighbor, 'remote_as'))
                    yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'next_hop_self'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' next-hop-self\n'
                if t_6(environment.getattr(l_2_neighbor, 'shutdown'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' shutdown\n'
                if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'enabled'), True):
                    pass
                    l_2_remove_private_as_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' remove-private-as', ))
                    _loop_vars['remove_private_as_cli'] = l_2_remove_private_as_cli
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'all'), True):
                        pass
                        l_2_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_2_remove_private_as_cli is missing else l_2_remove_private_as_cli), ' all', ))
                        _loop_vars['remove_private_as_cli'] = l_2_remove_private_as_cli
                        if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'replace_as'), True):
                            pass
                            l_2_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_2_remove_private_as_cli is missing else l_2_remove_private_as_cli), ' replace-as', ))
                            _loop_vars['remove_private_as_cli'] = l_2_remove_private_as_cli
                    yield '      '
                    yield str((undefined(name='remove_private_as_cli') if l_2_remove_private_as_cli is missing else l_2_remove_private_as_cli))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'enabled'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' remove-private-as\n'
                if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'as_path'), 'prepend_own_disabled'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' as-path prepend-own disabled\n'
                if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'as_path'), 'remote_as_replace_out'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' as-path remote-as replace out\n'
                if t_6(environment.getattr(l_2_neighbor, 'local_as')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' local-as '
                    yield str(environment.getattr(l_2_neighbor, 'local_as'))
                    yield ' no-prepend replace-as\n'
                if t_6(environment.getattr(l_2_neighbor, 'weight')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' weight '
                    yield str(environment.getattr(l_2_neighbor, 'weight'))
                    yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'passive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' passive\n'
                if t_6(environment.getattr(l_2_neighbor, 'update_source')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' update-source '
                    yield str(environment.getattr(l_2_neighbor, 'update_source'))
                    yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'bfd'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' bfd\n'
                    if ((t_6(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'interval')) and t_6(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'min_rx'))) and t_6(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'multiplier'))):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' bfd interval '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'interval'))
                        yield ' min-rx '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'min_rx'))
                        yield ' multiplier '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'multiplier'))
                        yield '\n'
                elif (t_6(environment.getattr(l_2_neighbor, 'bfd'), False) and t_6(environment.getattr(l_2_neighbor, 'peer_group'))):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' bfd\n'
                if t_6(environment.getattr(l_2_neighbor, 'description')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' description '
                    yield str(environment.getattr(l_2_neighbor, 'description'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'enabled'), True):
                    pass
                    l_2_allowas_in_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' allowas-in', ))
                    _loop_vars['allowas_in_cli'] = l_2_allowas_in_cli
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'times')):
                        pass
                        l_2_allowas_in_cli = str_join(((undefined(name='allowas_in_cli') if l_2_allowas_in_cli is missing else l_2_allowas_in_cli), ' ', environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'times'), ))
                        _loop_vars['allowas_in_cli'] = l_2_allowas_in_cli
                    yield '      '
                    yield str((undefined(name='allowas_in_cli') if l_2_allowas_in_cli is missing else l_2_allowas_in_cli))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), True):
                    pass
                    l_2_neighbor_rib_in_pre_policy_retain_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_2_neighbor_rib_in_pre_policy_retain_cli
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'all'), True):
                        pass
                        l_2_neighbor_rib_in_pre_policy_retain_cli = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_2_neighbor_rib_in_pre_policy_retain_cli is missing else l_2_neighbor_rib_in_pre_policy_retain_cli), ' all', ))
                        _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_2_neighbor_rib_in_pre_policy_retain_cli
                    yield '      '
                    yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_2_neighbor_rib_in_pre_policy_retain_cli is missing else l_2_neighbor_rib_in_pre_policy_retain_cli))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), False):
                    pass
                    l_2_neighbor_rib_in_pre_policy_retain_cli = str_join(('no neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_2_neighbor_rib_in_pre_policy_retain_cli
                    yield '      '
                    yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_2_neighbor_rib_in_pre_policy_retain_cli is missing else l_2_neighbor_rib_in_pre_policy_retain_cli))
                    yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'ebgp_multihop')):
                    pass
                    l_2_neighbor_ebgp_multihop_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' ebgp-multihop', ))
                    _loop_vars['neighbor_ebgp_multihop_cli'] = l_2_neighbor_ebgp_multihop_cli
                    if t_8(environment.getattr(l_2_neighbor, 'ebgp_multihop')):
                        pass
                        l_2_neighbor_ebgp_multihop_cli = str_join(((undefined(name='neighbor_ebgp_multihop_cli') if l_2_neighbor_ebgp_multihop_cli is missing else l_2_neighbor_ebgp_multihop_cli), ' ', environment.getattr(l_2_neighbor, 'ebgp_multihop'), ))
                        _loop_vars['neighbor_ebgp_multihop_cli'] = l_2_neighbor_ebgp_multihop_cli
                    yield '      '
                    yield str((undefined(name='neighbor_ebgp_multihop_cli') if l_2_neighbor_ebgp_multihop_cli is missing else l_2_neighbor_ebgp_multihop_cli))
                    yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'route_reflector_client'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-reflector-client\n'
                elif t_6(environment.getattr(l_2_neighbor, 'route_reflector_client'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-reflector-client\n'
                if t_6(environment.getattr(l_2_neighbor, 'timers')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' timers '
                    yield str(environment.getattr(l_2_neighbor, 'timers'))
                    yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' additional-paths receive\n'
                if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '      no neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' additional-paths send\n'
                    elif (t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send') == 'ecmp')):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' additional-paths send ecmp limit '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit'))
                        yield '\n'
                    elif (environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send') == 'limit'):
                        pass
                        if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit')):
                            pass
                            yield '      neighbor '
                            yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                            yield ' additional-paths send limit '
                            yield str(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit'))
                            yield '\n'
                    else:
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' additional-paths send '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send'))
                        yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_6(environment.getattr(l_2_neighbor, 'password')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' password 7 '
                    yield str(t_2(environment.getattr(l_2_neighbor, 'password'), (undefined(name='hide_passwords') if l_2_hide_passwords is missing else l_2_hide_passwords)))
                    yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'default_originate')):
                    pass
                    l_2_neighbor_default_originate_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' default-originate', ))
                    _loop_vars['neighbor_default_originate_cli'] = l_2_neighbor_default_originate_cli
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'default_originate'), 'route_map')):
                        pass
                        l_2_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_2_neighbor_default_originate_cli is missing else l_2_neighbor_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_2_neighbor, 'default_originate'), 'route_map'), ))
                        _loop_vars['neighbor_default_originate_cli'] = l_2_neighbor_default_originate_cli
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'default_originate'), 'always'), True):
                        pass
                        l_2_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_2_neighbor_default_originate_cli is missing else l_2_neighbor_default_originate_cli), ' always', ))
                        _loop_vars['neighbor_default_originate_cli'] = l_2_neighbor_default_originate_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_originate_cli') if l_2_neighbor_default_originate_cli is missing else l_2_neighbor_default_originate_cli))
                    yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'send_community'), 'all'):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' send-community\n'
                elif t_6(environment.getattr(l_2_neighbor, 'send_community')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' send-community '
                    yield str(environment.getattr(l_2_neighbor, 'send_community'))
                    yield '\n'
                if t_6(environment.getattr(l_2_neighbor, 'maximum_routes')):
                    pass
                    l_2_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' maximum-routes ', environment.getattr(l_2_neighbor, 'maximum_routes'), ))
                    _loop_vars['maximum_routes_cli'] = l_2_maximum_routes_cli
                    if t_6(environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit')):
                        pass
                        l_2_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_2_maximum_routes_cli is missing else l_2_maximum_routes_cli), ' warning-limit ', environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit'), ))
                        _loop_vars['maximum_routes_cli'] = l_2_maximum_routes_cli
                    if t_6(environment.getattr(l_2_neighbor, 'maximum_routes_warning_only'), True):
                        pass
                        l_2_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_2_maximum_routes_cli is missing else l_2_maximum_routes_cli), ' warning-only', ))
                        _loop_vars['maximum_routes_cli'] = l_2_maximum_routes_cli
                    yield '      '
                    yield str((undefined(name='maximum_routes_cli') if l_2_maximum_routes_cli is missing else l_2_maximum_routes_cli))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as_ingress'), 'enabled'), True):
                    pass
                    l_2_remove_private_as_ingress_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' remove-private-as ingress', ))
                    _loop_vars['remove_private_as_ingress_cli'] = l_2_remove_private_as_ingress_cli
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as_ingress'), 'replace_as'), True):
                        pass
                        l_2_remove_private_as_ingress_cli = str_join(((undefined(name='remove_private_as_ingress_cli') if l_2_remove_private_as_ingress_cli is missing else l_2_remove_private_as_ingress_cli), ' replace-as', ))
                        _loop_vars['remove_private_as_ingress_cli'] = l_2_remove_private_as_ingress_cli
                    yield '      '
                    yield str((undefined(name='remove_private_as_ingress_cli') if l_2_remove_private_as_ingress_cli is missing else l_2_remove_private_as_ingress_cli))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as_ingress'), 'enabled'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' remove-private-as ingress\n'
            l_2_neighbor = l_2_remove_private_as_cli = l_2_allowas_in_cli = l_2_neighbor_rib_in_pre_policy_retain_cli = l_2_neighbor_ebgp_multihop_cli = l_2_hide_passwords = l_2_neighbor_default_originate_cli = l_2_maximum_routes_cli = l_2_remove_private_as_ingress_cli = missing
            for l_2_network in t_3(environment.getattr(l_1_vrf, 'networks'), 'prefix'):
                _loop_vars = {}
                pass
                if t_6(environment.getattr(l_2_network, 'route_map')):
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_2_network, 'prefix'))
                    yield ' route-map '
                    yield str(environment.getattr(l_2_network, 'route_map'))
                    yield '\n'
                else:
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_2_network, 'prefix'))
                    yield '\n'
            l_2_network = missing
            if t_6(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'redistribute_internal'), True):
                pass
                yield '      bgp redistribute-internal\n'
            elif t_6(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'redistribute_internal'), False):
                pass
                yield '      no bgp redistribute-internal\n'
            for l_2_aggregate_address in t_3(environment.getattr(l_1_vrf, 'aggregate_addresses'), 'prefix'):
                l_2_aggregate_address_cli = missing
                _loop_vars = {}
                pass
                l_2_aggregate_address_cli = str_join(('aggregate-address ', environment.getattr(l_2_aggregate_address, 'prefix'), ))
                _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_6(environment.getattr(l_2_aggregate_address, 'as_set'), True):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' as-set', ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_6(environment.getattr(l_2_aggregate_address, 'summary_only'), True):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' summary-only', ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_6(environment.getattr(l_2_aggregate_address, 'attribute_map')):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' attribute-map ', environment.getattr(l_2_aggregate_address, 'attribute_map'), ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_6(environment.getattr(l_2_aggregate_address, 'match_map')):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' match-map ', environment.getattr(l_2_aggregate_address, 'match_map'), ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_6(environment.getattr(l_2_aggregate_address, 'advertise_only'), True):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' advertise-only', ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                yield '      '
                yield str((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli))
                yield '\n'
            l_2_aggregate_address = l_2_aggregate_address_cli = missing
            if t_6(environment.getattr(l_1_vrf, 'redistribute')):
                pass
                l_1_redistribute_var = environment.getattr(l_1_vrf, 'redistribute')
                _loop_vars['redistribute_var'] = l_1_redistribute_var
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'enabled'), True):
                    pass
                    l_1_redistribute_conn = 'redistribute connected'
                    _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' include leaked', ))
                        _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'route_map')):
                        pass
                        l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'route_map'), ))
                        _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'rcf')):
                        pass
                        l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'rcf'), ))
                        _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                    yield '      '
                    yield str((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'enabled'), True):
                    pass
                    l_1_redistribute_isis = 'redistribute isis'
                    _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'isis_level')):
                        pass
                        l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'isis_level'), ))
                        _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' include leaked', ))
                        _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'route_map')):
                        pass
                        l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'route_map'), ))
                        _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'rcf')):
                        pass
                        l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'rcf'), ))
                        _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                    yield '      '
                    yield str((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'enabled'), True):
                    pass
                    l_1_redistribute_ospf = 'redistribute ospf'
                    _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' include leaked', ))
                        _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'route_map')):
                        pass
                        l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'route_map'), ))
                        _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                    yield '      '
                    yield str((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'enabled'), True):
                    pass
                    l_1_redistribute_ospf = 'redistribute ospf match internal'
                    _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' include leaked', ))
                        _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'route_map')):
                        pass
                        l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'route_map'), ))
                        _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                    yield '      '
                    yield str((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'enabled'), True):
                    pass
                    l_1_redistribute_ospf_match = 'redistribute ospf match external'
                    _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' include leaked', ))
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'route_map')):
                        pass
                        l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'route_map'), ))
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                    yield '      '
                    yield str((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'enabled'), True):
                    pass
                    l_1_redistribute_ospf_match = 'redistribute ospf match nssa-external'
                    _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type')):
                        pass
                        l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type'), ))
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' include leaked', ))
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map')):
                        pass
                        l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map'), ))
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                    yield '      '
                    yield str((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'enabled'), True):
                    pass
                    l_1_redistribute_ospfv3 = 'redistribute ospfv3'
                    _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' include leaked', ))
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'route_map')):
                        pass
                        l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'route_map'), ))
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3))
                    yield '\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'enabled'), True):
                    pass
                    l_1_redistribute_ospfv3 = 'redistribute ospfv3 match internal'
                    _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' include leaked', ))
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map')):
                        pass
                        l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map'), ))
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'enabled'), True):
                    pass
                    l_1_redistribute_ospfv3_match = 'redistribute ospfv3 match external'
                    _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' include leaked', ))
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'route_map')):
                        pass
                        l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'route_map'), ))
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'enabled'), True):
                    pass
                    l_1_redistribute_ospfv3_match = 'redistribute ospfv3 match nssa-external'
                    _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type')):
                        pass
                        l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type'), ))
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' include leaked', ))
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map')):
                        pass
                        l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map'), ))
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                    yield '      '
                    yield str((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'enabled'), True):
                    pass
                    l_1_redistribute_static = 'redistribute static'
                    _loop_vars['redistribute_static'] = l_1_redistribute_static
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'include_leaked'), True):
                        pass
                        l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' include leaked', ))
                        _loop_vars['redistribute_static'] = l_1_redistribute_static
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'route_map')):
                        pass
                        l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'route_map'), ))
                        _loop_vars['redistribute_static'] = l_1_redistribute_static
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'rcf')):
                        pass
                        l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'rcf'), ))
                        _loop_vars['redistribute_static'] = l_1_redistribute_static
                    yield '      '
                    yield str((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'rip'), 'enabled'), True):
                    pass
                    l_1_redistribute_rip = 'redistribute rip'
                    _loop_vars['redistribute_rip'] = l_1_redistribute_rip
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'rip'), 'route_map')):
                        pass
                        l_1_redistribute_rip = str_join(((undefined(name='redistribute_rip') if l_1_redistribute_rip is missing else l_1_redistribute_rip), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'rip'), 'route_map'), ))
                        _loop_vars['redistribute_rip'] = l_1_redistribute_rip
                    yield '      '
                    yield str((undefined(name='redistribute_rip') if l_1_redistribute_rip is missing else l_1_redistribute_rip))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'enabled'), True):
                    pass
                    l_1_redistribute_host = 'redistribute attached-host'
                    _loop_vars['redistribute_host'] = l_1_redistribute_host
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'route_map')):
                        pass
                        l_1_redistribute_host = str_join(((undefined(name='redistribute_host') if l_1_redistribute_host is missing else l_1_redistribute_host), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'route_map'), ))
                        _loop_vars['redistribute_host'] = l_1_redistribute_host
                    yield '      '
                    yield str((undefined(name='redistribute_host') if l_1_redistribute_host is missing else l_1_redistribute_host))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'enabled'), True):
                    pass
                    l_1_redistribute_dynamic = 'redistribute dynamic'
                    _loop_vars['redistribute_dynamic'] = l_1_redistribute_dynamic
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'route_map')):
                        pass
                        l_1_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_1_redistribute_dynamic is missing else l_1_redistribute_dynamic), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'route_map'), ))
                        _loop_vars['redistribute_dynamic'] = l_1_redistribute_dynamic
                    elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'rcf')):
                        pass
                        l_1_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_1_redistribute_dynamic is missing else l_1_redistribute_dynamic), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'rcf'), ))
                        _loop_vars['redistribute_dynamic'] = l_1_redistribute_dynamic
                    yield '      '
                    yield str((undefined(name='redistribute_dynamic') if l_1_redistribute_dynamic is missing else l_1_redistribute_dynamic))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'bgp'), 'enabled'), True):
                    pass
                    l_1_redistribute_bgp = 'redistribute bgp leaked'
                    _loop_vars['redistribute_bgp'] = l_1_redistribute_bgp
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'bgp'), 'route_map')):
                        pass
                        l_1_redistribute_bgp = str_join(((undefined(name='redistribute_bgp') if l_1_redistribute_bgp is missing else l_1_redistribute_bgp), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'bgp'), 'route_map'), ))
                        _loop_vars['redistribute_bgp'] = l_1_redistribute_bgp
                    yield '      '
                    yield str((undefined(name='redistribute_bgp') if l_1_redistribute_bgp is missing else l_1_redistribute_bgp))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'user'), 'enabled'), True):
                    pass
                    l_1_redistribute_user = 'redistribute user'
                    _loop_vars['redistribute_user'] = l_1_redistribute_user
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'user'), 'rcf')):
                        pass
                        l_1_redistribute_user = str_join(((undefined(name='redistribute_user') if l_1_redistribute_user is missing else l_1_redistribute_user), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'user'), 'rcf'), ))
                        _loop_vars['redistribute_user'] = l_1_redistribute_user
                    yield '      '
                    yield str((undefined(name='redistribute_user') if l_1_redistribute_user is missing else l_1_redistribute_user))
                    yield '\n'
            elif t_6(environment.getattr(l_1_vrf, 'redistribute_routes')):
                pass
                for l_2_redistribute_route in t_3(environment.getattr(l_1_vrf, 'redistribute_routes'), 'source_protocol'):
                    l_2_redistribute_route_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    if (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                        pass
                        if t_6(environment.getattr(l_2_redistribute_route, 'ospf_route_type')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' match ', environment.getattr(l_2_redistribute_route, 'ospf_route_type'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    if (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'bgp'):
                        pass
                        l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    elif t_6(environment.getattr(l_2_redistribute_route, 'include_leaked'), True):
                        pass
                        l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    if t_6(environment.getattr(l_2_redistribute_route, 'route_map')):
                        pass
                        l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    elif (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                        pass
                        if t_6(environment.getattr(l_2_redistribute_route, 'rcf')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' rcf ', environment.getattr(l_2_redistribute_route, 'rcf'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                    yield '\n'
                l_2_redistribute_route = l_2_redistribute_route_cli = missing
            for l_2_neighbor_interface in t_3(environment.getattr(l_1_vrf, 'neighbor_interfaces'), 'name'):
                _loop_vars = {}
                pass
                if (t_6(environment.getattr(l_2_neighbor_interface, 'peer_group')) and t_6(environment.getattr(l_2_neighbor_interface, 'remote_as'))):
                    pass
                    yield '      neighbor interface '
                    yield str(environment.getattr(l_2_neighbor_interface, 'name'))
                    yield ' peer-group '
                    yield str(environment.getattr(l_2_neighbor_interface, 'peer_group'))
                    yield ' remote-as '
                    yield str(environment.getattr(l_2_neighbor_interface, 'remote_as'))
                    yield '\n'
                elif (t_6(environment.getattr(l_2_neighbor_interface, 'peer_group')) and t_6(environment.getattr(l_2_neighbor_interface, 'peer_filter'))):
                    pass
                    yield '      neighbor interface '
                    yield str(environment.getattr(l_2_neighbor_interface, 'name'))
                    yield ' peer-group '
                    yield str(environment.getattr(l_2_neighbor_interface, 'peer_group'))
                    yield ' peer-filter '
                    yield str(environment.getattr(l_2_neighbor_interface, 'peer_filter'))
                    yield '\n'
            l_2_neighbor_interface = missing
            if t_6(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4')):
                pass
                yield '      !\n      address-family flow-spec ipv4\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_6(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                l_2_neighbor = missing
            if t_6(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6')):
                pass
                yield '      !\n      address-family flow-spec ipv6\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_6(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                l_2_neighbor = missing
            if t_6(environment.getattr(l_1_vrf, 'address_family_ipv4')):
                pass
                yield '      !\n      address-family ipv4\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'install'), True):
                    pass
                    yield '         bgp additional-paths install\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'install_ecmp_primary'), True):
                    pass
                    yield '         bgp additional-paths install ecmp-primary\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '         no bgp additional-paths send\n'
                    elif (t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send') == 'ecmp')):
                        pass
                        yield '         bgp additional-paths send ecmp limit '
                        yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send_limit'))
                        yield '\n'
                    elif (environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send') == 'limit'):
                        pass
                        if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send_limit')):
                            pass
                            yield '         bgp additional-paths send limit '
                            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send_limit'))
                            yield '\n'
                    else:
                        pass
                        yield '         bgp additional-paths send '
                        yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'))
                        yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'neighbors'), 'ip_address'):
                    l_2_ipv6_originate_cli = resolve('ipv6_originate_cli')
                    _loop_vars = {}
                    pass
                    if t_6(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'receive'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' additional-paths receive\n'
                    if t_6(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_6(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                    if t_6(environment.getattr(l_2_neighbor, 'rcf_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' rcf in '
                        yield str(environment.getattr(l_2_neighbor, 'rcf_in'))
                        yield '\n'
                    if t_6(environment.getattr(l_2_neighbor, 'rcf_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' rcf out '
                        yield str(environment.getattr(l_2_neighbor, 'rcf_out'))
                        yield '\n'
                    if t_6(environment.getattr(l_2_neighbor, 'prefix_list_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_in'))
                        yield ' in\n'
                    if t_6(environment.getattr(l_2_neighbor, 'prefix_list_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_out'))
                        yield ' out\n'
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send')):
                        pass
                        if (environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send') == 'disabled'):
                            pass
                            yield '         no neighbor '
                            yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                            yield ' additional-paths send\n'
                        elif (t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send') == 'ecmp')):
                            pass
                            yield '         neighbor '
                            yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                            yield ' additional-paths send ecmp limit '
                            yield str(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit'))
                            yield '\n'
                        elif (environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send') == 'limit'):
                            pass
                            if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit')):
                                pass
                                yield '         neighbor '
                                yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                                yield ' additional-paths send limit '
                                yield str(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit'))
                                yield '\n'
                        else:
                            pass
                            yield '         neighbor '
                            yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                            yield ' additional-paths send '
                            yield str(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send'))
                            yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'enabled')):
                        pass
                        if t_6(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'enabled'), True):
                            pass
                            l_2_ipv6_originate_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' next-hop address-family ipv6', ))
                            _loop_vars['ipv6_originate_cli'] = l_2_ipv6_originate_cli
                            if t_6(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'originate'), True):
                                pass
                                l_2_ipv6_originate_cli = str_join(((undefined(name='ipv6_originate_cli') if l_2_ipv6_originate_cli is missing else l_2_ipv6_originate_cli), ' originate', ))
                                _loop_vars['ipv6_originate_cli'] = l_2_ipv6_originate_cli
                        elif t_6(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'enabled'), False):
                            pass
                            l_2_ipv6_originate_cli = str_join(('no neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' next-hop address-family ipv6', ))
                            _loop_vars['ipv6_originate_cli'] = l_2_ipv6_originate_cli
                        yield '         '
                        yield str((undefined(name='ipv6_originate_cli') if l_2_ipv6_originate_cli is missing else l_2_ipv6_originate_cli))
                        yield '\n'
                l_2_neighbor = l_2_ipv6_originate_cli = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_6(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
                if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'redistribute_internal'), True):
                    pass
                    yield '         bgp redistribute-internal\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'redistribute_internal'), False):
                    pass
                    yield '         no bgp redistribute-internal\n'
                if t_6(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'redistribute')):
                    pass
                    l_1_redistribute_var = environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'redistribute')
                    _loop_vars['redistribute_var'] = l_1_redistribute_var
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'enabled'), True):
                        pass
                        l_1_redistribute_host = 'redistribute attached-host'
                        _loop_vars['redistribute_host'] = l_1_redistribute_host
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'route_map')):
                            pass
                            l_1_redistribute_host = str_join(((undefined(name='redistribute_host') if l_1_redistribute_host is missing else l_1_redistribute_host), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'route_map'), ))
                            _loop_vars['redistribute_host'] = l_1_redistribute_host
                        yield '         '
                        yield str((undefined(name='redistribute_host') if l_1_redistribute_host is missing else l_1_redistribute_host))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'bgp'), 'enabled'), True):
                        pass
                        l_1_redistribute_bgp = 'redistribute bgp leaked'
                        _loop_vars['redistribute_bgp'] = l_1_redistribute_bgp
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'bgp'), 'route_map')):
                            pass
                            l_1_redistribute_bgp = str_join(((undefined(name='redistribute_bgp') if l_1_redistribute_bgp is missing else l_1_redistribute_bgp), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'bgp'), 'route_map'), ))
                            _loop_vars['redistribute_bgp'] = l_1_redistribute_bgp
                        yield '         '
                        yield str((undefined(name='redistribute_bgp') if l_1_redistribute_bgp is missing else l_1_redistribute_bgp))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'enabled'), True):
                        pass
                        l_1_redistribute_conn = 'redistribute connected'
                        _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' include leaked', ))
                            _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'route_map')):
                            pass
                            l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'route_map'), ))
                            _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'rcf')):
                            pass
                            l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'rcf'), ))
                            _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        yield '         '
                        yield str((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'enabled'), True):
                        pass
                        l_1_redistribute_dynamic = 'redistribute dynamic'
                        _loop_vars['redistribute_dynamic'] = l_1_redistribute_dynamic
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'route_map')):
                            pass
                            l_1_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_1_redistribute_dynamic is missing else l_1_redistribute_dynamic), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'route_map'), ))
                            _loop_vars['redistribute_dynamic'] = l_1_redistribute_dynamic
                        elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'rcf')):
                            pass
                            l_1_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_1_redistribute_dynamic is missing else l_1_redistribute_dynamic), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'rcf'), ))
                            _loop_vars['redistribute_dynamic'] = l_1_redistribute_dynamic
                        yield '         '
                        yield str((undefined(name='redistribute_dynamic') if l_1_redistribute_dynamic is missing else l_1_redistribute_dynamic))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'user'), 'enabled'), True):
                        pass
                        l_1_redistribute_user = 'redistribute user'
                        _loop_vars['redistribute_user'] = l_1_redistribute_user
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'user'), 'rcf')):
                            pass
                            l_1_redistribute_user = str_join(((undefined(name='redistribute_user') if l_1_redistribute_user is missing else l_1_redistribute_user), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'user'), 'rcf'), ))
                            _loop_vars['redistribute_user'] = l_1_redistribute_user
                        yield '         '
                        yield str((undefined(name='redistribute_user') if l_1_redistribute_user is missing else l_1_redistribute_user))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'enabled'), True):
                        pass
                        l_1_redistribute_isis = 'redistribute isis'
                        _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'isis_level')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'isis_level'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' include leaked', ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'route_map')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'route_map'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'rcf')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'rcf'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        yield '         '
                        yield str((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf = 'redistribute ospf'
                        _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' include leaked', ))
                            _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'route_map')):
                            pass
                            l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'route_map'), ))
                            _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        yield '         '
                        yield str((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf))
                        yield '\n'
                    elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf = 'redistribute ospf match internal'
                        _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' include leaked', ))
                            _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'route_map')):
                            pass
                            l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'route_map'), ))
                            _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        yield '         '
                        yield str((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3 = 'redistribute ospfv3'
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' include leaked', ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3))
                        yield '\n'
                    elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3 = 'redistribute ospfv3 match internal'
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' include leaked', ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3_match = 'redistribute ospfv3 match external'
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' include leaked', ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3_match = 'redistribute ospfv3 match nssa-external'
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' include leaked', ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf_match = 'redistribute ospf match external'
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' include leaked', ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf_match = 'redistribute ospf match nssa-external'
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type')):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type'), ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' include leaked', ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'rip'), 'enabled'), True):
                        pass
                        l_1_redistribute_rip = 'redistribute rip'
                        _loop_vars['redistribute_rip'] = l_1_redistribute_rip
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'rip'), 'route_map')):
                            pass
                            l_1_redistribute_rip = str_join(((undefined(name='redistribute_rip') if l_1_redistribute_rip is missing else l_1_redistribute_rip), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'rip'), 'route_map'), ))
                            _loop_vars['redistribute_rip'] = l_1_redistribute_rip
                        yield '         '
                        yield str((undefined(name='redistribute_rip') if l_1_redistribute_rip is missing else l_1_redistribute_rip))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'enabled'), True):
                        pass
                        l_1_redistribute_static = 'redistribute static'
                        _loop_vars['redistribute_static'] = l_1_redistribute_static
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' include leaked', ))
                            _loop_vars['redistribute_static'] = l_1_redistribute_static
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'route_map')):
                            pass
                            l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'route_map'), ))
                            _loop_vars['redistribute_static'] = l_1_redistribute_static
                        elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'rcf')):
                            pass
                            l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'rcf'), ))
                            _loop_vars['redistribute_static'] = l_1_redistribute_static
                        yield '         '
                        yield str((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static))
                        yield '\n'
                elif t_6(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'redistribute_routes')):
                    pass
                    for l_2_redistribute_route in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'redistribute_routes'), 'source_protocol'):
                        l_2_redistribute_route_cli = missing
                        _loop_vars = {}
                        pass
                        l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                            pass
                            if t_6(environment.getattr(l_2_redistribute_route, 'ospf_route_type')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' match ', environment.getattr(l_2_redistribute_route, 'ospf_route_type'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'bgp'):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif (t_6(environment.getattr(l_2_redistribute_route, 'include_leaked'), True) and (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['connected', 'isis', 'ospf', 'ospfv3', 'static'])):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if t_6(environment.getattr(l_2_redistribute_route, 'route_map')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                            pass
                            if t_6(environment.getattr(l_2_redistribute_route, 'rcf')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' rcf ', environment.getattr(l_2_redistribute_route, 'rcf'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        yield '         '
                        yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                        yield '\n'
                    l_2_redistribute_route = l_2_redistribute_route_cli = missing
            if t_6(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast')):
                pass
                yield '      !\n      address-family ipv4 multicast\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_6(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'receive'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' additional-paths receive\n'
                    if t_6(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_6(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                l_2_neighbor = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_6(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
                if t_6(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'redistribute')):
                    pass
                    l_1_redistribute_var = environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'redistribute')
                    _loop_vars['redistribute_var'] = l_1_redistribute_var
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'enabled'), True):
                        pass
                        l_1_redistribute_host = 'redistribute attached-host'
                        _loop_vars['redistribute_host'] = l_1_redistribute_host
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'route_map')):
                            pass
                            l_1_redistribute_host = str_join(((undefined(name='redistribute_host') if l_1_redistribute_host is missing else l_1_redistribute_host), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'route_map'), ))
                            _loop_vars['redistribute_host'] = l_1_redistribute_host
                        yield '         '
                        yield str((undefined(name='redistribute_host') if l_1_redistribute_host is missing else l_1_redistribute_host))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'enabled'), True):
                        pass
                        l_1_redistribute_conn = 'redistribute connected'
                        _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'route_map')):
                            pass
                            l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'route_map'), ))
                            _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        yield '         '
                        yield str((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'enabled'), True):
                        pass
                        l_1_redistribute_isis = 'redistribute isis'
                        _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'isis_level')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'isis_level'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' include leaked', ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'route_map')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'route_map'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'rcf')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'rcf'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        yield '         '
                        yield str((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf = 'redistribute ospf'
                        _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'route_map')):
                            pass
                            l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'route_map'), ))
                            _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        yield '         '
                        yield str((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf))
                        yield '\n'
                    elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf = 'redistribute ospf match internal'
                        _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'route_map')):
                            pass
                            l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'route_map'), ))
                            _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        yield '         '
                        yield str((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3 = 'redistribute ospfv3'
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3))
                        yield '\n'
                    elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3 = 'redistribute ospfv3 match internal'
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3_match = 'redistribute ospfv3 match external'
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3_match = 'redistribute ospfv3 match nssa-external'
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf_match = 'redistribute ospf match external'
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf_match = 'redistribute ospf match nssa-external'
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type')):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type'), ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'enabled'), True):
                        pass
                        l_1_redistribute_static = 'redistribute static'
                        _loop_vars['redistribute_static'] = l_1_redistribute_static
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'route_map')):
                            pass
                            l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'route_map'), ))
                            _loop_vars['redistribute_static'] = l_1_redistribute_static
                        yield '         '
                        yield str((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static))
                        yield '\n'
                elif t_6(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'redistribute_routes')):
                    pass
                    for l_2_redistribute_route in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'redistribute_routes'), 'source_protocol'):
                        l_2_redistribute_route_cli = missing
                        _loop_vars = {}
                        pass
                        l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                            pass
                            if t_6(environment.getattr(l_2_redistribute_route, 'ospf_route_type')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' match ', environment.getattr(l_2_redistribute_route, 'ospf_route_type'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if t_6(environment.getattr(l_2_redistribute_route, 'include_leaked'), True):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if t_6(environment.getattr(l_2_redistribute_route, 'route_map')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'isis'):
                            pass
                            if t_6(environment.getattr(l_2_redistribute_route, 'rcf')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' rcf ', environment.getattr(l_2_redistribute_route, 'rcf'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        yield '         '
                        yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                        yield '\n'
                    l_2_redistribute_route = l_2_redistribute_route_cli = missing
            if t_6(environment.getattr(l_1_vrf, 'address_family_ipv6')):
                pass
                yield '      !\n      address-family ipv6\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'install'), True):
                    pass
                    yield '         bgp additional-paths install\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'install_ecmp_primary'), True):
                    pass
                    yield '         bgp additional-paths install ecmp-primary\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send')):
                    pass
                    if (environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send') == 'disabled'):
                        pass
                        yield '         no bgp additional-paths send\n'
                    elif (t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send') == 'ecmp')):
                        pass
                        yield '         bgp additional-paths send ecmp limit '
                        yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send_limit'))
                        yield '\n'
                    elif (environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send') == 'limit'):
                        pass
                        if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send_limit')):
                            pass
                            yield '         bgp additional-paths send limit '
                            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send_limit'))
                            yield '\n'
                    else:
                        pass
                        yield '         bgp additional-paths send '
                        yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'))
                        yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_6(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'receive'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' additional-paths receive\n'
                    if t_6(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_6(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                    if t_6(environment.getattr(l_2_neighbor, 'rcf_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' rcf in '
                        yield str(environment.getattr(l_2_neighbor, 'rcf_in'))
                        yield '\n'
                    if t_6(environment.getattr(l_2_neighbor, 'rcf_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' rcf out '
                        yield str(environment.getattr(l_2_neighbor, 'rcf_out'))
                        yield '\n'
                    if t_6(environment.getattr(l_2_neighbor, 'prefix_list_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_in'))
                        yield ' in\n'
                    if t_6(environment.getattr(l_2_neighbor, 'prefix_list_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_out'))
                        yield ' out\n'
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send')):
                        pass
                        if (environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send') == 'disabled'):
                            pass
                            yield '         no neighbor '
                            yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                            yield ' additional-paths send\n'
                        elif (t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit')) and (environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send') == 'ecmp')):
                            pass
                            yield '         neighbor '
                            yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                            yield ' additional-paths send ecmp limit '
                            yield str(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit'))
                            yield '\n'
                        elif (environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send') == 'limit'):
                            pass
                            if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit')):
                                pass
                                yield '         neighbor '
                                yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                                yield ' additional-paths send limit '
                                yield str(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send_limit'))
                                yield '\n'
                        else:
                            pass
                            yield '         neighbor '
                            yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                            yield ' additional-paths send '
                            yield str(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'send'))
                            yield '\n'
                l_2_neighbor = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_6(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
                if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'redistribute_internal'), True):
                    pass
                    yield '         bgp redistribute-internal\n'
                elif t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'redistribute_internal'), False):
                    pass
                    yield '         no bgp redistribute-internal\n'
                if t_6(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'redistribute')):
                    pass
                    l_1_redistribute_var = environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'redistribute')
                    _loop_vars['redistribute_var'] = l_1_redistribute_var
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'enabled'), True):
                        pass
                        l_1_redistribute_host = 'redistribute attached-host'
                        _loop_vars['redistribute_host'] = l_1_redistribute_host
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'route_map')):
                            pass
                            l_1_redistribute_host = str_join(((undefined(name='redistribute_host') if l_1_redistribute_host is missing else l_1_redistribute_host), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'attached_host'), 'route_map'), ))
                            _loop_vars['redistribute_host'] = l_1_redistribute_host
                        yield '         '
                        yield str((undefined(name='redistribute_host') if l_1_redistribute_host is missing else l_1_redistribute_host))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'bgp'), 'enabled'), True):
                        pass
                        l_1_redistribute_bgp = 'redistribute bgp leaked'
                        _loop_vars['redistribute_bgp'] = l_1_redistribute_bgp
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'bgp'), 'route_map')):
                            pass
                            l_1_redistribute_bgp = str_join(((undefined(name='redistribute_bgp') if l_1_redistribute_bgp is missing else l_1_redistribute_bgp), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'bgp'), 'route_map'), ))
                            _loop_vars['redistribute_bgp'] = l_1_redistribute_bgp
                        yield '         '
                        yield str((undefined(name='redistribute_bgp') if l_1_redistribute_bgp is missing else l_1_redistribute_bgp))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dhcp'), 'enabled'), True):
                        pass
                        l_1_redistribute_dhcp = 'redistribute dhcp'
                        _loop_vars['redistribute_dhcp'] = l_1_redistribute_dhcp
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dhcp'), 'route_map')):
                            pass
                            l_1_redistribute_dhcp = str_join(((undefined(name='redistribute_dhcp') if l_1_redistribute_dhcp is missing else l_1_redistribute_dhcp), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dhcp'), 'route_map'), ))
                            _loop_vars['redistribute_dhcp'] = l_1_redistribute_dhcp
                        yield '         '
                        yield str((undefined(name='redistribute_dhcp') if l_1_redistribute_dhcp is missing else l_1_redistribute_dhcp))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'enabled'), True):
                        pass
                        l_1_redistribute_conn = 'redistribute connected'
                        _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' include leaked', ))
                            _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'route_map')):
                            pass
                            l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'route_map'), ))
                            _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'rcf')):
                            pass
                            l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'rcf'), ))
                            _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        yield '         '
                        yield str((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'enabled'), True):
                        pass
                        l_1_redistribute_dynamic = 'redistribute dynamic'
                        _loop_vars['redistribute_dynamic'] = l_1_redistribute_dynamic
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'route_map')):
                            pass
                            l_1_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_1_redistribute_dynamic is missing else l_1_redistribute_dynamic), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'route_map'), ))
                            _loop_vars['redistribute_dynamic'] = l_1_redistribute_dynamic
                        elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'rcf')):
                            pass
                            l_1_redistribute_dynamic = str_join(((undefined(name='redistribute_dynamic') if l_1_redistribute_dynamic is missing else l_1_redistribute_dynamic), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'dynamic'), 'rcf'), ))
                            _loop_vars['redistribute_dynamic'] = l_1_redistribute_dynamic
                        yield '         '
                        yield str((undefined(name='redistribute_dynamic') if l_1_redistribute_dynamic is missing else l_1_redistribute_dynamic))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'user'), 'enabled'), True):
                        pass
                        l_1_redistribute_user = 'redistribute user'
                        _loop_vars['redistribute_user'] = l_1_redistribute_user
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'user'), 'rcf')):
                            pass
                            l_1_redistribute_user = str_join(((undefined(name='redistribute_user') if l_1_redistribute_user is missing else l_1_redistribute_user), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'user'), 'rcf'), ))
                            _loop_vars['redistribute_user'] = l_1_redistribute_user
                        yield '         '
                        yield str((undefined(name='redistribute_user') if l_1_redistribute_user is missing else l_1_redistribute_user))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'enabled'), True):
                        pass
                        l_1_redistribute_isis = 'redistribute isis'
                        _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'isis_level')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'isis_level'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' include leaked', ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'route_map')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'route_map'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'rcf')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'rcf'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        yield '         '
                        yield str((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3 = 'redistribute ospfv3'
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' include leaked', ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3))
                        yield '\n'
                    elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3 = 'redistribute ospfv3 match internal'
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' include leaked', ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3_match = 'redistribute ospfv3 match external'
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' include leaked', ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3_match = 'redistribute ospfv3 match nssa-external'
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' include leaked', ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'enabled'), True):
                        pass
                        l_1_redistribute_static = 'redistribute static'
                        _loop_vars['redistribute_static'] = l_1_redistribute_static
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' include leaked', ))
                            _loop_vars['redistribute_static'] = l_1_redistribute_static
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'route_map')):
                            pass
                            l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'route_map'), ))
                            _loop_vars['redistribute_static'] = l_1_redistribute_static
                        elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'rcf')):
                            pass
                            l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'rcf'), ))
                            _loop_vars['redistribute_static'] = l_1_redistribute_static
                        yield '         '
                        yield str((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static))
                        yield '\n'
                elif t_6(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'redistribute_routes')):
                    pass
                    for l_2_redistribute_route in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'redistribute_routes'), 'source_protocol'):
                        l_2_redistribute_route_cli = missing
                        _loop_vars = {}
                        pass
                        l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'ospfv3'):
                            pass
                            if t_6(environment.getattr(l_2_redistribute_route, 'ospf_route_type')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' match ', environment.getattr(l_2_redistribute_route, 'ospf_route_type'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'bgp'):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif (t_6(environment.getattr(l_2_redistribute_route, 'include_leaked'), True) and (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['connected', 'isis', 'ospfv3', 'static'])):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if t_6(environment.getattr(l_2_redistribute_route, 'route_map')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                            pass
                            if t_6(environment.getattr(l_2_redistribute_route, 'rcf')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' rcf ', environment.getattr(l_2_redistribute_route, 'rcf'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        yield '         '
                        yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                        yield '\n'
                    l_2_redistribute_route = l_2_redistribute_route_cli = missing
            if t_6(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast')):
                pass
                yield '      !\n      address-family ipv6 multicast\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_6(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_6(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_6(environment.getattr(environment.getattr(l_2_neighbor, 'additional_paths'), 'receive'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' additional-paths receive\n'
                    if t_6(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_6(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                l_2_neighbor = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_6(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
                if t_6(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'redistribute')):
                    pass
                    l_1_redistribute_var = environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'redistribute')
                    _loop_vars['redistribute_var'] = l_1_redistribute_var
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'enabled'), True):
                        pass
                        l_1_redistribute_conn = 'redistribute connected'
                        _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'route_map')):
                            pass
                            l_1_redistribute_conn = str_join(((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'connected'), 'route_map'), ))
                            _loop_vars['redistribute_conn'] = l_1_redistribute_conn
                        yield '         '
                        yield str((undefined(name='redistribute_conn') if l_1_redistribute_conn is missing else l_1_redistribute_conn))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'enabled'), True):
                        pass
                        l_1_redistribute_isis = 'redistribute isis'
                        _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'isis_level')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'isis_level'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'include_leaked'), True):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' include leaked', ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'route_map')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'route_map'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        elif t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'rcf')):
                            pass
                            l_1_redistribute_isis = str_join(((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis), ' rcf ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'isis'), 'rcf'), ))
                            _loop_vars['redistribute_isis'] = l_1_redistribute_isis
                        yield '         '
                        yield str((undefined(name='redistribute_isis') if l_1_redistribute_isis is missing else l_1_redistribute_isis))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf = 'redistribute ospf'
                        _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'route_map')):
                            pass
                            l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'route_map'), ))
                            _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        yield '         '
                        yield str((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf))
                        yield '\n'
                    elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf = 'redistribute ospf match internal'
                        _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'route_map')):
                            pass
                            l_1_redistribute_ospf = str_join(((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_internal'), 'route_map'), ))
                            _loop_vars['redistribute_ospf'] = l_1_redistribute_ospf
                        yield '         '
                        yield str((undefined(name='redistribute_ospf') if l_1_redistribute_ospf is missing else l_1_redistribute_ospf))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3 = 'redistribute ospfv3'
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3))
                        yield '\n'
                    elif t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3 = 'redistribute ospfv3 match internal'
                        _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3 = str_join(((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_internal'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3'] = l_1_redistribute_ospfv3
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3') if l_1_redistribute_ospfv3 is missing else l_1_redistribute_ospfv3))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3_match = 'redistribute ospfv3 match external'
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospfv3_match = 'redistribute ospfv3 match nssa-external'
                        _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'nssa_type'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospfv3_match = str_join(((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospfv3'), 'match_nssa_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospfv3_match'] = l_1_redistribute_ospfv3_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospfv3_match') if l_1_redistribute_ospfv3_match is missing else l_1_redistribute_ospfv3_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf_match = 'redistribute ospf match external'
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'enabled'), True):
                        pass
                        l_1_redistribute_ospf_match = 'redistribute ospf match nssa-external'
                        _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type')):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'nssa_type'), ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        if t_6(environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map')):
                            pass
                            l_1_redistribute_ospf_match = str_join(((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match), ' route-map ', environment.getattr(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'ospf'), 'match_nssa_external'), 'route_map'), ))
                            _loop_vars['redistribute_ospf_match'] = l_1_redistribute_ospf_match
                        yield '         '
                        yield str((undefined(name='redistribute_ospf_match') if l_1_redistribute_ospf_match is missing else l_1_redistribute_ospf_match))
                        yield '\n'
                    if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'enabled'), True):
                        pass
                        l_1_redistribute_static = 'redistribute static'
                        _loop_vars['redistribute_static'] = l_1_redistribute_static
                        if t_6(environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'route_map')):
                            pass
                            l_1_redistribute_static = str_join(((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static), ' route-map ', environment.getattr(environment.getattr((undefined(name='redistribute_var') if l_1_redistribute_var is missing else l_1_redistribute_var), 'static'), 'route_map'), ))
                            _loop_vars['redistribute_static'] = l_1_redistribute_static
                        yield '         '
                        yield str((undefined(name='redistribute_static') if l_1_redistribute_static is missing else l_1_redistribute_static))
                        yield '\n'
                elif t_6(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'redistribute_routes')):
                    pass
                    for l_2_redistribute_route in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'redistribute_routes'), 'source_protocol'):
                        l_2_redistribute_route_cli = missing
                        _loop_vars = {}
                        pass
                        l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                            pass
                            if t_6(environment.getattr(l_2_redistribute_route, 'ospf_route_type')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' match ', environment.getattr(l_2_redistribute_route, 'ospf_route_type'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if t_6(environment.getattr(l_2_redistribute_route, 'include_leaked'), True):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if t_6(environment.getattr(l_2_redistribute_route, 'route_map')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'isis'):
                            pass
                            if t_6(environment.getattr(l_2_redistribute_route, 'rcf')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' rcf ', environment.getattr(l_2_redistribute_route, 'rcf'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        yield '         '
                        yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                        yield '\n'
                    l_2_redistribute_route = l_2_redistribute_route_cli = missing
            if t_6(environment.getattr(l_1_vrf, 'evpn_multicast'), True):
                pass
                yield '      evpn multicast\n'
                if t_6(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_gateway_dr_election'), 'algorithm')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_gateway_dr_election'), 'algorithm') == 'preference'):
                        pass
                        if t_6(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_gateway_dr_election'), 'preference_value')):
                            pass
                            yield '         gateway dr election algorithm preference '
                            yield str(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_gateway_dr_election'), 'preference_value'))
                            yield '\n'
                    else:
                        pass
                        yield '         gateway dr election algorithm '
                        yield str(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_gateway_dr_election'), 'algorithm'))
                        yield '\n'
                if (t_6(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4')) and t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4'), 'transit'), True)):
                    pass
                    yield '         address-family ipv4\n'
                    if t_6(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4'), 'transit'), True):
                        pass
                        yield '            transit\n'
            if t_6(environment.getattr(l_1_vrf, 'eos_cli')):
                pass
                yield '      !\n      '
                yield str(t_4(environment.getattr(l_1_vrf, 'eos_cli'), 6, False))
                yield '\n'
        l_1_vrf = l_1_paths_cli = l_1_redistribute_var = l_1_redistribute_conn = l_1_redistribute_isis = l_1_redistribute_ospf = l_1_redistribute_ospf_match = l_1_redistribute_ospfv3 = l_1_redistribute_ospfv3_match = l_1_redistribute_static = l_1_redistribute_rip = l_1_redistribute_host = l_1_redistribute_dynamic = l_1_redistribute_bgp = l_1_redistribute_user = l_1_redistribute_dhcp = missing
        for l_1_session_tracker in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'session_trackers'), 'name'):
            _loop_vars = {}
            pass
            yield '   session tracker '
            yield str(environment.getattr(l_1_session_tracker, 'name'))
            yield '\n'
            if t_6(environment.getattr(l_1_session_tracker, 'recovery_delay')):
                pass
                yield '      recovery delay '
                yield str(environment.getattr(l_1_session_tracker, 'recovery_delay'))
                yield ' seconds\n'
        l_1_session_tracker = missing
        if t_6(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'eos_cli')):
            pass
            yield '   !\n   '
            yield str(t_4(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'eos_cli'), 3, False))
            yield '\n'

blocks = {}
debug_info = '7=84&9=87&10=89&11=92&13=94&14=97&16=99&19=102&22=105&24=108&27=111&29=114&32=117&33=119&34=122&35=124&37=128&39=130&40=132&41=135&43=137&44=140&48=143&49=146&51=148&53=151&54=153&55=156&56=158&60=161&61=163&62=166&63=168&65=172&67=174&68=176&69=179&70=181&72=185&74=187&75=191&77=194&80=197&83=200&84=202&86=205&87=208&88=210&89=212&90=215&93=220&96=222&98=224&97=228&99=232&100=234&101=236&103=238&104=240&105=242&106=244&107=246&109=249&112=252&115=255&116=267&117=269&118=272&120=276&121=279&123=281&124=284&126=286&127=289&129=291&130=293&131=295&132=297&133=299&134=301&137=304&138=306&139=309&141=311&142=314&144=316&145=319&147=321&148=324&150=328&151=331&153=335&154=338&156=340&157=343&159=347&160=350&161=352&164=355&167=363&168=366&170=370&171=372&172=374&173=376&175=379&177=381&178=383&179=385&180=387&182=390&183=392&184=394&185=397&187=399&188=402&190=406&191=409&193=413&194=416&196=418&197=421&199=425&200=428&202=432&203=435&205=439&206=442&208=446&209=449&211=453&212=456&214=462&215=464&216=466&217=468&219=470&220=472&222=475&224=477&225=480&226=482&227=485&229=489&230=491&231=493&232=495&234=497&235=499&237=502&239=504&240=506&241=511&242=513&243=515&244=517&245=519&246=521&247=523&248=525&250=527&251=529&253=531&254=533&257=535&258=538&262=541&263=543&264=545&265=547&267=550&269=552&270=554&271=556&272=558&274=561&275=563&276=566&279=569&280=580&281=583&283=587&284=590&286=594&287=597&289=599&290=602&292=604&293=606&294=608&295=610&296=612&297=614&300=617&301=619&302=622&304=624&305=627&307=629&308=632&310=634&311=637&313=641&314=644&316=648&317=651&319=653&320=656&322=660&323=663&324=665&327=668&329=676&330=679&332=681&333=684&335=688&336=690&337=692&338=694&340=697&342=699&343=701&344=703&345=705&347=708&348=710&349=712&350=715&352=717&353=720&355=724&356=727&358=731&359=734&360=736&361=739&363=741&364=744&366=748&367=751&369=755&370=758&372=762&373=765&375=769&376=772&378=778&379=781&381=785&382=787&383=789&384=791&386=793&387=795&389=798&391=800&392=803&393=805&394=808&396=812&397=814&398=816&399=818&401=820&402=822&404=825&406=827&407=829&408=834&409=836&410=838&411=840&412=842&413=844&414=846&415=848&417=850&418=852&420=854&421=856&424=858&425=861&429=864&430=866&431=868&432=870&434=873&436=875&437=877&438=879&439=881&441=884&442=886&443=889&446=892&448=895&451=898&452=902&453=904&454=906&456=908&457=910&459=912&460=914&462=916&463=918&465=920&466=922&468=925&470=928&471=930&472=933&473=935&474=938&475=940&477=943&478=945&479=948&480=950&482=954&484=956&485=958&486=961&487=963&489=966&490=968&492=971&493=973&494=976&495=978&497=982&499=984&500=986&501=989&502=991&504=994&505=996&507=1000&508=1002&509=1004&510=1007&511=1009&513=1012&514=1014&516=1018&518=1020&519=1022&520=1025&521=1027&523=1030&524=1032&526=1036&528=1038&529=1040&530=1043&531=1045&533=1048&534=1050&536=1053&537=1055&539=1059&541=1061&542=1063&543=1066&544=1068&546=1071&547=1073&549=1077&550=1079&551=1081&552=1084&553=1086&555=1089&556=1091&558=1095&560=1097&561=1099&562=1102&563=1104&565=1107&566=1109&568=1113&570=1115&571=1117&572=1120&573=1122&575=1125&576=1127&578=1130&579=1132&581=1136&583=1138&584=1140&585=1143&586=1145&588=1148&589=1150&590=1153&591=1155&593=1159&595=1161&596=1163&597=1166&598=1168&600=1172&602=1174&603=1176&604=1179&605=1181&607=1185&609=1187&610=1189&611=1192&612=1194&613=1197&614=1199&616=1203&618=1205&619=1207&620=1210&621=1212&623=1216&625=1218&626=1220&627=1223&628=1225&630=1229&632=1231&633=1233&634=1237&635=1239&636=1241&637=1243&640=1245&641=1247&642=1249&643=1251&645=1253&646=1255&647=1257&648=1259&649=1261&652=1264&655=1267&656=1270&657=1273&658=1279&659=1282&663=1289&664=1291&666=1295&667=1297&668=1300&670=1302&671=1305&673=1309&674=1313&676=1316&677=1320&679=1323&680=1327&682=1330&683=1334&685=1339&686=1343&688=1348&689=1352&691=1357&692=1361&694=1364&695=1368&697=1371&699=1374&704=1377&705=1379&707=1383&708=1386&709=1388&710=1391&712=1393&713=1396&715=1398&718=1401&721=1404&722=1407&724=1409&725=1412&727=1415&728=1417&735=1423&737=1427&738=1429&739=1432&741=1434&742=1437&744=1441&745=1445&747=1448&748=1452&750=1455&751=1459&753=1462&754=1466&756=1471&757=1475&759=1480&760=1484&762=1489&763=1493&765=1496&766=1500&768=1504&769=1506&771=1509&776=1512&779=1515&782=1518&785=1521&787=1524&790=1527&791=1529&793=1532&794=1535&795=1537&796=1539&797=1542&800=1547&802=1549&804=1552&806=1555&808=1558&809=1561&810=1563&811=1566&813=1568&816=1571&817=1573&818=1576&819=1578&821=1582&822=1584&825=1587&826=1589&827=1592&828=1595&829=1597&830=1598&831=1600&832=1601&833=1603&836=1605&837=1608&840=1610&841=1614&842=1617&843=1619&844=1622&846=1624&847=1627&849=1629&850=1632&852=1636&853=1639&855=1643&856=1646&858=1650&859=1653&861=1657&862=1659&863=1661&864=1663&865=1665&866=1667&868=1670&870=1672&871=1674&872=1677&873=1679&874=1682&875=1686&876=1688&877=1691&880=1698&883=1702&884=1705&886=1709&887=1712&890=1715&891=1720&892=1723&893=1725&894=1728&896=1730&897=1733&899=1735&900=1738&902=1742&903=1745&905=1749&906=1752&908=1756&909=1759&911=1763&912=1765&913=1767&914=1769&915=1771&916=1773&918=1776&920=1778&921=1780&922=1783&923=1785&924=1788&925=1792&926=1794&927=1797&930=1804&933=1808&934=1810&935=1812&936=1814&938=1817&941=1820&942=1823&944=1825&945=1828&947=1830&950=1833&953=1836&954=1838&955=1841&956=1843&958=1847&960=1849&962=1852&963=1854&964=1857&965=1859&967=1862&968=1864&970=1867&971=1869&973=1872&974=1875&977=1877&978=1879&979=1882&980=1884&982=1888&984=1890&987=1893&989=1897&990=1899&991=1902&993=1904&994=1907&999=1910&1002=1913&1003=1916&1005=1918&1006=1921&1008=1923&1009=1926&1010=1929&1011=1931&1012=1934&1015=1937&1016=1940&1017=1943&1022=1946&1025=1949&1026=1952&1028=1954&1029=1957&1031=1959&1032=1962&1033=1965&1034=1967&1035=1970&1038=1973&1039=1976&1040=1979&1045=1982&1048=1985&1050=1988&1053=1991&1056=1994&1057=1996&1059=1999&1060=2002&1061=2004&1062=2006&1063=2009&1066=2014&1069=2016&1070=2022&1071=2025&1072=2027&1073=2030&1075=2032&1076=2035&1078=2037&1079=2040&1081=2044&1082=2047&1084=2051&1085=2054&1087=2058&1088=2061&1090=2065&1091=2068&1093=2072&1094=2075&1096=2079&1097=2081&1098=2083&1099=2085&1101=2087&1102=2089&1104=2092&1106=2094&1107=2096&1108=2099&1110=2103&1111=2105&1112=2107&1113=2109&1114=2111&1117=2115&1119=2117&1120=2119&1122=2121&1123=2124&1127=2126&1128=2128&1129=2130&1130=2132&1132=2135&1135=2138&1136=2143&1137=2146&1138=2148&1139=2151&1141=2153&1142=2156&1144=2158&1145=2161&1147=2165&1148=2168&1150=2172&1151=2175&1153=2179&1154=2182&1156=2186&1157=2189&1159=2193&1160=2196&1162=2200&1163=2202&1164=2204&1165=2206&1167=2208&1168=2210&1170=2213&1172=2215&1173=2217&1174=2220&1176=2224&1177=2226&1178=2228&1179=2230&1180=2232&1183=2236&1185=2238&1186=2240&1188=2242&1189=2245&1194=2248&1195=2251&1196=2254&1198=2261&1201=2264&1203=2267&1206=2270&1207=2272&1208=2275&1209=2277&1210=2280&1211=2282&1213=2286&1215=2288&1216=2290&1217=2293&1218=2295&1220=2299&1222=2301&1223=2303&1224=2306&1225=2308&1227=2311&1228=2313&1229=2316&1230=2318&1232=2322&1234=2324&1235=2326&1236=2329&1237=2331&1238=2334&1239=2336&1241=2340&1243=2342&1244=2344&1245=2347&1246=2349&1248=2353&1250=2355&1251=2357&1252=2360&1253=2362&1255=2365&1256=2367&1258=2370&1259=2372&1260=2375&1261=2377&1263=2381&1265=2383&1266=2385&1267=2388&1268=2390&1270=2393&1271=2395&1273=2399&1274=2401&1275=2403&1276=2406&1277=2408&1279=2411&1280=2413&1282=2417&1284=2419&1285=2421&1286=2424&1287=2426&1289=2429&1290=2431&1292=2435&1293=2437&1294=2439&1295=2442&1296=2444&1298=2447&1299=2449&1301=2453&1303=2455&1304=2457&1305=2460&1306=2462&1308=2465&1309=2467&1311=2471&1313=2473&1314=2475&1315=2478&1316=2480&1318=2483&1319=2485&1321=2488&1322=2490&1324=2494&1326=2496&1327=2498&1328=2501&1329=2503&1331=2506&1332=2508&1334=2512&1336=2514&1337=2516&1338=2519&1339=2521&1341=2524&1342=2526&1344=2529&1345=2531&1347=2535&1349=2537&1350=2539&1351=2542&1352=2544&1354=2548&1356=2550&1357=2552&1358=2555&1359=2557&1361=2560&1362=2562&1363=2565&1364=2567&1366=2571&1368=2573&1369=2575&1370=2579&1371=2581&1372=2583&1373=2585&1376=2587&1377=2589&1378=2591&1379=2593&1381=2595&1382=2597&1383=2599&1384=2601&1385=2603&1388=2606&1393=2609&1396=2612&1399=2615&1400=2617&1401=2622&1402=2624&1403=2626&1404=2628&1405=2630&1406=2632&1407=2634&1408=2636&1410=2638&1411=2640&1413=2642&1414=2644&1417=2646&1418=2649&1422=2652&1425=2655&1426=2657&1428=2660&1429=2663&1430=2665&1431=2667&1432=2670&1435=2675&1438=2677&1441=2680&1444=2683&1445=2685&1446=2688&1447=2691&1448=2693&1449=2694&1450=2696&1451=2698&1453=2699&1454=2701&1457=2703&1458=2706&1461=2708&1462=2712&1463=2715&1465=2720&1467=2722&1468=2725&1470=2727&1471=2730&1473=2732&1474=2735&1476=2739&1477=2742&1479=2746&1480=2749&1482=2753&1483=2756&1485=2760&1486=2763&1488=2767&1489=2769&1490=2772&1491=2774&1492=2777&1493=2781&1494=2783&1495=2786&1498=2793&1501=2797&1502=2800&1504=2802&1505=2805&1507=2807&1508=2810&1509=2814&1510=2817&1512=2821&1513=2823&1514=2825&1515=2827&1517=2830&1519=2832&1520=2834&1521=2839&1522=2841&1523=2843&1524=2845&1525=2847&1526=2849&1527=2851&1528=2853&1530=2855&1531=2857&1533=2859&1534=2861&1537=2863&1538=2866&1542=2869&1543=2872&1545=2874&1546=2877&1549=2880&1550=2884&1551=2887&1553=2892&1555=2894&1556=2897&1558=2899&1559=2902&1561=2904&1562=2907&1564=2911&1565=2914&1567=2918&1568=2921&1570=2925&1571=2928&1573=2932&1574=2935&1576=2939&1577=2941&1578=2944&1579=2946&1580=2949&1581=2953&1582=2955&1583=2958&1586=2965&1589=2969&1590=2972&1592=2974&1593=2977&1595=2979&1596=2982&1597=2986&1598=2989&1600=2993&1601=2995&1602=2997&1603=2999&1605=3002&1607=3004&1608=3006&1609=3011&1610=3013&1611=3015&1612=3017&1613=3019&1614=3021&1615=3023&1616=3025&1618=3027&1619=3029&1621=3031&1622=3033&1625=3035&1626=3038&1630=3041&1631=3044&1633=3046&1634=3049&1637=3052&1638=3054&1639=3058&1640=3060&1641=3062&1643=3065&1646=3068&1647=3070&1648=3074&1649=3076&1650=3078&1652=3081&1655=3084&1658=3087&1659=3090&1661=3092&1664=3095&1665=3097&1666=3101&1667=3103&1668=3105&1670=3108&1673=3111&1674=3113&1675=3116&1676=3119&1682=3122&1685=3125&1688=3128&1689=3131&1690=3134&1691=3136&1692=3139&1694=3141&1695=3144&1697=3146&1698=3149&1700=3153&1701=3156&1704=3161&1705=3164&1706=3167&1707=3169&1708=3172&1710=3174&1711=3177&1713=3179&1714=3182&1716=3186&1717=3189&1720=3194&1721=3196&1722=3199&1723=3201&1724=3204&1725=3206&1727=3210&1729=3212&1730=3214&1731=3217&1732=3219&1734=3223&1736=3225&1737=3227&1738=3230&1739=3232&1741=3235&1742=3237&1744=3240&1745=3242&1746=3245&1747=3247&1749=3251&1751=3253&1752=3255&1753=3258&1754=3260&1756=3264&1757=3266&1758=3268&1759=3271&1760=3273&1762=3277&1764=3279&1765=3281&1766=3284&1767=3286&1769=3290&1770=3292&1771=3294&1772=3297&1773=3299&1775=3303&1777=3305&1778=3307&1779=3310&1780=3312&1782=3316&1784=3318&1785=3320&1786=3323&1787=3325&1789=3328&1790=3330&1792=3334&1794=3336&1795=3338&1796=3341&1797=3343&1799=3347&1801=3349&1802=3351&1803=3354&1804=3356&1806=3359&1807=3361&1809=3365&1811=3367&1812=3369&1813=3372&1814=3374&1816=3378&1818=3380&1819=3382&1820=3386&1821=3388&1822=3390&1823=3392&1826=3394&1827=3396&1829=3398&1830=3400&1831=3402&1832=3404&1834=3407&1839=3410&1842=3413&1843=3416&1844=3419&1845=3421&1846=3424&1848=3426&1849=3429&1851=3433&1852=3436&1855=3441&1856=3444&1857=3447&1858=3449&1859=3452&1861=3454&1862=3457&1864=3461&1865=3464&1870=3469&1873=3472&1875=3475&1878=3478&1881=3481&1882=3483&1884=3486&1885=3489&1886=3491&1887=3493&1888=3496&1891=3501&1894=3503&1895=3507&1896=3510&1897=3512&1898=3515&1900=3517&1901=3520&1903=3522&1904=3525&1906=3529&1907=3532&1909=3536&1910=3539&1912=3543&1913=3546&1915=3550&1916=3553&1918=3557&1919=3560&1921=3564&1922=3566&1923=3569&1925=3573&1926=3575&1927=3577&1928=3579&1929=3581&1932=3585&1934=3587&1935=3589&1937=3591&1938=3594&1943=3597&1944=3601&1945=3604&1946=3606&1947=3609&1949=3611&1950=3614&1952=3616&1953=3619&1955=3623&1956=3626&1958=3630&1959=3633&1961=3637&1962=3640&1964=3644&1965=3647&1967=3651&1968=3654&1970=3658&1971=3660&1972=3663&1974=3667&1975=3669&1976=3671&1977=3673&1978=3675&1981=3679&1983=3681&1984=3683&1986=3685&1987=3688&1992=3691&1993=3694&1994=3697&1996=3704&1999=3707&2001=3710&2004=3713&2005=3715&2006=3718&2007=3720&2008=3723&2009=3725&2011=3729&2013=3731&2014=3733&2015=3736&2016=3738&2018=3742&2020=3744&2021=3746&2022=3749&2023=3751&2025=3755&2027=3757&2028=3759&2029=3762&2030=3764&2032=3767&2033=3769&2034=3772&2035=3774&2037=3778&2039=3780&2040=3782&2041=3785&2042=3787&2043=3790&2044=3792&2046=3796&2048=3798&2049=3800&2050=3803&2051=3805&2053=3809&2055=3811&2056=3813&2057=3816&2058=3818&2060=3821&2061=3823&2063=3826&2064=3828&2065=3831&2066=3833&2068=3837&2070=3839&2071=3841&2072=3844&2073=3846&2075=3849&2076=3851&2078=3855&2079=3857&2080=3859&2081=3862&2082=3864&2084=3867&2085=3869&2087=3873&2089=3875&2090=3877&2091=3880&2092=3882&2094=3885&2095=3887&2097=3891&2099=3893&2100=3895&2101=3898&2102=3900&2104=3903&2105=3905&2107=3908&2108=3910&2110=3914&2112=3916&2113=3918&2114=3921&2115=3923&2117=3926&2118=3928&2119=3931&2120=3933&2122=3937&2124=3939&2125=3941&2126=3945&2127=3947&2128=3949&2129=3951&2132=3953&2133=3955&2134=3957&2135=3959&2137=3961&2138=3963&2139=3965&2140=3967&2141=3969&2144=3972&2149=3975&2152=3978&2153=3981&2155=3983&2156=3986&2158=3988&2161=3991&2162=3994&2163=3997&2164=3999&2165=4002&2167=4004&2168=4007&2171=4010&2172=4013&2173=4016&2175=4018&2176=4021&2178=4023&2179=4026&2181=4030&2182=4033&2185=4038&2186=4042&2187=4044&2188=4046&2190=4049&2192=4052&2193=4054&2194=4057&2195=4059&2196=4062&2197=4064&2199=4068&2201=4070&2202=4072&2203=4075&2204=4077&2206=4080&2207=4082&2209=4085&2210=4087&2211=4090&2212=4092&2214=4096&2216=4098&2217=4100&2218=4103&2219=4105&2221=4109&2222=4111&2223=4113&2224=4116&2225=4118&2227=4122&2229=4124&2230=4126&2231=4129&2232=4131&2234=4135&2235=4137&2236=4139&2237=4142&2238=4144&2240=4148&2242=4150&2243=4152&2244=4155&2245=4157&2247=4161&2249=4163&2250=4165&2251=4168&2252=4170&2254=4173&2255=4175&2257=4179&2259=4181&2260=4183&2261=4186&2262=4188&2264=4192&2266=4194&2267=4196&2268=4199&2269=4201&2271=4204&2272=4206&2274=4210&2276=4212&2277=4214&2278=4217&2279=4219&2281=4223&2283=4225&2284=4227&2285=4231&2286=4233&2287=4235&2288=4237&2291=4239&2292=4241&2294=4243&2295=4245&2296=4247&2297=4249&2299=4252&2304=4255&2307=4258&2308=4261&2309=4264&2310=4266&2311=4269&2313=4271&2314=4274&2316=4278&2317=4281&2320=4286&2321=4289&2322=4292&2323=4294&2324=4297&2326=4299&2327=4302&2329=4306&2330=4309&2335=4314&2338=4317&2339=4320&2341=4322&2342=4325&2344=4327&2345=4330&2346=4333&2347=4335&2348=4338&2350=4340&2351=4343&2353=4347&2354=4350&2357=4355&2358=4358&2359=4361&2361=4363&2362=4366&2364=4370&2365=4373&2368=4378&2369=4380&2372=4383&2373=4385&2374=4388&2375=4390&2377=4393&2378=4395&2380=4399&2385=4401&2388=4404&2391=4407&2392=4409&2394=4412&2395=4415&2396=4417&2397=4419&2398=4422&2401=4427&2404=4429&2405=4432&2406=4435&2407=4437&2408=4440&2410=4442&2411=4445&2413=4447&2414=4449&2415=4452&2416=4454&2417=4457&2418=4461&2419=4463&2420=4466&2423=4473&2427=4478&2428=4481&2429=4484&2430=4486&2431=4489&2433=4491&2434=4494&2436=4496&2437=4498&2438=4501&2439=4503&2440=4506&2441=4510&2442=4512&2443=4515&2446=4522&2452=4527&2455=4530&2456=4533&2457=4536&2458=4538&2459=4541&2461=4543&2462=4545&2463=4548&2465=4553&2468=4555&2469=4558&2474=4561&2477=4564&2478=4568&2479=4571&2480=4573&2481=4576&2483=4578&2484=4581&2486=4585&2487=4588&2489=4592&2490=4595&2492=4599&2493=4602&2495=4606&2496=4608&2497=4610&2498=4612&2499=4614&2500=4616&2502=4619&2505=4622&2506=4626&2507=4629&2508=4631&2509=4634&2511=4636&2512=4639&2514=4643&2515=4646&2517=4650&2518=4653&2520=4657&2521=4660&2523=4664&2524=4666&2525=4668&2526=4670&2527=4672&2528=4674&2530=4677&2533=4680&2534=4683&2536=4685&2537=4688&2539=4690&2544=4693&2547=4696&2548=4700&2549=4703&2550=4705&2551=4708&2553=4710&2554=4713&2556=4717&2557=4720&2559=4724&2560=4727&2562=4731&2563=4734&2565=4738&2566=4740&2567=4742&2568=4744&2569=4746&2570=4748&2572=4751&2575=4754&2576=4758&2577=4761&2578=4763&2579=4766&2581=4768&2582=4771&2584=4775&2585=4778&2587=4782&2588=4785&2590=4789&2591=4792&2593=4796&2594=4798&2595=4800&2596=4802&2597=4804&2598=4806&2600=4809&2603=4812&2604=4815&2606=4817&2607=4820&2609=4822&2614=4825&2616=4844&2617=4846&2618=4849&2620=4851&2621=4853&2622=4857&2623=4859&2624=4861&2626=4863&2627=4865&2628=4867&2629=4869&2631=4872&2634=4875&2635=4877&2636=4880&2637=4884&2639=4889&2640=4891&2641=4893&2642=4896&2644=4905&2647=4909&2648=4912&2653=4917&2654=4919&2655=4922&2656=4926&2658=4931&2659=4933&2660=4935&2661=4938&2663=4947&2666=4951&2667=4954&2672=4959&2673=4962&2675=4964&2678=4967&2681=4970&2682=4973&2684=4975&2685=4977&2686=4979&2687=4981&2689=4984&2691=4986&2693=4989&2696=4992&2699=4995&2700=4997&2702=5000&2703=5003&2704=5005&2705=5007&2706=5010&2709=5015&2712=5017&2714=5019&2713=5023&2715=5027&2716=5029&2717=5031&2719=5033&2720=5035&2721=5037&2722=5039&2723=5041&2725=5044&2728=5047&2729=5058&2730=5061&2732=5065&2733=5068&2735=5072&2736=5075&2738=5077&2739=5080&2741=5082&2742=5084&2743=5086&2744=5088&2745=5090&2746=5092&2749=5095&2750=5097&2751=5100&2753=5102&2754=5105&2756=5107&2757=5110&2759=5112&2760=5115&2762=5119&2763=5122&2765=5126&2766=5129&2768=5131&2769=5134&2771=5138&2772=5141&2773=5143&2776=5146&2778=5154&2779=5157&2781=5159&2782=5162&2784=5166&2785=5168&2786=5170&2787=5172&2789=5175&2791=5177&2792=5179&2793=5181&2794=5183&2796=5186&2797=5188&2798=5190&2799=5193&2801=5195&2802=5197&2803=5199&2804=5201&2806=5204&2808=5206&2809=5209&2810=5211&2811=5214&2813=5216&2814=5219&2816=5223&2817=5226&2819=5230&2820=5233&2822=5235&2823=5237&2824=5240&2825=5242&2826=5245&2827=5249&2828=5251&2829=5254&2832=5261&2835=5265&2836=5268&2838=5272&2839=5275&2841=5279&2842=5281&2843=5283&2844=5285&2846=5287&2847=5289&2849=5292&2851=5294&2852=5297&2853=5299&2854=5302&2856=5306&2857=5308&2858=5310&2859=5312&2861=5314&2862=5316&2864=5319&2866=5321&2867=5323&2868=5325&2869=5327&2871=5330&2872=5332&2873=5335&2876=5338&2877=5341&2878=5344&2880=5351&2883=5354&2885=5357&2888=5360&2889=5364&2890=5366&2891=5368&2893=5370&2894=5372&2896=5374&2897=5376&2899=5378&2900=5380&2902=5382&2903=5384&2905=5387&2907=5390&2908=5392&2909=5394&2910=5396&2911=5398&2912=5400&2914=5402&2915=5404&2916=5406&2917=5408&2919=5411&2921=5413&2922=5415&2923=5417&2924=5419&2926=5421&2927=5423&2929=5425&2930=5427&2931=5429&2932=5431&2934=5434&2936=5436&2937=5438&2938=5440&2939=5442&2941=5444&2942=5446&2944=5449&2945=5451&2946=5453&2947=5455&2948=5457&2950=5459&2951=5461&2953=5464&2955=5466&2956=5468&2957=5470&2958=5472&2960=5474&2961=5476&2963=5479&2965=5481&2966=5483&2967=5485&2968=5487&2970=5489&2971=5491&2973=5493&2974=5495&2976=5498&2978=5500&2979=5502&2980=5504&2981=5506&2983=5508&2984=5510&2986=5513&2987=5515&2988=5517&2989=5519&2990=5521&2992=5523&2993=5525&2995=5528&2997=5530&2998=5532&2999=5534&3000=5536&3002=5538&3003=5540&3005=5543&3007=5545&3008=5547&3009=5549&3010=5551&3012=5553&3013=5555&3015=5557&3016=5559&3018=5562&3020=5564&3021=5566&3022=5568&3023=5570&3025=5572&3026=5574&3027=5576&3028=5578&3030=5581&3032=5583&3033=5585&3034=5587&3035=5589&3037=5592&3039=5594&3040=5596&3041=5598&3042=5600&3044=5603&3046=5605&3047=5607&3048=5609&3049=5611&3050=5613&3051=5615&3053=5618&3055=5620&3056=5622&3057=5624&3058=5626&3060=5629&3062=5631&3063=5633&3064=5635&3065=5637&3067=5640&3069=5642&3070=5644&3071=5648&3072=5650&3073=5652&3074=5654&3077=5656&3078=5658&3079=5660&3080=5662&3082=5664&3083=5666&3084=5668&3085=5670&3086=5672&3089=5675&3092=5678&3093=5681&3094=5684&3095=5690&3096=5693&3099=5700&3102=5703&3103=5706&3105=5708&3106=5711&3108=5713&3109=5716&3110=5719&3114=5722&3117=5725&3118=5728&3120=5730&3121=5733&3123=5735&3124=5738&3125=5741&3129=5744&3132=5747&3134=5750&3137=5753&3138=5756&3140=5758&3141=5761&3143=5763&3146=5766&3147=5768&3149=5771&3150=5774&3151=5776&3152=5778&3153=5781&3156=5786&3159=5788&3160=5792&3161=5795&3163=5797&3164=5800&3166=5802&3167=5805&3169=5809&3170=5812&3172=5816&3173=5819&3175=5823&3176=5826&3178=5830&3179=5833&3181=5837&3182=5840&3184=5844&3185=5846&3186=5849&3187=5851&3188=5854&3189=5858&3190=5860&3191=5863&3194=5870&3197=5874&3198=5876&3199=5878&3200=5880&3201=5882&3203=5884&3204=5886&3206=5889&3209=5892&3210=5896&3211=5898&3212=5900&3214=5903&3216=5906&3218=5909&3221=5912&3222=5914&3223=5916&3224=5918&3225=5920&3226=5922&3228=5925&3230=5927&3231=5929&3232=5931&3233=5933&3235=5936&3237=5938&3238=5940&3239=5942&3240=5944&3242=5946&3243=5948&3244=5950&3245=5952&3247=5955&3249=5957&3250=5959&3251=5961&3252=5963&3253=5965&3254=5967&3256=5970&3258=5972&3259=5974&3260=5976&3261=5978&3263=5981&3265=5983&3266=5985&3267=5987&3268=5989&3270=5991&3271=5993&3273=5995&3274=5997&3275=5999&3276=6001&3278=6004&3280=6006&3281=6008&3282=6010&3283=6012&3285=6014&3286=6016&3288=6019&3289=6021&3290=6023&3291=6025&3292=6027&3294=6029&3295=6031&3297=6034&3299=6036&3300=6038&3301=6040&3302=6042&3304=6044&3305=6046&3307=6049&3308=6051&3309=6053&3310=6055&3311=6057&3313=6059&3314=6061&3316=6064&3318=6066&3319=6068&3320=6070&3321=6072&3323=6074&3324=6076&3326=6079&3328=6081&3329=6083&3330=6085&3331=6087&3333=6089&3334=6091&3336=6093&3337=6095&3339=6098&3341=6100&3342=6102&3343=6104&3344=6106&3346=6108&3347=6110&3349=6113&3351=6115&3352=6117&3353=6119&3354=6121&3356=6123&3357=6125&3359=6127&3360=6129&3362=6132&3364=6134&3365=6136&3366=6138&3367=6140&3369=6143&3371=6145&3372=6147&3373=6149&3374=6151&3376=6153&3377=6155&3378=6157&3379=6159&3381=6162&3383=6164&3384=6166&3385=6170&3386=6172&3387=6174&3388=6176&3391=6178&3392=6180&3393=6182&3394=6184&3396=6186&3397=6188&3398=6190&3399=6192&3400=6194&3403=6197&3407=6200&3410=6203&3411=6206&3413=6208&3414=6211&3416=6213&3419=6216&3420=6219&3421=6222&3423=6224&3424=6227&3426=6229&3427=6232&3429=6236&3430=6239&3433=6244&3434=6248&3435=6250&3436=6252&3438=6255&3440=6258&3441=6260&3442=6262&3443=6264&3444=6266&3445=6268&3447=6271&3449=6273&3450=6275&3451=6277&3452=6279&3454=6282&3456=6284&3457=6286&3458=6288&3459=6290&3461=6292&3462=6294&3464=6296&3465=6298&3466=6300&3467=6302&3469=6305&3471=6307&3472=6309&3473=6311&3474=6313&3476=6316&3477=6318&3478=6320&3479=6322&3480=6324&3482=6327&3484=6329&3485=6331&3486=6333&3487=6335&3489=6338&3490=6340&3491=6342&3492=6344&3493=6346&3495=6349&3497=6351&3498=6353&3499=6355&3500=6357&3502=6360&3504=6362&3505=6364&3506=6366&3507=6368&3509=6370&3510=6372&3512=6375&3514=6377&3515=6379&3516=6381&3517=6383&3519=6386&3521=6388&3522=6390&3523=6392&3524=6394&3526=6396&3527=6398&3529=6401&3531=6403&3532=6405&3533=6407&3534=6409&3536=6412&3538=6414&3539=6416&3540=6420&3541=6422&3542=6424&3543=6426&3546=6428&3547=6430&3549=6432&3550=6434&3551=6436&3552=6438&3553=6440&3556=6443&3560=6446&3563=6449&3565=6452&3568=6455&3569=6458&3571=6460&3572=6463&3574=6465&3577=6468&3578=6470&3580=6473&3581=6476&3582=6478&3583=6480&3584=6483&3587=6488&3590=6490&3591=6493&3592=6496&3594=6498&3595=6501&3597=6503&3598=6506&3600=6510&3601=6513&3603=6517&3604=6520&3606=6524&3607=6527&3609=6531&3610=6534&3612=6538&3613=6541&3615=6545&3616=6547&3617=6550&3618=6552&3619=6555&3620=6559&3621=6561&3622=6564&3625=6571&3629=6576&3630=6580&3631=6582&3632=6584&3634=6587&3636=6590&3638=6593&3641=6596&3642=6598&3643=6600&3644=6602&3645=6604&3646=6606&3648=6609&3650=6611&3651=6613&3652=6615&3653=6617&3655=6620&3657=6622&3658=6624&3659=6626&3660=6628&3662=6631&3664=6633&3665=6635&3666=6637&3667=6639&3669=6641&3670=6643&3671=6645&3672=6647&3674=6650&3676=6652&3677=6654&3678=6656&3679=6658&3680=6660&3681=6662&3683=6665&3685=6667&3686=6669&3687=6671&3688=6673&3690=6676&3692=6678&3693=6680&3694=6682&3695=6684&3697=6686&3698=6688&3700=6690&3701=6692&3702=6694&3703=6696&3705=6699&3707=6701&3708=6703&3709=6705&3710=6707&3712=6709&3713=6711&3715=6714&3716=6716&3717=6718&3718=6720&3719=6722&3721=6724&3722=6726&3724=6729&3726=6731&3727=6733&3728=6735&3729=6737&3731=6739&3732=6741&3734=6744&3736=6746&3737=6748&3738=6750&3739=6752&3741=6754&3742=6756&3744=6758&3745=6760&3747=6763&3749=6765&3750=6767&3751=6769&3752=6771&3754=6773&3755=6775&3756=6777&3757=6779&3759=6782&3761=6784&3762=6786&3763=6790&3764=6792&3765=6794&3766=6796&3769=6798&3770=6800&3771=6802&3772=6804&3774=6806&3775=6808&3776=6810&3777=6812&3778=6814&3781=6817&3785=6820&3788=6823&3789=6826&3791=6828&3792=6831&3794=6833&3797=6836&3798=6839&3799=6842&3801=6844&3802=6847&3804=6849&3805=6852&3807=6856&3808=6859&3811=6864&3812=6868&3813=6870&3814=6872&3816=6875&3818=6878&3819=6880&3820=6882&3821=6884&3822=6886&3823=6888&3825=6891&3827=6893&3828=6895&3829=6897&3830=6899&3832=6901&3833=6903&3835=6905&3836=6907&3837=6909&3838=6911&3840=6914&3842=6916&3843=6918&3844=6920&3845=6922&3847=6925&3848=6927&3849=6929&3850=6931&3851=6933&3853=6936&3855=6938&3856=6940&3857=6942&3858=6944&3860=6947&3861=6949&3862=6951&3863=6953&3864=6955&3866=6958&3868=6960&3869=6962&3870=6964&3871=6966&3873=6969&3875=6971&3876=6973&3877=6975&3878=6977&3880=6979&3881=6981&3883=6984&3885=6986&3886=6988&3887=6990&3888=6992&3890=6995&3892=6997&3893=6999&3894=7001&3895=7003&3897=7005&3898=7007&3900=7010&3902=7012&3903=7014&3904=7016&3905=7018&3907=7021&3909=7023&3910=7025&3911=7029&3912=7031&3913=7033&3914=7035&3917=7037&3918=7039&3920=7041&3921=7043&3922=7045&3923=7047&3924=7049&3927=7052&3931=7055&3933=7058&3934=7060&3935=7062&3936=7065&3939=7070&3942=7072&3945=7075&3950=7078&3952=7081&3956=7084&3957=7088&3958=7090&3959=7093&3962=7096&3964=7099'