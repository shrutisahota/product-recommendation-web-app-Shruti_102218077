import { useState } from 'react'
import { recommendByQuery, generateDescription } from '../api.js'
import ProductCard from '../components/ProductCard.jsx'

export default function Recommend() {
  const [prompt, setPrompt] = useState('modern wooden chair for dining')
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)

  const onSearch = async () => {
    setLoading(true)
    const res = await recommendByQuery(prompt, 8)
    const withGen = await Promise.all((res.items||[]).map(async it => {
      try {
        const g = await generateDescription({
          title: it.title, material: it.material, category: it.categories, brand: it.brand, tone: 'professional'
        })
        return {...it, gen: g.description}
      } catch(e) {
        return it
      }
    }))
    setItems(withGen)
    setLoading(false)
  }

  return (
    <div>
      <div className="flex gap-2 mb-4">
        <input value={prompt} onChange={e=>setPrompt(e.target.value)}
               className="flex-1 border rounded-xl px-4 py-3 outline-none"
               placeholder="Describe what you want..."/>
        <button onClick={onSearch} className="px-5 py-3 rounded-xl bg-black text-white">
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((it,idx)=>(
          <div key={idx}>
            <ProductCard item={it} />
            {it.gen && <p className="text-sm text-gray-700 mt-2">{it.gen}</p>}
          </div>
        ))}
      </div>
    </div>
  )
}
