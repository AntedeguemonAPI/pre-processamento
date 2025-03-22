import { removeStopwords } from "./stopwords";
import { tokenize } from "./tokenizer";

/**
 * Remove acentos e caracteres especiais.
 * @param text Texto de entrada
 * @returns Texto normalizado
 */
export const normalizeText = (text: string): string => {
    return text
        .toLowerCase()
        .normalize("NFD") // Separa caracteres acentuados
        .replace(/[\u0300-\u036f]/g, "") // Remove acentos
        .replace(/[^\w\s]/gi, ""); // Remove caracteres especiais
};

/**
 * Normaliza um texto e aplica tokenização + remoção de stopwords.
 * @param text Texto de entrada
 * @returns Lista de tokens normalizados
 */
export const preprocessText = (text: string): string[] => {
    const normalized = normalizeText(text);
    const tokens = tokenize(normalized);
    return removeStopwords(tokens);
};
