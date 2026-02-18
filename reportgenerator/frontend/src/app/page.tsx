'use client'

import { useEffect, useMemo, useState, useCallback } from 'react'
import { CalendarDays, Upload } from 'lucide-react'
import { useDropzone } from 'react-dropzone'

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

interface ReviewIssue {
  category: string
  description: string
  suggestion: string
  severity: 'low' | 'medium' | 'high'
  original_text?: string
  revised_text?: string
}

interface ReviewData {
  issues: ReviewIssue[]
  strengths: string[]
  overall_score: number
  summary: string
}

interface ReviewResult {
  reviewer: string
  reviewer_ko: string
  reviewer_level: number
  reviewer_description: string
  review: ReviewData
}

interface DiffSegment {
  type: 'unchanged' | 'added' | 'removed'
  text: string
}

interface ReportSection {
  title: string
  content: string
}

/* ------------------------------------------------------------------ */
/* Constants                                                           */
/* ------------------------------------------------------------------ */

const REVIEWERS = [
  {
    level: 1,
    name: 'General Reader',
    name_ko: '일반 독자',
    description: 'No technical background',
    bg: 'bg-emerald-50',
    border: 'border-emerald-200',
    text: 'text-emerald-700',
    badge: 'bg-emerald-100 text-emerald-700',
    dot: 'bg-emerald-400',
  },
  {
    level: 2,
    name: 'Business Analyst',
    name_ko: '비즈니스 분석가',
    description: 'Investment & business focus',
    bg: 'bg-sky-50',
    border: 'border-sky-200',
    text: 'text-sky-700',
    badge: 'bg-sky-100 text-sky-700',
    dot: 'bg-sky-400',
  },
  {
    level: 3,
    name: 'Project Manager',
    name_ko: '프로젝트 매니저',
    description: 'Moderate technical understanding',
    bg: 'bg-amber-50',
    border: 'border-amber-200',
    text: 'text-amber-700',
    badge: 'bg-amber-100 text-amber-700',
    dot: 'bg-amber-400',
  },
  {
    level: 4,
    name: 'Senior Developer',
    name_ko: '시니어 개발자',
    description: 'Deep blockchain experience',
    bg: 'bg-orange-50',
    border: 'border-orange-200',
    text: 'text-orange-700',
    badge: 'bg-orange-100 text-orange-700',
    dot: 'bg-orange-400',
  },
  {
    level: 5,
    name: 'Blockchain Architect',
    name_ko: '블록체인 아키텍트',
    description: 'Protocol & systems architect',
    bg: 'bg-violet-50',
    border: 'border-violet-200',
    text: 'text-violet-700',
    badge: 'bg-violet-100 text-violet-700',
    dot: 'bg-violet-400',
  },
]

const MODEL_OPTIONS = [
  'gpt-5.2-pro',
  'gpt-5.2-mini',
  'gemini-3-pro',
  'gemini-3-flash',
  'deepseek-v3',
]

const SAMPLE_MARKDOWN = `### Highlight

Tokamak Network achieved significant development momentum with 1,232 GitHub commits across 61 repositories, led by key projects like ton-staking-v2 (152 commits) and tokamak-dao-v2 (65 commits), underscoring robust technical progress. Staked TON (TOKAMAK) surpassed 27.5 million, reflecting strong network participation, while the ecosystem maintained a stable market capitalization of $29.15M amid consistent trading volume of $6.78M over two weeks.

### Ecosystem

#### 1.1. Staking Update

As of January 16, 2026, the total amount of staked TON (TOKAMAK) has reached 27,539,665 TON.

By staking with Tokamak Network, you contribute to this growing total and enjoy several benefits:

1. Approximately 31% APY
2. Various benefits such as airdrops
3. The rights to participate in Tokamak Network DAO's operations and decision-making process
`

const PERIOD_OPTIONS = [
  { id: 'weekly', label: 'Weekly' },
  { id: 'biweekly', label: 'Biweekly' },
  { id: 'monthly', label: 'Monthly' },
  { id: 'custom', label: 'X-day' },
]

/* ------------------------------------------------------------------ */
/* Helpers                                                             */
/* ------------------------------------------------------------------ */

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

