# SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
#
# SPDX-License-Identifier: MPL-2.0

import warnings

import numpy as np
import pytest

from power_grid_model._utils import is_columnar
from power_grid_model.core.data_handling import create_output_data
from power_grid_model.core.dataset_definitions import ComponentType as CT, DatasetType as DT
from power_grid_model.core.power_grid_core import VoidPtr
from power_grid_model.core.power_grid_dataset import CMutableDataset
from power_grid_model.core.power_grid_meta import initialize_array


@pytest.mark.parametrize(
    ("output_component_types", "is_batch", "expected"),
    [
        (
            None,
            False,
            {
                CT.node: initialize_array(DT.sym_output, CT.node, 4),
                CT.sym_load: initialize_array(DT.sym_output, CT.sym_load, 3),
                CT.source: initialize_array(DT.sym_output, CT.source, 1),
            },
        ),
        (
            [CT.node, CT.sym_load],
            False,
            {
                CT.node: initialize_array(DT.sym_output, CT.node, 4),
                CT.sym_load: initialize_array(DT.sym_output, CT.sym_load, 3),
            },
        ),
        (
            {CT.node, CT.sym_load},
            False,
            {
                CT.node: initialize_array(DT.sym_output, CT.node, 4),
                CT.sym_load: initialize_array(DT.sym_output, CT.sym_load, 3),
            },
        ),
        pytest.param(
            {CT.node: [], CT.sym_load: []}, True, {CT.node: dict(), CT.sym_load: dict()}, marks=pytest.mark.xfail
        ),
        pytest.param({CT.node: [], CT.sym_load: ["p"]}, True, {}, marks=pytest.mark.xfail),
        pytest.param({CT.node: ["u"], CT.sym_load: ["p"]}, True, {}, marks=pytest.mark.xfail),
        pytest.param({CT.node: None, CT.sym_load: ["p"]}, True, {}, marks=pytest.mark.xfail),
    ],
)
def test_create_output_data(output_component_types, is_batch, expected):
    # TODO use is_batch and shorten parameterization after columnar data implementation
    all_component_count = {CT.node: 4, CT.sym_load: 3, CT.source: 1}
    batch_size = 15 if is_batch else 1
    actual = create_output_data(
        output_component_types=output_component_types,
        output_type=DT.sym_output,
        all_component_count=all_component_count,
        is_batch=is_batch,
        batch_size=batch_size,
    )

    assert actual.keys() == expected.keys()
    for comp in expected:
        if not is_columnar(expected[comp]):
            assert actual[comp].dtype == expected[comp].dtype
        elif expected[comp] == dict():
            # Empty atrtibutes columnar
            assert actual[comp] == expected[comp]
        else:
            assert actual[comp].keys() == expected[comp].keys()
            assert all(actual[comp][attr].dtype == expected[comp][attr].dtype for attr in expected[comp])


def test_dtype_compatibility_check_normal():
    nodes = initialize_array(DT.sym_output, CT.node, (1, 2))
    nodes_ptr = nodes.ctypes.data_as(VoidPtr)

    data = {CT.node: nodes}
    mutable_dataset = CMutableDataset(data, DT.sym_output)
    buffer_views = mutable_dataset.get_buffer_views()

    assert buffer_views[0].data.value == nodes_ptr.value


def test_dtype_compatibility_check_compatible():
    nodes = initialize_array(DT.sym_output, CT.node, 4)
    nodes = nodes[::2]
    nodes_ptr = nodes.ctypes.data_as(VoidPtr)

    data = {CT.node: nodes}
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        mutable_dataset = CMutableDataset(data, DT.sym_output)
        buffer_views = mutable_dataset.get_buffer_views()

    assert buffer_views[0].data.value != nodes_ptr.value


def test_dtype_compatibility_check__error():
    nodes = initialize_array(DT.sym_output, CT.node, (1, 2))
    data = {CT.node: nodes.astype(nodes.dtype.newbyteorder("S"))}
    with pytest.warns(DeprecationWarning):
        CMutableDataset(data, DT.sym_output)
