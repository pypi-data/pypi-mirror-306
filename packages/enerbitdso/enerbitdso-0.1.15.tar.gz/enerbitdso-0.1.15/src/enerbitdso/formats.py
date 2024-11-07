import csv
import io

import orjson
import pydantic


def as_json(records: list[pydantic.BaseModel]) -> io.StringIO:
    content = orjson.dumps([r.model_dump() for r in records])
    res = io.BytesIO(content)
    wrapper = io.TextIOWrapper(res, encoding="utf-8")
    return wrapper


def as_csv(records: list[pydantic.BaseModel], header: bool) -> io.StringIO:
    res = io.StringIO(newline="")
    fields = records[0].model_fields.keys()
    content_lines = [r.model_dump() for r in records]
    writer = csv.DictWriter(res, fields, lineterminator="\n")
    if header:
        writer.writeheader()
    for i in content_lines:
        writer.writerow(i)
    return res


def as_jsonl(records: list[pydantic.BaseModel]) -> io.StringIO:
    res = io.StringIO()
    for i in records:
        res.write(i.model_dump_json())
        res.write("\n")
    return res
