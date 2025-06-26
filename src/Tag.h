#ifndef TAG_H
#define TAG_H

typedef struct Tag Tag;

Tag* tag_criar(const char* nome, const char* cor_hex);
void tag_destruir(Tag* tag);

int tag_set_nome(Tag* tag, const char* novo_nome);
int tag_set_cor(Tag* tag, const char* nova_cor_hex);

const char* tag_get_nome(const Tag* tag);
const char* tag_get_cor(const Tag* tag);

#endif
