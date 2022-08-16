import prompt from './utils/prompt'
import { UserAuthParams } from 'telegram/client/auth'
import { StoreSession } from 'telegram/sessions'
import { ConnectionOptions } from 'mysql2'

export const serverOptions: ServerOptions = {
    httpPort: Number(process.env.SERVER_HTTP_PORT),
    httpsPort: Number(process.env.SERVER_HTTPS_PORT),
    httpsEnabled: process.env.SERVER_HTTPS_ENABLED === 'true'
}

export const databaseOptions: ConnectionOptions = {
    database: process.env.DATABASE_NAME,
    user: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD,
    host: process.env.DATABASE_HOST,
    port: Number(process.env.DATABASE_PORT)
}

export const telegramOptions = [
    new StoreSession(String(process.env.SESSIONS_PATH)),
    Number(process.env.TELEGRAM_API_ID),
    String(process.env.TELEGRAM_API_HASH),
    {}
] as const

export const telegramClientOptions: UserAuthParams = {
    phoneNumber: prompt({
        type: 'text',
        name: 'value',
        message: 'Please enter your phone number'
    }),
    password: prompt({
        type: 'password',
        name: 'value',
        message: 'Please enter your password'
    }),
    phoneCode: prompt({
        type: 'text',
        name: 'value',
        message: 'Please enter the secret code'
    }),
    onError: (err) => console.log(err)
}
