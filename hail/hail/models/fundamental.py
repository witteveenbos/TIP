from hail.models.matrix import Matrix


Value = float | int


class AttrDict(dict):
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(
                f"Requested data {item} not found in {self}. This data should be present either in inputs, gqueries or ui."
            )


class FilterList(list):

    def __init__(self, *args, etm_key: str = None, **kwargs):
        self.etm_key = etm_key
        super().__init__(*args, **kwargs)

    def __getattr__(self, item):

        if item == "etm_key":
            return self.etm_key

        try:
            return Matrix([(getattr(x, item)) for x in self])
        except AttributeError:
            raise AttributeError(
                f"Requested field {item} not found in {self}. Check whether you've used the correct field for this datasource."
            )

    def __hash__(self):
        return hash(self.etm_key)
