import { test, expect, type Page } from '@playwright/test'
import { randomUUID } from 'node:crypto'
import type { Catalog, Patient, PatientDetails, Schedule, Session } from '../src/types'

async function loginAdmin(page:Page) {
 await page.goto('/')
 await page.getByLabel('Username',{exact:true}).fill('demo_admin')
 await page.getByLabel('Password',{exact:true}).fill(process.env.E2E_PASSWORD!)
 await page.getByRole('button',{name:'Sign in',exact:true}).click()
 await expect(page.getByRole('heading',{name:/Daily schedule/})).toBeVisible()
}

async function write<T>(page:Page,path:string,data:unknown):Promise<T> {
 const csrf=await (await page.request.get('/api/auth/csrf/')).json()
 const result=await page.request.post('/api/'+path,{data,headers:{'X-CSRFToken':csrf.csrfToken,'Idempotency-Key':randomUUID()}})
 expect(result.status(),await result.text()).toBe(200)
 return result.json()
}

function operationalDay(today:string,offset:number) {
 const date=new Date(today+'T12:00:00Z')
 date.setUTCDate(date.getUTCDate()+offset)
 if(date.getUTCDay()===0)date.setUTCDate(date.getUTCDate()+1)
 return date.toISOString().slice(0,10)
}

test('ordinary replacement reopens one child and displays original cancellation history',async({page})=>{
 await loginAdmin(page)
 const catalog:Catalog=await (await page.request.get('/api/catalog/')).json()
 const day=operationalDay(catalog.today,14)
 const suffix=randomUUID().slice(0,8)
 const first=await write<Patient>(page,'patients/',{name:'Synthetic Original '+suffix})
 const second=await write<Patient>(page,'patients/',{name:'Synthetic Replacement '+suffix})
 const session=await write<Session>(page,'sessions/',{date:day,slot:0,therapy:'OT',providers:[catalog.providers[0].id],participants:[{patient_id:first.id}]})
 await page.getByLabel('Schedule date').fill(day)
 await page.locator('.slot').filter({hasText:first.name}).click()
 await page.getByLabel('Search for a patient').fill(second.name)
 await page.getByRole('button',{name:new RegExp(second.name)}).click()
 await page.getByRole('button',{name:'Save appointment',exact:true}).click()
 await expect(page.locator('.cell-name').filter({hasText:second.name})).toBeVisible()
 await page.locator('.slot').filter({hasText:second.name}).click()
 await expect(page.getByLabel('Status for '+second.name)).toHaveCount(1)
 await expect(page.getByLabel('Status for '+first.name)).toHaveCount(0)
 await page.getByRole('button',{name:'Save appointment',exact:true}).click()
 await page.getByRole('button',{name:'1 cancelled participations',exact:true}).click()
 await expect(page.getByRole('heading',{name:'Cancelled participation history'})).toBeVisible()
 await expect(page.getByRole('row').filter({hasText:first.name})).toContainText(day)
 const daily:Schedule=await (await page.request.get('/api/schedule/?date='+day)).json()
 expect(daily.sessions.find(s=>s.id===session.id)?.participants.map(p=>p.patient_id)).toEqual([second.id])
 expect(daily.cancelled_history[0].providers).toEqual([catalog.providers[0].id])
 await page.screenshot({path:'test-results/ordinary-replacement-history.png',fullPage:true})
})

test('shared group correction bills each completed child once and retains cancellation',async({page})=>{
 await loginAdmin(page)
 const catalog:Catalog=await (await page.request.get('/api/catalog/')).json()
 const day=operationalDay(catalog.today,-7)
 const suffix=randomUUID().slice(0,8)
 const children=await Promise.all(['Alpha','Beta','Gamma'].map(name=>write<Patient>(page,'patients/',{name:'Synthetic Group '+name+' '+suffix})))
 const providers=catalog.providers.slice(1,3).map(p=>p.id)
 let session=await write<Session>(page,'sessions/',{date:day,slot:2,therapy:'GROUP',providers,participants:children.map((p,i)=>({patient_id:p.id,status:i===2?'Cancelled':'Completed'}))})
 for(const child of children.slice(0,2)) {
  const profile:PatientDetails=await (await page.request.get('/api/patients/'+child.id+'/?month='+day.slice(0,7))).json()
  expect(profile.completed).toBe(1)
  expect(profile.balance_paise).toBe(-90000)
  expect(Object.values(profile.providers)).toEqual([1,1])
 }
 for(const provider of providers)expect((await (await page.request.get('/api/history/?month='+day.slice(0,7)+'&provider='+provider)).json()).total).toBe(1)
 await page.getByLabel('Schedule date').fill(day)
 await page.locator('.slot').filter({hasText:children[0].name}).first().click()
 await page.getByLabel('Status for '+children[0].name).selectOption('Cancelled')
 await page.getByRole('button',{name:'Save appointment',exact:true}).click()
 await expect(page.locator('.cell-name').filter({hasText:children[0].name})).toHaveCount(0)
 const profile:PatientDetails=await (await page.request.get('/api/patients/'+children[0].id+'/?month='+day.slice(0,7))).json()
 expect(profile.balance_paise).toBe(0)
 expect(profile.completed).toBe(0)
 expect(profile.cancelled).toBe(1)
 session=await (await page.request.get('/api/sessions/'+session.id+'/')).json()
 expect(session.participants.filter(p=>p.status==='Completed')).toHaveLength(1)
 await page.getByRole('button',{name:'2 cancelled participations',exact:true}).click()
 await expect(page.getByRole('row').filter({hasText:children[0].name})).toContainText('Cancelled')
 await page.screenshot({path:'test-results/group-correction-history.png',fullPage:true})
})
