/* OWNER: FE track — GRP14. */
import Stub from './Stub'

export default function Login() {
  return (
    <Stub
      screen="Log in"
      track="FE"
      owner="GRP14"
      file="src/app/components/Login.tsx"
      todo={[
        'Roll number and password, two controlled inputs. No second factor.',
        'POST /api/auth/login/ — store the access token in memory, not localStorage.',
        'On success, send students to /mark and staff to /admin.',
        'Show the server error on a 401. "Something went wrong" helps nobody.',
      ]}
    />
  )
}
