import dataclasses
from typing import Any

from typing_extensions import Annotated

from litestar import Litestar, get
from litestar.openapi.spec.example import Example
from litestar.openapi.spec.external_documentation import ExternalDocumentation
from litestar.params import PathParameter


@dataclasses.dataclass
class Version:
    id: int
    specs: dict[str, Any]

    def __post_init__(self) -> None:
        if not 1 <= self.id <= 10:
            raise ValueError()


VERSIONS = {1: Version(id=1, specs={"some": "value"})}


@get(path="/versions/{version:int}", sync_to_thread=False)
def get_product_version(
    version: Annotated[
        int,
        PathParameter(
            ge=1,
            le=10,
            title="Available Product Versions",
            description="Get a specific version spec from the available specs",
            examples=[Example(value=1)],
            external_docs=ExternalDocumentation(
                url="https://mywebsite.com/documentation/product#versions",  # type: ignore[arg-type]
            ),
        ),
    ],
) -> Version:
    return VERSIONS[version]


app = Litestar(route_handlers=[get_product_version])
