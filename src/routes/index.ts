import { Router } from 'express';
import uploadRoutes from './uploadRoutes';
import processRoutes from './processRoutes';

const router = Router();

router.use('/upload', uploadRoutes);
router.use('/process', processRoutes);

export default router;