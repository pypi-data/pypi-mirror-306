import fileinput
import sys
from typing import Sequence

import libcst as cst


class SplitImportTransformer(cst.CSTTransformer):
    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ):
        if isinstance(updated_node.names, cst.ImportStar):
            return updated_node
        elif isinstance(updated_node.names, Sequence) and len(updated_node.names) > 1:
            new_imports = []
            for alias in updated_node.names:
                new_import = cst.ImportFrom(
                    module=updated_node.module,
                    names=[alias.with_changes(comma=cst.MaybeSentinel.DEFAULT)],
                    relative=updated_node.relative,
                    whitespace_after_from=updated_node.whitespace_after_from,
                    whitespace_before_import=updated_node.whitespace_before_import,
                )

                new_imports.append(new_import)
            return cst.FlattenSentinel(new_imports)
        else:
            return updated_node


def transform_code(code: str) -> str:
    module = cst.parse_module(code)
    return module.visit(SplitImportTransformer()).code


def main():
    original_code = "".join(fileinput.input())
    new_code = transform_code(original_code)
    sys.stdout.write(new_code)


if __name__ == "__main__":
    main()
