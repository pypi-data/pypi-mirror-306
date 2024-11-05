from __future__ import annotations
from typing import Any, Dict, Final, List, Optional, Callable, Union, Tuple
import json
import os
import pathlib

from dataclasses import dataclass

from ai_core_sdk.helpers import get_home
from ai_core_sdk.helpers.constants import (AI_CORE_PREFIX, AUTH_ENDPOINT_SUFFIX, CONFIG_FILE_ENV_VAR, PROFILE_ENV_VAR,
                                           VCAP_AICORE_SERVICE_NAME, VCAP_SERVICES_ENV_VAR)


def get_nested_value(data_dict, keys: List[str]):
    """
    Retrieve a nested value from a dictionary using a list of strings.

    :param data_dict: The dictionary to search.
    :param keys: A list of strings representing nested keys.
    :return: The value associated with the nested keys, or None if not found.
    """
    current_value = data_dict
    for key in keys:
        current_value = current_value[key]
    return current_value


@dataclass
class VCAPEnvironment:
    services: List[Service]

    @classmethod
    def from_env(cls, env_var: Optional[str] = None):
        env_var = env_var or VCAP_SERVICES_ENV_VAR
        env = json.loads(os.environ.get(env_var, '{}'))
        return cls.from_dict(env)

    @classmethod
    def from_dict(cls, env: Dict[str, Any]):
        services = [Service(service) for services in env.values() for service in services]
        return cls(services=services)

    def __getitem__(self, name) -> Service:
        return self.get_service(name, exactly_one=True)

    def get_service(self, label, exactly_one: bool = True) -> Service:
        services = [s for s in self.services if s.label == label]
        if exactly_one:
            if len(services) == 0:
                raise KeyError(f"No service found with label '{label}'.")
            return services[0]
        else:
            return services

    def get_service_by_name(self, name, exactly_one: bool = True) -> Service:
        services = [s for s in self.services if s.name == name]
        if exactly_one:
            if len(services) == 0:
                raise KeyError(f"No service found with name '{name}'.")
            return services[0]
        else:
            return services


NoDefault = object()


class Service:

    def __init__(self, env: Dict[str, Any]):
        self._env = env

    @property
    def label(self) -> Optional[str]:
        return self._env.get('label')

    @property
    def name(self) -> Optional[str]:
        return self._env.get('name')

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, default=NoDefault):
        if isinstance(key, str):
            key_splitted = key.split('.')
        else:
            key_splitted = key
        try:
            return get_nested_value(self._env, key_splitted) or default
        except KeyError:
            if default is NoDefault:
                raise KeyError(f"Key '{key}' not found in service '{self.name}'.")
            return default


@dataclass
class CredentialsValue:
    name: str
    vcap_key: Optional[Tuple[str, ...]] = None
    default: Optional[str] = None
    transform_fn: Optional[Callable] = None


CREDENTIAL_VALUES: Final[List[CredentialsValue]] = [
    CredentialsValue(name='client_id', vcap_key=('credentials', 'clientid')),
    CredentialsValue(name='client_secret', vcap_key=('credentials', 'clientsecret')),
    CredentialsValue(name='auth_url',
                     vcap_key=('credentials', 'url'),
                     transform_fn=lambda url: url.rstrip('/') +
                                              ('' if url.endswith(AUTH_ENDPOINT_SUFFIX) else AUTH_ENDPOINT_SUFFIX)),
    CredentialsValue(name='base_url',
                     vcap_key=('credentials', 'serviceurls', 'AI_API_URL'),
                     transform_fn=lambda url: url.rstrip('/') + ('' if url.endswith('/v2') else '/v2')),
    CredentialsValue(name='resource_group'),
    CredentialsValue(name='cert_url', vcap_key=('credentials', 'certurl'),
                     transform_fn=lambda url: url.rstrip('/') +
                                              ('' if url.endswith(AUTH_ENDPOINT_SUFFIX) else AUTH_ENDPOINT_SUFFIX)),
    # Even though the certificate and key in VCAP_SERVICES are not file paths, the names are defined this way in order
    # to keep it compatible with the config names. It'll be handled in fetch_credentials function.
    CredentialsValue(name='cert_file_path'),
    CredentialsValue(name='key_file_path'),
    CredentialsValue(name='cert_str', vcap_key=('credentials', 'certificate'),
                     transform_fn=lambda cert_str: cert_str.replace('\\n', '\n')),
    CredentialsValue(name='key_str', vcap_key=('credentials', 'key'),
                     transform_fn=lambda key_str: key_str.replace('\\n', '\n'))
]


def init_conf(profile: str = None):
    # Read configuration from ${AICORE_HOME}/config_<profile>.json.
    home = pathlib.Path(get_home())
    profile = profile or os.environ.get(PROFILE_ENV_VAR)
    profile_config_file = f'config_{profile}.json'
    path_to_config = (os.getenv(CONFIG_FILE_ENV_VAR) or
                      (home / ('config.json' if profile in ('default', '', None) else profile_config_file)))
    config = {}
    if path_to_config.exists():
        try:
            with path_to_config.open(encoding='utf-8') as f:
                return json.load(f)
        except json.decoder.JSONDecodeError:
            raise KeyError(f'{path_to_config} is not a valid json file. Please fix or remove it!')
    elif profile:
        raise FileNotFoundError(f"Unable to locate profile config file '{profile_config_file}' "
                                f"in AICORE_HOME '{home}')")
    return config


def fetch_credentials(profile: str = None) -> Dict[str, str]:
    config = init_conf(profile=profile)
    try:
        vcap_service = VCAPEnvironment.from_env()[VCAP_AICORE_SERVICE_NAME]
    except KeyError:
        vcap_service = None
    credentials = {}
    cred_value: CredentialsValue
    for cred_value in CREDENTIAL_VALUES:
        config_name = f'{AI_CORE_PREFIX}_{cred_value.name.upper()}'
        default_value = cred_value.default
        if cred_value.vcap_key is not None and vcap_service is not None:
            vcap_value = vcap_service.get(cred_value.vcap_key, cred_value.default)
        else:
            vcap_value = None
        env_value = os.getenv(config_name)
        config_value = config.get(config_name)
        value = env_value or config_value or vcap_value or default_value
        if value is not None:
            if cred_value.transform_fn:
                value = cred_value.transform_fn(value)
            credentials[cred_value.name] = value
    return credentials
