import * as DialogPrimitive from '@radix-ui/react-dialog'
import type { ReactNode } from 'react'
import { X } from 'lucide-react'
// shadcn/ui-style composition of accessible Radix dialog primitives.
export function Dialog({open,onClose,title,children}:{open:boolean;onClose:()=>void;title:string;children:ReactNode}) {
 return <DialogPrimitive.Root open={open} onOpenChange={v=>!v&&onClose()}><DialogPrimitive.Portal><DialogPrimitive.Overlay className="dialog-overlay"/><DialogPrimitive.Content className="dialog-content" aria-describedby={undefined}><div className="dialog-title"><DialogPrimitive.Title>{title}</DialogPrimitive.Title><DialogPrimitive.Close aria-label="Close dialog"><X size={18}/></DialogPrimitive.Close></div>{children}</DialogPrimitive.Content></DialogPrimitive.Portal></DialogPrimitive.Root>
}
