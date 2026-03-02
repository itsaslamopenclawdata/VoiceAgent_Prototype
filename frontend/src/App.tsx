import { useState } from 'react'
import './App.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-md w-96">
          <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">
            RepCon Voice Agent
          </h1>
          <p className="text-gray-600 mb-6 text-center">
            Sign in to access your dashboard
          </p>
          <button
            onClick={() => setIsLoggedIn(true)}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Sign In
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-800">
            RepCon Voice Agent
          </h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">Admin</span>
            <button
              onClick={() => setIsLoggedIn(false)}
              className="text-blue-600 hover:underline"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Dashboard Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard title="Today's Calls" value="15" color="blue" />
          <StatCard title="Today's Leads" value="8" color="green" />
          <StatCard title="This Week" value="42" color="purple" />
          <StatCard title="Conversion Rate" value="12.5%" color="orange" />
        </div>

        {/* Leads Table */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Recent Leads</h2>
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4">Name</th>
                <th className="text-left py-3 px-4">Phone</th>
                <th className="text-left py-3 px-4">Course</th>
                <th className="text-left py-3 px-4">Status</th>
                <th className="text-left py-3 px-4">Date</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b hover:bg-gray-50">
                <td className="py-3 px-4">Rahul Sharma</td>
                <td className="py-3 px-4">+91 98765 43210</td>
                <td className="py-3 px-4">Python Data Science</td>
                <td className="py-3 px-4">
                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                    New
                  </span>
                </td>
                <td className="py-3 px-4">Today</td>
              </tr>
              <tr className="border-b hover:bg-gray-50">
                <td className="py-3 px-4">Priya Patel</td>
                <td className="py-3 px-4">+91 98765 43211</td>
                <td className="py-3 px-4">Web Development</td>
                <td className="py-3 px-4">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                    Contacted
                  </span>
                </td>
                <td className="py-3 px-4">Yesterday</td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>
    </div>
  )
}

function StatCard({ title, value, color }: { title: string; value: string; color: string }) {
  const colorClasses: Record<string, string> = {
    blue: 'bg-blue-50 border-blue-200',
    green: 'bg-green-50 border-green-200',
    purple: 'bg-purple-50 border-purple-200',
    orange: 'bg-orange-50 border-orange-200'
  }

  return (
    <div className={`p-6 rounded-lg border ${colorClasses[color]}`}>
      <p className="text-gray-600 text-sm">{title}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
    </div>
  )
}

export default App
