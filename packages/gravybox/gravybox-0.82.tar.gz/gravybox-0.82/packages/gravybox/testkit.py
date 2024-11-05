import json
from typing import List

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from gravybox.betterstack import collect_logger
from gravybox.protocol import Condition

logger = collect_logger()


def validate_all_fields_populated(instance: BaseModel, fields_to_ignore: List[str] = None):
    if fields_to_ignore is None:
        fields_to_ignore = []
    assert instance is not None
    instance_dict = jsonable_encoder(instance)
    logger.info(json.dumps(instance_dict, indent=4, sort_keys=True))
    for key, value in instance_dict.items():
        if key not in fields_to_ignore:
            assert value is not None
            if isinstance(value, str):
                assert len(value) > 0
            elif isinstance(value, bool):
                pass
            elif isinstance(value, int) or isinstance(value, float):
                assert value > 0


def validate_success_response(response, model, fields_to_ignore=None):
    assert response.status_code == 200
    link_response = model.model_validate(response.json())
    result = link_response.content
    validate_all_fields_populated(result, fields_to_ignore)


def validate_data_unavailable_response(response, model):
    assert response.status_code == 200
    response_model = model.model_validate(response.json())
    assert response_model.success is False
    assert response_model.error == Condition.data_unavailable.value
