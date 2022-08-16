import http from 'http'
import https from 'https'
import { Express } from 'express'

export default function startServer(certs: Certificates, app: Express, options: ServerOptions = {}): ServerResult {
    const httpsOptions: https.ServerOptions = {
        SNICallback(domain, cb) {
            const cert = certs[domain]
    
            if (!cert) {
                return cb(new Error('Domain not found'))
            }
    
            cb(null, cert)
        }
    }

    const result: ServerResult = {
        http: http.createServer(app).listen(options.httpPort || 3000)
    }

    if (options.httpsEnabled) {
        result.https = https.createServer(httpsOptions, app).listen(options.httpsPort || 4443)
    }

    return result
}
