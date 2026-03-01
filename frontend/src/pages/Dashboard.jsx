import { useEffect, useMemo, useState } from 'react'
import { useEffect, useState } from 'react'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { Button, Card, Input } from '../components/ui'
import { getDailyPerformance, getMonthlyPnl, runSync, updateToken } from '../lib/api'

const BROKERS = [
  { value: 'kotak', label: 'Kotak Neo' },
  { value: 'zerodha', label: 'Zerodha Kite' }
]

export default function Dashboard() {
  const [memberId, setMemberId] = useState(1)
  const [aggregate, setAggregate] = useState(false)
  const [dailyRows, setDailyRows] = useState([])
  const [monthlyRows, setMonthlyRows] = useState([])
  const [tokenPayload, setTokenPayload] = useState({
    broker_name: 'kotak',
    access_token: '',
    api_key: ''
  })

  const isZerodha = useMemo(() => tokenPayload.broker_name === 'zerodha', [tokenPayload.broker_name])
  const [tokenPayload, setTokenPayload] = useState({ broker_name: 'kotak', access_token: '', api_key: '' })

  const loadData = async () => {
    const [daily, monthly] = await Promise.all([
      getDailyPerformance(memberId),
      getMonthlyPnl(memberId, aggregate)
    ])
    setDailyRows(daily)
    setMonthlyRows(monthly)
  }

  useEffect(() => {
    loadData()
  }, [memberId, aggregate])

  const handleBrokerChange = (brokerName) => {
    setTokenPayload((prev) => ({
      ...prev,
      broker_name: brokerName,
      api_key: brokerName === 'zerodha' ? prev.api_key : ''
    }))
  }

  return (
    <div className="min-h-screen bg-slate-950 p-8 text-slate-100">
      <div className="mx-auto grid max-w-7xl gap-6">
        <h1 className="text-3xl font-bold">Multi-Broker Trading Journal</h1>

        <Card>
          <div className="grid gap-3 md:grid-cols-4">
            <Input
              type="number"
              value={memberId}
              onChange={(e) => setMemberId(Number(e.target.value))}
              placeholder="Member ID"
            />
            <select
              className="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-white"
              value={tokenPayload.broker_name}
              onChange={(e) => handleBrokerChange(e.target.value)}
            >
              {BROKERS.map((broker) => (
                <option key={broker.value} value={broker.value}>
                  {broker.label}
                </option>
              ))}
            </select>
            <Input
              value={tokenPayload.access_token}
              onChange={(e) => setTokenPayload({ ...tokenPayload, access_token: e.target.value })}
              placeholder={isZerodha ? 'Access token (Zerodha)' : 'Session token / TOTP token (Kotak)'}
            />
            {isZerodha ? (
              <Input
                value={tokenPayload.api_key}
                onChange={(e) => setTokenPayload({ ...tokenPayload, api_key: e.target.value })}
                placeholder="API key (required for Zerodha)"
              />
            ) : (
              <div className="rounded-lg border border-slate-800 bg-slate-900 px-3 py-2 text-sm text-slate-400">
                No API key needed for Kotak token flow.
              </div>
            )}
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
            <Button onClick={async () => { await updateToken(memberId, tokenPayload); await loadData() }}>
              Save Token
            </Button>
            <Button onClick={async () => { await runSync(memberId); await loadData() }}>
              Daily Sync
            </Button>
            <Input type="number" value={memberId} onChange={(e) => setMemberId(Number(e.target.value))} placeholder="Member ID" />
            <Input value={tokenPayload.broker_name} onChange={(e) => setTokenPayload({ ...tokenPayload, broker_name: e.target.value })} placeholder="Broker" />
            <Input value={tokenPayload.access_token} onChange={(e) => setTokenPayload({ ...tokenPayload, access_token: e.target.value })} placeholder="Session token / TOTP token" />
            <Input value={tokenPayload.api_key} onChange={(e) => setTokenPayload({ ...tokenPayload, api_key: e.target.value })} placeholder="API key (Zerodha)" />
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
            <Button onClick={async () => { await updateToken(memberId, tokenPayload); await loadData() }}>Save Token</Button>
            <Button onClick={async () => { await runSync(memberId); await loadData() }}>Daily Sync</Button>
            <Button className="bg-emerald-600 hover:bg-emerald-500" onClick={() => setAggregate((v) => !v)}>
              {aggregate ? 'View Individual Member P&L' : 'View Aggregated Firm P&L'}
            </Button>
          </div>
        </Card>

        <Card>
          <h2 className="mb-3 text-xl font-semibold">Daily Performance</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-700 text-slate-300">
                  <th className="p-2">Symbol</th><th className="p-2">Segment</th><th className="p-2">Side</th>
                  <th className="p-2">Qty</th><th className="p-2">Price</th><th className="p-2">Net P&L</th>
                </tr>
              </thead>
              <tbody>
                {dailyRows.map((row, idx) => (
                  <tr key={`${row.symbol}-${idx}`} className="border-b border-slate-800">
                    <td className="p-2">{row.symbol}</td><td className="p-2">{row.segment}</td><td className="p-2">{row.side}</td>
                    <td className="p-2">{row.quantity}</td><td className="p-2">{row.price}</td>
                    <td className={`p-2 ${row.net_pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>{row.net_pnl}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        <Card>
          <h2 className="mb-3 text-xl font-semibold">Monthly P&L</h2>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthlyRows}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="month" stroke="#cbd5e1" />
                <YAxis stroke="#cbd5e1" />
                <Tooltip />
                <Bar dataKey="pnl" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  )
}
