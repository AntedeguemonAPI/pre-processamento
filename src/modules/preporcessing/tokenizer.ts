import natural from "natural";

const tokenizer = new natural.WordTokenizer();

export const tokenize = (text: string): string[] => {
    return tokenizer.tokenize(text);
};
