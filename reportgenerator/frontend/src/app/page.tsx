'use client'

import { useMemo, useState, useCallback } from 'react'
import { CalendarDays, Upload } from 'lucide-react'
import { useDropzone } from 'react-dropzone'

const SAMPLE_MARKDOWN = `### Highlight

Tokamak Network achieved significant development momentum with 1,232 GitHub commits across 61 repositories, led by key projects like ton-staking-v2 (152 commits) and tokamak-dao-v2 (65 commits), underscoring robust technical progress. Staked TON (TOKAMAK) surpassed 27.5 million, reflecting strong network participation, while the ecosystem maintained a stable market capitalization of $29.15M amid consistent trading volume of $6.78M over two weeks.

### Ecosystem

#### 1.1. Staking Update

As of January 16, 2026, the total amount of staked TON (TOKAMAK) has reached 27,539,665 TON.

By staking with Tokamak Network, you contribute to this growing total and enjoy several benefits:

1. Approximately 31% APY
2. Various benefits such as airdrops
3. The rights to participate in Tokamak Network DAO’s operations and decision-making process
`


const PERIOD_OPTIONS = [
  { id: 'weekly', label: 'Weekly' },
  { id: 'biweekly', label: 'Biweekly' },
  { id: 'monthly', label: 'Monthly' },
  { id: 'custom', label: 'X-day' },
]

const parseDate = (value: string) => {
  const parts = value.replace(/\s+/g, '').split('.')
  if (parts.length < 3) return null
  const [year, month, day] = parts
  if (!year || !month || !day) return null
  const date = new Date(Number(year), Number(month) - 1, Number(day))
  return Number.isNaN(date.getTime()) ? null : date
}

const formatDate = (value: string | null) => {
  if (!value) return ''
  const parts = value.split('-')
  if (parts.length !== 3) return ''
  const [year, month, day] = parts
  return `${year}. ${month.padStart(2, '0')}. ${day.padStart(2, '0')}.`
}

const getDaysBetween = (start: string, end: string) => {
  const startDate = parseDate(start)
  const endDate = parseDate(end)
  if (!startDate || !endDate) return null
  const diff = Math.abs(endDate.getTime() - startDate.getTime())
  return Math.floor(diff / (1000 * 60 * 60 * 24)) + 1
}

const detectPeriodType = (days: number | null) => {
  if (!days) return 'weekly'
  if (days <= 10) return 'weekly'
  if (days <= 20) return 'biweekly'
  if (days <= 35) return 'monthly'
  return 'custom'
}

const resolveReportScope = (value: string) => {
  if (value === 'biweekly' || value === 'monthly' || value === 'quarterly') return value
  return 'auto'
}

