interface Env { BACKEND_ORIGIN:string; PROXY_SECRET:string }
interface Context {request:Request;env:Env}
export async function onRequest({request,env}:Context):Promise<Response>{
 const url=new URL(request.url)
 if(!env.BACKEND_ORIGIN||!env.PROXY_SECRET)return Response.json({detail:'Clinic connection is not configured.'},{status:503})
 const upstream=new URL(env.BACKEND_ORIGIN)
 if(upstream.protocol!=='https:'||!upstream.hostname.endsWith('.onrender.com')||upstream.username||upstream.password)return Response.json({detail:'Invalid clinic connection.'},{status:503})
 if(!url.pathname.startsWith('/api/')||url.pathname==='/api/maintenance/')return new Response(null,{status:404})
 if(!['GET','POST','HEAD'].includes(request.method))return new Response(null,{status:405})
 const origin=request.headers.get('Origin')
 if(origin&&origin!==url.origin)return Response.json({detail:'Cross-origin requests are not allowed.'},{status:403})
 if(Number(request.headers.get('Content-Length')||0)>1_048_576)return new Response(null,{status:413})
 const headers=new Headers()
 for(const key of ['Content-Type','Accept','Cookie','X-CSRFToken','Idempotency-Key','Referer']){const value=request.headers.get(key);if(value)headers.set(key,value)}
 if(origin)headers.set('Origin',origin)
 headers.set('X-Clinic-Proxy',env.PROXY_SECRET)
 headers.set('X-Clinic-Client-IP',request.headers.get('CF-Connecting-IP')||'unknown')
 headers.set('X-Forwarded-Proto','https')
 upstream.pathname=url.pathname;upstream.search=url.search
 try{
  const response=await fetch(upstream,{method:request.method,headers,body:request.method==='POST'?request.body:undefined,redirect:'manual',signal:AbortSignal.timeout(35000)})
  const output=new Headers(response.headers)
  output.set('Cache-Control','no-store, private')
  output.delete('Access-Control-Allow-Origin')
  output.delete('Server')
  const location=output.get('Location')
  if(location){const redirect=new URL(location,upstream);if(redirect.origin!==upstream.origin)return Response.json({detail:'Unexpected upstream redirect.'},{status:502});output.set('Location',url.origin+redirect.pathname+redirect.search)}
  return new Response(response.body,{status:response.status,headers:output})
 }catch{return Response.json({detail:'The clinic system is starting or reconnecting. Please retry shortly.'},{status:503,headers:{'Cache-Control':'no-store'}})}
}
