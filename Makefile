testes:
	gcc -O3 -Wall -Wextra test/testes.c unity/unity.c -o testes-task-manager

app:
	gcc -O3 -Wall -Wextra src/principal.c -o task-manager
