import { Router } from 'express'
import userHistoryHandler from './userHistoryHandler'
import userHandler from './userHandler'
import usersHandler from './usersHandler'
import userValidator from './userValidator'

const router = Router()

router.get('/', (req, res) => {
    res.render('pages/api-v1')
})

router.get('/users', usersHandler)
router.use('/user/:id', userValidator)
router.get('/user/:id', userHandler)
router.get('/user/:id/history', userHistoryHandler)

export default router
