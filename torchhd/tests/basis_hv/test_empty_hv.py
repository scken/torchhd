import pytest
import torch

import torchhd
from torchhd import functional

from ..utils import (
    torch_dtypes,
    supported_dtype,
    vsa_tensors,
)

seed = 2147483644


class Testempty:
    @pytest.mark.parametrize("n", [1, 3, 55])
    @pytest.mark.parametrize("d", [84, 10])
    @pytest.mark.parametrize("vsa", vsa_tensors)
    def test_shape(self, n, d, vsa):
        hv = functional.empty(n, d, vsa)

        assert hv.dim() == 2
        assert hv.size(0) == n
        assert hv.size(1) == d

    @pytest.mark.parametrize("dtype", torch_dtypes)
    @pytest.mark.parametrize("vsa", vsa_tensors)
    def test_value(self, dtype, vsa):
        if not supported_dtype(dtype, vsa):
            with pytest.raises(ValueError):
                functional.empty(3, 26, vsa, dtype=dtype)

            return

        hv = functional.empty(8, 26, vsa, dtype=dtype)
        assert hv.requires_grad == False
        assert hv.dim() == 2
        assert hv.size(0) == 8
        assert hv.size(1) == 26

        if vsa == "BSC":
            assert torch.all((hv == False) | (hv == True)).item()

        else:
            hv = functional.empty(8, 26, vsa, dtype=dtype)
            assert torch.all(hv == 0.0).item()

    @pytest.mark.parametrize("dtype", torch_dtypes)
    @pytest.mark.parametrize("vsa", vsa_tensors)
    def test_device(self, dtype, vsa):
        if not supported_dtype(dtype, vsa):
            return

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        hv = functional.empty(3, 52, vsa, device=device, dtype=dtype)
        assert hv.device == device

    def test_uses_default_dtype(self):
        hv = functional.empty(3, 52, "BSC")
        assert hv.dtype == torch.bool

        torch.set_default_dtype(torch.float32)
        hv = functional.empty(3, 52, "MAP")
        assert hv.dtype == torch.float32
        hv = functional.empty(3, 52, "HRR")
        assert hv.dtype == torch.float32

        torch.set_default_dtype(torch.float64)
        hv = functional.empty(3, 52, "MAP")
        assert hv.dtype == torch.float64
        hv = functional.empty(3, 52, "HRR")
        assert hv.dtype == torch.float64

        hv = functional.empty(3, 52, "FHRR")
        assert hv.dtype == torch.complex64

    def test_requires_grad(self):
        hv = functional.empty(3, 52, "MAP", requires_grad=True)
        assert hv.requires_grad == True

        hv = functional.empty(3, 52, "HRR", requires_grad=True)
        assert hv.requires_grad == True

        hv = functional.empty(3, 52, "FHRR", requires_grad=True)
        assert hv.requires_grad == True
