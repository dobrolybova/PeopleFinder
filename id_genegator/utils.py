from schemes import Request


def construct_param_url(param, param_url, is_first_param):
    if is_first_param:
        base = "?"
    else:
        base = "&"
    if param is not None:
        is_first_param = False
        return base + f"{param_url}={param}", is_first_param
    else:
        return "", is_first_param


def construct_url(body: Request) -> str:
    base = "/find_person"
    is_first_param = True
    first_name, is_first_param = construct_param_url(body.first_name, "first_name", is_first_param)
    last_name, is_first_param = construct_param_url(body.last_name, "last_name", is_first_param)
    age, is_first_param = construct_param_url(body.age, "age", is_first_param)
    msisdn, is_first_param = construct_param_url(body.msisdn, "msisdn", is_first_param)
    email, is_first_param = construct_param_url(body.email, "email", is_first_param)
    city, is_first_param = construct_param_url(body.city, "city", is_first_param)

    return base + first_name + last_name + age + msisdn + email + city
