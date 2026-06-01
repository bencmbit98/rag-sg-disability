import Link from 'next/link'

const SOURCES = [
  {
    label: 'TP SEN Support',
    url: 'https://www.tp.edu.sg/life-at-tp/special-educational-needs-sen-support.html',
    description: 'Special Educational Needs support for Temasek Polytechnic students.',
  },
  {
    label: 'Disability Transport',
    url: 'https://www.enablingguide.sg/im-looking-for-disability-support/transport',
    description: 'Transport schemes and subsidies for persons with disabilities in Singapore.',
  },
  {
    label: 'Care Services',
    url: 'https://www.enablingguide.sg/im-looking-for-disability-support/child-adult-care',
    description: 'Child and adult care services for persons with disabilities.',
  },
  {
    label: 'Training & Employment',
    url: 'https://www.enablingguide.sg/im-looking-for-disability-support/training-employment',
    description: 'Training and employment support for persons with disabilities.',
  },
]

export default function About() {
  return (
    <main className="min-h-screen bg-white px-4 py-6 max-w-lg mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <Link
          href="/"
          className="text-blue-600 hover:underline text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 rounded min-h-[44px] flex items-center"
          aria-label="Back to chat"
        >
          ← Back
        </Link>
        <h1 className="text-xl font-semibold text-gray-900">About</h1>
      </div>

      <section className="mb-6">
        <h2 className="text-base font-semibold text-gray-800 mb-2">What this app does</h2>
        <p className="text-sm text-gray-600 leading-relaxed">
          This app helps students with SEN, persons with disabilities, and caregivers in Singapore
          find relevant support services. Ask questions in plain language and get answers sourced
          directly from official Singapore government and TP websites.
        </p>
      </section>

      <section className="mb-6">
        <h2 className="text-base font-semibold text-gray-800 mb-3">Data sources</h2>
        <div className="space-y-3">
          {SOURCES.map((s) => (
            <div key={s.url} className="border border-gray-200 rounded-lg p-3">
              <p className="text-sm font-medium text-gray-800">{s.label}</p>
              <p className="text-xs text-gray-500 mt-0.5 mb-1.5">{s.description}</p>
              <a
                href={s.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-blue-600 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 rounded break-all"
                aria-label={`Visit ${s.label} source (opens in new tab)`}
              >
                {s.url}
              </a>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-base font-semibold text-gray-800 mb-2">Privacy notice</h2>
        <p className="text-sm text-gray-600 leading-relaxed">
          This app logs your questions and AI responses anonymously to help improve the service. No
          personal information is collected. Your session is identified only by a random ID stored
          in your browser. You can clear it at any time by clearing your browser data.
        </p>
      </section>
    </main>
  )
}
