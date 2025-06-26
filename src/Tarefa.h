#ifndef TAREFA_H
#define TAREFA_H

#include <time.h>
#include <stddef.h>
#include "Usuario.h"
#include "Tag.h"

typedef enum {
    TAREFA_ABERTA,
    TAREFA_EM_PROGRESSO,
    TAREFA_CONCLUIDA,
    TAREFA_CANCELADA
} StatusTarefa;

typedef struct Tarefa Tarefa;

Tarefa* tarefa_criar(const char* titulo,
                     const char* descricao,
                     Usuario* responsavel,
                     time_t prazo);

void tarefa_destruir(Tarefa* t);
int tarefa_set_status(Tarefa* t, StatusTarefa s);
StatusTarefa tarefa_get_status(const Tarefa* t);
int tarefa_add_tag(Tarefa* t, Tag* tag);
size_t tarefa_list_tags(const Tarefa* t, Tag** buffer, size_t max);

#endif
