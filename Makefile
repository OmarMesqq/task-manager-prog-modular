SRCS := $(wildcard src/*.c)
CJSON := lib/cjson/cJSON.c
TESTS := $(wildcard test/*.c)
UNITY := unity/unity.c

testes:
	gcc -O3 -Wall -Wextra \
	src/Principal.c \
	$(TESTS) \
	$(UNITY) \
	-o testes-task-manager

app:
	gcc -O3 -Wall -Wextra $(SRCS) -o task-manager
