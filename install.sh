#!/bin/bash

GDB_DIR=/etc/gdb/
SCRIPTS="plist.py pbtree.py"

for s in $SCRIPTS
do
	cp $s ${GDB_DIR}
	if ! grep -q "source.*$s" ${GDB_DIR}/gdbinit; then
		echo "source ${GDB_DIR}/$s" >> ${GDB_DIR}/gdbinit
	fi
done
