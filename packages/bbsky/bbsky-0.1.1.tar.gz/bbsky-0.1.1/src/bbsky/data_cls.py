import pendulum
import yarl
from cattrs import Converter

URL = yarl.URL
TZ = pendulum.UTC
DateTime = pendulum.DateTime
Duration = pendulum.Duration

converter = Converter()
structure = converter.structure
unstructure = converter.unstructure


@converter.register_structure_hook
def url_from_str(instance: str, cl: URL) -> URL:
    return URL(instance)


@converter.register_unstructure_hook
def url_to_str(instance: URL) -> str:
    return str(instance)


@converter.register_structure_hook
def datetime_from_str(instance: str, cl: DateTime) -> DateTime:
    return pendulum.parse(instance)  # type: ignore


@converter.register_unstructure_hook
def datetime_to_str(instance: DateTime) -> str:
    return instance.to_iso8601_string()
