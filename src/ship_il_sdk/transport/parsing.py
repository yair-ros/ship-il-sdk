from pydantic import TypeAdapter


def parse_model(model, data):
    if hasattr(model, "model_validate"):
        return model.model_validate(data)
    return TypeAdapter(model).validate_python(data)
