import { useEffect, useState } from 'react'
import { getAnalytics } from '../api.js'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'

export default function Analytics() {
  const [data, setData] = useState(null)

  useEffect(()=>{
    (async ()=>{
      const res = await getAnalytics()
      setData(res)
    })()
  },[])

  if (!data) return <div>Loading analytics...</div>

  const pieData = (data.top_categories||[]).map(d => ({name:d.category, value:d.count}))

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <div className="text-gray-500 text-sm">Rows</div>
          <div className="text-2xl font-semibold">{data.n_rows}</div>
        </div>
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <div className="text-gray-500 text-sm">Brands</div>
          <div className="text-2xl font-semibold">{data.n_brands}</div>
        </div>
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <div className="text-gray-500 text-sm">Avg Price</div>
          <div className="text-2xl font-semibold">{data.price_stats?.mean?.toFixed(2) || '-'}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <div className="font-medium mb-2">Top Categories</div>
          <div style={{width:'100%', height:300}}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" label>
                  {pieData.map((_, index) => <Cell key={`c-${index}`} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <div className="font-medium mb-2">Price Stats (min/median/max)</div>
          <div style={{width:'100%', height:300}}>
            <ResponsiveContainer>
              <BarChart data={[{name:'Stats', min:data.price_stats?.min, median:data.price_stats?.median, max:data.price_stats?.max}]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="min" />
                <Bar dataKey="median" />
                <Bar dataKey="max" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  )
}
