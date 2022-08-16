interface ServerOptions {
    httpPort?: number
    httpsPort?: number
    httpsEnabled?: boolean
}

interface ServerResult {
    http: import('http').Server
    https?: import('https').Server
}