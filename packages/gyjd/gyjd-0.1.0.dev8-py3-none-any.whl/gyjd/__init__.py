import logging
from collections.abc import Callable
from dataclasses import fields, is_dataclass
from functools import partial

from gyjd.config import LoggerConfig
from gyjd.core.cli import CLI
from gyjd.core.config_loader import load_config_file
from gyjd.core.gyjd_callable import GYJDCallable
from gyjd.core.logger import GYJDLogger, get_default_logger
from gyjd.core.simple_injector import inject_dependencies, register_dependency

register_dependency(get_default_logger, cls=GYJDLogger, singleton=True, if_exists="skip")
register_dependency(get_default_logger, cls=logging.Logger, singleton=True, if_exists="skip")
register_dependency(LoggerConfig, singleton=True, if_exists="skip")


class gyjd:
    register_dependency = partial(register_dependency, if_exists="overwrite")

    def __new__(
        cls,
        func: Callable | None = None,
        *,
        return_exception_on_fail: bool = False,
        retry_attempts=-0,
        retry_delay=0,
        retry_max_delay=None,
        retry_backoff=1,
        retry_on_exceptions=(Exception,),
    ) -> GYJDCallable:
        if func is None:
            return gyjd

        return GYJDCallable(
            func=inject_dependencies(func),
            return_exception_on_fail=return_exception_on_fail,
            retry_attempts=retry_attempts,
            retry_delay=retry_delay,
            retry_max_delay=retry_max_delay,
            retry_backoff=retry_backoff,
            retry_on_exceptions=retry_on_exceptions,
        )

    @classmethod
    def command(cls, func: Callable | None = None, *, alias=None):
        if func is None:
            return partial(cls.command, alias=alias)

        alias = alias or getattr(func, "__name__", None)
        CLI.registry(inject_dependencies(func), alias)

        return func

    @classmethod
    def _collect_children_config(cls, dataclass_type: type, subtree: str = ""):
        for field in fields(dataclass_type):
            full_tree = f"{subtree}.{field.name}" if subtree else field.name
            if is_dataclass(field.type):
                yield full_tree, field.type
                yield from cls._collect_children_config(field.type, full_tree)

    @classmethod
    def register_config_file(
        cls,
        *,
        config_type: type,
        filepath: str,
        allow_if_file_not_found: bool = False,
        subtree: str = "",
    ) -> None:
        subtree = subtree.strip(".")

        base_loader = partial(
            load_config_file,
            filepath=filepath,
            allow_if_file_not_found=allow_if_file_not_found,
        )

        register_dependency(
            partial(
                base_loader,
                config_type=config_type,
                subtree=subtree.split("."),
            ),
            cls=config_type,
            singleton=True,
        )

        for child_subtree, child_type in cls._collect_children_config(config_type):
            register_dependency(
                partial(
                    base_loader,
                    config_type=child_type,
                    subtree=child_subtree.split("."),
                ),
                cls=child_type,
                singleton=True,
                if_exists="overwrite",
            )

    @classmethod
    def run(cls):
        CLI.run()


__all__ = ["gyjd"]
