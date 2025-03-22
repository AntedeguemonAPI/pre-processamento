import { analyzeSentiment } from "../modules/analysis/sentiment";
import { getTopTerms, addDocument } from "../modules/analysis/tfidf";
import { removePunctuation, toLowerCase, trimSpaces } from "../utils/textHelper";

/**
 * Executa o pipeline de NLP em um texto
 * @param text Texto a ser processado
 * @returns Objeto com resultado do processamento
 */
export function processText(text: string) {
    let processedText = toLowerCase(text);
    processedText = removePunctuation(processedText);
    processedText = trimSpaces(processedText);

    addDocument(processedText);
    const sentiment = analyzeSentiment(processedText);
    const topTerms = getTopTerms(0, 5);

    return { processedText, sentiment, topTerms };
}
