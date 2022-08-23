
process.chdir(__dirname)
process.chdir('../')

import 'dotenv/config'
import mysql from 'mysql2'
import { TelegramClient } from 'telegram'
import express from 'express'
import mainRouter from './routers/main'
import { telegramClientOptions, telegramOptions, databaseOptions } from './options'

const PORT = process.env.HTTP_PORT || 3000


async function main() {

    const app = express()
    const connection = mysql.createConnection(databaseOptions)

    const client = new TelegramClient(...telegramOptions)
    await client.start(telegramClientOptions)
    
    client.session.save()

    app.listen(PORT, () => console.log(`App avaliable on http://localhost:${PORT}`))

    app.set('client', client)
    app.set('db', connection)
    app.set('json spaces', 4)
    app.set('view engine', 'ejs')

    app.use('/', mainRouter)
}

main()

