/**
 * Remove pontuações e caracteres especiais de um texto
 * @param text Texto de entrada
 * @returns Texto sem pontuação
 */
export function removePunctuation(text: string): string {
    return text.replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, "");
}

/**
 * Converte um texto para minúsculas
 * @param text Texto de entrada
 * @returns Texto em letras minúsculas
 */
export function toLowerCase(text: string): string {
    return text.toLowerCase();
}

/**
 * Remove espaços extras no texto
 * @param text Texto de entrada
 * @returns Texto sem espaços extras
 */
export function trimSpaces(text: string): string {
    return text.replace(/\s+/g, " ").trim();
}
