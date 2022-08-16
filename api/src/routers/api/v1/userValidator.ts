import express from 'express'

export default function(req: express.Request, res: express.Response, next: express.NextFunction) {
    const userId = Number(req.params.id)
    
    if (isNaN(userId)) {
        res.status(400)
        next(new Error(`Invalid user ID: ${req.params.id}`))
    }

    next()
}