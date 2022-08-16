import { TelegramClient, Api } from 'telegram'
import express from 'express'

export default async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const client: TelegramClient = req.app.get('client')
    const userId = req.params.id
    const request = new Api.users.GetFullUser({ id: userId })

    try {
        const response = await client.invoke(request)
        const user: any = response.users[0]
        const result = {
            id: user.id,
            firstName: user.firstName,
            lastName: user.lastName,
            username: user.username,
            online: user.status instanceof Api.UserStatusOnline
        }
        
        res.json(result)
    }
    
    catch (err: any) {
        res.status(404)
        next(new Error(`User with ID ${userId} not found`, {cause: err}))
    }
}