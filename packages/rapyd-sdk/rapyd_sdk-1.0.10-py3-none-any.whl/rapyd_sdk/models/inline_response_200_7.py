from __future__ import annotations
from typing import Union
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.one_of_base_model import OneOfBaseModel
from .status_1 import Status1
from .card_issuing import CardIssuing
from .card_issuing_masked import CardIssuingMasked


class InlineResponse200_7DataGuard(OneOfBaseModel):
    class_list = {"CardIssuing": CardIssuing, "CardIssuingMasked": CardIssuingMasked}


InlineResponse200_7Data = Union[CardIssuing, CardIssuingMasked]


@JsonMap({})
class InlineResponse200_7(BaseModel):
    """InlineResponse200_7

    :param data: data, defaults to None
    :type data: InlineResponse200_7Data, optional
    :param status: status, defaults to None
    :type status: Status1, optional
    """

    def __init__(self, data: InlineResponse200_7Data = None, status: Status1 = None):
        """InlineResponse200_7

        :param data: data, defaults to None
        :type data: InlineResponse200_7Data, optional
        :param status: status, defaults to None
        :type status: Status1, optional
        """
        self.data = InlineResponse200_7DataGuard.return_one_of(data)
        self.status = self._define_object(status, Status1)
