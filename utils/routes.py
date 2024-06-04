def unregister_route(app, rule):
    rules = list(app.url_map.iter_rules(rule))
    for r in rules:
        app.url_map._rules.remove(r)
        for method in r.methods:
            if method in app.url_map._rules_by_endpoint[r.endpoint]:
                app.url_map._rules_by_endpoint[r.endpoint][method].remove(r)
        if not app.url_map._rules_by_endpoint[r.endpoint]:
            del app.url_map._rules_by_endpoint[r.endpoint]
    del app.view_functions['scoreboard.listing']
