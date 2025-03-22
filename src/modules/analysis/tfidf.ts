import natural from "natural";

const TfIdf = natural.TfIdf;
const tfidf = new TfIdf();

/**
 * Adiciona um documento ao modelo TF-IDF
 * @param document Texto a ser indexado
 */
export function addDocument(document: string) {
    tfidf.addDocument(document);
}

/**
 * Obtém a relevância de cada termo em um documento específico
 * @param term Palavra a ser analisada
 * @param docIndex Índice do documento no corpus
 * @returns Score do TF-IDF para o termo no documento específico
 */
export function getTermScore(term: string, docIndex: number) {
    const scores: { term: string; score: number }[] = [];
    tfidf.tfidfs(term, (i, measure) => {
        if (i === docIndex) {
            scores.push({ term, score: measure });
        }
    });
    return scores;
}

/**
 * Obtém os termos mais relevantes do documento
 * @param docIndex Índice do documento
 * @returns Lista de termos e seus scores
 */
export function getTopTerms(docIndex: number, topN = 5) {
    const terms: { term: string; score: number }[] = [];
    tfidf.listTerms(docIndex).slice(0, topN).forEach(item => {
        terms.push({ term: item.term, score: item.tfidf });
    });
    return terms;
}
