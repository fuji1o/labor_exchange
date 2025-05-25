def update_model(model_instanse, update_data: dict):
    for field, value in update_data.items():
        if value is not None and hasattr(model_instanse, field):
            setattr(model_instanse, field, value)
