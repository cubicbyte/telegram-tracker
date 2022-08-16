import { createSecureContext, SecureContext } from 'tls'
import { readFileSync, readdirSync } from 'fs'
import { join } from 'path'

export default function loadCerts(dirpath: string): Certificates {
    const domains = readdirSync(dirpath)
    const certs: Certificates = {}

    for (const domain of domains) {
        const cert: SecureContext = createSecureContext({
            cert: readFileSync(join(dirpath, domain, 'fullchain.pem'), 'utf8'),
            key: readFileSync(join(dirpath, domain, 'privkey.pem'), 'utf8')
        }).context

        certs[domain] = cert
    }

    return certs
}
