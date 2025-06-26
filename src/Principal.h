#ifndef PRINCIPAL_H
#define PRINCIPAL_H

#include <stddef.h>
#include <time.h>

#include "Time.h"
#include "Usuario.h"
#include "Tag.h"
#include "Tarefa.h"
#include "GT.h"

/* --- tipo opaco --- */
typedef struct Principal Principal;

/* === ciclo de vida do “app” === */
Principal* principal_iniciar(void);                  /* carrega dependências, configura GT... */
void principal_encerrar(Principal* p);               /* fecha GT, libera heap, persiste estado */

/* ========== CRUD: Time ========== */
Time* principal_criar_time(Principal* p, const char* nome);
int principal_renomear_time(Principal* p, Time* time, const char* novo_nome);
int principal_excluir_time(Principal* p, Time* time);
const Time** principal_listar_times(const Principal* p, size_t* out_qtd);

#endif
