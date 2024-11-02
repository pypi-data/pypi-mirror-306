from typing import List


class TensorMock(List):
    @property
    def shape(self):
        def get_shape(lst):
            if isinstance(lst, list):
                return [len(lst)] + get_shape(lst[0])
            return []

        return tuple(get_shape(self))

    @classmethod
    def ones(cls, shape):
        def create_ones(shape):
            if len(shape) == 1:
                return [1] * shape[0]
            return [create_ones(shape[1:]) for _ in range(shape[0])]

        return cls(create_ones(shape))
