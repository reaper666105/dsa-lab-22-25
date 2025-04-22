# lab_requests_25.py
"""
Лабораторная работа №3. Взаимодействие с веб‑приложением.
Файл объединяет:
  • FastAPI‑сервер с эндпоинтами /number/  (GET, POST, DELETE);
  • клиентскую функцию, выполняющую требования раздела II;
  • CLI‑оболочку:  python lab_requests_25.py server|client.
Автор: Юшков Вадим Дмитриевич — ФБИ‑22 (38.03.05 «Бизнес‑информатика»)
"""
from enum import Enum
import argparse
import random
import typing as t

import requests
from fastapi import FastAPI, Query, Body
from pydantic import BaseModel
import uvicorn


# ----------- общие объекты ---------------------------------------------------
class Operation(str, Enum):
    sum = "sum"
    sub = "sub"
    mul = "mul"
    div = "div"


def _build_response(input_value: float | None = None) -> dict[str, t.Any]:
    """Формирует JSON‑ответ согласно методичке."""
    number = random.uniform(1, 100)
    op = random.choice(list(Operation))
    if input_value is not None:
        number *= input_value
    return {"number": number, "operation": op}


# ----------- API‑СЕРВЕР (раздел I) -------------------------------------------
app = FastAPI(title="Lab‑3 API")


class PostBody(BaseModel):
    jsonParam: float


@app.get("/number/")
def get_number(param: float = Query(..., alias="param")) -> dict[str, t.Any]:
    """GET /number/?param=..."""
    return _build_response(param)


@app.post("/number/")
def post_number(body: PostBody = Body(...)) -> dict[str, t.Any]:
    """POST /number/  JSON: {"jsonParam": ...}"""
    return _build_response(body.jsonParam)


@app.delete("/number/")
def delete_number() -> dict[str, t.Any]:
    """DELETE /number/"""
    return _build_response()


# ----------- КЛИЕНТ (раздел II) ---------------------------------------------
def _apply(a: float, op: str, b: float) -> float:
    """Выполняет арифметическую операцию a (op) b."""
    return {
        "sum": a + b,
        "sub": a - b,
        "mul": a * b,
        "div": a / b if b else float("inf"),
    }[op]


def run_client(base_url: str = "http://127.0.0.1:8000") -> None:
    """Отправляет 3 запроса, собирает выражение и печатает результат."""
    numbers: list[float] = []
    operations: list[str] = []

    # 1. GET
    x = random.randint(1, 10)
    resp = requests.get(f"{base_url}/number/", params={"param": x}, timeout=3).json()
    numbers.append(resp["number"])
    operations.append(resp["operation"])

    # 2. POST
    y = random.randint(1, 10)
    resp = requests.post(
        f"{base_url}/number/",
        json={"jsonParam": y},
        headers={"Content-Type": "application/json"},
        timeout=3,
    ).json()
    numbers.append(resp["number"])
    operations.append(resp["operation"])

    # 3. DELETE
    resp = requests.delete(f"{base_url}/number/", timeout=3).json()
    numbers.append(resp["number"])
    # третью полученную операцию игнорируем, иначе останется «лишняя»
    # но выводим её для отчёта
    extra_op = resp["operation"]

    # ---- расчёт выражения ----------------------------------------------------
    result = numbers[0]
    for idx in range(1, len(numbers)):
        result = _apply(result, operations[idx - 1], numbers[idx])

    expr = (
        f"{numbers[0]:.2f} {operations[0]} {numbers[1]:.2f} "
        f"{operations[1]} {numbers[2]:.2f}"
    )

    print(f"GET → {numbers[0]:.2f}, op={operations[0]}")
    print(f"POST→ {numbers[1]:.2f}, op={operations[1]}")
    print(f"DEL → {numbers[2]:.2f}, op={extra_op} (не используется)")
    print(f"Выражение: {expr}")
    print(f"Результат (int) = {int(result)}")


# ----------- CLI -------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="ЛР‑3: server — запустить API, "
        "client — выполнить пункты раздела II."
    )
    parser.add_argument("mode", choices=["server", "client"])
    args = parser.parse_args()

    if args.mode == "server":
        uvicorn.run("lab_requests_25:app", host="0.0.0.0", port=8000, reload=False)
    else:
        run_client()


if __name__ == "__main__":
    main()