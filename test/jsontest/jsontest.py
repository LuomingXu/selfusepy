from typing import List

from selfusepy.jsonparse import BaseJsonObject
from selfusepy.utils import override_str


@override_str
class One(BaseJsonObject):

  def __init__(self):
    self.x: str = ''
    self.two: One.Two = One.Two()

  @override_str
  class Two(BaseJsonObject):
    def __init__(self):
      self.y: str = ''
      self.three: One.Two.Three = One.Two.Three()

    @override_str
    class Three(BaseJsonObject):
      def __init__(self):
        self.z: str = ''


@override_str
class One1(BaseJsonObject):

  def __init__(self):
    self.x: str = ''
    self.two: List[One1.Two] = [One1.Two()]

  @override_str
  class Two(BaseJsonObject):
    def __init__(self):
      self.y: str = ''
