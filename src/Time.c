#include "Time.h"
#include <stdlib.h>
#include <stdio.h>

/**
 * 
 */
typedef struct Time {
    const char* nome;
    size_t qtdMembros;
} Time;


/**
 * 
 */
Time* time_criar(const char* nome) {
    if (!nome) {
        printf("Time deve ter um nome válido!");
        return NULL;
    }

    Time* t = malloc(sizeof(Time));
    if (!t) {
        printf("Falha de alocação de memória ao criar Time!\n");
        return NULL;
    }

    t->nome = nome;
    t->qtdMembros = 0;
    
    return t;
}