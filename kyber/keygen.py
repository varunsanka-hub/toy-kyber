from .module_lwe import module_lwe_sample


def keygen(rng=None):
    if rng is None:
        A, s, e, t = module_lwe_sample()
    else:
        A, s, e, t = module_lwe_sample(rng=rng)

    public_key = (A, t)
    secret_key = s

    return public_key, secret_key
