import { useRef, useState, type ReactNode } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { api } from '../api'
export function ErrorBox({error}:{error:unknown}) {return error?<div role="alert" className="error">{error instanceof Error?error.message:String(error)}</div>:null}
export function Empty({children}:{children:ReactNode}) {return <div className="empty">{children}</div>}
export function Field({label,children}:{label:string;children:ReactNode}) {return <label className="field"><span>{label}</span>{children}</label>}
export function Fee({show}:{show?:boolean}) {return show?<span className="fee" title="Special fee arrangement. Financial review required." aria-label="Special fee review">₹!</span>:null}
export function useSave(){
 const [error,setError]=useState<unknown>(null),[busy,setBusy]=useState(false)
 const pending=useRef<{content:string;key:string}|null>(null)
 const client=useQueryClient()
 async function save<T>(path:string,body:unknown,done?:(result:T)=>void){
  const content=path+JSON.stringify(body)
  if(pending.current?.content!==content)pending.current={content,key:crypto.randomUUID()}
  setBusy(true);setError(null)
  try {const result=await api<T>(path,body,pending.current.key);pending.current=null;await client.invalidateQueries();done?.(result);if(!path.startsWith('auth/')&&path!=='sync/')void api('sync/',{}).catch(()=>{});return result}
  catch(e){setError(e)}finally{setBusy(false)}
 }
 return {save,error,busy,setError}
}
