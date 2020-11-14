from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class StdModel:
    name: str
    code: str
    pub_time: date
    act_time: date
    status: str  # 现行，即将实施，废止，有更新版

    def dict(self):
        return super(StdModel, self).__dict__


@dataclass
class NatureStdModel(StdModel):
    url: str


@dataclass
class NatureStdSearchModel:
    total_size: int
    data: List[NatureStdModel]

    def dict(self):
        return {
            "total_size": self.total_size,
            "data": [row.__dict__ for row in self.data]
        }


@dataclass
class GBModel(StdModel):
    caibiao_status: str
    hcno: str
    std_type: str
    url: str


@dataclass
class GBSearchModel:
    total_size: int
    data: List[GBModel]

    def dict(self):
        return {
            "total_size": self.total_size,
            "data": [row.__dict__ for row in self.data]
        }
