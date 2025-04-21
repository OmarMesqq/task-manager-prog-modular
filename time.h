#ifndef TIME_H
#define TIME_H
/* 
* Esse módulo (Time) atua como servidor dos módulos Principal e Gerenciamento de Tarefas (GT) 
*/

typedef struct time {
    char* nome;
} Time;


/*
 * Retorna ponteiro válido para time caso criação seja bem sucedida
 * Retorna NULL em caso de falha
 * */
Time* cria_time(char* nome);

/*
 * Retorna ponteiro válido para time caso consulta seja bem sucedida
 * Retorna NULL em caso de falha
 * */
Time* consulta_time(char* nome);

/*
 * Retorna ponteiro válido para time caso alteração seja bem sucedida
 * Retorna NULL em caso de falha
 * */
Time* altera_time(char* nome, Time* timePatch);

/*
 * Retorna 1 caso a remoção seja bem sucedida 
 * Retorna 0 em caso contrário
 * */
int apaga_time(char* nome);


#endif
