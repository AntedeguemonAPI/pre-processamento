import { Router } from 'express';
import { processFile } from '../controllers/processController';

const routes = Router();

routes.post('/:filename', processFile);

export default routes;
