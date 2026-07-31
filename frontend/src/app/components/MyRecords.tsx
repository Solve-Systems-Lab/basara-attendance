/* OWNER: FE track — GRP14. */
import Stub from './Stub'

export default function MyRecords() {
  return (
    <Stub
      screen="My records"
      track="FE"
      owner="GRP14"
      file="src/app/components/MyRecords.tsx"
      todo={[
        'GET /api/attendance/my-records/ for the selected month.',
        'Month calendar and a list view, with a toggle between them.',
        'Use the five status colours from theme.css. Do not invent your own.',
        'Show the running attendance percentage — this is the number students care about.',
      ]}
    />
  )
}
