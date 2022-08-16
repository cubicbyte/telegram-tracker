import { Connection } from 'mysql2'
import convertDate from '../../../utils/convertDate'
import express from 'express'

export default (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const connection: Connection = req.app.get('db')

    const userId = req.params.id
    const { from, to } = req.query

    let query = 'SELECT UserStatus, UpdateTime FROM statuses WHERE Id = ?'

    if (to || from) {
        query += ' AND UpdateTime '
    }

    if (to && from) {
        query += 'BETWEEN '
    } else if (to && !from) {
        query += '< '
    } else if (!to && from) {
        query += '> '
    }

    if (from) {
        const dateValue = isNaN(Number(from)) ? from.toString() : Number(from)
        const fromDate = new Date(dateValue)
        
        if (fromDate.toString() === 'Invalid Date') {
            return next(new Error(`Invalid date`))
        }

        query += convertDate(fromDate)
    }

    if (from && to) {
        query += ' AND '
    }

    if (to) {
        const dateValue = isNaN(Number(to)) ? to.toString() : Number(to)
        const toDate = new Date(dateValue)
        
        if (toDate.toString() === 'Invalid Date') {
            return next(new Error(`Invalid date`))
        }

        query += convertDate(toDate)
    }

    query += ';'

    connection.query(query, [userId], (err, results: any[]) => {
        if (err) {
            return next(err)
        }

        res.json(results)
    })
}