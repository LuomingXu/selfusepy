import sys

sys.path.append('..')
sys.path.append('../selfusepy')
sys.path.append('../test')

from typing import List
from dataclasses import dataclass
import selfusepy
from selfusepy.jsonparse import BaseJsonObject, DeserializeConfig, ClassField
from selfusepy.utils import override_str
from datetime import datetime


@override_str
@dataclass(init=False)
class One(BaseJsonObject):
    x: str
    two: 'One.Two'

    @override_str
    @dataclass(init=False)
    class Two(BaseJsonObject):
        y: str
        three: 'One.Two.Three'

        @override_str
        @dataclass(init=False)
        class Three(BaseJsonObject):
            z: str


@override_str
@dataclass(init=False)
class One1(BaseJsonObject):
    x: str
    two: 'List[One1.Two]'

    @override_str
    @dataclass(init=False)
    class Two(BaseJsonObject):
        y: str


@override_str
@DeserializeConfig({'x--': ClassField(varname='x')})
@dataclass(init=False)
class One2(BaseJsonObject):
    x: str
    two: 'One2.Two'

    @override_str
    @DeserializeConfig({'y--': ClassField(varname='y')})
    @dataclass(init=False)
    class Two(BaseJsonObject):
        y: str
        three: "One2.Two.Three"

        @override_str
        @dataclass(init=False)
        @DeserializeConfig({'z--': ClassField(varname='z')})
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


def json_test_0() -> bool:
    with open('./jsontest/eg8.json', 'r', encoding='utf-8') as f:
        obj: WebHookData = selfusepy.parse_json(f.read(), WebHookData())
        print(obj)
        return isinstance(obj, WebHookData)


def json_test_1() -> bool:
    """
    json test
    e.g. 1
    """
    print('多级复杂json转化测试: ')
    f = open('./jsontest/eg1.json', 'r')
    obj: One = selfusepy.parse_json(f.read(), One())
    print(obj)
    f.close()
    return isinstance(obj, One)


def json_test_2() -> bool:
    """
    json test with jsonarray
    e.g. 2
    """
    print('包含json array的转化测试: ')
    f = open('./jsontest/eg2.json', 'r')
    obj: One1 = selfusepy.parse_json(f.read(), One1())
    print(obj)
    f.close()
    return isinstance(obj, One1)


def json_test_3() -> tuple[bool, bool]:
    """
    json test, parse jsonArrary
    e.g. 3
    """
    print('json array测试: ')
    f = open('./jsontest/eg3.json', 'r')
    l: List[One] = selfusepy.parse_json_array(f.read(), One())
    for i, item in enumerate(l):
        print('i: %s, value: %s' % (i, item))
    f.close()
    return isinstance(l, list), isinstance(l.pop(0), One)


def json_test_4() -> bool:
    """
    json test, json-key is different from variable name
    e.g. 3
    """
    print('json不同变量名测试: ')
    f = open('./jsontest/eg4.json', 'r')
    obj: One2 = selfusepy.parse_json(f.read(), One2())
    print(obj)
    f.close()
    return isinstance(obj, One2)


def json_test_5() -> bool:
    print('多级list测试')
    f = open('./jsontest/eg5.json', 'r')
    obj: One3 = selfusepy.parse_json(f.read(), One3())
    print(obj)
    f.close()
    return isinstance(obj, One3)


def json_test_6() -> bool:
    print('线程安全测试')
    f = open('./jsontest/eg1.json', 'r')
    s1 = f.read()
    f.close()
    f = open('./jsontest/eg2.json', 'r')
    s2 = f.read()
    f.close()
    f = open('./jsontest/eg3.json', 'r')
    s3 = f.read()
    f.close()
    from multiprocessing import Pool
    from multiprocessing.pool import ApplyResult
    p = Pool(processes=3)
    res: List[ApplyResult] = list()
    res.append(p.apply_async(func=selfusepy.parse_json, args=(s1, One(),)))
    res.append(p.apply_async(func=selfusepy.parse_json, args=(s2, One1(),)))
    res.append(p.apply_async(func=selfusepy.parse_json_array, args=(s3, One(),)))
    p.close()
    p.join()
    for item in res:
        value = item.get()
        if isinstance(value, list):
            print('list: ')
            for l in value:
                print(l)
        else:
            print(value)

    return True


def json_test_7() -> bool:
    print("List[int]测试")
    f = open('./jsontest/eg6.json', 'r')
    s = f.read()
    f.close()
    obj: One4 = selfusepy.parse_json(s, One4())
    print(obj)
    return isinstance(obj, One4)


def handle(x):
    x = x[0:-1]  # 去除后缀的"Z"
    return datetime.fromisoformat(x)


@override_str
@dataclass(init=False)
class Obj(BaseJsonObject):
    id: 'Obj.Id'
    client: str
    status: 'Obj.Status'

    @DeserializeConfig({"$oid": ClassField("oid")})
    @dataclass(init=False)
    class Id(BaseJsonObject):
        oid: str

    @dataclass(init=False)
    class Status(BaseJsonObject):
        capture_time: 'Obj.Status.Capture_time'
        cpu_number: int
        memory_cap: int
        load: int
        cpu_usage: int
        memory_usage: int

        @DeserializeConfig({"$date": ClassField("date", func=handle)})
        @dataclass(init=False)
        class Capture_time(BaseJsonObject):
            date: datetime


def json_test_8() -> bool:
    print("多级; 不同变量名; variable handler")
    with open("./jsontest/eg7.json", "r") as f:
        s = f.read()
    obj: Obj = selfusepy.parse_json(s, Obj())
    print(obj)
    return isinstance(obj, Obj)

@override_str
@dataclass(init=False)
class One9(BaseJsonObject):
    x: str
    y: str

def json_test_9() -> bool:
    print("obj缺失变量")
    with open("./jsontest/eg9.json", "r") as f:
        s = f.read()
    obj: One9 = selfusepy.parse_json(s, One9())
    print(obj)
    return isinstance(obj, One9)

@override_str
@dataclass(init=False)
class One10(BaseJsonObject):
    x: str
    y: str
    z: str

def json_test_10() -> bool:
    print("json缺失变量")
    with open("./jsontest/eg10.json", "r") as f:
        s = f.read()
    obj: One10 = selfusepy.parse_json(s, One10())
    print(obj)
    return isinstance(obj, One10)