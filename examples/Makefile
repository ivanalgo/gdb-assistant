CC := gcc
CFLAGS = -Wall -g

BINS=$(patsubst %.c, %, $(wildcard *.c))

all: $(BINS)

$(BINS): %:%.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

clean:
	rm -rf $(BINS)

test: $(BINS)
	for bin in $(BINS); do gdb -q "$$bin" < "$$bin"_gdb; done
