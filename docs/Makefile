LIB  = libeauty.a
OBJS = ../src/acceptor.o \
       ../src/application.o \
       ../src/attributes.o \
       ../src/client.o \
       ../src/exception.o \
       ../src/route.o \
       ../src/router.o \
       ../src/server.o \
       ../src/sha1.o \
       ../src/signal.o \
       ../src/swagger.o \
       ../src/timer.o \
       ../src/url.o \
       ../src/utils.o

.cpp.o:
	g++ -std=c++17 -Wall -O2 -c -o $@ $< -I../include -I.

$(LIB): $(OBJS)
	ar -r $@ $(OBJS)

clean:
	rm -f libeauty.a ../src/*.o
