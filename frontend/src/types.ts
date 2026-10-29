export type Role = 'ADMIN' | 'RECEPTIONIST' | 'THERAPIST'
export interface User {id:number; username:string; full_name:string; role:Role; provider_id:number|null}
export interface Provider {id:number; name:string; full_name:string; active:boolean; order:number}
export interface Therapy {code:string; name:string; fee_paise:number; group:boolean}
export interface Catalog {providers:Provider[]; therapies:Therapy[]; slots:string[]; today:string; operating_days:number[]}
export type Status = 'Scheduled'|'Completed'|'Cancelled'
export interface Participant {id?:number; patient_id:number; name:string; status:Status; special_fee?:boolean}
export interface Session {id:string; date:string; slot:number; therapy:string; therapy_name:string; providers:number[]; participants:Participant[]; version:number; ends_at:string; patient_status?:Status}
export interface Schedule {date:string; published:boolean; sessions:Session[]}
export interface Patient {id:number; name:string; active:boolean; special_fee:boolean; weekly:number; monthly:number; balance_paise:number}
export interface PatientDetails extends Patient {completed:number; cancelled:number; categories:Record<string,number>; providers:Record<string,number>; total_payments_paise:number; total_charges_paise:number; history:Session[]; plans:{weekly:number;monthly:number;effective_date:string}[]}
export interface LedgerEntry {id:string; kind:string; amount_paise:number; description:string; effective_at:string; created_at:string; actor:string; reverses:string|null; reversed:boolean; running_balance_paise:number}
export interface Staff extends User {email:string; active:boolean; pending_activation:boolean; specialization:string; display_name:string; display_order:number}
export interface Frequency extends Patient {actual_weekly:number; actual_monthly:number; cancelled:number}