function renderMarkdown(md: string) {
  return md
    .replace(/^### (.+)$/gm, '<h3 class="text-base font-semibold text-gray-900 mt-6 mb-2">$1</h3>')
    .replace(/^#### (.+)$/gm, '<h4 class="font-semibold text-gray-800 mt-4 mb-2">$1</h4>')
    .replace(/^\* (.+)$/gm, '<li class="ml-4 mb-1">$1</li>')
    .replace(/^- (.+)$/gm, '<li class="ml-4 mb-1">$1</li>')
    .replace(/^\d+\. (.+)$/gm, '<li class="ml-4 mb-1">$1</li>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="text-blue-600 hover:underline">$1</a>')
}

function computeDiff(original: string, improved: string): DiffSegment[] {
  const origLines = original.split('\n')
  const impLines = improved.split('\n')
  const segments: DiffSegment[] = []
  const maxLen = Math.max(origLines.length, impLines.length)

  let oi = 0, ii = 0
  while (oi < origLines.length || ii < impLines.length) {
    if (oi < origLines.length && ii < impLines.length) {
      if (origLines[oi] === impLines[ii]) {
        segments.push({ type: 'unchanged', text: origLines[oi] })
        oi++; ii++
      } else {
        // Look ahead to find matching line
        let foundInImp = -1
        for (let j = ii + 1; j < Math.min(ii + 5, impLines.length); j++) {
          if (impLines[j] === origLines[oi]) { foundInImp = j; break }
        }
        let foundInOrig = -1
        for (let j = oi + 1; j < Math.min(oi + 5, origLines.length); j++) {
          if (origLines[j] === impLines[ii]) { foundInOrig = j; break }
        }

        if (foundInOrig >= 0 && (foundInImp < 0 || (foundInOrig - oi) <= (foundInImp - ii))) {
          while (oi < foundInOrig) { segments.push({ type: 'removed', text: origLines[oi++] }) }
        } else if (foundInImp >= 0) {
          while (ii < foundInImp) { segments.push({ type: 'added', text: impLines[ii++] }) }
        } else {
          segments.push({ type: 'removed', text: origLines[oi++] })
          segments.push({ type: 'added', text: impLines[ii++] })
        }
      }
    } else if (oi < origLines.length) {
      segments.push({ type: 'removed', text: origLines[oi++] })
    } else {
      segments.push({ type: 'added', text: impLines[ii++] })
    }
  }
  return segments
}

function scoreColor(score: number): string {
  if (score >= 8) return 'text-emerald-600'
  if (score >= 6) return 'text-amber-600'
  return 'text-red-500'
}

function severityBadge(severity: string) {
  if (severity === 'high') return 'bg-red-100 text-red-700'
  if (severity === 'medium') return 'bg-amber-100 text-amber-700'
  return 'bg-gray-100 text-gray-600'
}

/* ------------------------------------------------------------------ */
/* Component                                                           */
/* ------------------------------------------------------------------ */

export default function Home() {
  /* ---- Step management ---- */
  const [step, setStep] = useState<1 | 2>(1)

  /* ---- Step 1: Generate ---- */
  const [period, setPeriod] = useState('weekly')
  const [startDate, setStartDate] = useState('2026. 02. 01.')
  const [endDate, setEndDate] = useState('2026. 02. 10.')
  const [useAI, setUseAI] = useState(true)
  const [reportType, setReportType] = useState<'public' | 'technical'>('public')
  const [reportGrouping, setReportGrouping] = useState<'repository' | 'project'>('repository')
  const [reportFormat, setReportFormat] = useState<'concise' | 'structured'>('concise')
  const [repoLimit, setRepoLimit] = useState('0')
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
  const [sections, setSections] = useState<ReportSection[]>([])
  const [stats, setStats] = useState<{ commits: number; repos: number; prs: number } | null>(null)
  const [dateRange, setDateRange] = useState<{ start: string | null; end: string | null; days: number | null } | null>(null)
  const [reportTitle, setReportTitle] = useState<string | null>(null)
  const [reportHeadline, setReportHeadline] = useState<string | null>(null)
  const [fullReport, setFullReport] = useState<string | null>(null)
  const [repoMeta, setRepoMeta] = useState<{ applied: boolean; total: number; shown: number } | null>(null)
  const [selectedModel, setSelectedModel] = useState('gpt-5.2-pro')
  const [showModelMenu, setShowModelMenu] = useState(false)

  /* ---- Step 2: Review & Improve ---- */
  const [reviews, setReviews] = useState<ReviewResult[]>([])
  const [reviewingLevel, setReviewingLevel] = useState<number | null>(null)
  const [expandedReview, setExpandedReview] = useState<number | null>(null)
  const [improving, setImproving] = useState(false)
  const [improvedReport, setImprovedReport] = useState<string | null>(null)
  const [copiedFinal, setCopiedFinal] = useState(false)
  const [viewMode, setViewMode] = useState<'original' | 'improved' | 'diff'>('original')
  const [editingReport, setEditingReport] = useState(false)
  const [editableText, setEditableText] = useState('')
  const [reviewError, setReviewError] = useState<string | null>(null)

  /* ---- Derived values ---- */
  const detectedDays = useMemo(() => {
    if (detectedDaysOverride) return detectedDaysOverride
    return getDaysBetween(startDate, endDate)
  }, [startDate, endDate, detectedDaysOverride])

  const detectedPeriod = useMemo(() => detectPeriodType(detectedDays), [detectedDays])
  const effectivePeriod = periodSource === 'manual' ? period : detectedPeriod
  const effectiveScope = resolveReportScope(effectivePeriod)

  const metaText = useMemo(() => {
    if (!generated || !stats) return 'No report generated yet'
    const range =
      dateRange?.start && dateRange?.end
        ? `${dateRange.start} ~ ${dateRange.end}`
        : 'Range unknown'
    return `${range}  |  ${stats.commits} commits  |  ${stats.repos} repos`
  }, [generated, stats, dateRange])

  const modelCandidateList = [...MODEL_OPTIONS]
  const exportContent = improvedReport ?? fullReport ?? rawMarkdown

  const originalReport = fullReport ?? rawMarkdown
  const currentReport = viewMode === 'improved' && improvedReport ? improvedReport : (editingReport ? editableText : originalReport)
  const diffSegments = useMemo(() => {
    if (!improvedReport) return []
    return computeDiff(originalReport, improvedReport)
  }, [originalReport, improvedReport])

  /* ---- Drag prevention ---- */
  useEffect(() => {
    const preventDefaults = (event: DragEvent) => {
      event.preventDefault()
      event.stopPropagation()
    }
    window.addEventListener('dragover', preventDefaults)
    window.addEventListener('drop', preventDefaults)
    return () => {
      window.removeEventListener('dragover', preventDefaults)
      window.removeEventListener('drop', preventDefaults)
    }
  }, [])

  /* ---- Handlers ---- */

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
      formData.append('include_individuals', 'false')
      formData.append('project_filter', 'all')
      formData.append('member_filter', 'all')
      formData.append('report_grouping', reportGrouping)
      formData.append('report_format', reportFormat)
      formData.append('repo_limit', repoLimit)
      formData.append('model', selectedModel)

      const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        body: formData,
      })
      if (!response.ok) throw new Error('Failed to generate report')

      const data = await response.json()
      const reportSections: ReportSection[] = Array.isArray(data.sections)
        ? data.sections.map((s: ReportSection) => ({ title: s.title, content: s.content }))
        : []

      const fullReportContent =
        typeof data.full_report === 'string' && data.full_report.trim().length > 0
          ? data.full_report.trim()
          : null

      const rawContent = fullReportContent
        ? fullReportContent
        : [
            data.title ? `### ${data.title}\n\n` : '',
            data.headline ? `#### ${data.headline}\n\n` : '',
            `### Highlight\n\n${data.highlight}\n`,
            `### Development Activity\n`,
            data.sections?.map((s: { content: string }) => s.content).join('\n') ?? '',
          ].join('\n')

      setHighlight(data.highlight || '')
      setReportTitle(fullReportContent ? null : data.title || null)
      setReportHeadline(fullReportContent ? null : data.headline || null)
      setSections(reportSections)
      setFullReport(fullReportContent)
      setRawMarkdown(rawContent)
      setRepoMeta(
        data.report_grouping === 'repository'
          ? { applied: Boolean(data.repo_limit_applied), total: data.repo_count_total ?? 0, shown: data.repo_count_shown ?? 0 }
          : null,
      )
      setStats({ commits: data.stats?.total_commits ?? 0, repos: data.stats?.total_repos ?? 0, prs: data.stats?.total_prs ?? 0 })
      setDateRange(data.date_range || null)
      setGenerated(true)
      setActiveView('preview')

      // Reset review state
      setReviews([])
      setImprovedReport(null)
      setViewMode('original')
    } catch (error) {
      setAnalysisError(error instanceof Error ? error.message : 'Failed to generate report')
    } finally {
      setLoading(false)
    }
  }

  const analyzeCsv = async (csvFile: File) => {
    setAnalyzing(true)
    setAnalysisError(null)
    try {
      const formData = new FormData()
      formData.append('file', csvFile)
      const response = await fetch('http://localhost:8000/api/analyze', { method: 'POST', body: formData })
      if (!response.ok) throw new Error('Failed to analyze CSV')
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
    const dropped = acceptedFiles[0]
    setFileName(dropped.name)
    setFile(dropped)
    setPeriodSource('detected')
    analyzeCsv(dropped)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/csv': ['.csv'] },
    multiple: false,
  })

  const handleCopy = async (text: string, setter: (v: boolean) => void) => {
    try {
      await navigator.clipboard.writeText(text)
      setter(true)
      setTimeout(() => setter(false), 1600)
    } catch {
      setter(false)
    }
  }

  const handleDownload = (content: string, filename: string) => {
    const blob = new Blob([content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    link.click()
    URL.revokeObjectURL(url)
  }

  const handleReview = async (level: number) => {
    const reportText = editingReport ? editableText : (fullReport ?? rawMarkdown)
    setReviewingLevel(level)
    setReviewError(null)

    try {
      const formData = new FormData()
      formData.append('report_text', reportText)
      formData.append('report_type', reportType)
      formData.append('report_format', reportFormat)
      formData.append('reviewer_level', level.toString())
      formData.append('model', selectedModel)

      const response = await fetch('http://localhost:8000/api/review', { method: 'POST', body: formData })
      if (!response.ok) throw new Error('Review request failed')

      const data = await response.json()
      if (data.success) {
        setReviews((prev) => {
          const filtered = prev.filter((r) => r.reviewer_level !== level)
          return [...filtered, data as ReviewResult].sort((a, b) => a.reviewer_level - b.reviewer_level)
        })
        setExpandedReview(level)
      } else {
        setReviewError(`Review failed: ${data.error || 'Unknown error'}`)
      }
    } catch (error) {
      setReviewError(`Review failed: ${error instanceof Error ? error.message : 'Network error'}`)
    } finally {
      setReviewingLevel(null)
    }
  }

  const handleImprove = async () => {
    if (reviews.length === 0) return
    setImproving(true)

    try {
      const reportText = editingReport ? editableText : (fullReport ?? rawMarkdown)
      const formData = new FormData()
      formData.append('report_text', reportText)
      formData.append('report_type', reportType)
      formData.append('report_format', reportFormat)
      formData.append('reviews_json', JSON.stringify(reviews))
      formData.append('model', selectedModel)

      const response = await fetch('http://localhost:8000/api/improve', { method: 'POST', body: formData })
      if (!response.ok) throw new Error('Improve request failed')

      const data = await response.json()
      if (data.success) {
        setImprovedReport(data.improved_report)
        setViewMode('diff')
      }
    } catch (error) {
      console.error('Improve failed:', error)
    } finally {
      setImproving(false)
    }
  }

  /* ================================================================ */
  /* STEP 1 — Generate                                                 */
  /* ================================================================ */

  if (step === 1) {
    return (
      <div className="min-h-screen bg-white text-gray-900">
        <main className="mx-auto w-full max-w-6xl px-6 pb-16 pt-12">
          <div className="mb-10">
            <h1 className="text-3xl font-semibold text-gray-900">Biweekly Report Generator</h1>
            <p className="mt-2 text-sm text-gray-500">
              Generate ecosystem reports from GitHub activity data, then review and refine with AI reviewers.
            </p>
            {/* Step indicator */}
            <div className="mt-4 flex items-center gap-3 text-xs">
              <span className="flex items-center gap-1.5 rounded-full bg-blue-600 px-3 py-1 font-semibold text-white">
                1. Generate
              </span>
              <span className="h-px w-6 bg-gray-300" />
              <span className="flex items-center gap-1.5 rounded-full border border-gray-200 px-3 py-1 text-gray-400">
                2. Review &amp; Improve
              </span>
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
            {/* Left: Controls */}
            <section className="space-y-6">
              <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                {/* CSV Upload */}
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
                    <div className="font-medium">{fileName ? fileName : 'Drag & drop CSV file here'}</div>
                    <div className="mt-1 text-xs text-gray-400">or click to select</div>
                  </div>
                  {analyzing && <div className="mt-2 text-xs text-blue-600">Analyzing CSV...</div>}
                  {analysisError && <div className="mt-2 text-xs text-red-500">{analysisError}</div>}
                </div>

                {/* Period */}
                <div className="mb-4 flex items-center justify-between text-xs font-semibold uppercase tracking-wide text-gray-400">
                  <span>Report Period</span>
                  <span className="text-[11px] font-medium text-gray-500">
                    Detected: {detectedPeriod} {detectedDays ? `(${detectedDays} days)` : ''}
                  </span>
                </div>
                <div className="mb-3 rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-xs text-gray-600">
                  Applying: {effectivePeriod} {detectedDays ? `(${detectedDays} days)` : ''} | Source:{' '}
                  {periodSource === 'manual' ? 'manual override' : 'auto-detected'}
                </div>
                <div className="flex flex-wrap gap-2">
                  {PERIOD_OPTIONS.map((option) => (
                    <button
                      key={option.id}
                      onClick={() => { setPeriod(option.id); setPeriodSource('manual') }}
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

                {/* Date pickers */}
                <div className="mt-6 grid gap-4 md:grid-cols-2">
                  <div className="rounded-xl border border-gray-200 p-4">
                    <label className="text-xs font-semibold uppercase tracking-wide text-gray-400">Start Date</label>
                    <div className="mt-3 flex items-center justify-between rounded-lg border border-gray-200 px-3 py-2">
                      <input
                        type="text"
                        value={startDate}
                        onChange={(e) => { setStartDate(e.target.value); setPeriodSource('manual'); setDetectedDaysOverride(null) }}
                        className="w-full text-sm text-gray-700 focus:outline-none"
                      />
                      <CalendarDays className="h-4 w-4 text-gray-400" />
                    </div>
                  </div>
                  <div className="rounded-xl border border-gray-200 p-4">
                    <label className="text-xs font-semibold uppercase tracking-wide text-gray-400">End Date</label>
                    <div className="mt-3 flex items-center justify-between rounded-lg border border-gray-200 px-3 py-2">
                      <input
                        type="text"
                        value={endDate}
                        onChange={(e) => { setEndDate(e.target.value); setPeriodSource('manual'); setDetectedDaysOverride(null) }}
                        className="w-full text-sm text-gray-700 focus:outline-none"
                      />
                      <CalendarDays className="h-4 w-4 text-gray-400" />
                    </div>
                  </div>
                </div>

                {/* Options */}
                <div className="mt-6 text-xs font-semibold uppercase tracking-wide text-gray-400">Options</div>
                <div className="mt-4 space-y-3 rounded-xl border border-gray-200 p-4">
                  {/* Report type */}
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <div className="text-sm font-medium text-gray-800">Report type</div>
                      <p className="mt-1 text-xs text-gray-500">Choose the audience focus for generated summaries.</p>
                    </div>
                    <div className="flex items-center gap-2">
                      {(['public', 'technical'] as const).map((t) => (
                        <button
                          key={t}
                          onClick={() => setReportType(t)}
                          className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
                            reportType === t
                              ? 'border-blue-600 bg-blue-50 text-blue-700'
                              : 'border-gray-200 text-gray-500 hover:border-gray-300'
                          }`}
                        >
                          {t === 'public' ? 'Public' : 'Technical'}
                        </button>
                      ))}
                    </div>
                  </div>
                  {/* AI toggle */}
                  <div className="flex items-start justify-between gap-4 rounded-lg border border-gray-200 px-4 py-3">
                    <div>
                      <div className="text-sm font-medium text-gray-800">Use AI for summaries</div>
                      <p className="mt-1 text-xs text-gray-500">Toggles Tokamak AI summaries when credentials are available.</p>
                    </div>
                    <button
                      onClick={() => setUseAI((prev) => !prev)}
                      className={`flex h-7 w-12 items-center rounded-full px-1 transition ${useAI ? 'bg-blue-600' : 'bg-gray-200'}`}
                    >
                      <span className={`h-5 w-5 rounded-full bg-white shadow transition ${useAI ? 'translate-x-5' : 'translate-x-0'}`} />
                    </button>
                  </div>
                  {/* AI Model Selection */}
                  <div className="rounded-lg border border-gray-200 px-4 py-3">
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <div>
                        <div className="text-sm font-medium text-gray-800">AI model selection</div>
                        <p className="mt-1 text-xs text-gray-500">Choose a model to generate the report.</p>
                      </div>
                      <div className="text-xs font-medium text-gray-500">{selectedModel || 'None'}</div>
                    </div>
                    <div className="mt-3 flex flex-col gap-3">
                      <button
                        type="button"
                        onClick={() => setShowModelMenu((prev) => !prev)}
                        className="flex w-full items-center justify-between rounded-lg border border-gray-200 bg-white px-3 py-2 text-left text-sm text-gray-700 transition hover:border-gray-300"
                      >
                        <span className="truncate">{selectedModel || 'Select model'}</span>
                        <span className="ml-3 text-xs text-gray-400">{showModelMenu ? 'Hide' : 'Edit'}</span>
                      </button>
                      {showModelMenu && (
                        <div className="rounded-lg border border-gray-200 bg-gray-50 p-3">
                          <div className="grid gap-2 sm:grid-cols-2">
                            {modelCandidateList.map((modelName) => (
                              <label key={modelName} className="flex items-center gap-2 text-sm text-gray-700">
                                <input
                                  type="radio"
                                  name="report-model"
                                  value={modelName}
                                  checked={selectedModel === modelName}
                                  onChange={() => { setSelectedModel(modelName); setShowModelMenu(false) }}
                                  className="h-4 w-4 border-gray-300 text-blue-600"
                                />
                                <span>{modelName}</span>
                              </label>
                            ))}
                          </div>
                        </div>
                      )}
                      <div className="flex flex-wrap gap-2">
                        <button
                          type="button"
                          onClick={() => setSelectedModel('gpt-5.2-pro')}
                          className="rounded-lg border border-gray-200 px-3 py-2 text-xs font-semibold text-gray-600 transition hover:border-gray-300"
                        >
                          Reset to default
                        </button>
                      </div>
                    </div>
                    <p className="mt-2 text-[11px] text-gray-500">The selected model is used for report generation.</p>
                  </div>
                  {/* Grouping */}
                  <div className="flex flex-wrap items-center justify-between gap-4 rounded-lg border border-gray-200 px-4 py-3">
                    <div>
                      <div className="text-sm font-medium text-gray-800">Report grouping</div>
                      <p className="mt-1 text-xs text-gray-500">Choose repository-based or project-based sections.</p>
                    </div>
                    <div className="flex items-center gap-2">
                      {(['repository', 'project'] as const).map((g) => (
                        <button
                          key={g}
                          onClick={() => setReportGrouping(g)}
                          className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
                            reportGrouping === g
                              ? 'border-blue-600 bg-blue-50 text-blue-700'
                              : 'border-gray-200 text-gray-500 hover:border-gray-300'
                          }`}
                        >
                          {g === 'repository' ? 'Repository' : 'Project'}
                        </button>
                      ))}
                    </div>
                  </div>
                  {/* Report format */}
                  {reportType === 'public' && (
                    <div className="rounded-lg border border-gray-200 px-4 py-3">
                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <div>
                          <div className="text-sm font-medium text-gray-800">Report format</div>
                          <p className="mt-1 text-xs text-gray-500">Choose output structure for each section.</p>
                        </div>
                        <div className="flex items-center gap-2">
                          {(['concise', 'structured'] as const).map((f) => (
                            <button
                              key={f}
                              onClick={() => setReportFormat(f)}
                              className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
                                reportFormat === f
                                  ? 'border-blue-600 bg-blue-50 text-blue-700'
                                  : 'border-gray-200 text-gray-500 hover:border-gray-300'
                              }`}
                            >
                              {f === 'concise' ? 'A: Concise' : 'B: Structured'}
                            </button>
                          ))}
                        </div>
                      </div>
                      <div className="mt-2 rounded-md bg-gray-50 px-3 py-2 text-[11px] text-gray-500">
                        {reportFormat === 'concise'
                          ? 'Format A: One-liner intro → 5 bullet points with bold titles. Compact and scannable.'
                          : 'Format B: Title → Intro paragraph → "Key Accomplishments" header → 5 bullet points. More context and structure.'}
                      </div>
                    </div>
                  )}
                  {/* Repo limit */}
                  {reportGrouping === 'repository' && (
                    <div className="flex flex-wrap items-center justify-between gap-4 rounded-lg border border-gray-200 px-4 py-3">
                      <div>
                        <div className="text-sm font-medium text-gray-800">Repository limit</div>
                        <p className="mt-1 text-xs text-gray-500">Set 0 to include all. Use a smaller number to group remaining repos.</p>
                        {repoMeta && (
                          <p className="mt-2 text-xs font-medium text-gray-600">
                            Showing {repoMeta.shown} of {repoMeta.total} repos{repoMeta.applied ? ' (others grouped)' : ''}
                          </p>
                        )}
                      </div>
                      <input
                        type="number"
                        min={0}
                        value={repoLimit}
                        onChange={(e) => setRepoLimit(e.target.value)}
                        className="w-20 rounded-lg border border-gray-200 px-3 py-2 text-sm text-gray-700 focus:outline-none"
                      />
                    </div>
                  )}
                </div>

                <button
                  onClick={handleGenerate}
                  disabled={loading}
                  className="mt-6 w-full rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? 'Generating...' : 'Generate Report'}
                </button>
              </div>
            </section>

            {/* Right: Preview */}
            <section className="space-y-6">
              <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h2 className="text-lg font-semibold text-gray-900">Generated Report</h2>
                    {reportTitle && <p className="mt-2 text-sm font-semibold text-gray-800">{reportTitle}</p>}
                    {reportHeadline && <p className="mt-1 text-sm text-gray-600">{reportHeadline}</p>}
                    <p className="mt-2 text-xs text-gray-500">{metaText}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    {(['preview', 'raw'] as const).map((v) => (
                      <button
                        key={v}
                        onClick={() => setActiveView(v)}
                        className={`rounded-lg px-3 py-1.5 text-xs font-medium ${
                          activeView === v ? 'bg-blue-50 text-blue-600' : 'bg-gray-100 text-gray-500'
                        }`}
                      >
                        {v === 'preview' ? 'Preview' : 'Raw'}
                      </button>
                    ))}
                    <button
                      onClick={() => handleCopy(fullReport ?? rawMarkdown, setCopied)}
                      className="rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-500"
                    >
                      {copied ? 'Copied!' : 'Copy'}
                    </button>
                  </div>
                </div>

                <div className="mt-5 h-[460px] overflow-y-auto rounded-xl border border-gray-200 bg-gray-50 p-5">
                  {generated ? (
                    activeView === 'preview' ? (
                      fullReport ? (
                        <div
                          className="whitespace-pre-wrap text-sm leading-6 text-gray-700"
                          dangerouslySetInnerHTML={{ __html: renderMarkdown(fullReport) }}
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
                                dangerouslySetInnerHTML={{ __html: renderMarkdown(section.content) }}
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

                {/* Proceed to Review */}
                {generated && (
                  <button
                    onClick={() => setStep(2)}
                    className="mt-4 w-full rounded-xl bg-gray-900 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-gray-800"
                  >
                    Proceed to Review &amp; Improve →
                  </button>
                )}
              </div>
            </section>
          </div>
        </main>
      </div>
    )
  }

  /* ================================================================ */
  /* STEP 2 — Review & Improve                                         */
  /* ================================================================ */

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <main className="mx-auto w-full max-w-7xl px-6 pb-16 pt-8">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <button
              onClick={() => { setStep(1); setEditingReport(false) }}
              className="mb-2 flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition"
            >
              ← Back to Generator
            </button>
            <h1 className="text-2xl font-semibold text-gray-900">Review &amp; Improve</h1>
            <p className="mt-1 text-xs text-gray-500">{metaText}</p>
          </div>
          {/* Step indicator */}
          <div className="flex items-center gap-3 text-xs">
            <span className="flex items-center gap-1.5 rounded-full border border-gray-200 px-3 py-1 text-gray-400">
              1. Generate
            </span>
            <span className="h-px w-6 bg-gray-300" />
            <span className="flex items-center gap-1.5 rounded-full bg-blue-600 px-3 py-1 font-semibold text-white">
              2. Review &amp; Improve
            </span>
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1fr_380px]">
          {/* Left: Expanded Report View */}
          <div className="space-y-4">
            {/* View toggle bar */}
            <div className="flex items-center justify-between rounded-xl border border-gray-200 bg-white px-4 py-3 shadow-sm">
              <div className="flex items-center gap-2">
                <span className={`rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase ${
                  reportType === 'public' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'
                }`}>
                  {reportType}
                </span>
                <div className="flex items-center gap-1 ml-2">
                  <button
                    onClick={() => { setViewMode('original'); setEditingReport(false) }}
                    className={`rounded-lg px-3 py-1 text-xs font-medium transition ${viewMode === 'original' && !editingReport ? 'bg-gray-100 text-gray-700' : 'text-gray-400 hover:text-gray-600'}`}
                  >
                    Original
                  </button>
                  <button
                    onClick={() => {
                      setEditingReport(true)
                      setViewMode('original')
                      if (!editableText) setEditableText(originalReport)
                    }}
                    className={`rounded-lg px-3 py-1 text-xs font-medium transition ${editingReport ? 'bg-amber-50 text-amber-700' : 'text-gray-400 hover:text-gray-600'}`}
                  >
                    Edit
                  </button>
                  {improvedReport && (
                    <>
                      <button
                        onClick={() => { setViewMode('improved'); setEditingReport(false) }}
                        className={`rounded-lg px-3 py-1 text-xs font-medium transition ${viewMode === 'improved' ? 'bg-emerald-50 text-emerald-700' : 'text-gray-400 hover:text-gray-600'}`}
                      >
                        Improved
                      </button>
                      <button
                        onClick={() => { setViewMode('diff'); setEditingReport(false) }}
                        className={`rounded-lg px-3 py-1 text-xs font-medium transition ${viewMode === 'diff' ? 'bg-purple-50 text-purple-700' : 'text-gray-400 hover:text-gray-600'}`}
                      >
                        Changes
                      </button>
                    </>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2">
                {editingReport && (
                  <button
                    onClick={() => {
                      setFullReport(editableText)
                      setRawMarkdown(editableText)
                      setEditingReport(false)
                      setViewMode('original')
                    }}
                    className="rounded-lg bg-blue-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-blue-700 transition"
                  >
                    Save Changes
                  </button>
                )}
                <button
                  onClick={() => handleCopy(currentReport, setCopiedFinal)}
                  className="rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-500 hover:bg-gray-200 transition"
                >
                  {copiedFinal ? 'Copied!' : 'Copy'}
                </button>
                <button
                  onClick={() => handleDownload(currentReport, `report-${viewMode}.md`)}
                  className="rounded-lg bg-emerald-500 px-3 py-1.5 text-xs font-semibold text-white hover:bg-emerald-600 transition"
                >
                  Download .md
                </button>
              </div>
            </div>

            {/* Report content */}
            <div className="rounded-2xl border border-gray-200 bg-white shadow-sm">
              <div className="max-h-[calc(100vh-220px)] overflow-y-auto p-8">
                {editingReport ? (
                  <textarea
                    value={editableText}
                    onChange={(e) => setEditableText(e.target.value)}
                    className="w-full h-[calc(100vh-280px)] resize-none border-0 bg-transparent font-mono text-sm leading-7 text-gray-700 focus:outline-none focus:ring-0"
                    spellCheck={false}
                  />
                ) : viewMode === 'diff' && improvedReport ? (
                  <div className="text-sm leading-7 font-mono">
                    {diffSegments.map((seg, i) => (
                      <div
                        key={i}
                        className={
                          seg.type === 'added'
                            ? 'bg-emerald-50 border-l-4 border-emerald-400 pl-3 text-emerald-800'
                            : seg.type === 'removed'
                            ? 'bg-red-50 border-l-4 border-red-300 pl-3 text-red-600 line-through'
                            : 'text-gray-700'
                        }
                      >
                        {seg.type === 'added' && <span className="text-emerald-500 font-bold mr-1">+</span>}
                        {seg.type === 'removed' && <span className="text-red-400 font-bold mr-1">−</span>}
                        {seg.text || '\u00A0'}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div
                    className="prose max-w-none whitespace-pre-wrap text-sm leading-7 text-gray-700 markdown-preview"
                    dangerouslySetInnerHTML={{ __html: renderMarkdown(currentReport) }}
                  />
                )}
              </div>
            </div>
          </div>

          {/* Right: Reviewer Panel */}
          <div className="space-y-4">
            <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
              <h3 className="text-sm font-semibold text-gray-900">Report Reviewers</h3>
              <p className="mt-1 text-[11px] text-gray-500">
                Select reviewers to evaluate the report from different perspectives.
              </p>

              {/* Reviewer expertise scale */}
              <div className="mt-3 flex items-center justify-between text-[10px] text-gray-400">
                <span>Most Public</span>
                <span className="h-px flex-1 mx-2 bg-gradient-to-r from-emerald-200 via-amber-200 to-violet-200" />
                <span>Most Expert</span>
              </div>

              {/* Review error */}
              {reviewError && (
                <div className="mt-2 rounded-lg bg-red-50 border border-red-200 p-2.5">
                  <p className="text-[11px] text-red-600">{reviewError}</p>
                </div>
              )}

              {/* Reviewer cards */}
              <div className="mt-3 space-y-2">
                {REVIEWERS.map((reviewer) => {
                  const result = reviews.find((r) => r.reviewer_level === reviewer.level)
                  const isReviewing = reviewingLevel === reviewer.level
                  const isExpanded = expandedReview === reviewer.level

                  return (
                    <div key={reviewer.level} className={`rounded-xl border transition ${result ? reviewer.border : 'border-gray-200'}`}>
                      {/* Card header */}
                      <div
                        className={`flex items-center justify-between px-4 py-3 cursor-pointer rounded-xl transition ${
                          result ? reviewer.bg : 'hover:bg-gray-50'
                        }`}
                        onClick={() => setExpandedReview(isExpanded ? null : reviewer.level)}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`h-2.5 w-2.5 rounded-full ${result ? reviewer.dot : 'bg-gray-300'}`} />
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-semibold text-gray-800">{reviewer.name_ko}</span>
                              <span className="text-[10px] text-gray-400">{reviewer.name}</span>
                              <span className={`rounded px-1.5 py-0.5 text-[9px] font-medium ${reviewer.badge}`}>Lv.{reviewer.level}</span>
                            </div>
                            <p className="text-[10px] text-gray-500 mt-0.5">{reviewer.description}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          {result && (
                            <span className={`text-sm font-bold ${scoreColor(result.review.overall_score)}`}>
                              {result.review.overall_score}/10
                            </span>
                          )}
                          {!result && !isReviewing && (
                            <button
                              onClick={(e) => { e.stopPropagation(); handleReview(reviewer.level) }}
                              className={`rounded-lg px-3 py-1 text-[11px] font-semibold transition ${reviewer.badge} hover:opacity-80`}
                            >
                              Review
                            </button>
                          )}
                          {isReviewing && (
                            <span className="flex items-center gap-1 text-[11px] text-gray-400">
                              <span className="inline-block h-3 w-3 animate-spin rounded-full border-2 border-gray-300 border-t-gray-600" />
                              Reviewing...
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Expanded content */}
                      {isExpanded && (
                        <div className="border-t border-gray-100 px-4 py-3 space-y-3">
                          {/* Persona description (always visible) */}
                          <div className={`rounded-lg p-2.5 ${reviewer.bg}`}>
                            <div className="text-[10px] font-semibold uppercase text-gray-500 mb-1">Reviewer Profile</div>
                            <p className="text-[11px] text-gray-600 leading-4">{reviewer.description}</p>
                          </div>

                          {!result ? (
                            <button
                              onClick={() => handleReview(reviewer.level)}
                              disabled={isReviewing}
                              className={`w-full rounded-lg px-3 py-2 text-xs font-semibold transition ${reviewer.badge} hover:opacity-80 disabled:opacity-50`}
                            >
                              {isReviewing ? 'Reviewing...' : `Start Review as ${reviewer.name_ko}`}
                            </button>
                          ) : (
                            <>
                              {/* Summary */}
                              <p className="text-xs text-gray-600 leading-5">{result.review.summary}</p>

                              {/* Strengths */}
                              {result.review.strengths && result.review.strengths.length > 0 && (
                                <div>
                                  <div className="text-[10px] font-semibold uppercase text-emerald-600 mb-1">Strengths</div>
                                  <ul className="space-y-1">
                                    {result.review.strengths.map((s, i) => (
                                      <li key={i} className="flex items-start gap-1.5 text-[11px] text-gray-600">
                                        <span className="mt-0.5 text-emerald-400">+</span>
                                        <span>{s}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}

                              {/* Issues with suggested changes */}
                              {result.review.issues && result.review.issues.length > 0 && (
                                <div>
                                  <div className="text-[10px] font-semibold uppercase text-gray-500 mb-1">
                                    Feedback ({result.review.issues.length})
                                  </div>
                                  <div className="space-y-2">
                                    {result.review.issues.map((issue, i) => (
                                      <div key={i} className="rounded-lg border border-gray-100 p-2.5">
                                        <div className="flex items-center gap-2 mb-1">
                                          <span className={`rounded px-1.5 py-0.5 text-[9px] font-semibold uppercase ${severityBadge(issue.severity)}`}>
                                            {issue.severity}
                                          </span>
                                          <span className="text-[10px] text-gray-400">{issue.category}</span>
                                        </div>
                                        <p className="text-[11px] text-gray-700 leading-4">{issue.description}</p>
                                        {issue.suggestion && (
                                          <p className="mt-1 text-[11px] text-blue-600 leading-4">Suggestion: {issue.suggestion}</p>
                                        )}
                                        {issue.original_text && issue.revised_text && (
                                          <div className="mt-2 space-y-1">
                                            <div className="rounded bg-red-50 px-2 py-1 text-[10px] text-red-700 line-through">{issue.original_text}</div>
                                            <div className="rounded bg-emerald-50 px-2 py-1 text-[10px] text-emerald-700">{issue.revised_text}</div>
                                          </div>
                                        )}
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              )}

                              {/* Re-review button */}
                              <button
                                onClick={() => handleReview(reviewer.level)}
                                disabled={isReviewing}
                                className="text-[11px] text-gray-400 hover:text-gray-600 transition"
                              >
                                Re-review
                              </button>
                            </>
                          )}
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>

              {/* Review all button */}
              {reviews.length < REVIEWERS.length && (
                <button
                  onClick={async () => {
                    for (const reviewer of REVIEWERS) {
                      if (!reviews.find((r) => r.reviewer_level === reviewer.level)) {
                        await handleReview(reviewer.level)
                      }
                    }
                  }}
                  disabled={reviewingLevel !== null}
                  className="mt-3 w-full rounded-lg border border-gray-200 px-3 py-2 text-xs font-medium text-gray-600 hover:bg-gray-50 transition disabled:opacity-50"
                >
                  {reviewingLevel !== null ? 'Reviewing...' : `Review All (${REVIEWERS.length - reviews.length} remaining)`}
                </button>
              )}
            </div>

            {/* Improve Section */}
            <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
              <h3 className="text-sm font-semibold text-gray-900">AI Improvement</h3>
              <p className="mt-1 text-[11px] text-gray-500">
                Use reviewer feedback to generate an improved version of the report.
              </p>

              {reviews.length > 0 && (
                <div className="mt-3 rounded-lg bg-gray-50 p-3">
                  <div className="flex items-center justify-between text-xs text-gray-600">
                    <span>{reviews.length} review{reviews.length > 1 ? 's' : ''} collected</span>
                    <span className="font-medium">
                      Avg score: {(reviews.reduce((sum, r) => sum + r.review.overall_score, 0) / reviews.length).toFixed(1)}/10
                    </span>
                  </div>
                  <div className="mt-2 flex flex-wrap gap-1">
                    {reviews.map((r) => (
                      <span key={r.reviewer_level} className={`rounded px-2 py-0.5 text-[10px] font-medium ${
                        REVIEWERS.find((rv) => rv.level === r.reviewer_level)?.badge ?? 'bg-gray-100 text-gray-600'
                      }`}>
                        {r.reviewer_ko} {r.review.overall_score}/10
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <button
                onClick={handleImprove}
                disabled={reviews.length === 0 || improving}
                className="mt-3 w-full rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {improving ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    Improving...
                  </span>
                ) : reviews.length === 0 ? (
                  'Run at least 1 review first'
                ) : (
                  'Improve Report with AI'
                )}
              </button>

              {improvedReport && (
                <div className="mt-3 rounded-lg bg-emerald-50 border border-emerald-200 p-3">
                  <div className="flex items-center gap-2 text-xs font-semibold text-emerald-700">
                    <span className="flex h-4 w-4 items-center justify-center rounded-full bg-emerald-200 text-[10px]">&#10003;</span>
                    Improved report generated
                  </div>
                  <p className="mt-1 text-[11px] text-emerald-600">
                    Switch to &quot;Improved&quot; tab above to view the result.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
