import Sentiment from "sentiment";

const sentimentAnalyzer = new Sentiment();

/**
 * Analisa o sentimento de um texto e retorna um score.
 * @param text Texto para análise de sentimento
 * @returns Um objeto contendo score e análise detalhada
 */
export function analyzeSentiment(text: string) {
    const result = sentimentAnalyzer.analyze(text);
    return {
        score: result.score, // Score geral (positivo, negativo, neutro)
        comparative: result.comparative, // Score relativo ao tamanho do texto
        words: {
            positive: result.positive,
            negative: result.negative
        }
    };
}
