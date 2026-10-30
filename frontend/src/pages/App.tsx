import { useState } from 'react'
import { NavLink, Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { CalendarDays, Users, Activity, Wallet, Bell, LogOut, Sprout, Settings, RefreshCw } from 'lucide-react'
import { api, ApiError } from '../api'
import type { User, Catalog } from '../types'
import { ErrorBox, Field, useSave } from '../components/common'
import { SchedulePage } from './Schedule'
import { PatientsPage, PatientPage, FrequencyPage, FinancePage } from './Patients'
import { HistoryPage, StaffPage, NotificationsPage, ProfilePage } from './Operations'

function Brand(){return <div className="brand"><div className="brand-mark"><Sprout size={25}/></div><div><strong>Sanjivani</strong><small>a ray of hope</small></div></div>}
function Login({onLogin}:{onLogin:()=>void}){
 const [username,setUsername]=useState(''),[password,setPassword]=useState(''),[shared,setShared]=useState(false),[reset,setReset]=useState(false),[email,setEmail]=useState(''),[sent,setSent]=useState(false)
 const {save,error,busy}=useSave()
 return <div className="auth-layout"><section className="auth-story"><Brand/><div><span className="eyebrow">A LITTLE MORE CARE. EVERY DAY.</span><h1>More time for<br/>what matters.</h1><p>A thoughtful workspace for your clinic.<br/>Schedules, progress and care, together.</p></div><small>Sanjivani Clinic Management System</small></section><main className="auth-form"><h2>{reset?'Reset your password':'Welcome back'}</h2><p className="muted">{reset?'We will email a secure link if the account is eligible.':'Sign in to your clinic workspace.'}</p><form onSubmit={e=>{e.preventDefault();void save(reset?'auth/reset/':'auth/login/',reset?{email}:{username,password,shared_computer:shared},()=>reset?setSent(true):onLogin())}}>{reset?<Field label="Email address"><input type="email" autoComplete="email" required value={email} onChange={e=>setEmail(e.target.value)}/></Field>:<><Field label="Username"><input autoComplete="username" required value={username} onChange={e=>setUsername(e.target.value)}/></Field><Field label="Password"><input type="password" autoComplete="current-password" required value={password} onChange={e=>setPassword(e.target.value)}/></Field><label className="check"><input type="checkbox" checked={shared} onChange={e=>setShared(e.target.checked)}/> I am using a shared computer</label></>}<ErrorBox error={error}/>{sent&&<p role="status">Request received. Check your email or contact your administrator.</p>}<button className="primary wide" disabled={busy}>{busy?'Please wait...':reset?'Send reset link':'Sign in'}</button></form><button className="text-button" onClick={()=>setReset(!reset)}>{reset?'Back to sign in':'Forgot your password?'}</button><p className="privacy-note">For authorized clinic staff. Patient information stays in your secure workspace.</p></main></div>
}
function Activate(){
 const [token]=useState(()=>new URLSearchParams(location.hash.slice(1)).get('token')||''); const [password,setPassword]=useState(''),[done,setDone]=useState(false)
 const {save,error,busy}=useSave()
 return <main className="activation"><Brand/><h1>Set your password</h1>{done?<a href="/">Password saved. Sign in</a>:<form onSubmit={e=>{e.preventDefault();void save('auth/activate/',{token,password},()=>{history.replaceState(null,'',location.pathname);setDone(true)})}}><Field label="New password (at least 12 characters)"><input type="password" autoComplete="new-password" minLength={12} required value={password} onChange={e=>setPassword(e.target.value)}/></Field><ErrorBox error={error}/><button className="primary" disabled={busy}>Save password</button></form>}</main>
}
export function App(){
 const client=useQueryClient(),navigate=useNavigate()
 const me=useQuery({queryKey:['me'],queryFn:()=>api<User>('auth/me/')})
 const catalog=useQuery({queryKey:['catalog'],queryFn:()=>api<Catalog>('catalog/'),enabled:!!me.data})
 const [logoutError,setLogoutError]=useState<unknown>(null)
 if(location.pathname==='/activate')return <Activate/>
 if(me.isPending || (me.error instanceof ApiError && (me.error.status===0||me.error.status>=500)))return <main className="connecting"><Brand/><div className="loading-ring"/><h1>Connecting to Sanjivani</h1><p>The clinic system is starting or reconnecting.<br/>Your workspace will open when it is ready.</p><button onClick={()=>void me.refetch()}><RefreshCw size={15}/> Retry</button>{me.error&&<ErrorBox error={me.error}/>}</main>
 if(!me.data)return <Login onLogin={()=>{client.clear();navigate('/schedule')}}/>
 if(!catalog.data)return <main className="connecting"><Brand/><p>Loading clinic settings...</p><ErrorBox error={catalog.error}/><button onClick={()=>void catalog.refetch()}>Retry</button></main>
 const user=me.data, therapist=user.role==='THERAPIST'
 const links=therapist?[['/schedule','My Schedule',CalendarDays],['/history','My Session History',Activity]] as const:[['/schedule','Daily Schedule',CalendarDays],['/patients','Patients',Users],['/history','Therapist History',Activity],['/frequency','Frequency',Activity],['/finance','Payments & Dues',Wallet],['/notifications','Notifications',Bell]] as const
 return <div className="app"><header className="app-header"><Brand/><nav aria-label="Main navigation">{links.map(([to,label,Icon])=><NavLink to={to} key={to}><Icon size={16}/><span>{label}</span></NavLink>)}{user.role==='ADMIN'&&<NavLink to="/staff"><Settings size={16}/><span>Staff</span></NavLink>}</nav><div className="account"><NavLink to="/profile" title="Profile and password">{user.full_name}<small>{user.role.toLowerCase()}</small></NavLink><button aria-label="Sign out" title="Sign out" onClick={()=>{void api('auth/logout/',{}).then(()=>{client.clear();navigate('/')}).catch(setLogoutError)}}><LogOut size={17}/></button></div></header><ErrorBox error={logoutError}/><main className="workspace"><Routes><Route path="/schedule" element={<SchedulePage user={user} catalog={catalog.data}/>}/><Route path="/history" element={<HistoryPage user={user} catalog={catalog.data}/>}/><Route path="/profile" element={<ProfilePage user={user}/>}/>{!therapist&&<><Route path="/patients" element={<PatientsPage/>}/><Route path="/patients/:id" element={<PatientPage catalog={catalog.data}/>}/><Route path="/frequency" element={<FrequencyPage/>}/><Route path="/finance" element={<FinancePage/>}/><Route path="/notifications" element={<NotificationsPage/>}/></>}{user.role==='ADMIN'&&<Route path="/staff" element={<StaffPage/>}/>}<Route path="*" element={<Navigate to="/schedule" replace/>}/></Routes></main><footer className="app-footer"><span>All times in IST</span><span>Private clinic workspace</span></footer></div>
}
