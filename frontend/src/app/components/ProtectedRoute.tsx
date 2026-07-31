/* Route guard.
 *
 *     OWNER: FE track — GRP8.
 *
 * Note what this is and is not. It stops a logged-out user from *seeing* a
 * screen. It does not stop anyone from *reading data* — every endpoint must
 * enforce its own permissions server-side, because anyone can call the API
 * directly and never load your JavaScript at all.
 *
 * A guard is a courtesy to the user. It is not a security control.
 */
import { Navigate, Outlet, useLocation } from 'react-router'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ staffOnly = false }: { staffOnly?: boolean }) {
  const { user, isAuthenticated } = useAuth()
  const location = useLocation()

  if (!isAuthenticated) {
    // Remember where they were going so login can send them back.
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  if (staffOnly && !user?.isStaff) {
    return <Navigate to="/mark" replace />
  }

  return <Outlet />
}
