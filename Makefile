all: 
	make -C ./lib/keylogger
	make -C ./lib/brightness
clean:
	rm -rf ./lib/keylogger/bin
	rm -rf ./lib/brightness/bin


