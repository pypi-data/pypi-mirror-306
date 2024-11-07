"""
Module providing helpers to load configuration files
"""

import argparse
from dataclasses import dataclass, field, fields, make_dataclass
from typing import Dict, List, Literal, NoReturn, Union, Type

import nectarine
from nectarine.providers.arguments import argument_parser_for
from nectarine import arguments, env
from nectarine.extensions.yaml import yaml
from nectarine.errors import NectarineError

from panza.backends.docker import DockerConfiguration as PanzaDockerConfiguration
from panza.backends.ignite import IgniteConfiguration as PanzaIgniteConfiguration


class ConfigurationLoadError(Exception):
    """
    Class representing an error related to configuration loading
    """

    def __init__(self, cause):
        super().__init__()
        self.__cause__ = cause

    def __str__(self):
        return f"cannot load configuration: {self.__cause__}"


@dataclass
class RabbitMQConfiguration:
    host: str
    port: int
    username: str
    password: str
    virtual_host: str = None
    use_ssl: bool = True
    prefetch_count: int = 5


@dataclass
class QueueConfiguration:
    name: str
    driver: str

    @staticmethod
    def parse(value: str) -> 'QueueConfiguration':
        return QueueConfiguration(*value.split(":"))


@dataclass
class UsernamePasswordCredentials:
    username: str
    password: str


@dataclass
class TokenCredentials:
    token: str


@dataclass
class CacheConfiguration:
    max_entries: int = 512


Credentials = Union[UsernamePasswordCredentials, TokenCredentials]


def make_tagged_dataclass(name: str, base: Type, type: Type):
    base_fields = [("type", type)] + [(f.name, f.type, f) for f in fields(base)]
    return make_dataclass(name, base_fields)


IgniteConfiguration = make_tagged_dataclass("IgniteConfiguration", PanzaIgniteConfiguration, Literal["ignite"])
DockerConfiguration = make_tagged_dataclass("DockerConfiguration", PanzaDockerConfiguration, Literal["docker"])

BackendConfiguration = Union[IgniteConfiguration, DockerConfiguration]


@dataclass
class RocinanteConfiguration:
    rabbitmq: RabbitMQConfiguration
    queues: List[QueueConfiguration]
    backend: BackendConfiguration
    credentials: Dict[str, Credentials]
    cache: CacheConfiguration = field(default_factory=CacheConfiguration)
    max_job_retries: int = 10
    log_directory: str = "/var/log/rocinante/"
    root_directory: str = "/var/lib/rocinante/"
    debug: bool = False
    job_timeout: float = 60 * 12


def _parse_config_file():
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument(
        "-c", "--config-file", type=str, metavar="FILE",
        help="the path to the configuration file"
    )
    arg_parser.add_argument("-h", "--help", action='store_true', help="show this help message and exit")
    return arg_parser.parse_known_args()


def _print_help() -> NoReturn:
    arg_parser = argument_parser_for(target_type=RocinanteConfiguration)
    arg_parser.add_argument(
        "-c", "--config-file", type=str, required=True, metavar="FILE",
        help="the path to the configuration file"
    )
    arg_parser.print_help()
    exit(0)


def load_config() -> RocinanteConfiguration:
    """
    Load the configuration

    :return:                the loaded configuration
    """

    args, remaining_args = _parse_config_file()

    if args.help is True or args.config_file is None:
        _print_help()

    try:
        return nectarine.load(
            target=RocinanteConfiguration,
            providers=[
                arguments(argv=remaining_args),
                env(prefix="ROCINANTE_"),
                yaml(args.config_file),
            ]
        )
    except (NectarineError, OSError) as e:
        raise ConfigurationLoadError(e)
