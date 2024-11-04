import ast
from .attach_cfg_id import AttachCFGId
from .strip_comment_nodes import StripCommentNodes

class InitializePredsSuccsProperty(ast.NodeTransformer):
    def visit(self, N):
        N.predecessors = []
        N.successors = []
        self.generic_visit(N)
        return N

class AttachPredsSuccsProperty(ast.NodeTransformer):
    def visit_FunctionDef(self, N: ast.FunctionDef):
        self.add_edge(N, N.body[0])
        self.visit_body(N.body)
        return N

    def visit_body(self, body):
        for i in range(len(body)):
            child = body[i]
            next = body[i+1] if i + 1 < len(body) else None

            if isinstance(child, ast.While):
                self.visit_While(child)

            if isinstance(child, ast.If):
                self.visit_If(child)
            
            for t in self.get_exits(child):
                self.add_edge(t, next)

    def visit_While(self, N):
        self.add_edge(N, N.body[0])
        self.visit_body(N.body)
        body_exits = self.get_exits(N.body[-1])
        # Add back edges for while loop
        for t in body_exits:
            self.add_edge(t, N)

    def visit_If(self, N):
        self.add_edge(N, N.body[0])
        if len(N.orelse) > 0:
            self.add_edge(N, N.orelse[0])

        self.visit_body(N.body)
        self.visit_body(N.orelse)
        
    def get_exits(self, N):
        if isinstance(N, ast.While):
            return [N]
        elif isinstance(N, ast.If):
            exits = self.get_exits(N.body[-1])
            if len(N.orelse) > 0:
                exits += self.get_exits(N.orelse[-1])
            else:
                # directly exit from the condition node
                exits += [N]
            return exits
        else:
            return [N]

    def add_edge(self, this, next):
        if isinstance(this, ast.Return):
            return
            
        if next != None:
            this.successors.append(next)
            next.predecessors.append(this)


def dump_node_preds_succs(N):
    print("node:", ast.unparse(N).split('\n')[0])
    print("predecessors:", [ast.unparse(n).split('\n')[0] for n in N.predecessors])
    print("successors:", [ast.unparse(n).split('\n')[0] for n in N.successors])
    print()

def dump_node_pred_succ_ids(N):
    print("node:", ast.unparse(N).split('\n')[0], N.cfg_id)
    print("predecessors:", [ast.unparse(n).split('\n')[0] for n in N.predecessors], [n.cfg_id for n in N.predecessors])
    print("successors:", [ast.unparse(n).split('\n')[0] for n in N.successors], [n.cfg_id for n in N.successors])
    print()



class DumpPredsSuccsProperty(ast.NodeVisitor):
    def visit(self, N):
        if isinstance(N, (ast.While, ast.Assign)):            
            dump_node_pred_succ_ids(N)
        self.generic_visit(N)
        return N


def transform(tree):
    tree = StripCommentNodes().visit(tree)
    tree = AttachCFGId().visit(tree)
    tree = InitializePredsSuccsProperty().visit(tree)
    tree = AttachPredsSuccsProperty().visit(tree)
    #tree = DumpPredsSuccsProperty().visit(tree)
    return tree