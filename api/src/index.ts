
process.chdir(__dirname)
process.chdir('../')

import 'dotenv/config'
import loadCerts from './utils/loadCerts'
import startServer from './utils/startServer'
import mysql from 'mysql2'
import { TelegramClient } from 'telegram'
import express from 'express'
import mainRouter from './routers/main'
import { telegramClientOptions, telegramOptions, databaseOptions, serverOptions } from './options'



async function main() {
    const app = express()
    const connection = mysql.createConnection(databaseOptions)
    const certs = loadCerts(String(process.env.CERTS_PATH))
    const client = new TelegramClient(...telegramOptions)

    startServer(certs, app, serverOptions)
    await client.start(telegramClientOptions)
    client.session.save()

    app.set('client', client)
    app.set('db', connection)
    app.set('json spaces', 4)
    app.set('view engine', 'ejs')

    app.use('/', mainRouter)
}

main()

