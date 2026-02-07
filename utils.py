def parse_operator(value: str):
    if value.startswith(">="):
        return ">=", value[2:]
    if value.startswith("<="):
        return "<=", value[2:]
    if value.startswith(">"):
        return ">", value[1:]
    if value.startswith("<"):
        return "<", value[1:]
    if value.startswith("="):
        return "=", value[1:]
    return "=", value
