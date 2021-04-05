import codecs
import pickle


def encode(obj) -> str:
    return codecs.encode(pickle.dumps(obj), "base64").decode()


def decode(bin_user):
    return pickle.loads(codecs.decode(bin_user.encode(), "base64"))
