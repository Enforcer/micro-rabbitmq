from fastapi import FastAPI, Response
from pydantic import BaseModel

from shipping import tracing

app = FastAPI()


@app.on_event("startup")
def setup() -> None:
    app.state.tracer = tracing.setup("shipping", app)


_labels = {}


ids = iter(range(1, 10_001))


class ProductDto(BaseModel):
    weight: int
    width: int
    height: int
    length: int


@app.post("/labels")
def labels(dto: ProductDto) -> dict:
    label_id = next(ids)
    label = {
        "id": label_id,
        "weight": dto.weight,
        "width": dto.width,
        "height": dto.height,
        "length": dto.length,
        "price": _price(dto.weight, dto.width, dto.height, dto.length),
    }
    _labels[label_id] = label
    return label


@app.get("/labels/{id}")
def labels(id: int) -> Response:
    try:
        return _labels[id]
    except KeyError:
        return Response(status_code=404)


def _price(weight: int, width: int, height: int, length: int) -> float:
    volumetric_weight = int(width * height * length / 5000)
    weight_to_take = max(weight, volumetric_weight)
    if weight_to_take < 1:
        return 9.99
    elif weight_to_take < 3:
        return 12.99
    elif weight_to_take < 5:
        return 15.99
    elif weight_to_take < 10:
        return 18.99
    elif weight_to_take < 20:
        return 32.99
    else:
        return 49.99
