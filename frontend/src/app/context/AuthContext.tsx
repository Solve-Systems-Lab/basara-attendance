/* Authentication state.
 *
 *     OWNER: FE track — GRP8.
 *
 * A stub. It compiles and it lies: isAuthenticated is always false and login()
 * throws. Replace it with the real thing.
 *
 * One decision to make deliberately rather than by accident — where the access
 * token lives. The reference app puts it in localStorage, which means any
 * injected script on the page can read it. Holding it in memory and asking for
 * a new one on 401 is more work and materially safer. Whatever you choose, be
 * able to say why in your pull request.
 */
import { createContext, useContext, useMemo, useState, type ReactNode } from 'react'

export type User = {
  id: number
  rollNo: string
  name: string
  isStaff: boolean
}

type AuthState = {
  user: User | null
  isAuthenticated: boolean
  login: (rollNo: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthState | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const value = useMemo<AuthState>(
    () => ({
      user,
      isAuthenticated: user !== null,
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      login: async (_rollNo: string, _password: string) => {
        throw new Error('Not implemented — see src/app/context/AuthContext.tsx')
      },
      logout: () => setUser(null),
    }),
    [user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>')
  return ctx
}
