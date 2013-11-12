all:
	echo "#!/usr/bin/python2" > voltcraft
	cat voltcraft.py >> voltcraft
	chmod 755 voltcraft

install:
	cp voltcraft /usr/local/bin/

clean:
	rm voltcraft
