from functools import cache
from pathlib import Path
from typing import Mapping, Optional

from rich import print
from rich.panel import Panel
from ruamel.yaml import YAML


from goose.profile import Profile
from goose.utils import load_plugins

GOOSE_GLOBAL_PATH = Path("~/.config/goose").expanduser()
PROFILES_CONFIG_PATH = GOOSE_GLOBAL_PATH.joinpath("profiles.yaml")
SESSIONS_PATH = GOOSE_GLOBAL_PATH.joinpath("sessions")
SESSION_FILE_SUFFIX = ".jsonl"
LOG_PATH = GOOSE_GLOBAL_PATH.joinpath("logs")
RECOMMENDED_DEFAULT_PROVIDER = "openai"


@cache
def default_profiles() -> Mapping[str, callable]:
    return load_plugins(group="goose.profile")


def session_path(name: str) -> Path:
    SESSIONS_PATH.mkdir(parents=True, exist_ok=True)
    return SESSIONS_PATH.joinpath(f"{name}{SESSION_FILE_SUFFIX}")


def write_config(profiles: dict[str, Profile]) -> None:
    """Overwrite the config with the passed profiles"""
    PROFILES_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    converted = {name: profile.to_dict() for name, profile in profiles.items()}
    yaml = YAML()
    with PROFILES_CONFIG_PATH.open("w") as f:
        yaml.dump(converted, f)


def ensure_config(name: Optional[str]) -> tuple[str, Profile]:
    """Ensure that the config exists and has the default section"""
    # TODO we should copy a templated default config in to better document
    # but this is complicated a bit by autodetecting the provider
    default_profile_name = "default"
    name = name or default_profile_name
    default_profiles_dict = default_profiles()
    provider, processor, accelerator = default_model_configuration()
    default_profile = default_profiles_dict.get(name, default_profiles_dict[default_profile_name])(
        provider, processor, accelerator
    )

    if not PROFILES_CONFIG_PATH.exists():
        print(
            Panel(
                f"[yellow]No configuration present, we will create a profile '{name}'"
                + f" at: [/]{str(PROFILES_CONFIG_PATH)}\n"
                + "You can add your own profile in this file to further configure goose!"
            )
        )
        write_config({name: default_profile})
        return (name, default_profile)

    profiles = read_config()
    if name in profiles:
        return (name, profiles[name])
    print(Panel(f"[yellow]Your configuration doesn't have a profile named '{name}', adding one now[/yellow]"))
    profiles.update({name: default_profile})
    write_config(profiles)
    return (name, default_profile)


def read_config() -> dict[str, Profile]:
    """Return config from the configuration file and validates its contents"""

    yaml = YAML()
    with PROFILES_CONFIG_PATH.open("r") as f:
        data = yaml.load(f)

    return {name: Profile(**profile) for name, profile in data.items()}


def default_model_configuration() -> tuple[str, str, str]:
    providers = load_plugins(group="exchange.provider")
    for provider, cls in providers.items():
        try:
            cls.from_env()
            break
        except Exception:
            pass
    else:
        provider = RECOMMENDED_DEFAULT_PROVIDER
    processor, accelerator = providers.get(provider).recommended_models()
    return provider, processor, accelerator
