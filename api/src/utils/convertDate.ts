export default function convertDate(date: Date): string {
    return `FROM_UNIXTIME(${Number(date) / 1000})`
}

