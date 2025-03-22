import natural from "natural";
import logger from "../config/logger";

// Configuração do tokenizador
const tokenizer = new natural.WordTokenizer();

const stemmer = natural.PorterStemmerPt;

const classifier = new natural.BayesClassifier();

/**
 * Inicializa os módulos de PLN e retorna as instâncias configuradas.
 */
export const loadNlpTools = () => {
    logger.info("Biblioteca de NLP inicializada.");
    
    return {
        tokenizer,
        stemmer,
        classifier,
    };
};