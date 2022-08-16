import { Connection } from 'mysql2'
import express from 'express'

export default (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const connection: Connection = req.app.get('db')
    const query = 'SELECT Id FROM users;'

    connection.query(query, (err, results: any[]) => {
        if (err) {
            return next(err)
        }

        const result: number[] = results.map(res => res.Id)

        res.json(result)
    })
}

