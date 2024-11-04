import os
try:
    import tomllib as toml
except ImportError:
    import tomli as toml


class TomlEnvError(Exception):
    pass


class EnvObject(object):
    true_values = ["True", "true", 1, "1"]
    false_values = ["False", "false", 0, "0"]
    bool_values = true_values + false_values

    def __init__(self, toml_dict):
        self.toml_dict = toml_dict

    def get(self, key, default=None, nullable=False):
        if key not in self.toml_dict and not nullable:
            return default
        return self.toml_dict.get(key, default)

    def get_str(self, key, default=None, nullable=False):
        if key not in self.toml_dict and not nullable:
            raise TomlEnvError(f"'{key}' not found in environment")
        elif key not in self.toml_dict and nullable:
            return default
        return str(self.toml_dict[key])

    def get_int(self, key, default=None, nullable=False):
        if key not in self.toml_dict and not nullable:
            raise TomlEnvError(f"'{key}' not found in environment")
        elif key not in self.toml_dict and nullable:
            return default
        return int(self.toml_dict[key])

    def get_float(self, key, default=None, nullable=False):
        if key not in self.toml_dict and not nullable:
            raise TomlEnvError(f"'{key}' not found in environment")
        elif key not in self.toml_dict and nullable:
            return default
        return float(self.toml_dict[key])

    def get_bool(self, key, default=False, nullable=False):
        if key not in self.toml_dict and not nullable:
            raise TomlEnvError(f"'{key}' not found in environment")
        value = self.toml_dict.get(key, default)
        if value not in self.bool_values:
            raise TomlEnvError(f"'{key}={value}' is not a boolean value")
        return value in self.true_values


def load_env(path: str = ".env.toml"):
    with open(path, "rb") as f:
        toml_dict = toml.load(f)
    if "ENV" not in os.environ:
        raise TomlEnvError("The environment variable 'ENV' is not set")
    env_name = os.environ["ENV"]
    if env_name not in toml_dict:
        raise TomlEnvError(f"ENV '{env_name}' not found in {path}")
    return EnvObject(toml_dict[env_name])

