install:
	install -m755 term-write.py /usr/bin/term-write
	gzip -c term-write.1 > term-write.1.gz
	install term-write.1.gz /usr/share/man/man1/

.PHONY: install
