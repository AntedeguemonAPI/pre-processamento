import fs from "fs";
import csvParser from "csv-parser";
import { format } from "fast-csv";

/**
 * Lê um arquivo CSV e retorna um array de objetos
 * @param filePath Caminho do arquivo CSV
 * @returns Promise com os dados do CSV
 */
export async function readCSV(filePath: string): Promise<any[]> {
    return new Promise((resolve, reject) => {
        const results: any[] = [];
        fs.createReadStream(filePath)
            .pipe(csvParser())
            .on("data", (data) => results.push(data))
            .on("end", () => resolve(results))
            .on("error", (error) => reject(error));
    });
}

/**
 * Salva dados em um arquivo CSV
 * @param filePath Caminho do arquivo de saída
 * @param data Array de objetos para salvar
 */
export function writeCSV(filePath: string, data: any[]) {
    const ws = fs.createWriteStream(filePath);
    const csvStream = format({ headers: true });
    data.forEach((row) => csvStream.write(row));
    csvStream.pipe(ws);
    csvStream.end();
}

/**
 * Lê um arquivo JSON
 * @param filePath Caminho do JSON
 * @returns Promise com os dados do JSON
 */
export async function readJSON(filePath: string): Promise<any> {
    const data = await fs.promises.readFile(filePath, "utf-8");
    return JSON.parse(data);
}

/**
 * Salva dados em um arquivo JSON
 * @param filePath Caminho do arquivo JSON
 * @param data Objeto para salvar
 */
export async function writeJSON(filePath: string, data: any) {
    await fs.promises.writeFile(filePath, JSON.stringify(data, null, 2), "utf-8");
}
