import prompt from './utils/prompt'
import { UserAuthParams } from 'telegram/client/auth'
import { StoreSession } from 'telegram/sessions'
import { ConnectionOptions } from 'mysql2'

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
