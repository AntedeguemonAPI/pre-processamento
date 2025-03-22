import natural from "natural";

const stemmer = natural.PorterStemmerPt;

/**
 * Aplica stemming a um token.
 * @param token Palavra a ser reduzida
 * @returns Palavra reduzida ao radical
 */
export const stem = (token: string): string => {
    return stemmer.stem(token);
};

/**
 * Aplica stemming a uma lista de tokens.
 * @param tokens Lista de palavras
 * @returns Lista de palavras reduzidas ao radical
 */
export const stemTokens = (tokens: string[]): string[] => {
    return tokens.map(stem);
};
