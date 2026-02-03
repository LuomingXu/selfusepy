from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

import selfusepy
from selfusepy.jsonparse import BaseJsonObject, ClassField, DeserializeConfig
from selfusepy.utils import override_str

"""
目录结构：
project or package
├── test/
│   └── data/
│       └── userinfo.csv
│   └── test_pytest_datadir/
│       └── userinfo_local.csv
└── test_pytest_datadir.py
shared_datadir: => /test/data 目录下
datadir: => /test/pyfile_name.py
"""


@override_str
@dataclass(init=False)
class One(BaseJsonObject):
    x: str
    two: "One.Two"

    @override_str
    @dataclass(init=False)
    class Two(BaseJsonObject):
        y: str
        three: "One.Two.Three"

        @override_str
        @dataclass(init=False)
        class Three(BaseJsonObject):
            z: str


@override_str
@dataclass(init=False)
class One1(BaseJsonObject):
    x: str
    two: "List[One1.Two]"

    @override_str
    @dataclass(init=False)
    class Two(BaseJsonObject):
        y: str


@override_str
@DeserializeConfig({"x--": ClassField(varname="x")})
@dataclass(init=False)
class One2(BaseJsonObject):
    x: str
    two: "One2.Two"

    @override_str
    @DeserializeConfig({"y--": ClassField(varname="y")})
    @dataclass(init=False)
    class Two(BaseJsonObject):
        y: str
        three: "One2.Two.Three"

        @override_str
        @dataclass(init=False)
        @DeserializeConfig({"z--": ClassField(varname="z")})
        class Three(BaseJsonObject):
            z: str


@override_str
@dataclass(init=False)
class One3(BaseJsonObject):
    x: str
    two: "List[One3.Two]"

    @override_str
    @dataclass(init=False)
    class Two(BaseJsonObject):
        y: str
        three: "List[One3.Two.Three]"

        @override_str
        @dataclass(init=False)
        class Three(BaseJsonObject):
            z: str


@override_str
@dataclass(init=False)
class One4(BaseJsonObject):
    x: str
    y: List[int]


@override_str
@dataclass(init=False)
class WebHookData(BaseJsonObject):
    @override_str
    @dataclass(init=False)
    class EventData(BaseJsonObject):
        SessionId: str
        RelativePath: str
        FileSize: int
        Duration: float
        FileOpenTime: str
        FileCloseTime: str
        RoomId: int
        ShortId: int
        Name: str
        Title: str
        AreaNameParent: str
        AreaNameChild: str
        Recording: bool
        Streaming: bool
        DanmakuConnected: bool

    EventType: str
    EventTimestamp: str
    EventId: str
    EventData: "WebHookData.EventData"


def test_json(shared_datadir: Path):
    print()
    import os

    print(os.getcwd())
    print(Path.cwd())
    print(f"当前脚本位置: {Path(__file__).resolve()}")
    p = shared_datadir / "eg8.json"
    with open(p, "r", encoding="utf-8") as f:
        obj: WebHookData = selfusepy.parse_json(f.read(), WebHookData())
        print(obj)
    assert isinstance(obj, WebHookData)


def test_多级复杂json转化测试(shared_datadir: Path):
    p = shared_datadir / "eg1.json"
    with open(p, "r", encoding="utf-8") as f:
        obj: One = selfusepy.parse_json(f.read(), One())
        print(obj)
    assert isinstance(obj, One)


def test_包含json_array的转化测试(shared_datadir: Path):
    p = shared_datadir / "eg2.json"
    with open(p, "r", encoding="utf-8") as f:
        obj: One1 = selfusepy.parse_json(f.read(), One1())
        print(obj)
    assert isinstance(obj, One1)


def test_json_array测试(shared_datadir: Path):
    print("json array测试: ")
    p = shared_datadir / "eg3.json"
    with open(p, "r", encoding="utf-8") as f:
        l: List[One] = selfusepy.parse_json_array(f.read(), One())
        for i, item in enumerate(l):
            print("i: %s, value: %s" % (i, item))
    assert isinstance(l, list)
    assert isinstance(l.pop(0), One)


