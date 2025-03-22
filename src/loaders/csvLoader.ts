import fs from "fs";
import path from "path";
import csvParser from "csv-parser";
import logger from "../config/logger";
import { ENV } from "../config/env";

export interface CsvRow {
    [key: string]: string;
}

/**
 * Carrega um arquivo CSV e retorna os dados como um array de objetos.
 * @param filePath Caminho do arquivo CSV
 * @returns Promise com os dados do CSV
 */
export const loadCsv = async (filePath: string = ENV.CSV_FILE_PATH): Promise<CsvRow[]> => {
    return new Promise((resolve, reject) => {
        const file = path.resolve(filePath);
        
        if (!fs.existsSync(file)) {
            logger.error(`Arquivo CSV não encontrado: ${file}`);
            reject(new Error("Arquivo CSV não encontrado"));
            return;
        }

        const results: CsvRow[] = [];
        
        fs.createReadStream(file)
            .pipe(csvParser())
            .on("data", (row) => results.push(row))
            .on("end", () => {
                logger.info(`Arquivo CSV carregado com ${results.length} linhas.`);
                resolve(results);
            })
            .on("error", (error) => {
                logger.error(`Erro ao processar CSV: ${error.message}`);
                reject(error);
            });
    });
};
