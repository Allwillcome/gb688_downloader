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
    url: str

    def dict(self):
        return super(StdModel, self).__dict__


@dataclass
class NatureStdModel(StdModel):
    pass


@dataclass
class NatureStdSearchModel:
    total_size: int
    data: List[NatureStdModel]

    def dict(self):
        return {
            "total_size": self.total_size,
            "data": [row.__dict__ for row in self.data],
        }


@dataclass
class GBModel(StdModel):
    caibiao_status: str
    hcno: str
    std_type: str


@dataclass
class GBSearchModel:
    total_size: int
    data: List[GBModel]

    def dict(self):
        return {
            "total_size": self.total_size,
            "data": [row.__dict__ for row in self.data],
        }


@dataclass
class HDBModel(StdModel):
    pk: str
    charge_department: str
    industry: str
    std_type: str


@dataclass
class HDBSearchModel:
    total_size: int
    data: List[HDBModel]

    def dict(self):
        return {
            "total_size": self.total_size,
            "data": [row.__dict__ for row in self.data],
        }
