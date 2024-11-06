import pytest
import ebm2onnx.graph as graph
import ebm2onnx.operators as ops

import numpy as np
import onnx

from .utils import assert_model_result


def test_add():
    g = graph.create_graph()

    a = graph.create_initializer(g, "a", onnx.TensorProto.FLOAT, [1], [0.3])
    i = graph.create_input(g, "i", onnx.TensorProto.FLOAT, [None])

    l = ops.add()(graph.merge(i, a))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None])

    assert_model_result(l,
        input={
            'i': [0.1, 1.2, 11, 4.2],
        },
        expected_result=[[0.4, 1.5, 11.3, 4.5]]
    )


@pytest.mark.parametrize(
    "from_type,to_type,input,output",
    [
        pytest.param(
            onnx.TensorProto.INT64,
            onnx.TensorProto.FLOAT,
            {'i': [[1], [2], [11], [4]]},
            [[[1.0], [2.0], [11.0], [4.0]]],
            id='int64_to_float'
        ),
        pytest.param(
            onnx.TensorProto.INT64,
            onnx.TensorProto.STRING,
            {'i': [[1], [2], [11], [4]]},
            [[["1"], ["2"], ["11"], ["4"]]],
            id='int64_to_string'
        ),
        pytest.param(
            onnx.TensorProto.BOOL,
            onnx.TensorProto.UINT8,
            {'i': [[False], [True]]},
            [[[0], [1]]],
            id='bool_to_uint8'
        ),
        pytest.param(
            onnx.TensorProto.BOOL,
            onnx.TensorProto.STRING,
            {'i': [[False], [True]]},
            [[["0"], ["1"]]],
            id='bool_to_string'
        ),
    ]
)
def test_cast(from_type, to_type, input, output):
    g = graph.create_graph()
    i = graph.create_input(g, "i", from_type, [None, 1])
    l = ops.cast(to_type)(i)
    l = graph.add_output(l, l.transients[0].name, to_type, [None, 1])

    assert_model_result(
        l,
        input=input,
        expected_result=output,
        exact_match=to_type in [onnx.TensorProto.INT64, onnx.TensorProto.STRING]
    )


def test_flatten():
    g = graph.create_graph()

    i = graph.create_input(g, "i", onnx.TensorProto.FLOAT, [None])

    l = ops.flatten()(i)
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None, 1])

    assert_model_result(l,
        input={
            'i': [0.1, 0.2, 0.3, 0.4]
        },
        expected_result=[[
            [0.1],
            [0.2],
            [0.3],
            [0.4]
        ]]
    )


def test_greater_or_equal():
    g = graph.create_graph()

    a = graph.create_initializer(g, "a", onnx.TensorProto.FLOAT, [4], [0.1, 2.3, 3.55, 9.6])
    b = graph.create_input(g, "b", onnx.TensorProto.FLOAT, [None, 1])

    l = ops.greater_or_equal()(graph.merge(b, a))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.BOOL, [None, 4])

    assert_model_result(l,
        input={
            'b': [
                [0.5],
                [1.2],
                [11],
                [4.2],
                [np.nan],
            ]
        },
        expected_result=[[
            [True, False, False, False],
            [True, False, False, False],
            [True, True, True, True],
            [True, True, True, False],
            [False, False, False, False],
        ]]
    )


def test_less():
    g = graph.create_graph()

    a = graph.create_initializer(g, "a", onnx.TensorProto.FLOAT, [4], [1.1, 2.3, 3.5, 9.6])
    b = graph.create_input(g, "b", onnx.TensorProto.FLOAT, [None, 1])

    l = ops.less()(graph.merge(a, b))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.BOOL, [None, 4])

    assert_model_result(l, 
        input={
            'b': [
                [0.1],
                [1.2],
                [11],
                [4.2],
                [np.nan],
            ]
        },
        expected_result=[[
            [False, False, False, False],
            [True, False, False, False],
            [True, True, True, True],
            [True, True, True, False],
            [False, False, False, False],
        ]]
    )


def test_mul():
    g = graph.create_graph()

    a = graph.create_initializer(g, "a", onnx.TensorProto.FLOAT, [3], [1.0, 2.0, 3.0])
    b = graph.create_input(g, "b", onnx.TensorProto.FLOAT, [None, 3])

    l = ops.mul()(graph.merge(a, b))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None, 3])

    assert_model_result(l,
        input={
            'b': [
                [0.1, 0.1, 0.1],
                [0.1, 0.2, 0.3],
            ]
        },
        expected_result=[[
            [0.1, 0.2, 0.3],
            [0.1, 0.4, 0.9],
        ]]
    )


def test_argmax():
    g = graph.create_graph()
    i = graph.create_input(g, "i", onnx.TensorProto.FLOAT, [None, 3])

    l = ops.argmax(axis=1)(i)
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.INT64, [None, 1])

    assert_model_result(l,
        input={
            'i': [
                [1, 4, 2],
                [2, 8, 12],
                [11, 0, 5],
            ]
        },
        expected_result=[[
            [1],
            [2],
            [0],
        ]]
    )


def test_gather():
    g = graph.create_graph()

    indices = graph.create_initializer(g, "indices", onnx.TensorProto.INT64, [1], [1])
    data = graph.create_input(g, "data", onnx.TensorProto.INT64, [None, 3])

    l = ops.gather(axis=1)(graph.merge(data, indices))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.INT64, [None, 1])

    assert_model_result(l,
        input={
            'data': [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                [10, 11, 12],
            ]
        },
        expected_result=[[
            [[2], [5], [8], [11]],
        ]]
    )


