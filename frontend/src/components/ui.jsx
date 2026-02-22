export function Card({ children }) {
  return <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4 shadow-lg">{children}</div>
}

export function Button({ className = '', ...props }) {
  return (
    <button
      className={`rounded-xl bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 ${className}`}
      {...props}
    />
  )
}

export function Input(props) {
  return <input className="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-white" {...props} />
}
