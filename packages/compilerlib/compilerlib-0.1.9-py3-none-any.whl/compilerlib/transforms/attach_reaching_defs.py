import ast
from compilerlib.ast_utils import *
from .attach_def_use_vars import AttachDefUseVars

class InitializeInsAndOuts(ast.NodeTransformer):
    def visit(self, N):
        N.ins = {}
        N.outs = {}
        self.generic_visit(N)
        return N

class ReachingDefs(ast.NodeVisitor):
    def add_to_outs(self, node, var, defining_node):
        node.outs.setdefault(var, set()).add(defining_node)
 
    def add_to_ins(self, node, var, defining_node):
        node.ins.setdefault(var, set()).add(defining_node)

    def visit_FunctionDef(self, N):
        for arg in N.args.args:            
            self.add_to_outs(N, arg.arg, N)
        
        queue = [] + N.successors
        while len(queue) > 0:
            node = queue.pop(0)            
            node.ins = self.merge_defs([x.outs for x in node.predecessors])
            old_outs = node.outs.copy()
            # This will modify the outs prop in-place
            self.transfer(node) 
            # Add node.successors if its outs set has changed
            if node.outs != old_outs: 
                queue += node.successors
        return N

    def merge_defs(self, defs):
        '''
        Each dict in `defs` maps a variable name to a set of nodes
        '''
        merged_dict = {}
        for d in defs:
            for key, value in d.items():
                merged_dict.setdefault(key, set()).update(value)
        
        return merged_dict

    def transfer(self, node):
        node.outs = node.ins.copy()
        if isinstance(node, ast.Assign):
            var = node.targets[0].id
            # Kill all existing defs of `var`
            if var in node.outs:
                node.outs.pop(var)

            # Add new defs
            self.add_to_outs(node, var, node)

    def are_dicts_equivalent(self, dict1, dict2):
        # Check if both dictionaries have the same keys
        if dict1.keys() != dict2.keys():
            return False

        # Check if each list for a given key has the same elements (ignoring order)
        for key in dict1:
            if dict1[key] != dict2[key]:
                return False
        
        return True


class PruneReachingDefs(ast.NodeVisitor):
    '''
    This transformer will prune the def sets such that only the definitions of the 
    variables that are used in the node are kept.
    '''
    def visit(self, N):        
        if hasattr(N, 'use_vars'):
            N.ins = {k:v for k,v in N.ins.items() if k in N.use_vars}

        self.generic_visit(N)
        return N


class PrintReachingDefs(ast.NodeTransformer):
    def print_set(self, set, prefix):
        print(f'{prefix}: ', end='')
        for k in set:
            print(f'{k}=>{[x.cfg_id for x in set[k]]}', end=', ')
        print()
        

    def visit(self, N):
        if hasattr(N, 'cfg_id'):
            print(f"node {N.cfg_id}: {ast.unparse(N).split('\n')[0]}")
            self.print_set(N.ins, "in set")
            #self.print_set(N.outs, "outs")
            print()

        self.generic_visit(N)
        return N

        

def transform(node, relevant_only=True):
    node = InitializeInsAndOuts().visit(node)
    node = ReachingDefs().visit(node)
    if relevant_only:
        node = AttachDefUseVars().visit(node)
        node = PruneReachingDefs().visit(node)
    #node = PrintReachingDefs().visit(node)
    return node