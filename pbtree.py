import traceback

class Pbtree(gdb.Command):
    """
pbtree - print all elements in user-defined binary tree data structure
    """

    def __init__(self):
        super(self.__class__, self).__init__("pbtree", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)

        if len(argv) < 1:
            raise gdb.GdbError("invalide argument")

        _head = argv[0]
        var = gdb.parse_and_eval(_head)
        if var.type.code == gdb.TYPE_CODE_INT and len(argv) != 4:
            raise gdb.GdbError("Invalide argument")

        if var.type.code == gdb.TYPE_CODE_INT:
            _type = gdb.lookup_type(argv[1])
            _pointer = _type.pointer()
            var = var.cast(_pointer).dereference()
            left_field = argv[2]
            right_field = argv[3]
        elif var.type.code == gdb.TYPE_CODE_PTR:
            _type = var.dereference().type
            _pointer = var.type
            var = var.dereference()
            left_field = argv[1]
            right_field = argv[2]
        elif var.type.code == gdb.TYPE_CODE_STRUCT:
            _type = var.type
            _pointer = _type.pointer()
            left_field = argv[1]
            right_field = argv[2]
        else:
            raise gdb.GdbError("Head '" + _type + "' unspport type")

        null_address = gdb.Value(0x00).cast(_pointer)

        try:
            if (gdb.types.has_field(_type, left_field) == False
                or gdb.types.has_field(_type, right_field) == False):
                raise gdb.GdbError(str(_type) + " has no field " + left_field + " or " + right_field)

            if _type[left_field].type != _pointer or _type[right_field].type != _pointer:
                raise gdb.GdbError("field " + left_field + " or " + right_field + " in type " + str(_type) + " is not a pointer type")
        except TypeError as err:
            raise gdb.GdbError(traceback.format_exc())

        # visit the binary tree
        try:
            visit_bin_tree(var, left_field, right_field, null_address)
        except TypeError as err:
            raise gdb.GdbError(str(err) + traceback.format_exc())
        except MemoryError as err:
            raise gdb.GdbError(str(err) + traceback.format_exc())

Pbtree()

def visit_bin_tree(tree, left, right, null, index = 0):
    print("[%d] <0x%x> %s %s" % (index, tree.address, str(tree.type), str(tree))) 
    index = index + 1
    lptr = tree[left]
    if lptr != null:
        index = visit_bin_tree(lptr.dereference(), left, right, null, index)

    rptr = tree[right]
    if rptr != null:
        index = visit_bin_tree(rptr.dereference(), left, right, null, index)

    return index
