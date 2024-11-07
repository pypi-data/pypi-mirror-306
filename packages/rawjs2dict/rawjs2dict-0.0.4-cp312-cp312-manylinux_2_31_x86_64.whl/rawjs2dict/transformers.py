import inspect
import sys
from abc import ABC
from typing import Any

from rawjs2dict.utils import LITERAL_VALUE
from rawjs2dict.utils import merge_dicts


class JSTransformer:
    @staticmethod
    def __get_transformer__(transformer_name: str) -> "BaseJSTransformer | None":
        transformer: "BaseJSTransformer | None" = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass)).get(
            f"{transformer_name}Transformer", None
        )

        return transformer

    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        transformer = cls.__get_transformer__(ast.get("type", ""))
        return transformer.transform(ast) if transformer else {}


class BaseJSTransformer(ABC):
    field: str = ""

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return ""

    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        data = ast[cls.field]
        name = cls.__get_name__(ast)

        if isinstance(data, list):
            output: dict[str, Any] = {}
            for statement in data:
                result = JSTransformer.transform(statement)
                output = merge_dicts(output, result)
        else:
            output = JSTransformer.transform(data)

        return {name: output} if name else output


class LiteralTransformer(BaseJSTransformer):
    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        return {LITERAL_VALUE: ast["value"]}


class ArrayExpressionTransformer(BaseJSTransformer):
    field = "elements"


class ObjectExpressionTransformer(BaseJSTransformer):
    field = "properties"


class PropertyTransformer(BaseJSTransformer):
    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        name = None
        if ast["value"]:
            if ast["key"]["type"] == "Identifier":
                name = ast["key"]["name"]
            else:
                name = "_".join([str(v) for v in JSTransformer.transform(ast["key"]).values()])

        return name or super().__get_name__(ast)

    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        output = {}
        name = cls.__get_name__(ast)

        if ast["value"]:
            output = JSTransformer.transform(ast["value"])

        return {name: output} if name else output


class FunctionExpressionTransformer(BaseJSTransformer):
    field = "body"

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class ArrowFunctionExpressionTransformer(FunctionExpressionTransformer):
    field = "body"

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class ClassExpressionTransformer(FunctionExpressionTransformer):
    field = "body"

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class ClassBodyTransformer(BaseJSTransformer):
    field = "body"


class MethodDefinitionTransformer(PropertyTransformer):
    pass


class CallExpressionTransformer(BaseJSTransformer):
    field = "arguments"


class NewExpressionTransformer(BaseJSTransformer):
    field = "arguments"


class SpreadElementTransformer(BaseJSTransformer):
    field = "argument"


class YieldExpressionTransformer(SpreadElementTransformer):
    field = "argument"


class AssignmentExpressionTransformer(BaseJSTransformer):
    field = "right"

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        left = ast["left"]
        if "name" in left:
            name = left["name"]
        elif "name" in left["object"]:
            name = f"{left['object']['name']}_{left['property']['name']}"
        elif "object" in left["property"]:
            name = cls.__get_name__({"left": left["property"]})
        else:
            name = f"{left['property']['name']}"

        return name or super().__get_name__(ast)


class ClassDeclarationTransformer(BaseJSTransformer):
    field = "body"

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class FunctionDeclarationTransformer(BaseJSTransformer):
    field = "body"

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class VariableDeclaratorTransformer(BaseJSTransformer):
    field = "init"

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class VariableDeclarationTransformer(BaseJSTransformer):
    field = "declarations"


class BlockStatementTransformer(BaseJSTransformer):
    field = "body"


class ExpressionStatementTransformer(BaseJSTransformer):
    field = "expression"


class IfStatementTransformer(BaseJSTransformer):
    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        output = JSTransformer.transform(ast["consequent"])
        if ast.get("alternate"):
            output = merge_dicts(output, JSTransformer.transform(ast["alternate"]))

        return output


class LabeledStatementTransformer(BaseJSTransformer):
    field = "body"

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return ast.get("label", {}).get("name", "") or super().__get_name__(ast)


class SwitchStatementTransformer(BaseJSTransformer):
    field = "cases"


class SwitchCaseTransformer(BaseJSTransformer):
    field = "consequent"


class TryStatementTransformer(BaseJSTransformer):
    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        output = {}

        output["try"] = JSTransformer.transform(ast["block"])
        if ast["handler"]:
            output["catch"] = JSTransformer.transform(ast["handler"])
        if ast["finalizer"]:
            output["finally"] = JSTransformer.transform(ast["finalizer"])

        return output


class CatchClauseTransformer(BaseJSTransformer):
    field = "body"


class WithStatementTransformer(BaseJSTransformer):
    field = "body"


class ProgramTransformer(BaseJSTransformer):
    field = "body"
