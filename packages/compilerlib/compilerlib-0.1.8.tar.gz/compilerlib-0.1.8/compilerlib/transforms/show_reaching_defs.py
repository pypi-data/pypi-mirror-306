import ast_comments as ast
import json

class ShowReachingDefs(ast.NodeTransformer):
    def reaching_defs_to_string(self, defs):
        items = []
        for k in defs:
            items.append(f'{k}=>{[x.cfg_id for x in defs[k]]}')
        return ', '.join(items)

    def visit(self, node):
        if hasattr(node, 'cfg_id') and not isinstance(node, ast.FunctionDef):
            comment = f'# node {node.cfg_id}, reaching_defs: {self.reaching_defs_to_string(node.ins)}'
            node.comment = ast.Comment(value=comment, inline=False)

        self.generic_visit(node)

        if hasattr(node, 'comment'):
            return [node.comment, node]
        else:
            return node

def transform(node):
    return ShowReachingDefs().visit(node)