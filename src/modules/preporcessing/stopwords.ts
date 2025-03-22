// Lista personalizada de stopwords (pode ser expandida)
const customStopwords = new Set([
    "de", "da", "do", "em", "para", "com", "o", "a", "os", "as", "e", "é", "um", "uma"
]);

/**
 * Remove stopwords de um array de tokens.
 * @param tokens Lista de tokens
 * @returns Tokens filtrados sem stopwords
 */
export const removeStopwords = (tokens: string[]): string[] => {
    return tokens.filter(token => !customStopwords.has(token.toLowerCase()));
};
