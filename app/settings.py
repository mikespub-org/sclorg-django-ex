import os


class MetaFlaskEnv(type):
    """
    Based on Flask-Env: https://github.com/brettlangdon/flask-env
    Waiting for ENV_LOAD_ALL to be available on PyPi
    """
    def __init__(cls, name, bases, dict):
        """
        MetaFlaskEnv class initializer.
        This function will get called when a new class which utilizes this metaclass is defined,
        as opposed to when it is initialized.
        """
        super(MetaFlaskEnv, cls).__init__(name, bases, dict)

        # Get our internal settings
        prefix = dict.get('ENV_PREFIX', '')
        load_all = dict.get('ENV_LOAD_ALL', False)


        # Override default configuration from environment variables
        for key, value in os.environ.items():
            # Only include environment keys that start with our prefix (if we have one)
            if not key.startswith(prefix):
                continue

            # Strip the prefix from the environment variable name
            key = key[len(prefix):]

            if not load_all and not hasattr(cls, key):
                continue

            # If value is "true" or "false", parse as a boolean
            # Otherwise, if it contains a "." then try to parse as a float
            # Otherwise, try to parse as an integer
            # If all else fails, just keep it a string
            if value.lower() in ('true', 'false'):
                value = True if value.lower() == 'true' else False
            elif '.' in value:
                try:
                    value = float(value)
                except ValueError:
                    pass
            else:
                try:
                    value = int(value)
                except ValueError:
                    pass

            # Update our config with the value from `os.environ`
            setattr(cls, key, value)


class EnvConfiguration(metaclass=MetaFlaskEnv):
    ENV_PREFIX = 'APP_'
    ENV_LOAD_ALL = True


class FileConfiguration:
    """
    Gets all the configuration parameters from the python module
    """
    def __init__(self, config_module):
        blacklist = ["os", "basedir"]
        double_underscore = "__"
        for attribute in dir(config_module):
            if attribute not in blacklist and not attribute.startswith(double_underscore):
                setattr(self, attribute, getattr(config_module, attribute))
