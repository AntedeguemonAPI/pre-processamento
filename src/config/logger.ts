import winston from "winston";

// Define o formato do log
const logFormat = winston.format.combine(
    winston.format.timestamp(),
    winston.format.printf(({ timestamp, level, message }) => {
        return `[${timestamp}] ${level.toUpperCase()}: ${message}`;
    })
);

// Configuração do logger
const logger = winston.createLogger({
    level: "info", // Pode ser 'debug', 'info', 'warn', 'error'
    format: logFormat,
    transports: [
        new winston.transports.Console(), // Log no console
        new winston.transports.File({ filename: "logs/app.log" }) // Log em arquivo
    ],
});

export default logger;