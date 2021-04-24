import configparser

config = configparser.ConfigParser()
config.read("config.ini")


# server

def read_data_base_host():
    if "IP_config" in config and "dataBaseHost" in config["IP_config"]:
        return config["IP_config"]["dataBaseHost"]
    return None


def read_data_base_port():
    if "IP_config" in config and "dataBasePort" in config["IP_config"]:
        return config["IP_config"]["dataBasePort"]
    return None


def read_data_base_url():
    if "IP_config" in config and "dataBaseStartName" in config["IP_config"]:
        start_name = config["IP_config"]["dataBaseStartName"]
        host = read_data_base_host()
        port = read_data_base_port()
        if all(map(lambda x: x is not None, [start_name, host, port])):
            return f"{start_name}{host}:{port}"

    return None


def read_web_application_protocol():
    if "IP_config" in config and "dataBaseStartName" in config["IP_config"]:
        return config["IP_config"]["dataBaseStartName"]
    return None


def read_web_application_host():
    if "IP_config" in config and "webApplicationHost" in config["IP_config"]:
        return config["IP_config"]["webApplicationHost"]
    return None


def read_web_application_port():
    if "IP_config" in config and "webApplicationPort" in config["IP_config"]:
        return config["IP_config"]["webApplicationPort"]
    return None


# api url

def read_get_bin_user_api_url():
    if "API_config" in config and "getBinUser" in config["API_config"]:
        return config["API_config"]["getBinUser"]
    return None


def read_user_api_url():
    if "API_config" in config and "user" in config["API_config"]:
        return config["API_config"]["user"]
    return None


def read_check_email_api_url():
    if "API_config" in config and "checkEmail" in config["API_config"]:
        return config["API_config"]["checkEmail"]
    return None


def read_check_id_api_url():
    if "API_config" in config and "checkId" in config["API_config"]:
        return config["API_config"]["checkId"]
    return None


def read_users_api_url():
    if "API_config" in config and "users" in config["API_config"]:
        return config["API_config"]["users"]
    return None


def read_add_random_salt_value_api_url():
    if "API_config" in config and "addRandomSaltValue" in config["API_config"]:
        return config["API_config"]["addRandomSaltValue"]
    return None


def read_add_salt_value_api_url():
    if "API_config" in config and "addSaltValue" in config["API_config"]:
        return config["API_config"]["addSaltValue"]
    return None


def read_send_password_reset_email():
    if "API_config" in config and "sendPasswordResetEmail" in config["API_config"]:
        return config["API_config"]["sendPasswordResetEmail"]
    return None


def read_send_confirmation_email():
    if "API_config" in config and "sendConfirmationEmail" in config["API_config"]:
        return config["API_config"]["sendConfirmationEmail"]
    return None


# email

def read_mail_server():
    if "EMail_config" in config and "MAIL_SERVER" in config["EMail_config"]:
        return config["EMail_config"]["MAIL_SERVER"]
    return None


def read_mail_port():
    if "EMail_config" in config and "MAIL_PORT" in config["EMail_config"]:
        return config["EMail_config"]["MAIL_PORT"]
    return None


def read_mail_use_tls():
    if "EMail_config" in config and "MAIL_USE_TLS" in config["EMail_config"]:
        return config["EMail_config"]["MAIL_USE_TLS"]
    return None


def read_mail_username():
    if "EMail_config" in config and "MAIL_USERNAME" in config["EMail_config"]:
        return config["EMail_config"]["MAIL_USERNAME"]
    return None


def read_mail_admins():
    if "EMail_config" in config and "ADMINS" in config["EMail_config"]:
        return config["EMail_config"]["ADMINS"]
    return None


def read_mail_password():
    if "EMail_config" in config and "MAIL_PASSWORD" in config["EMail_config"]:
        return config["EMail_config"]["MAIL_PASSWORD"]
    return None
