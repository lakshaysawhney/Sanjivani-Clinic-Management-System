import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { App } from './pages/App'
import './styles.css'
const queryClient = new QueryClient({defaultOptions:{queries:{retry:(count,error)=> count<3 && (!('status' in error)|| Number(error.status)===0 || Number(error.status)>=500), retryDelay:attempt=>Math.min(1500*2**attempt,12000), refetchOnWindowFocus:true},mutations:{retry:false}}})
ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><QueryClientProvider client={queryClient}><BrowserRouter><App/></BrowserRouter></QueryClientProvider></React.StrictMode>)
