SRCS := $(wildcard src/*.c)
TESTS := $(wildcard test/*.c)
UNITY := unity/unity.c

testes:
	gcc -O3 -Wall -Wextra $(SRCS) $(TESTS) $(UNITY) -o testes-task-manager

app:
	gcc -O3 -Wall -Wextra $(SRCS) -o task-manager
