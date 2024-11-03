import torch
from torch.utils.data import DataLoader


class PostgresDataLoader(DataLoader):
    def __init__(self, dataset, batch_size, dtype: torch.dtype = torch.float32):
        super().__init__(dataset, batch_size=batch_size)
        self.dtype = dtype

    def __iter__(self):
        for batch in super().__iter__():
            yield torch.stack(batch).type(self.dtype).T
