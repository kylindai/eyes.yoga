
from typing import Any, Dict, List, Tuple, Union

from comm.utils import AttrDict

def build_result(success: bool = False,
                 error_code: int = -100,
                 error_msg: str = 'ERROR',
                 data: Union[Dict, List[Dict]] = None) -> AttrDict:
    """
    build ajax result
      - success
      - error_code
      - error_msg
      - data
    """
    result = AttrDict()
    result['success'] = success
    result['error_code'] = error_code
    result['error_msg'] = error_msg
    result['data'] = data
    return result


def result_success(result: AttrDict,
                   data: Union[Dict, List[Dict]] = None) -> AttrDict:
    result['success'] = True
    result['error_code'] = 0
    result['error_msg'] = 'SUCCESS'
    if data is not None:
        result['data'] = data


def result_failure(result: AttrDict,
                   error_code: int = -100,
                   error_msg: str = 'ERROR',
                   data: Union[Dict, List[Dict]] = None) -> AttrDict:
    result['success'] = False
    result['error_code'] = error_code
    result['error_msg'] = error_msg
    if data is not None:
        result['data'] = data
