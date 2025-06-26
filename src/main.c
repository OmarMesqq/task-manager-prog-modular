#include "Principal.h"
#include <stdio.h>
#include <stdlib.h>

// Funções internas utilizadas apenas na main
static void imprime_logo();

/**
 * Ponto de entrada do aplicativo
 */
int main(void) {
    imprime_logo();
}


static void imprime_logo() {
    printf(
        "___________              __        _____                                             \n"
        "\\__    ___/____    _____|  | __   /     \\ _____    ____ _____     ____   ___________ \n"
        "  |    |  \\__  \\  /  ___/  |/ /  /  \\ /  \\\\__  \\  /    \\\\__  \\   / ___\\_/ __ \\_  __ \\\n"
        "  |    |   / __ \\_\\___ \\|    <  /    Y    \\/ __ \\|   |  \\/ __ \\_/ /_/  >  ___/|  | \\/\n"
        "  |____|  (____  /____  >__|_ \\ \\____|__  (____  /___|  (____  /\\___  / \\___  >__|   \n"
        "               \\/     \\/     \\/         \\/     \\/     \\/     \\/_____/      \\/        \n"
    );
}