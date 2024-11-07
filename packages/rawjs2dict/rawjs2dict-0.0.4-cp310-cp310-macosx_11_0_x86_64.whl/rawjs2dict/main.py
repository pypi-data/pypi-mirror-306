import typing as _typing

import pythonmonkey as _pm

from rawjs2dict.transformers import JSTransformer as _JSTransformer
from rawjs2dict.utils import clean_dict as _clean_dict
from rawjs2dict.utils import replace_pythonmonkey_nulls as _clean_ast

_acorn = _pm.require("acorn")


def transform(script: str) -> dict[str, _typing.Any]:
    ast = _acorn.parse(script, {"ecmaVersion": "latest"})
    cleaned_ast = _clean_ast(ast)
    output = _JSTransformer.transform(cleaned_ast)
    cleaned_output: dict[str, _typing.Any] = _clean_dict(output)

    return cleaned_output
