from fastapi_camelcase import CamelModel
from sqlalchemy import Column


class FilterModel(CamelModel):
    def get_filters(self, *args, **kwargs):
        filters_dict = self.dict(*args, **kwargs)
        return (Column(k) == v for k, v in filters_dict.items())