export default function Home() {
  const [period, setPeriod] = useState('weekly')
  const [startDate, setStartDate] = useState('2026. 02. 01.')
  const [endDate, setEndDate] = useState('2026. 02. 10.')
  const [useAI, setUseAI] = useState(false)
  const [reportType, setReportType] = useState<'public' | 'technical'>('public')
  const [includeIndividuals, setIncludeIndividuals] = useState(true)
  const [activeView, setActiveView] = useState<'preview' | 'raw'>('preview')
  const [loading, setLoading] = useState(false)
  const [generated, setGenerated] = useState(false)
  const [copied, setCopied] = useState(false)
  const [fileName, setFileName] = useState<string | null>(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [detectedDaysOverride, setDetectedDaysOverride] = useState<number | null>(null)
  const [analysisError, setAnalysisError] = useState<string | null>(null)
  const [periodSource, setPeriodSource] = useState<'detected' | 'manual'>('detected')
  const [file, setFile] = useState<File | null>(null)
  const [rawMarkdown, setRawMarkdown] = useState(SAMPLE_MARKDOWN)
  const [highlight, setHighlight] = useState('')
  const [sections, setSections] = useState<Array<{ title: string; content: string }>>([])
  const [stats, setStats] = useState<{ commits: number; repos: number; prs: number } | null>(null)
  const [dateRange, setDateRange] = useState<{ start: string | null; end: string | null; days: number | null } | null>(null)
  const [reportTitle, setReportTitle] = useState<string | null>(null)
  const [reportHeadline, setReportHeadline] = useState<string | null>(null)
  const [fullReport, setFullReport] = useState<string | null>(null)

  const detectedDays = useMemo(() => {
    if (detectedDaysOverride) return detectedDaysOverride
    return getDaysBetween(startDate, endDate)
  }, [startDate, endDate, detectedDaysOverride])
  const detectedPeriod = useMemo(() => detectPeriodType(detectedDays), [detectedDays])
  const effectivePeriod = periodSource === 'manual' ? period : detectedPeriod
  const effectiveScope = resolveReportScope(effectivePeriod)

  const metaText = useMemo(() => {
    if (!generated || !stats) return 'No report generated yet'
    const range = dateRange?.start && dateRange?.end ? `${dateRange.start} ~ ${dateRange.end}` : 'Range unknown'
    return `${range} • ${stats.commits} commits • ${stats.repos} repos`
  }, [generated, stats, dateRange])

  const handleGenerate = async () => {
    if (!file) {
      setAnalysisError('Please upload a CSV file first.')
      return
    }

    setLoading(true)
    setCopied(false)
    setAnalysisError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('report_type', reportType)
      formData.append('use_ai', useAI.toString())
      formData.append('report_scope', effectiveScope)
      formData.append('include_individuals', includeIndividuals.toString())
      formData.append('project_filter', 'all')
      formData.append('member_filter', 'all')

      const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to generate report')
      }

      const data = await response.json()
      const reportSections = Array.isArray(data.sections)
        ? data.sections.map((section: { title: string; content: string }) => ({
            title: section.title,
            content: section.content,
          }))
        : []

      const fullReportContent = typeof data.full_report === 'string' && data.full_report.trim().length > 0
        ? data.full_report.trim()
        : null

      const rawContent = fullReportContent
        ? fullReportContent
        : [
            data.title ? `### ${data.title}\n\n` : '',
            data.headline ? `#### ${data.headline}\n\n` : '',
            `### Highlight\n\n${data.highlight}\n`,
            `### Development Activity\n`,
            data.sections?.map((section: { content: string }) => section.content).join('\n') ?? '',
          ].join('\n')

      setHighlight(data.highlight || '')
      setReportTitle(fullReportContent ? null : data.title || null)
      setReportHeadline(fullReportContent ? null : data.headline || null)
      setSections(reportSections)
      setFullReport(fullReportContent)
      setRawMarkdown(rawContent)
      setStats({
        commits: data.stats?.total_commits ?? 0,
        repos: data.stats?.total_repos ?? 0,
        prs: data.stats?.total_prs ?? 0,
      })
      setDateRange(data.date_range || null)
      setGenerated(true)
      setActiveView('preview')
    } catch (error) {
      setAnalysisError(error instanceof Error ? error.message : 'Failed to generate report')
    } finally {
      setLoading(false)
    }
  }

  const analyzeCsv = async (file: File) => {
    setAnalyzing(true)
    setAnalysisError(null)
    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      })
      if (!response.ok) {
        throw new Error('Failed to analyze CSV')
      }
      const data = await response.json()
      const range = data.date_range || {}
      if (range.start && range.end) {
        setStartDate(formatDate(range.start))
        setEndDate(formatDate(range.end))
      }
      if (typeof range.days === 'number') {
        setDetectedDaysOverride(range.days)
        setPeriod(detectPeriodType(range.days))
        setPeriodSource('detected')
      }
    } catch (error) {
      setAnalysisError(error instanceof Error ? error.message : 'Failed to analyze CSV')
    } finally {
      setAnalyzing(false)
    }
  }

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return
    const file = acceptedFiles[0]
    setFileName(file.name)
    setFile(file)
    setPeriodSource('detected')
    analyzeCsv(file)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/csv': ['.csv'] },
    multiple: false,
  })

  const exportContent = fullReport ?? rawMarkdown

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(exportContent)
      setCopied(true)
      setTimeout(() => setCopied(false), 1600)
    } catch (error) {
      setCopied(false)
    }
  }

  const handleDownload = () => {
    const blob = new Blob([exportContent], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'biweekly-report.md'
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <main className="mx-auto w-full max-w-6xl px-6 pb-16 pt-12">
        <div className="mb-10">
          <h1 className="text-3xl font-semibold text-gray-900">Biweekly Report Generator</h1>
          <p className="mt-2 text-sm text-gray-500">
            Generate ecosystem reports with GitHub statistics, staking data, and market information.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
          <section className="space-y-6">
            <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
              <div className="mb-6">
                <div className="text-xs font-semibold uppercase tracking-wide text-gray-400">CSV Upload</div>
                <div
                  {...getRootProps()}
                  className={`mt-3 flex min-h-[120px] cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-4 py-6 text-center text-sm transition ${
                    isDragActive
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 text-gray-500 hover:border-gray-300'
                  }`}
                >
                  <input {...getInputProps()} />
                  <Upload className="mb-2 h-6 w-6 text-gray-400" />
                  <div className="font-medium">
                    {fileName ? fileName : 'Drag & drop CSV file here'}
                  </div>
                  <div className="mt-1 text-xs text-gray-400">or click to select</div>
                </div>
                {analyzing && (
                  <div className="mt-2 text-xs text-blue-600">Analyzing CSV…</div>
                )}
                {analysisError && (
                  <div className="mt-2 text-xs text-red-500">{analysisError}</div>
                )}
              </div>

              <div className="mb-4 flex items-center justify-between text-xs font-semibold uppercase tracking-wide text-gray-400">
                <span>Report Period</span>
                <span className="text-[11px] font-medium text-gray-500">
                  Detected: {detectedPeriod} {detectedDays ? `(${detectedDays} days)` : ''}
                </span>
              </div>
              <div className="mb-3 rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-xs text-gray-600">
                Applying: {effectivePeriod}{' '}
                {detectedDays ? `(${detectedDays} days)` : ''} • Source:{' '}
                {periodSource === 'manual' ? 'manual override' : 'auto-detected'}
              </div>
              <div className="flex flex-wrap gap-2">
                {PERIOD_OPTIONS.map((option) => (
                  <button
                    key={option.id}
                    onClick={() => {
                      setPeriod(option.id)
                      setPeriodSource('manual')
                    }}
                    className={`rounded-full border px-4 py-2 text-sm transition ${
                      effectivePeriod === option.id
                        ? 'border-blue-600 bg-blue-50 text-blue-700'
                        : 'border-gray-200 text-gray-500 hover:border-gray-300'
                    }`}
                  >
                    {option.id === 'custom' && detectedDays ? `${detectedDays}-day` : option.label}
                  </button>
                ))}
              </div>

              <div className="mt-6 grid gap-4 md:grid-cols-2">
                <div className="rounded-xl border border-gray-200 p-4">
                  <label className="text-xs font-semibold uppercase tracking-wide text-gray-400">Start Date</label>
                  <div className="mt-3 flex items-center justify-between rounded-lg border border-gray-200 px-3 py-2">
                    <input
                      type="text"
                      value={startDate}
                      onChange={(event) => {
                        setStartDate(event.target.value)
                        setPeriodSource('manual')
                        setDetectedDaysOverride(null)
                      }}
                      className="w-full text-sm text-gray-700 focus:outline-none"
                    />
                    <button className="text-gray-400 hover:text-gray-600" aria-label="Open start date calendar">
                      <CalendarDays className="h-4 w-4" />
                    </button>
                  </div>
                </div>
                <div className="rounded-xl border border-gray-200 p-4">
                  <label className="text-xs font-semibold uppercase tracking-wide text-gray-400">End Date</label>
                  <div className="mt-3 flex items-center justify-between rounded-lg border border-gray-200 px-3 py-2">
                    <input
                      type="text"
                      value={endDate}
                      onChange={(event) => {
                        setEndDate(event.target.value)
                        setPeriodSource('manual')
                        setDetectedDaysOverride(null)
                      }}
                      className="w-full text-sm text-gray-700 focus:outline-none"
                    />
                    <button className="text-gray-400 hover:text-gray-600" aria-label="Open end date calendar">
                      <CalendarDays className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>

              <div className="mt-6 text-xs font-semibold uppercase tracking-wide text-gray-400">Options</div>
              <div className="mt-4 space-y-3 rounded-xl border border-gray-200 p-4">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <div className="text-sm font-medium text-gray-800">Report type</div>
                    <p className="mt-1 text-xs text-gray-500">Choose the audience focus for generated summaries.</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setReportType('public')}
                      className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
                        reportType === 'public'
                          ? 'border-blue-600 bg-blue-50 text-blue-700'
                          : 'border-gray-200 text-gray-500 hover:border-gray-300'
                      }`}
                    >
                      Public
                    </button>
                    <button
                      onClick={() => setReportType('technical')}
                      className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
                        reportType === 'technical'
                          ? 'border-blue-600 bg-blue-50 text-blue-700'
                          : 'border-gray-200 text-gray-500 hover:border-gray-300'
                      }`}
                    >
                      Technical
                    </button>
                  </div>
                </div>
                <div className="flex items-start justify-between gap-4 rounded-lg border border-gray-200 px-4 py-3">
                  <div>
                    <div className="text-sm font-medium text-gray-800">Use AI for summaries</div>
                    <p className="mt-1 text-xs text-gray-500">
                      API 키 사용량 초과로 현재 비활성화되어 있습니다.
                    </p>
                    <span className="mt-2 inline-flex items-center rounded-full bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-700">
                      AI 일시 중단
                    </span>
                  </div>
                  <button
                    disabled
                    className="flex h-7 w-12 cursor-not-allowed items-center rounded-full bg-gray-200 px-1 opacity-70"
                    aria-disabled="true"
                  >
                    <span className="h-5 w-5 translate-x-0 rounded-full bg-white shadow" />
                  </button>
                </div>
                <div className="flex items-start justify-between gap-4 rounded-lg border border-gray-200 px-4 py-3">
                  <div>
                    <div className="text-sm font-medium text-gray-800">Include individual contributions</div>
                    <p className="mt-1 text-xs text-gray-500">
                      Toggle personal updates in section 2.5.
                    </p>
                  </div>
                  <button
                    onClick={() => setIncludeIndividuals((prev) => !prev)}
                    className={`flex h-7 w-12 items-center rounded-full px-1 transition ${
                      includeIndividuals ? 'bg-blue-600' : 'bg-gray-200'
                    }`}
                  >
                    <span
                      className={`h-5 w-5 rounded-full bg-white shadow transition ${
                        includeIndividuals ? 'translate-x-5' : 'translate-x-0'
                      }`}
                    />
                  </button>
                </div>
              </div>

              <button
                onClick={handleGenerate}
                className="mt-6 w-full rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700"
              >
                {loading ? 'Generating...' : '🚀 Generate Report'}
              </button>
            </div>
          </section>

          <section className="space-y-6">
            <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">Generated Report</h2>
                  {reportTitle && (
                    <p className="mt-2 text-sm font-semibold text-gray-800">{reportTitle}</p>
                  )}
                  {reportHeadline && (
                    <p className="mt-1 text-sm text-gray-600">{reportHeadline}</p>
                  )}
                  <p className="mt-2 text-xs text-gray-500">{metaText}</p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setActiveView('preview')}
                    className={`rounded-lg px-3 py-1.5 text-xs font-medium ${
                      activeView === 'preview'
                        ? 'bg-blue-50 text-blue-600'
                        : 'bg-gray-100 text-gray-500'
                    }`}
                  >
                    Preview
                  </button>
                  <button
                    onClick={() => setActiveView('raw')}
                    className={`rounded-lg px-3 py-1.5 text-xs font-medium ${
                      activeView === 'raw'
                        ? 'bg-blue-50 text-blue-600'
                        : 'bg-gray-100 text-gray-500'
                    }`}
                  >
                    Raw
                  </button>
                  <button
                    onClick={handleCopy}
                    className="rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-500"
                  >
                    {copied ? 'Copied!' : 'Copy'}
                  </button>
                  <button
                    onClick={handleDownload}
                    className="rounded-lg bg-green-500 px-3 py-1.5 text-xs font-semibold text-white"
                  >
                    Download .md
                  </button>
                </div>
              </div>

              <div className="mt-5 h-[460px] overflow-y-auto rounded-xl border border-gray-200 bg-gray-50 p-5">
                {generated ? (
                  activeView === 'preview' ? (
                    fullReport ? (
                      <div
                        className="whitespace-pre-wrap text-sm leading-6 text-gray-700"
                        dangerouslySetInnerHTML={{
                          __html: fullReport
                            .replace(/^### (.+)$/gm, '<h3 class="text-base font-semibold text-gray-900 mt-6 mb-2">$1</h3>')
                            .replace(/^#### (.+)$/gm, '<h4 class="font-semibold text-gray-800 mt-4 mb-2">$1</h4>')
                            .replace(/^\* (.+)$/gm, '<li class="ml-4 mb-1">$1</li>')
                            .replace(/^- (.+)$/gm, '<li class="ml-4 mb-1">$1</li>')
                            .replace(/^\d+\. (.+)$/gm, '<li class="ml-4 mb-1">$1</li>')
                            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="text-blue-600 hover:underline">$1</a>')
                        }}
                      />
                    ) : (
                      <div className="space-y-6 text-sm text-gray-700">
                        <div>
                          <h3 className="text-base font-semibold text-gray-900">Highlight</h3>
                          <p className="mt-2 leading-6">{highlight || 'No highlight available.'}</p>
                        </div>
                        {sections.map((section, index) => (
                          <div key={`${section.title}-${index}`}>
                            <h3 className="text-base font-semibold text-gray-900">{section.title}</h3>
                            <div
                              className="mt-2 whitespace-pre-wrap leading-6 text-gray-700"
                              dangerouslySetInnerHTML={{
                                __html: section.content
                                  .replace(/^#### (.+)$/gm, '<h4 class="font-semibold text-gray-800 mt-4 mb-2">$1</h4>')
                                  .replace(/^\* (.+)$/gm, '<li class="ml-4 mb-1">$1</li>')
                                  .replace(/^- (.+)$/gm, '<li class="ml-4 mb-1">$1</li>')
                                  .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="text-blue-600 hover:underline">$1</a>')
                              }}
                            />
                          </div>
                        ))}
                      </div>
                    )
                  ) : (
                    <div className="h-full whitespace-pre-wrap rounded-lg bg-white p-4 font-mono text-xs text-gray-700">
                      {rawMarkdown}
                    </div>
                  )
                ) : (
                  <div className="flex h-full items-center justify-center text-sm text-gray-400">
                    Generate a report to preview the output.
                  </div>
                )}
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}
