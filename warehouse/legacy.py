from dataclasses import dataclass
from random import randint, random, seed
from time import sleep


def reserve_stock(product_id: int) -> None:
    sleep_for = random()
    sleep(sleep_for)


@dataclass
class Sizes:
    weight: int
    width: int
    height: int
    length: int


def get_product_sizes(product_id: int) -> Sizes:
    seed(product_id)
    return Sizes(
        weight=randint(1, 10),
        width=randint(1, 30),
        height=randint(1, 30),
        length=randint(1, 30),
    )
