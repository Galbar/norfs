from collections import deque
import norfs.helpers
import ast
import astunparse


class TypeHintRemover(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        # remove the return type defintion
        node.returns = None
        # remove all argument annotations
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None
        if node.args.kwonlyargs:
            for arg in node.args.kwonlyargs:
                arg.annotation = None
        if node.args.vararg:
            node.args.vararg.annotation = None
        if node.args.kwarg:
            node.args.kwarg.annotation = None

        node.body = [y for y in (self.visit(x) for x in node.body) if y]
        return node

    def visit_Import(self, node):
        node.names = [n for n in node.names if n.name != 'typing']
        return node if node.names else None

    def visit_ImportFrom(self, node):
        return node if node.module != 'typing' else None

    def visit_AnnAssign(self, node):
        if node.value is None:
            return None

        return ast.Assign(targets=[self.visit(node.target)],
                          value=self.visit(node.value))

    def visit_JoinedStr(self, node):
        template = ''
        args = []

        for value in node.values:
            if type(value) is ast.Str:
                template += value.s
                continue

            template += '{' + str(len(args)) + '}'
            args.append(self.visit(value.value))

        return ast.Call(func=ast.Attribute(value=ast.Str(s=template), attr='format', ctx=ast.Load()),
                        args=args,
                        keywords=[])

    def _fix_starred_args(self, arg, right_args):
        if not right_args:
            return [arg]

        fixed_right_args = self._fix_starred_args(right_args[0], right_args[1:])
        if type(arg) != ast.Starred:
            return [arg] + fixed_right_args

        return [ast.Starred(value=ast.BinOp(left=ast.Call(func=ast.Name(id='list', ctx=ast.Load()),
                                                          args=[arg.value],
                                                          keywords=[]),
                                            op=ast.Add(),
                                            right=ast.List(elts=fixed_right_args,
                                                           ctx=ast.Load())))]

    def visit_Call(self, node):
        node.args = [y for y in (self.visit(x) for x in node.args) if y]
        node.keywords = [y for y in (self.visit(x) for x in node.keywords) if y]

        if node.args:
            node.args = self._fix_starred_args(node.args[0], node.args[1:])

        if type(node.func) is not ast.Name or node.func.id != 'cast':
            return node

        return node.args[1]


def backport_file(src, dst):
    # parse the source code into an AST
    parsed_source = ast.parse(src.read())
    # remove all type annotations, function return type definitions
    # and import statements from 'typing'
    transformed = TypeHintRemover().visit(parsed_source)
    # convert the AST back to source code
    dst.write(astunparse.unparse(transformed).encode('utf-8'))


def get_src_dst_list():
    local = norfs.helpers.local()
    root = local.dir('./norfs')
    target = local.dir('./py3.4/norfs')

    dirs = deque([(root, target)])

    while dirs:
        src, dst = dirs.pop()

        for item in src.list():
            if item.is_dir():
                dirs.append((item, dst.subdir(item.name)))
            elif item.name.endswith('.py'):
                print(f'backporting file: {item.path}')
                yield item, dst.file(item.name)


if __name__ == "__main__":
    for src, dst in get_src_dst_list():
        backport_file(src, dst)
