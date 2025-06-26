#ifndef USUARIO_H
#define USUARIO_H

typedef struct Usuario Usuario;

Usuario* usuario_criar       (const char* nome, const char* email);
void     usuario_destruir    (Usuario *u);

int      usuario_set_email   (Usuario* u, const char* novo_email);
const char* usuario_get_nome (const Usuario* u);
const char* usuario_get_email(const Usuario* u);

#endif
