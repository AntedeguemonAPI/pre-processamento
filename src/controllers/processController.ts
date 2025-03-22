import { Request, Response, NextFunction } from 'express';
import path from 'path';
import fs from 'fs';
import { preprocessCSV } from '../services/pipeline';

const inputDir = path.join(__dirname, '../data/input');
const outputDir = path.join(__dirname, '../data/output');

export const processFile = async (req: Request, res: Response): Promise<void> => {
  const inputPath = path.join(inputDir, req.params.filename);
  const outputPath = path.join(outputDir, `processed_${req.params.filename}`);

  if (!fs.existsSync(inputPath)) {
    res.status(404).json({ message: 'Arquivo não encontrado' });
    return Promise.resolve();

  }

  try {
    await preprocessCSV(inputPath, outputPath);
    res.json({ message: 'Processamento concluído', outputFile: `processed_${req.params.filename}` });
    return Promise.resolve();
  } catch (error: any) {
    res.status(500).json({ message: 'Erro no processamento', error: error.message });
    return Promise.resolve();
  }
};
