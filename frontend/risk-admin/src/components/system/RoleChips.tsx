export default function RoleChips(props: { roles: string[] }) {
  if (props.roles.length === 0) return <span className="text-xs text-zinc-500">—</span>
  return (
    <div className="flex flex-wrap gap-1">
      {props.roles.map((r) => (
        <span key={r} className="rounded-full bg-zinc-100 px-2 py-0.5 text-xs text-zinc-700">
          {r}
        </span>
      ))}
    </div>
  )
}

