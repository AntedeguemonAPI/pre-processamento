import fs from 'fs';
import csvParser from 'csv-parser';
import { processText } from './textPipeline';

/**
 * Processa um CSV, aplicando NLP nos textos de uma coluna específica
 * @param inputPath Caminho do CSV de entrada
 * @param outputPath Caminho do CSV processado de saída
 * @param columnName Nome da coluna a ser analisada (exemplo: "texto")
 */
export async function preprocessCSV(inputPath: string, outputPath: string, columnName: string = 'texto') {
    const results: any[] = [];

    return new Promise<void>((resolve, reject) => {
        fs.createReadStream(inputPath)
            .pipe(csvParser())
            .on('data', (row) => {
                if (row[columnName]) {
                    const analysis = processText(row[columnName]);
                    results.push({ ...row, ...analysis });
                } else {
                    results.push(row);
                }
            })
            .on('end', () => {
                fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
                resolve();
            })
            .on('error', (error) => reject(error));
    });
}
