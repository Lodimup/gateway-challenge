from pydantic import BaseModel, model_validator


class ITaskResponse(BaseModel):
    """
    Generic task response
    """

    data: dict | None
    error: dict | None

    @model_validator(mode="before")
    def check_exclusive(self):
        print(self)
        if self["data"] is None and self["error"] is None:
            raise ValueError("data and error cannot be both None")
        return self
