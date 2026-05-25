import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from 'recharts'

const COLORS = ['#FF7A59', '#E6B566', '#34D399', '#60A5FA', '#A78BFA']

export default function BreakdownChart({ breakdown }) {
  const data = [
    { name: 'Structure', score: breakdown?.resume_structure ?? 0, max: 15 },
    { name: 'Tech Depth', score: breakdown?.technical_depth ?? 0, max: 20 },
    { name: 'Projects', score: breakdown?.project_quality ?? 0, max: 20 },
    { name: 'Impact', score: breakdown?.quantified_impact ?? 0, max: 15 },
    { name: 'Relevance', score: breakdown?.role_relevance ?? 0, max: 20 },
    { name: 'Readability', score: breakdown?.ats_readability ?? 0, max: 10 },
  ]

  return (
    <div style={{ width: '100%', height: '260px' }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ left: 0, right: 24, top: 8, bottom: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2A2D32" horizontal={false} />
          <XAxis
            type="number"
            domain={[0, 20]}
            tick={{ fill: '#9CA3AF', fontSize: 12, fontFamily: 'Inter' }}
            axisLine={{ stroke: '#2A2D32' }}
            tickLine={{ stroke: '#2A2D32' }}
          />
          <YAxis
            type="category"
            dataKey="name"
            tick={{ fill: '#F5F1EA', fontSize: 13, fontFamily: 'Inter' }}
            width={95}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            contentStyle={{
              background: '#1A1D21',
              border: '1px solid #2A2D32',
              borderRadius: '12px',
              color: '#F5F1EA',
              fontSize: '13px',
              fontFamily: 'Inter',
            }}
            formatter={(value, name, props) => [`${value} / ${props.payload.max}`, 'Score']}
          />
          <Bar dataKey="score" radius={[0, 6, 6, 0]} barSize={20}>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
