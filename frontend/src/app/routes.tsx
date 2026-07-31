import { createBrowserRouter, Navigate } from 'react-router'
import Login from './components/Login'
import MyRecords from './components/MyRecords'
import ProtectedRoute from './components/ProtectedRoute'
import AdminDashboard from './components/admin/AdminDashboard'
import MarkAttendance from './components/employee/MarkAttendance'

/* Routes are flat and few on purpose. A student does two things: marks
 * attendance, and looks at their own history. Staff do one: read the day.
 *
 * While AuthContext is a stub, isAuthenticated is always false — so every
 * guarded route bounces to /login. That is correct behaviour, not a bug.
 * To see the other screens before auth exists, visit them directly after
 * temporarily returning <Outlet /> from ProtectedRoute.
 */
export const router = createBrowserRouter([
  { path: '/', element: <Navigate to="/mark" replace /> },
  { path: '/login', element: <Login /> },

  {
    element: <ProtectedRoute />,
    children: [
      { path: '/mark', element: <MarkAttendance /> },
      { path: '/records', element: <MyRecords /> },
    ],
  },

  {
    element: <ProtectedRoute staffOnly />,
    children: [{ path: '/admin', element: <AdminDashboard /> }],
  },

  { path: '*', element: <Navigate to="/" replace /> },
])
