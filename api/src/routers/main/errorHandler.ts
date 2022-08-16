import express from 'express'

export default (err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
    res.end(`Error: ${err.message}`)
}