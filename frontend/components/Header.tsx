import Link from 'next/link'

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-10 bg-blue-700 text-white px-4 py-3 flex items-center justify-between shadow-md">
      <div>
        <h1 className="text-lg font-semibold leading-tight">SEN &amp; Disability Support</h1>
        <p className="text-xs text-blue-200">Singapore · AI-powered</p>
      </div>
      <Link
        href="/about"
        className="text-sm text-blue-100 hover:text-white underline underline-offset-2 focus:outline-none focus:ring-2 focus:ring-white rounded px-1 min-h-[44px] flex items-center"
        aria-label="About this app and data sources"
      >
        About
      </Link>
    </header>
  )
}
