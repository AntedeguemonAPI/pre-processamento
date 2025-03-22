import { Request, Response } from 'express';
import path from 'path';
import fs from 'fs';

const uploadDir = path.join(__dirname, '../data/input');

export const uploadFile = (req: Request, res: Response): Promise<void> => {
    if (!req.file) {
        res.status(400).json({ message: 'Nenhum arquivo enviado' });
        return Promise.resolve();
    }
    res.json({ message: 'Arquivo recebido com sucesso', file: req.file.filename });
    return Promise.resolve();
};

export const downloadFile = (req: Request, res: Response): Promise<void> => {
    const filePath = path.join(uploadDir, req.params.filename);
    if (fs.existsSync(filePath)) {
        res.download(filePath);
    } else {
        res.status(404).json({ message: 'Arquivo não encontrado' });
    }
    return Promise.resolve();
};
