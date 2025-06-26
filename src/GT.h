#ifndef GERENCIAMENTO_DE_TAREFAS_H
#define GERENCIAMENTO_DE_TAREFAS_H

#include <stddef.h>
#include <time.h>
#include "Time.h"
#include "Tarefa.h"
#include "Tag.h"
#include "Usuario.h"

typedef struct GerenciamentoDeTarefas GT;

GT* gt_inicializar(void);
void gt_finalizar(GT* gt);

int gt_registrar_time(GT* gt, Time* time);

Tarefa* gt_criar_tarefa(GT* gt,
                        Time* time,
                        const char* titulo,
                        const char* descricao,
                        Usuario* resp,
                        Tag** tags,
                        size_t n_tags,
                        time_t prazo);

int gt_remover_tarefa(GT* gt, Tarefa* t);

const Tarefa** gt_listar_tarefas_time(const GT* gt, const Time* time, size_t* out_qtd);

#endif
