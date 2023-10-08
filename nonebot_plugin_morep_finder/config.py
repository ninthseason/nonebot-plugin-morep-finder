from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    kook_auth_key: str = None
    morep_config: list[dict] = []
