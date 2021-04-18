import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def readDataBaseHost():
    if "IP_config" in config and "dataBaseHost" in config["IP_config"]:
        return config["IP_config"]["dataBaseHost"]
    return None


def readDataBasePort():
    if "IP_config" in config and "dataBasePort" in config["IP_config"]:
        return config["IP_config"]["dataBasePort"]
    return None


def readDataBaseUrl():
    if "IP_config" in config and "dataBaseStartName" in config["IP_config"]:
        start_name = config["IP_config"]["dataBaseStartName"]
        host = readDataBaseHost()
        port = readDataBasePort()
        if all(map(lambda x: x is not None, [start_name, host, port])):
            return f"{start_name}{host}:{port}"

    return None


def readWebApplicationProtocol():
    if "IP_config" in config and "dataBaseStartName" in config["IP_config"]:
        return config["IP_config"]["dataBaseStartName"]
    return None


def readWebApplicationHost():
    if "IP_config" in config and "webApplicationHost" in config["IP_config"]:
        return config["IP_config"]["webApplicationHost"]
    return None


def readWebApplicationPort():
    if "IP_config" in config and "webApplicationPort" in config["IP_config"]:
        return config["IP_config"]["webApplicationPort"]
    return None
