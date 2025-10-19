export default function ProductCard({item}) {
  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm hover:shadow-md transition">
      <img src={item.image_url || 'https://via.placeholder.com/300x200?text=Image'} alt={item.title} className="w-full h-40 object-cover rounded-xl mb-3"/>
      <div className="font-semibold text-lg line-clamp-1">{item.title}</div>
      <div className="text-sm text-gray-600">{item.brand}</div>
      <div className="text-sm text-gray-500 line-clamp-2 my-1">{item.description}</div>
      <div className="text-sm text-gray-700">Category: {item.categories}</div>
      <div className="text-sm text-gray-900 font-medium mt-1">Score: {item.score?.toFixed(3)}</div>
      {typeof item.price === 'number' && <div className="text-emerald-600 font-semibold mt-1">₹ {item.price.toFixed(2)}</div>}
    </div>
  )
}
