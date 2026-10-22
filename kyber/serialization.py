import json

from .params import PARAMS

Q = PARAMS.q
N = PARAMS.n
K = 2

VERSION = 1


def _validate_poly(poly, name, centered=False):
    if not isinstance(poly, list) or len(poly) != N:
        raise ValueError(f"{name} must be a list of N coefficients.")

    for coefficient in poly:
        if (
            not isinstance(coefficient, int)
            or isinstance(coefficient, bool)
        ):
            raise ValueError(f"{name} coefficients must be integers.")

        if centered:
            valid = -Q < coefficient < Q
        else:
            valid = 0 <= coefficient < Q

        if not valid:
            raise ValueError(f"{name} contains an out-of-range coefficient.")


def _validate_vector(vector, name, centered=False):
    if not isinstance(vector, list) or len(vector) != K:
        raise ValueError(f"{name} must contain exactly K polynomials.")

    for i, poly in enumerate(vector):
        _validate_poly(poly, f"{name}[{i}]", centered=centered)


def _validate_matrix(matrix, name):
    if not isinstance(matrix, list) or len(matrix) != K:
        raise ValueError(f"{name} must be a K x K matrix.")

    for i, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != K:
            raise ValueError(f"{name} must be a K x K matrix.")

        for j, poly in enumerate(row):
            _validate_poly(poly, f"{name}[{i}][{j}]")


def _encode(kind, data):
    return json.dumps(
        {
            "format": f"toy-kyber-{kind}",
            "version": VERSION,
            "data": data,
        },
        separators=(",", ":"),
        sort_keys=True,
    )


def _decode(serialized, kind):
    if not isinstance(serialized, str):
        raise ValueError("Serialized input must be a JSON string.")

    try:
        obj = json.loads(serialized)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError("Invalid JSON input.") from exc

    if not isinstance(obj, dict):
        raise ValueError("Serialized input must be a JSON object.")

    if set(obj) != {"format", "version", "data"}:
        raise ValueError("Unexpected serialized object fields.")

    if obj["format"] != f"toy-kyber-{kind}":
        raise ValueError("Unexpected serialized object format.")

    if obj["version"] != VERSION or isinstance(obj["version"], bool):
        raise ValueError("Unsupported serialization version.")

    return obj["data"]


def serialize_public_key(public_key):
    if not isinstance(public_key, (tuple, list)) or len(public_key) != 2:
        raise ValueError("Public key must contain (A, t).")

    A, t = public_key
    _validate_matrix(A, "A")
    _validate_vector(t, "t")

    return _encode("public-key", {"A": A, "t": t})


def deserialize_public_key(serialized):
    data = _decode(serialized, "public-key")

    if not isinstance(data, dict) or set(data) != {"A", "t"}:
        raise ValueError("Public-key data must contain A and t.")

    A, t = data["A"], data["t"]
    _validate_matrix(A, "A")
    _validate_vector(t, "t")

    return A, t


def serialize_secret_key(secret_key):
    _validate_vector(secret_key, "secret_key", centered=True)
    return _encode("secret-key", {"s": secret_key})


def deserialize_secret_key(serialized):
    data = _decode(serialized, "secret-key")

    if not isinstance(data, dict) or set(data) != {"s"}:
        raise ValueError("Secret-key data must contain s.")

    secret_key = data["s"]
    _validate_vector(secret_key, "secret_key", centered=True)

    return secret_key


def serialize_ciphertext(ciphertext):
    if not isinstance(ciphertext, (tuple, list)) or len(ciphertext) != 2:
        raise ValueError("Ciphertext must contain (u, v).")

    u, v = ciphertext
    _validate_vector(u, "u")
    _validate_poly(v, "v")

    return _encode("ciphertext", {"u": u, "v": v})


def deserialize_ciphertext(serialized):
    data = _decode(serialized, "ciphertext")

    if not isinstance(data, dict) or set(data) != {"u", "v"}:
        raise ValueError("Ciphertext data must contain u and v.")

    u, v = data["u"], data["v"]
    _validate_vector(u, "u")
    _validate_poly(v, "v")

    return u, v
