/* OWNER: FE track — DRAGONS. */
import Stub from '../Stub'

export default function AdminDashboard() {
  return (
    <Stub
      screen="Admin dashboard"
      track="FE"
      owner="DRAGONS"
      file="src/app/components/admin/AdminDashboard.tsx"
      todo={[
        'GET /api/admin/overview/?date= for a chosen day.',
        'A recharts donut: present / absent / not marked, with live counts beside it.',
        'A searchable student list with filter tabs, each showing its own count.',
        'Staff only. A student who reaches this URL gets sent away, not shown an empty page.',
      ]}
    />
  )
}
