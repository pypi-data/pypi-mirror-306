# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from types import ModuleType
import importlib

def public_api(module: ModuleType = None, symbol: str = None):
    def export_impl(obj):
        nonlocal module, symbol

        module = module or importlib.import_module(__package__)
        symbol = symbol or obj.__name__

        if not hasattr(module, "__all__"):
            module.__all__ = []

        module.__all__.append(symbol)
        setattr(module, symbol, obj)

        return obj

    return export_impl
