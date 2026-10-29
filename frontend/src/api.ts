export class ApiError extends Error { constructor(public status:number, message:string){super(message)} }
let csrf = ''
export async function api<T>(path:string, body?:unknown, key?:string):Promise<T> {
  if (body !== undefined && !csrf) { const result = await api<{csrfToken:string}>('auth/csrf/'); csrf = result.csrfToken }
  let response:Response
  try {
    response = await fetch('/api/' + path, {method:body === undefined?'GET':'POST', credentials:'same-origin', headers: body === undefined?{}:{'Content-Type':'application/json','X-CSRFToken':csrf,'Idempotency-Key':key || crypto.randomUUID()}, body:body === undefined?undefined:JSON.stringify(body), signal:AbortSignal.timeout(45000)})
  } catch { throw new ApiError(0, 'The connection was interrupted. Your form is preserved. Check the saved record before retrying.') }
  const text = await response.text()
  let value
  try { value = JSON.parse(text) } catch { throw new ApiError(response.status >= 500?503:response.status, 'The clinic system is starting or reconnecting. Please retry shortly.') }
  if (!response.ok) throw new ApiError(response.status, typeof value.detail === 'string'?value.detail:JSON.stringify(value))
  if (path === 'auth/login/' || path === 'auth/logout/') csrf = ''
  return value as T
}
export const money = (paise:number) => new Intl.NumberFormat('en-IN', {style:'currency', currency:'INR', maximumFractionDigits:2}).format(paise/100)
export const localDate = () => new Intl.DateTimeFormat('en-CA', {timeZone:'Asia/Kolkata'}).format(new Date())
export const monthNow = () => localDate().slice(0,7)
export const shiftDay = (date:string, offset:number) => { const d = new Date(date+'T12:00:00Z'); d.setUTCDate(d.getUTCDate()+offset); return d.toISOString().slice(0,10) }
