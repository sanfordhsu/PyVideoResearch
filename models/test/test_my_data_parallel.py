import unittest
from models.utils import MyDataParallel
import torch


class TestMyDataParallel(unittest.TestCase):
    def test_scatter_tensors(self):
        if torch.cuda.is_available():
            data = torch.Tensor(10, 2, 3)
            my_data_parallel = MyDataParallel(torch.nn.Module())
            out = my_data_parallel.scatter(data, {}, [0, 1])
            self.assertSequenceEqual(out[0].shape, (5, 2, 3))