def test_gather_elements():
    g = graph.create_graph()

    a = graph.create_initializer(g, "a", onnx.TensorProto.FLOAT, [3, 1], [0.1, 0.2, 0.3])
    b = graph.create_input(g, "b", onnx.TensorProto.INT64, [None, 1])

    l = ops.gather_elements()(graph.merge(a, b))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None, 1])

    assert_model_result(l,
        input={
            'b': [
                [2],
                [1],
                [0],
            ]
        },
        expected_result=[[
            [0.3],
            [0.2],
            [0.1],
        ]]
    )


def test_gather_nd():
    g = graph.create_graph()

    a = graph.create_initializer(g, "a", onnx.TensorProto.FLOAT, [3, 3], np.array([
        [0.1, 0.2, 0.3],
        [1.1, 2.2, 3.3],
        [0.1, 20.2, 30.3],
    ]).flatten())
    b = graph.create_input(g, "b", onnx.TensorProto.INT64, [None, 2])

    l = ops.gather_nd()(graph.merge(a, b))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None])

    assert_model_result(l,
        input={
            'b': [
                [2, 0],
                [1, 1],
                [0, 1],
            ]
        },
        expected_result=np.array([[0.1, 2.2, 0.2]])
    )


def test_concat():
    g = graph.create_graph()

    a = graph.create_input(g, "a", onnx.TensorProto.FLOAT, [3, 1])
    b = graph.create_input(g, "b", onnx.TensorProto.FLOAT, [3, 1])

    l = ops.concat(axis=1)(graph.merge(a, b))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None, 2])

    assert_model_result(l,
        input={
            'a': [[0.1], [0.2], [0.3]],
            'b': [[1.1], [1.2], [1.3]],
        },
        expected_result=[[
            [0.1, 1.1],
            [0.2, 1.2],
            [0.3, 1.3],
        ]]
    )


def test_expand():
    g = graph.create_graph()

    shape = graph.create_initializer(g, "shape", onnx.TensorProto.INT64, [2], [4, 3])
    i = graph.create_input(g, "i", onnx.TensorProto.FLOAT, [None, 1])

    l = ops.expand()(graph.merge(i, shape))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None, 3])

    assert_model_result(l,
        input={
            'i': [
                [0.1],
                [1.2],
                [11],
                [4.2],
            ]
        },
        expected_result=[[
            [0.1, 0.1, 0.1],
            [1.2, 1.2, 1.2],
            [11, 11, 11],
            [4.2, 4.2, 4.2]
        ]],
    )


def test_reduce_sum():
    g = graph.create_graph()

    axis = graph.create_initializer(g, "axis", onnx.TensorProto.INT64, [1], [1])
    i = graph.create_input(g, "i", onnx.TensorProto.FLOAT, [None, 3])

    l = ops.reduce_sum(keepdims=0)(graph.merge(i, axis))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None])

    assert_model_result(l,
        input={
            'i': [
                [0.1, 1.0, 1.2],
                [1.2, 0.4, 0.9],
                [11, 0.8, -0.2],
                [4.2, 3.2, -6.4],
            ]
        },
        expected_result=[[2.3, 2.5, 11.6, 1.0]]
    )


def test_reshape():
    g = graph.create_graph()

    shape = graph.create_initializer(g, "shape", onnx.TensorProto.INT64, [1], [0])
    i = graph.create_input(g, "i", onnx.TensorProto.FLOAT, [None, 1])

    l = ops.reshape()(graph.merge(i, shape))
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None])

    assert_model_result(l,
        input={
            'i': [
                [0.1],
                [1.2],
                [11],
                [4.2],
            ]
        },
        expected_result=[[0.1, 1.2, 11, 4.2]]
    )


def test_softmax():
    g = graph.create_graph()

    i = graph.create_input(g, "i", onnx.TensorProto.FLOAT, [None, 2])

    l = ops.softmax()(i)
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None, 2])

    assert_model_result(l,
        input={
            'i': [
                [0.0, 0.68],
                [0.0, 0.2],
                [1.2, 0.3],
                [0.0, -0.2],
            ]
        },
        expected_result=[[
            [0.3362613 , 0.66373867],
            [0.450166  , 0.54983395],
            [0.7109495 , 0.2890505 ],
            [0.54983395, 0.450166  ]
        ]],
    )


def test_split():
    g = graph.create_graph()

    i = graph.create_input(g, "i", onnx.TensorProto.FLOAT, [None, 3])

    l = ops.split(axis=1)(i)
    l = graph.add_output(l, l.transients[0].name, onnx.TensorProto.FLOAT, [None, 1])
    l = graph.add_output(l, l.transients[1].name, onnx.TensorProto.FLOAT, [None, 1])
    l = graph.add_output(l, l.transients[2].name, onnx.TensorProto.FLOAT, [None, 1])

    assert_model_result(l,
        input={
            'i': [
                [0.0, 0.68, 1.3],
                [0.0, 0.2, 4.3],
                [1.2, 0.3, 5.2],
                [0.0, -0.2, 8.3],
            ]
        },
        expected_result=[
            [[0.0], [0.0], [1.2], [0.0]],
            [[0.68], [0.2], [0.3], [-0.2]],
            [[1.3], [4.3], [5.2], [8.3]],
        ],
    )
