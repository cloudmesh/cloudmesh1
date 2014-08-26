def nova_provider(kind):
    sh_nova = None
    if kind is "sh":
        from sh import nova as sh_nova
    elif kind.startswith("sim"):
        def sh_nova (*args, **kwargs):
            print args, kwargs
    return sh_nova


# nova = nova_providor("simulator")

# nova("a", "b", h="k")
