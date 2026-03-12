from typing import Type


def parse_model(model: Type, data):
    if hasattr(model, "model_validate"):
        return model.model_validate(data)

    return model.parse_obj(data)
