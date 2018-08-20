import traceback

class Plist(gdb.Command):
    """
plist - print all elements in private defined List data structure

usage:
    1) the list head is a variable or a pointer
        (gdb) plist <head> <next_field_in_struct>
    2) the list head is just an address
        (gdb) plist <head_address> <list_struct_type> <next_field_in_struct>

List data structure is a widely-used data structure in software project,
plist command is to provide a powerful way to show all elements of the List.

Before use plist command, need know the head(variable, pointer or address of
The list), and what type the List is(if the head is address), then tell the
'Next' field's Name.

For Example (code and gdb plist command illustration)

struct ilist {
    int data;
    struct ilist *next;
};

struct ilist *head;

struct ilist *build_list()
{
    ...
}

int main()
{
    struct ilist *phead = build_list();
    | 
    | 1) use list pointer
    | (gdb) plist phead next

    struct ilist vhead = *phead;
    |
    | 2) use list variable
    | (gdb) plist vhead next

    | assume phead is 0x555555756260
    | 3) use address as a List
    | (gdb) plist 0x555555756260 "struct ilist" next
    | 
    | Note: because type 'struct ilist' has a space, so need a quote
}
    """

    def __init__(self):
        super(self.__class__, self).__init__("plist", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)

        if len(argv) < 1:
            raise gdb.GdbError("Invalid argument")

        _head = argv[0]
        var = gdb.parse_and_eval(_head)
        if var.type.code == gdb.TYPE_CODE_INT and len(argv) != 3:
            raise gdb.GdbError("Invalid argument")

        if var.type.code == gdb.TYPE_CODE_INT:
            _type = gdb.lookup_type(argv[1])
            _pointer = _type.pointer()
            var = var.cast(_pointer)
            head_address = var
            var = var.dereference()
            next_field = argv[2]
        elif var.type.code == gdb.TYPE_CODE_PTR:
            _type = var.dereference().type
            _pointer = var.type
            head_address = var
            var = var.dereference()
            next_field = argv[1]
        elif var.type.code == gdb.TYPE_CODE_STRUCT:
            _type = var.type
            _pointer = _type.pointer()
            next_field = argv[1]
            head_address = var.address
        else:
            raise gdb.GdbError("Unsport type")

        null_address = gdb.Value(0x00).cast(_pointer)

        try:
            if gdb.types.has_field(_type, next_field) == False:
                raise gdb.GdbError("type '" + str(_type) + "' has no field '" + next_field + "'")

            if _type[next_field].type != _type.pointer():
                raise gdb.GdbError("field '" + next_field + "' in type '" + str(_type) + "' is not a pointer type")

        except TypeError as err:
            raise gdb.GdbError(traceback.format_exc())

        try:
            idx = 0
            while True:
                print("[%d] <0x%x> %s %s" % (idx, var.address, str(_type), str(var)))
                ptr = var[next_field]
                if ptr == head_address or ptr == null_address:
                    break

                var = ptr.dereference()
                idx = idx + 1

        except TypeError as err:
            raise gdb.GdbError("TypeError:" + str(err) + traceback.format_exc())
        except MemoryError as err:
            raise gdb.GdbError("MemoryError: " + str(err) + " " + traceback.format_exc())
Plist()
