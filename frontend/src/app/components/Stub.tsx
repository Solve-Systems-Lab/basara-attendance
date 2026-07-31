/* A placeholder screen.
 *
 * Every route in this scaffold renders one of these. It exists so that
 * `npm run dev` shows you something on day one and so the router, the build
 * and the type-checker are all proven to work before anybody writes a feature.
 *
 * Delete this component when the last real screen lands. If it is still here
 * in week three, something has gone wrong.
 */

type StubProps = {
  screen: string
  track: string
  owner: string
  file: string
  todo: string[]
}

export default function Stub({ screen, track, owner, file, todo }: StubProps) {
  return (
    <main className="mx-auto max-w-2xl px-5 py-10">
      <p className="text-xs font-semibold uppercase tracking-widest text-accent">
        {track} &middot; {owner}
      </p>
      <h1 className="mt-1 text-3xl font-bold text-navy">{screen}</h1>
      <p className="mt-2 text-muted">
        Not built yet. This is a placeholder so the app runs before anyone has
        written a line of it.
      </p>

      <div className="mt-6 rounded border-l-4 border-accent bg-surface p-4">
        <p className="text-sm">
          You are looking for{' '}
          <code className="rounded bg-line/40 px-1 py-0.5 text-[0.85em]">
            {file}
          </code>
        </p>
      </div>

      <h2 className="mt-8 text-sm font-bold uppercase tracking-wider text-navy">
        What this screen has to do
      </h2>
      <ul className="mt-2 space-y-1.5">
        {todo.map((item) => (
          <li key={item} className="flex gap-2 text-sm">
            <span className="text-muted">&#9744;</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>

      <p className="mt-8 border-t border-line pt-4 text-sm text-muted">
        The full task list is on your track page in{' '}
        <code className="text-[0.85em]">docs/brief.pdf</code>.
      </p>
    </main>
  )
}
