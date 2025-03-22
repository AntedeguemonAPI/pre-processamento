import dotenv from "dotenv";

// Carrega as variáveis do arquivo .env
dotenv.config();

export const ENV = {
    NODE_ENV: process.env.NODE_ENV || "development",
    PORT: process.env.PORT ? parseInt(process.env.PORT) : 3000,
    LOG_LEVEL: process.env.LOG_LEVEL || "info",
    CSV_FILE_PATH: process.env.CSV_FILE_PATH || "./data/input/dataset.csv",
};