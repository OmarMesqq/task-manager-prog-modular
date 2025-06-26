#ifndef PRINCIPAL_H
#define PRINCIPAL_H

#include <stddef.h>
#include <time.h>

#include "Time.h"
#include "Usuario.h"
#include "Tag.h"
#include "Tarefa.h"
#include "GT.h"

/**
 * Tipo propositalmente opaco no .h para encapsular o TAD 
 * e forçar o uso das funções de acesso
 */
typedef struct Principal Principal;

/**
 * Nome do arquivo de prefências de um uso do Task Manager.
 * É imutável e inacessível para demais módulos
 */
static const char* ARQUIVO_PREFERENCIAS_TASK_MANAGER = "preferencias.json";

/* === ciclo de vida do app === */
Principal* principal_iniciar(void);                  /* carrega dependências, configura GT... */
void principal_encerrar(Principal* p);               /* fecha GT, libera heap, persiste estado */

/* ========== CRUD: Time ========== */
Time* principal_criar_time(Principal* p, const char* nome);
int principal_renomear_time(Principal* p, Time* time, const char* novo_nome);
int principal_excluir_time(Principal* p, Time* time);
const Time** principal_listar_times(const Principal* p, size_t* out_qtd);

/* ========= CRUD: Usuário ========= */
Usuario *principal_criar_usuario   (Principal *p, const char *nome, const char *email);

int      principal_alterar_email   (Principal *p,
                                    Usuario *u,
                                    const char *novo_email);

int      principal_excluir_usuario (Principal *p, Usuario *u);

const Usuario **principal_listar_usuarios(const Principal *p, size_t *out_qtd);


/* ========= CRUD: Tag ========= */
Tag* principal_criar_tag(Principal *p, const char *nome, const char* cor_hex);

int  principal_renomear_tag        (Principal *p,
                                    Tag *tag,
                                    const char *novo_nome);

int  principal_mudar_cor_tag       (Principal *p,
                                    Tag *tag,
                                    const char *nova_cor_hex);

int  principal_excluir_tag         (Principal *p, Tag *tag);

const Tag **principal_listar_tags  (const Principal *p, size_t *out_qtd);

/* ========== Operações sobre tarefas (via módulo gerenciamento de tarefas) ========== */
Tarefa *principal_nova_tarefa      (Principal *p,
                                    Time *time,
                                    const char *titulo,
                                    const char *descricao,
                                    Usuario *responsavel,
                                    Tag **tags,
                                    size_t n_tags,
                                    time_t prazo);

int     principal_mudar_status_tarefa (Principal *p,
                                       Tarefa *t,
                                       StatusTarefa novo_status);

int     principal_remover_tarefa      (Principal *p, Tarefa *t);

const Tarefa **principal_listar_tarefas_time(const Principal *p,
                                             const Time *time,
                                             size_t *out_qtd);

#endif
