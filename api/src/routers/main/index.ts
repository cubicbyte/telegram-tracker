import express from 'express'
import apiRouter from '../api/v1'
import errorHandler from './errorHandler'
import pathSetter from './pathSetter'

const router = express.Router()

router.use(pathSetter)

router.use('/api/v1', apiRouter)
router.use('/public', express.static('public'))

router.get('/', (req, res) => {
    res.render('pages/index')
})

router.get('/api', (req, res) => {
    res.render('pages/api')
})

router.use(errorHandler)

export default router