def test_json不同变量名测试(shared_datadir: Path):
    """
    json test, json-key is different from variable name
    e.g. 3
    """
    p = shared_datadir / "eg4.json"
    with open(p, "r", encoding="utf-8") as f:
        obj: One2 = selfusepy.parse_json(f.read(), One2())
        print(obj)
    assert isinstance(obj, One2)


def test_多级list测试(shared_datadir: Path):
    p = shared_datadir / "eg5.json"
    with open(p, "r", encoding="utf-8") as f:
        obj: One3 = selfusepy.parse_json(f.read(), One3())
        print(obj)
    assert isinstance(obj, One3)


def test_线程安全测试(shared_datadir: Path):
    p1 = shared_datadir / "eg1.json"
    p2 = shared_datadir / "eg2.json"
    p3 = shared_datadir / "eg3.json"
    with open(p1, "r", encoding="utf-8") as f:
        s1 = f.read()
    with open(p2, "r", encoding="utf-8") as f:
        s2 = f.read()
    with open(p3, "r", encoding="utf-8") as f:
        s3 = f.read()
    from multiprocessing import Pool
    from multiprocessing.pool import ApplyResult

    p = Pool(processes=3)
    res: List[ApplyResult] = list()
    res.append(
        p.apply_async(
            func=selfusepy.parse_json,
            args=(
                s1,
                One(),
            ),
        )
    )
    res.append(
        p.apply_async(
            func=selfusepy.parse_json,
            args=(
                s2,
                One1(),
            ),
        )
    )
    res.append(
        p.apply_async(
            func=selfusepy.parse_json_array,
            args=(
                s3,
                One(),
            ),
        )
    )
    p.close()
    p.join()
    for item in res:
        value = item.get()
        if isinstance(value, list):
            print("list: ")
            for l in value:
                print(l)
        else:
            print(value)

    assert True


def test_list_int测试(shared_datadir: Path):
    print("List[int]测试")
    p = shared_datadir / "eg6.json"
    with open(p, "r", encoding="utf-8") as f:
        s = f.read()
    obj: One4 = selfusepy.parse_json(s, One4())
    print(obj)
    assert isinstance(obj, One4)


def handle(x):
    x = x[0:-1]  # 去除后缀的"Z"
    return datetime.fromisoformat(x)


@override_str
@dataclass(init=False)
class Obj(BaseJsonObject):
    id: "Obj.Id"
    client: str
    status: "Obj.Status"

    @DeserializeConfig({"$oid": ClassField("oid")})
    @dataclass(init=False)
    class Id(BaseJsonObject):
        oid: str

    @dataclass(init=False)
    class Status(BaseJsonObject):
        capture_time: "Obj.Status.Capture_time"
        cpu_number: int
        memory_cap: int
        load: int
        cpu_usage: int
        memory_usage: int

        @DeserializeConfig({"$date": ClassField("date", func=handle)})
        @dataclass(init=False)
        class Capture_time(BaseJsonObject):
            date: datetime


def test_多级_不同变量名_variable_handler(shared_datadir: Path):
    p = shared_datadir / "eg7.json"
    with open(p, "r", encoding="utf-8") as f:
        s = f.read()
    obj: Obj = selfusepy.parse_json(s, Obj())
    print(obj)
    assert isinstance(obj, Obj)


@override_str
@dataclass(init=False)
class One9(BaseJsonObject):
    x: str
    y: str


def test_obj缺失变量(shared_datadir: Path):
    p = shared_datadir / "eg9.json"
    with open(p, "r", encoding="utf-8") as f:
        s = f.read()
    obj: One9 = selfusepy.parse_json(s, One9())
    print(obj)
    assert isinstance(obj, One9)


@override_str
@dataclass(init=False)
class One10(BaseJsonObject):
    x: str
    y: str
    z: str


def test_json缺失变量(shared_datadir: Path):
    print("json缺失变量")
    p = shared_datadir / "eg10.json"
    with open(p, "r", encoding="utf-8") as f:
        s = f.read()
    obj: One10 = selfusepy.parse_json(s, One10())
    print(obj)
    assert isinstance(obj, One10)
