#ifndef TIME_H
#define TIME_H

#include <stddef.h>
#include "Usuario.h"

typedef struct Time Time;

Time* time_criar (const char* nome);
void time_destruir (Time* t);
int time_adicionar_usuario(Time* t, Usuario* u);
int time_remover_usuario (Time* t, const Usuario* u);
size_t time_qtd_membros (const Time* t);

#endif
