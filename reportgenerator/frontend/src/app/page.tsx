'use client'

import { useEffect, useMemo, useState, useCallback, useRef } from 'react'
import { CalendarDays, Upload } from 'lucide-react'
import { useDropzone } from 'react-dropzone'
import dynamic from 'next/dynamic'

// Dynamic import for VisualReport to avoid SSR issues with recharts
const VisualReport = dynamic(
  () => import('./VisualReport').catch((err) => {
    console.error('Failed to load VisualReport chunk:', err)
    // Return a fallback component on chunk load failure
    return { default: ({ stats }: any) => (
      <div className="p-8 text-center text-gray-500">
        <p className="text-lg font-medium mb-2">Visual report could not be loaded</p>
        <p className="text-sm">Switch to Raw view to see the report content. ({String(err?.message || err)})</p>
      </div>
    )}
  }),
  { ssr: false }
)

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

interface AppliedChange {
  issueKey: string
  reviewerKo: string
  category: string
  originalText: string
  revisedText: string
}

interface DiffSegment {
  type: 'unchanged' | 'added' | 'removed'
  text: string
}

interface ReportSection {
  project: string
  title: string
  content: string
}

interface ReviewHistoryEntry {
  id: string
  timestamp: string
  dateRange: { start: string; end: string }
  model: string
  reviews: Array<{
    reviewer_level: number
    reviewer_ko: string
    score: number
  }>
  avgScore: number
  report: string
  improvedReport?: string
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

// Default models - will be updated from server if available
const DEFAULT_MODEL_OPTIONS = [
  'gpt-5.2-pro',
  'gpt-5.2',
  'gpt-5.2-codex',
  'deepseek-v3.2',
  'deepseek-chat',
  'gemini-3-pro',
  'gemini-3-flash',
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
    .replace(/^### (.+)$/gm, '<h3 style="font-size:1.25rem;font-weight:700;color:#111827;margin:1.5rem 0 0.5rem;padding-bottom:0.4rem;border-bottom:1px solid #e5e7eb;white-space:normal">$1</h3>')
    .replace(/^#### (.+)$/gm, '<h4 style="font-size:1.1rem;font-weight:600;color:#1f2937;margin:1rem 0 0.5rem;white-space:normal">$1</h4>')
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
  const [step, setStep] = useState<1 | 2 | 3>(1)

  /* ---- Step 1: Generate ---- */
  const [period, setPeriod] = useState('weekly')
  const [startDate, setStartDate] = useState('2026. 02. 01.')
  const [endDate, setEndDate] = useState('2026. 02. 10.')
  const [useAI, setUseAI] = useState(true)
  const [reportType, setReportType] = useState<'public' | 'technical'>('public')
  const [reportGrouping, setReportGrouping] = useState<'repository' | 'project'>('repository')
  const [reportFormat, setReportFormat] = useState<'comprehensive' | 'concise' | 'structured'>('comprehensive')
  const [outputFormat, setOutputFormat] = useState<'markdown' | 'html'>('html')
  const [htmlReport, setHtmlReport] = useState<string | null>(null)
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
  const [stats, setStats] = useState<{
    commits: number
    repos: number
    prs: number
    linesAdded?: number
    linesDeleted?: number
    totalChanges?: number
    netChange?: number
    contributors?: number
  } | null>(null)
  const [dateRange, setDateRange] = useState<{ start: string | null; end: string | null; days: number | null } | null>(null)
  const [reportHeadline, setReportHeadline] = useState<string | null>(null)
  const [fullReport, setFullReport] = useState<string | null>(null)
  const [fullReportEn, setFullReportEn] = useState<string | null>(null)
  const [fullReportKr, setFullReportKr] = useState<string | null>(null)
  const [repoMeta, setRepoMeta] = useState<{ applied: boolean; total: number; shown: number } | null>(null)
  const [selectedModel, setSelectedModel] = useState('gpt-5.2-pro')
  const [showModelMenu, setShowModelMenu] = useState(false)
  const [reportLanguage, setReportLanguage] = useState<'en' | 'kr' | 'both'>('en')
  const [reportNumber, setReportNumber] = useState('2')
  const [reportTitle, setReportTitle] = useState('')
  const [langTab, setLangTab] = useState<'en' | 'kr'>('en')

  /* ---- Step 2: Review & Improve ---- */
  const [reviews, setReviews] = useState<ReviewResult[]>([])
  const [reviewingLevel, setReviewingLevel] = useState<number | null>(null)
  const [expandedReview, setExpandedReview] = useState<number | null>(null)
  const [improving, setImproving] = useState(false)
  const [improveError, setImproveError] = useState<string | null>(null)
  const [improvedReport, setImprovedReport] = useState<string | null>(null)
  const [copiedFinal, setCopiedFinal] = useState(false)
  const [viewMode, setViewMode] = useState<'original' | 'improved' | 'diff' | 'visual'>('original')
  const [editingReport, setEditingReport] = useState(false)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [reportSummaries, setReportSummaries] = useState<Record<string, any>>({})
  const [editableText, setEditableText] = useState('')
  const [reviewError, setReviewError] = useState<string | null>(null)
  const [highlightedText, setHighlightedText] = useState<string | null>(null)
  const [appliedIssues, setAppliedIssues] = useState<Set<string>>(new Set())
  const [appliedChanges, setAppliedChanges] = useState<AppliedChange[]>([])
  const [excludedIssues, setExcludedIssues] = useState<Set<string>>(new Set())
  const [selectedReviewers, setSelectedReviewers] = useState<Set<number>>(new Set())
  const [preScores, setPreScores] = useState<Record<number, number>>({})
  const [postScores, setPostScores] = useState<Record<number, number>>({})
  const [reReviewing, setReReviewing] = useState(false)
  const [copiedMedium, setCopiedMedium] = useState(false)
  const [editingPublish, setEditingPublish] = useState(false)
  const [editablePublishText, setEditablePublishText] = useState('')
  const reportContentRef = useRef<HTMLDivElement>(null)

  // Podcast state
  const [podcastScript, setPodcastScript] = useState<string | null>(null)
  const [podcastAudio, setPodcastAudio] = useState<string | null>(null)
  const [generatingScript, setGeneratingScript] = useState(false)
  const [generatingAudio, setGeneratingAudio] = useState(false)
  const [podcastError, setPodcastError] = useState<string | null>(null)
  const [availableModels, setAvailableModels] = useState<string[]>(DEFAULT_MODEL_OPTIONS)

  // Verify state
  const [verifying, setVerifying] = useState(false)
  const [verifyResult, setVerifyResult] = useState<{
    summary: {
      total_repos_checked: number
      repos_with_stat_issues: number
      total_accomplishments: number
      phantom_features: number
      invented_contributors: number
      accuracy_score: number
    }
    details: Array<{
      repo: string
      stat_issues: Array<{ metric: string; stated: number; actual: number }>
      phantom_bullets: string[]
      invented_contributors: string[]
    }>
    overall_grade: string
  } | null>(null)
  const [verifyExpanded, setVerifyExpanded] = useState(false)

  // Review history state
  const [reviewHistory, setReviewHistory] = useState<ReviewHistoryEntry[]>([])
  const [showHistory, setShowHistory] = useState(false)

  // Fetch available models from server on mount
  useEffect(() => {
    fetch('http://localhost:8010/api/health')
      .then(res => res.json())
      .then(data => {
        if (data.tokamak_models && data.tokamak_models.length > 0) {
          setAvailableModels(data.tokamak_models)
        }
      })
      .catch(() => {
        // Keep default models on error
      })
  }, [])

  // Load review history from localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem('reviewHistory')
      if (saved) {
        setReviewHistory(JSON.parse(saved))
      }
    } catch {
      // Ignore parse errors
    }
  }, [])

  // Save current review to history
  const saveToHistory = useCallback(() => {
    if (!dateRange?.start || !dateRange?.end || reviews.length === 0) return

    const entry: ReviewHistoryEntry = {
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      dateRange: { start: dateRange.start, end: dateRange.end },
      model: selectedModel,
      reviews: reviews.map(r => ({
        reviewer_level: r.reviewer_level,
        reviewer_ko: r.reviewer_ko,
        score: r.review.overall_score,
      })),
      avgScore: reviews.reduce((sum, r) => sum + r.review.overall_score, 0) / reviews.length,
      report: fullReport ?? rawMarkdown,
      improvedReport: improvedReport ?? undefined,
    }

    setReviewHistory(prev => {
      // Check if this exact entry already exists (same timestamp within 1 minute)
      const isDuplicate = prev.some(h =>
        h.dateRange.start === entry.dateRange.start &&
        h.dateRange.end === entry.dateRange.end &&
        h.model === entry.model &&
        Math.abs(new Date(h.timestamp).getTime() - new Date(entry.timestamp).getTime()) < 60000
      )
      if (isDuplicate) return prev

      const updated = [entry, ...prev].slice(0, 50) // Keep last 50 entries
      localStorage.setItem('reviewHistory', JSON.stringify(updated))
      return updated
    })
  }, [dateRange, reviews, selectedModel, fullReport, rawMarkdown, improvedReport])

  // Get history entries matching current date range
  const matchingHistory = useMemo(() => {
    if (!dateRange?.start || !dateRange?.end) return []
    return reviewHistory.filter(
      h => h.dateRange.start === dateRange.start && h.dateRange.end === dateRange.end
    )
  }, [reviewHistory, dateRange])

  // Load a history entry
  const loadHistoryEntry = (entry: ReviewHistoryEntry) => {
    setFullReport(entry.report)
    setRawMarkdown(entry.report)
    if (entry.improvedReport) {
      setImprovedReport(entry.improvedReport)
      setViewMode('improved')
    } else {
      setImprovedReport(null)
      setViewMode('original')
    }
    setShowHistory(false)
  }

  // Delete a history entry
  const deleteHistoryEntry = (id: string) => {
    setReviewHistory(prev => {
      const updated = prev.filter(h => h.id !== id)
      localStorage.setItem('reviewHistory', JSON.stringify(updated))
      return updated
    })
  }

  // Auto-save to history when proceeding to publish or when improved report is generated
  useEffect(() => {
    if (step === 3 && reviews.length > 0) {
      saveToHistory()
    }
  }, [step, saveToHistory, reviews.length])

  // Also save when improved report is generated
  useEffect(() => {
    if (improvedReport && reviews.length > 0) {
      saveToHistory()
    }
  }, [improvedReport, saveToHistory, reviews.length])

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

  const modelCandidateList = [...availableModels]
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
      formData.append('output_format', outputFormat)
      formData.append('repo_limit', repoLimit)
      formData.append('model', selectedModel)
      formData.append('language', reportLanguage)
      formData.append('report_number', reportNumber)
      formData.append('report_title', reportTitle)

      const response = await fetch('http://localhost:8010/api/generate', {
        method: 'POST',
        body: formData,
      })
      if (!response.ok) throw new Error('Failed to generate report')

      const data = await response.json()
      console.log('[DEBUG] full_report type:', typeof data.full_report, 'value:', data.full_report ? data.full_report.substring(0, 100) : data.full_report)
      console.log('[DEBUG] sections count:', data.sections?.length, 'titles:', data.sections?.map((s: { title?: string }) => s.title))
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
            data.sections?.map((s: { title?: string; content: string }) =>
              `${s.title ? `\n### ${s.title}\n\n` : '\n'}${s.content}`
            ).join('\n') ?? '',
          ].join('\n')

      console.log('[DEBUG] fullReportContent is null:', fullReportContent === null)
      console.log('[DEBUG] rawContent first 500 chars:', rawContent.substring(0, 500))

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
      setStats({
        commits: data.stats?.total_commits ?? 0,
        repos: data.stats?.total_repos ?? 0,
        prs: data.stats?.total_prs ?? 0,
        linesAdded: data.stats?.total_lines_added ?? 0,
        linesDeleted: data.stats?.total_lines_deleted ?? 0,
        totalChanges: data.stats?.total_changes ?? 0,
        netChange: data.stats?.net_change ?? 0,
        contributors: data.stats?.total_contributors ?? 0,
      })
      setDateRange(data.date_range || null)
      setReportSummaries(data.summaries || {})
      setHtmlReport(data.html_report || null)
      setFullReportEn(data.full_report_en || null)
      setFullReportKr(data.full_report_kr || null)
      setGenerated(true)
      setActiveView('preview')

      // Reset review state
      setReviews([])
      setImprovedReport(null)
      // Default to visual mode for comprehensive format
      setViewMode(reportFormat === 'comprehensive' ? 'visual' : 'original')
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
      const response = await fetch('http://localhost:8010/api/analyze', { method: 'POST', body: formData })
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

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return
    const dropped = acceptedFiles[0]
    console.log('[DEBUG] File dropped:', dropped.name)
    setFileName(dropped.name)
    setFile(dropped)
    setPeriodSource('detected')

    // Inline analyze to avoid stale closure
    setAnalyzing(true)
    setAnalysisError(null)
    try {
      const formData = new FormData()
      formData.append('file', dropped)
      const response = await fetch('http://localhost:8010/api/analyze', { method: 'POST', body: formData })
      if (!response.ok) throw new Error('Failed to analyze CSV')
      const data = await response.json()
      console.log('[DEBUG] CSV analysis result:', data)
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
      console.error('[DEBUG] CSV analysis error:', error)
      setAnalysisError(error instanceof Error ? error.message : 'Failed to analyze CSV')
    } finally {
      setAnalyzing(false)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.csv'],
      'text/plain': ['.csv'],
    },
    multiple: false,
    noClick: false,
    noKeyboard: false,
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

      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 360000) // 6-minute timeout for large reports

      const response = await fetch('http://localhost:8010/api/review', {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      })
      clearTimeout(timeoutId)

      if (!response.ok) {
        let errorMsg = `HTTP ${response.status}`
        try {
          const errData = await response.json()
          errorMsg = errData.detail || errData.error || errorMsg
        } catch { /* ignore parse error */ }
        throw new Error(errorMsg)
      }

      const data = await response.json()
      if (data.success) {
        setReviews((prev) => {
          const filtered = prev.filter((r) => r.reviewer_level !== level)
          return [...filtered, data as ReviewResult].sort((a, b) => a.reviewer_level - b.reviewer_level)
        })
        // Only auto-select reviewer if the review has actionable feedback (issues)
        if (data.review?.issues?.length > 0) {
          setSelectedReviewers((prev) => { const next = new Set(Array.from(prev)); next.add(level); return next })
        }
        setExpandedReview(level)
      } else {
        setReviewError(`Review failed: ${data.error || 'Unknown error'}`)
      }
    } catch (error) {
      if (error instanceof DOMException && error.name === 'AbortError') {
        setReviewError('Review timed out (6 min). Try again or use a faster model.')
      } else {
        setReviewError(`Review failed: ${error instanceof Error ? error.message : 'Network error'}`)
      }
    } finally {
      setReviewingLevel(null)
    }
  }

  const handleApplyIssue = (issue: ReviewIssue, reviewerKo?: string) => {
    if (!issue.original_text || !issue.revised_text) return
    const issueKey = `${issue.original_text}::${issue.revised_text}`
    const report = editingReport ? editableText : (fullReport ?? rawMarkdown)

    // Try exact match first
    let updated = report.replace(issue.original_text, issue.revised_text)

    // If exact match failed, try flexible whitespace matching
    if (updated === report) {
      try {
        const escaped = issue.original_text
          .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
          .replace(/\s+/g, '\\s+')
        const regex = new RegExp(escaped)
        updated = report.replace(regex, issue.revised_text)
      } catch { /* regex construction failed */ }
    }

    // If still failed, try case-insensitive match
    if (updated === report) {
      try {
        const escaped = issue.original_text
          .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
          .replace(/\s+/g, '\\s+')
        const regex = new RegExp(escaped, 'i')
        updated = report.replace(regex, issue.revised_text)
      } catch { /* regex construction failed */ }
    }

    if (updated !== report) {
      setFullReport(updated)
      setRawMarkdown(updated)
      if (editingReport) setEditableText(updated)
      setAppliedIssues((prev) => { const next = new Set(Array.from(prev)); next.add(issueKey); return next })
      setAppliedChanges((prev) => [...prev, {
        issueKey,
        reviewerKo: reviewerKo ?? 'Reviewer',
        category: issue.category,
        originalText: issue.original_text!,
        revisedText: issue.revised_text!,
      }])
      setHighlightedText(null)
    }
  }

  const handleUndoChange = (change: AppliedChange) => {
    const report = editingReport ? editableText : (fullReport ?? rawMarkdown)

    // Replace revised text back with original text
    let reverted = report.replace(change.revisedText, change.originalText)

    // Try flexible whitespace matching if exact match failed
    if (reverted === report) {
      try {
        const escaped = change.revisedText
          .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
          .replace(/\s+/g, '\\s+')
        const regex = new RegExp(escaped)
        reverted = report.replace(regex, change.originalText)
      } catch { /* regex construction failed */ }
    }

    if (reverted !== report) {
      setFullReport(reverted)
      setRawMarkdown(reverted)
      if (editingReport) setEditableText(reverted)

      // Remove from appliedIssues
      setAppliedIssues((prev) => {
        const next = new Set(Array.from(prev))
        next.delete(change.issueKey)
        return next
      })

      // Remove from appliedChanges
      setAppliedChanges((prev) => prev.filter((c) => c.issueKey !== change.issueKey))
    }
  }

  const handleHighlightIssue = (originalText: string | undefined) => {
    if (!originalText) return
    if (highlightedText === originalText) {
      setHighlightedText(null)
      return
    }
    setHighlightedText(originalText)
    if (editingReport) {
      setEditingReport(false)
      setViewMode('original')
    }
    setTimeout(() => {
      const el = reportContentRef.current?.querySelector('[data-highlight="active"]')
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }, 100)
  }

  const renderMarkdownWithHighlight = (md: string) => {
    let html = renderMarkdown(md)

    // Highlight applied changes inline in the report body
    if (appliedChanges.length > 0 && viewMode === 'original' && !editingReport && !highlightedText) {
      for (const change of appliedChanges) {
        const escapedRegex = change.revisedText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
        try {
          // HTML-escape original text for safe display
          const origDisplay = change.originalText
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
          const truncOrig = origDisplay.length > 120 ? origDisplay.slice(0, 120) + '…' : origDisplay
          html = html.replace(
            new RegExp(`(${escapedRegex})`),
            `<span class="applied-change-inline" style="position:relative;">` +
            `<del style="color:#f87171;background:#fef2f2;border-radius:2px;padding:0 2px;font-size:0.7em;line-height:1;vertical-align:baseline;text-decoration:line-through;">${truncOrig}</del>` +
            `<span style="color:#d1d5db;font-size:0.7em;margin:0 3px;">→</span>` +
            `<ins style="color:#047857;background:#ecfdf5;border-bottom:2px solid #34d399;border-radius:2px;padding:0 2px;text-decoration:none;">$1</ins>` +
            `</span>`
          )
        } catch { /* regex construction failed */ }
      }
    }

    // Highlight preview text (yellow) — takes precedence (applied-change highlights skipped when highlightedText is set)
    if (highlightedText) {
      const escaped = highlightedText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      html = html.replace(
        new RegExp(`(${escaped})`, 'gi'),
        '<mark data-highlight="active" class="bg-yellow-200 ring-2 ring-yellow-400 rounded px-0.5">$1</mark>'
      )
    }
    return html
  }

  const handleImprove = async () => {
    // Filter selected reviews, exclude already-applied and user-excluded issues
    const activeReviews = reviews
      .filter((r) => selectedReviewers.has(r.reviewer_level))
      .map((r) => ({
        ...r,
        review: {
          ...r.review,
          issues: r.review.issues.filter((issue) => {
            if (!issue.original_text || !issue.revised_text) return true
            const issueKey = `${issue.original_text}::${issue.revised_text}`
            return !appliedIssues.has(issueKey) && !excludedIssues.has(issueKey)
          })
        }
      }))
    if (activeReviews.length === 0) return
    setImproving(true)
    setImproveError(null)

    // Save pre-improvement scores
    const scores: Record<number, number> = {}
    activeReviews.forEach((r) => { scores[r.reviewer_level] = r.review.overall_score })
    setPreScores(scores)
    setPostScores({})

    try {
      const reportText = editingReport ? editableText : (fullReport ?? rawMarkdown)
      const formData = new FormData()
      formData.append('report_text', reportText)
      formData.append('report_type', reportType)
      formData.append('report_format', reportFormat)
      formData.append('reviews_json', JSON.stringify(activeReviews))
      formData.append('model', selectedModel)

      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 360000) // 6-minute timeout for slower models

      const response = await fetch('http://localhost:8010/api/improve', {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      })
      clearTimeout(timeoutId)

      if (!response.ok) throw new Error('Improve request failed')

      const data = await response.json()
      if (data.success && data.improved_report) {
        setImprovedReport(data.improved_report)
        setViewMode('diff')

        // Automatically start re-review in background
        setReReviewing(true)
        const levels = Object.keys(scores).map(Number)
        Promise.allSettled(
          levels.map(async (level) => {
            const reviewFormData = new FormData()
            reviewFormData.append('report_text', data.improved_report)
            reviewFormData.append('report_type', reportType)
            reviewFormData.append('report_format', reportFormat)
            reviewFormData.append('reviewer_level', level.toString())
            reviewFormData.append('model', selectedModel)

            const previousReview = reviews.find((r) => r.reviewer_level === level)
            if (previousReview) {
              reviewFormData.append('is_improved', 'true')
              reviewFormData.append('previous_score', (previousReview.review?.overall_score ?? '').toString())
              reviewFormData.append('previous_summary', previousReview.review?.summary ?? '')
            }

            const reviewResponse = await fetch('http://localhost:8010/api/review', { method: 'POST', body: reviewFormData })
            if (!reviewResponse.ok) return { level, score: null }
            const reviewData = await reviewResponse.json()
            return { level, score: reviewData.success ? reviewData.review.overall_score : null }
          })
        ).then((results) => {
          const newPostScores: Record<number, number> = {}
          for (const result of results) {
            if (result.status === 'fulfilled' && result.value.score !== null) {
              newPostScores[result.value.level] = result.value.score
            }
          }
          setPostScores(newPostScores)
          setReReviewing(false)
        }).catch(() => setReReviewing(false))
      } else {
        setImproveError(data.error || 'Improvement returned empty result. Try again.')
      }
    } catch (error) {
      const msg = error instanceof Error && error.name === 'AbortError'
        ? 'Improvement timed out (6 min). Try a shorter report or different model.'
        : `Improve failed: ${error instanceof Error ? error.message : 'Network error'}`
      setImproveError(msg)
      console.error('Improve failed:', error)
    } finally {
      setImproving(false)
    }
  }

  const handleReReviewImproved = async () => {
    if (!improvedReport) return
    setReReviewing(true)

    try {
      const levels = Object.keys(preScores).map(Number)
      const results = await Promise.allSettled(
        levels.map(async (level) => {
          const formData = new FormData()
          formData.append('report_text', improvedReport)
          formData.append('report_type', reportType)
          formData.append('report_format', reportFormat)
          formData.append('reviewer_level', level.toString())
          formData.append('model', selectedModel)

          // Pass previous review context so reviewer can compare against their prior assessment
          const previousReview = reviews.find((r) => r.reviewer_level === level)
          if (previousReview) {
            formData.append('is_improved', 'true')
            formData.append('previous_score', (previousReview.review?.overall_score ?? '').toString())
            formData.append('previous_summary', previousReview.review?.summary ?? '')
          }

          const response = await fetch('http://localhost:8010/api/review', { method: 'POST', body: formData })
          if (!response.ok) return { level, score: null }
          const data = await response.json()
          return { level, score: data.success ? data.review.overall_score : null }
        })
      )

      const newPostScores: Record<number, number> = {}
      for (const result of results) {
        if (result.status === 'fulfilled' && result.value.score !== null) {
          newPostScores[result.value.level] = result.value.score
        }
      }
      setPostScores(newPostScores)
    } catch (error) {
      console.error('Re-review failed:', error)
    } finally {
      setReReviewing(false)
    }
  }

  const handleVerify = async () => {
    if (!file || !fullReport) return
    setVerifying(true)
    setVerifyResult(null)
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('report_text', fullReport)
      formData.append('report_grouping', reportGrouping)
      const response = await fetch('http://localhost:8010/api/verify', { method: 'POST', body: formData })
      if (!response.ok) throw new Error('Verify failed')
      const data = await response.json()
      if (data.success) {
        setVerifyResult({ summary: data.summary, details: data.details, overall_grade: data.overall_grade })
      }
    } catch (error) {
      console.error('Verify failed:', error)
    } finally {
      setVerifying(false)
    }
  }

  const handleGeneratePodcast = async () => {
    const reportText = improvedReport || fullReport || rawMarkdown
    if (!reportText) return

    setGeneratingScript(true)
    setPodcastError(null)
    setPodcastScript(null)
    setPodcastAudio(null)

    try {
      // Step 1: Generate script
      const scriptFormData = new FormData()
      scriptFormData.append('report_text', reportText)
      scriptFormData.append('duration_minutes', '4')

      const scriptResponse = await fetch('http://localhost:8010/api/generate-podcast-script', {
        method: 'POST',
        body: scriptFormData,
      })

      const scriptData = await scriptResponse.json()
      if (!scriptData.success) {
        setPodcastError(scriptData.error || 'Failed to generate script')
        setGeneratingScript(false)
        return
      }

      setPodcastScript(scriptData.script)
      setGeneratingScript(false)
      setGeneratingAudio(true)

      // Step 2: Generate audio
      const audioFormData = new FormData()
      audioFormData.append('script', scriptData.script)

      const audioResponse = await fetch('http://localhost:8010/api/generate-podcast-audio', {
        method: 'POST',
        body: audioFormData,
      })

      const audioData = await audioResponse.json()
      if (!audioData.success) {
        setPodcastError(audioData.error || 'Failed to generate audio')
        setGeneratingAudio(false)
        return
      }

      setPodcastAudio(audioData.audio_base64)
    } catch (error) {
      setPodcastError(`Podcast generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setGeneratingScript(false)
      setGeneratingAudio(false)
    }
  }

  const handleDownloadPodcast = () => {
    if (!podcastAudio) return

    const byteCharacters = atob(podcastAudio)
    const byteNumbers = new Array(byteCharacters.length)
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i)
    }
    const byteArray = new Uint8Array(byteNumbers)
    const blob = new Blob([byteArray], { type: 'audio/mp3' })
    const url = URL.createObjectURL(blob)

    const a = document.createElement('a')
    a.href = url
    a.download = `podcast-report-${dateRange?.start ?? 'draft'}.mp3`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const convertToMediumFormat = (md: string): string => {
    return md
      // Convert header markers (# ## ### ####) to bold text for Medium
      .replace(/^#{1,4}\s+(.+)$/gm, '**$1**')
      // Keep bold markers (**text**) - Medium supports these
      // Remove italic markers (*text* or _text_) - keep text only
      .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '$1')
      .replace(/_([^_]+)_/g, '$1')
      // Convert markdown links [text](url) to "text (url)"
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '$1 ($2)')
      // Convert bullet points (* or -) to simple dash
      .replace(/^[\*\-]\s+/gm, '• ')
      // Remove code blocks ```
      .replace(/```[\s\S]*?```/g, '')
      // Remove inline code `text`
      .replace(/`([^`]+)`/g, '$1')
      // Clean up excessive newlines
      .replace(/\n{3,}/g, '\n\n')
      .trim()
  }

  /* ================================================================ */
  /* STEP 1 — Generate                                                 */
  /* ================================================================ */

  if (step === 1) {
    return (
      <div className="min-h-screen tokamak-grid text-gray-900">
        <main className="mx-auto w-full max-w-6xl px-6 pb-16 pt-12">
          <div className="mb-10">
            <h1 className="text-4xl font-light tracking-tight text-gray-900">
              BIWEEKLY REPORT
              <span className="block text-2xl font-normal text-gray-400 mt-1">GENERATOR</span>
            </h1>
            <p className="mt-4 text-sm text-gray-500">
              Generate ecosystem reports from GitHub activity data, then review and refine with AI reviewers.
            </p>
            {/* Step indicator */}
            <div className="mt-6 flex items-center gap-3 text-xs">
              <span className="flex items-center gap-1.5 rounded-full bg-gray-900 px-4 py-1.5 font-semibold text-white">
                1. Generate
              </span>
              <span className="h-px w-8 bg-gray-300" />
              <span className="flex items-center gap-1.5 rounded-full border border-gray-300 px-4 py-1.5 text-gray-400">
                2. Review
              </span>
              <span className="h-px w-8 bg-gray-300" />
              <span className="flex items-center gap-1.5 rounded-full border border-gray-300 px-4 py-1.5 text-gray-400">
                3. Publish
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
                  {/* Language */}
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <div className="text-sm font-medium text-gray-800">Language</div>
                      <p className="mt-1 text-xs text-gray-500">Choose the report language.</p>
                    </div>
                    <div className="flex items-center gap-2">
                      {([['en', 'English'], ['kr', '한국어'], ['both', 'Both (Toggle)']] as const).map(([val, label]) => (
                        <button
                          key={val}
                          onClick={() => setReportLanguage(val as 'en' | 'kr' | 'both')}
                          className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
                            reportLanguage === val
                              ? val === 'both'
                                ? 'border-violet-600 bg-violet-50 text-violet-700'
                                : 'border-blue-600 bg-blue-50 text-blue-700'
                              : 'border-gray-200 text-gray-500 hover:border-gray-300'
                          }`}
                        >
                          {label}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Report Title */}
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <div className="text-sm font-medium text-gray-800">Report Title</div>
                      <p className="mt-1 text-xs text-gray-500">Cover page title (e.g. &quot;Biweekly Report #2&quot;)</p>
                    </div>
                    <input
                      type="text"
                      value={reportTitle}
                      onChange={(e) => setReportTitle(e.target.value)}
                      placeholder="Biweekly Report #2"
                      className="w-56 rounded-lg border border-gray-200 px-3 py-1.5 text-sm text-gray-800 focus:border-blue-500 focus:outline-none"
                    />
                  </div>

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
                          {(['comprehensive', 'concise', 'structured'] as const).map((f) => (
                            <button
                              key={f}
                              onClick={() => setReportFormat(f)}
                              className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
                                reportFormat === f
                                  ? f === 'comprehensive'
                                    ? 'border-violet-600 bg-violet-50 text-violet-700'
                                    : 'border-blue-600 bg-blue-50 text-blue-700'
                                  : 'border-gray-200 text-gray-500 hover:border-gray-300'
                              }`}
                            >
                              {f === 'comprehensive' ? 'Comprehensive' : f === 'concise' ? 'Concise' : 'Structured'}
                            </button>
                          ))}
                        </div>
                      </div>
                      <div className="mt-2 rounded-md bg-gray-50 px-3 py-2 text-[11px] text-gray-500">
                        {reportFormat === 'comprehensive'
                          ? '📊 Full detailed report: ALL repositories included with statistics, goals, accomplishments, and GitHub links. Best for investors.'
                          : reportFormat === 'concise'
                          ? 'Format A: One-liner intro → 5 bullet points with bold titles. Compact and scannable.'
                          : 'Format B: Title → Intro paragraph → "Key Accomplishments" header → 5 bullet points. More context and structure.'}
                      </div>
                    </div>
                  )}
                  {/* Output format toggle (only for comprehensive + public) */}
                  {reportFormat === 'comprehensive' && reportType === 'public' && (
                    <div className="rounded-lg border border-gray-200 px-4 py-3">
                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <div>
                          <div className="text-sm font-medium text-gray-800">Output format</div>
                          <p className="mt-1 text-xs text-gray-500">Generate styled HTML in addition to Markdown.</p>
                        </div>
                        <div className="flex items-center gap-2">
                          {(['markdown', 'html'] as const).map((f) => (
                            <button
                              key={f}
                              onClick={() => setOutputFormat(f)}
                              className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
                                outputFormat === f
                                  ? f === 'html'
                                    ? 'border-orange-600 bg-orange-50 text-orange-700'
                                    : 'border-gray-600 bg-gray-50 text-gray-700'
                                  : 'border-gray-200 text-gray-500 hover:border-gray-300'
                              }`}
                            >
                              {f === 'html' ? '🌐 HTML' : '📝 Markdown'}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                  {/* Repo limit - hidden for comprehensive mode which includes all repos */}
                  {reportGrouping === 'repository' && reportFormat !== 'comprehensive' && (
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
                  {/* Info for comprehensive mode */}
                  {reportGrouping === 'repository' && reportFormat === 'comprehensive' && (
                    <div className="rounded-lg border border-violet-200 bg-violet-50 px-4 py-3">
                      <div className="text-sm font-medium text-violet-800">All repositories included</div>
                      <p className="mt-1 text-xs text-violet-600">
                        Comprehensive mode includes ALL active repositories with detailed statistics and GitHub links.
                      </p>
                    </div>
                  )}
                </div>

                <button
                  onClick={handleGenerate}
                  disabled={loading}
                  className="mt-6 w-full rounded-full bg-gray-900 px-6 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-gray-800 hover:shadow-lg disabled:opacity-50"
                >
                  {loading ? 'Generating...' : 'GENERATE REPORT'}
                </button>
                <button
                  onClick={async () => {
                    if (!file) return
                    const fd = new FormData()
                    fd.append('file', file)
                    try {
                      const res = await fetch('http://localhost:8010/api/infographic', { method: 'POST', body: fd })
                      if (!res.ok) throw new Error(await res.text())
                      const blob = await res.blob()
                      const url = URL.createObjectURL(blob)
                      window.open(url, '_blank')
                    } catch (e) {
                      alert(`Infographic error: ${e instanceof Error ? e.message : e}`)
                    }
                  }}
                  disabled={!file || loading}
                  className="mt-3 w-full rounded-full border-2 border-blue-500 bg-white px-6 py-3 text-sm font-semibold text-blue-600 shadow-sm transition hover:bg-blue-50 hover:shadow-lg disabled:opacity-50"
                >
                  🗺️ Ecosystem Map
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

                {/* Bilingual tab switcher */}
                {generated && reportLanguage === 'both' && fullReportEn && fullReportKr && (
                  <div className="mt-4 flex items-center gap-1 rounded-lg bg-gray-100 p-1 w-fit">
                    <button
                      onClick={() => setLangTab('en')}
                      className={`rounded-md px-3 py-1.5 text-xs font-medium transition ${langTab === 'en' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
                    >
                      🇺🇸 English
                    </button>
                    <button
                      onClick={() => setLangTab('kr')}
                      className={`rounded-md px-3 py-1.5 text-xs font-medium transition ${langTab === 'kr' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
                    >
                      🇰🇷 한국어
                    </button>
                  </div>
                )}

                <div className="mt-5 h-[460px] overflow-y-auto rounded-xl border border-gray-200 bg-gray-50 p-5">
                  {generated ? (
                    activeView === 'preview' ? (
                      <div
                        className="prose max-w-none whitespace-pre-wrap text-sm leading-7 text-gray-700 markdown-preview"
                        dangerouslySetInnerHTML={{ __html: renderMarkdown(
                          reportLanguage === 'both' && langTab === 'kr' && fullReportKr
                            ? fullReportKr
                            : (reportLanguage === 'both' && langTab === 'en' && fullReportEn
                              ? fullReportEn
                              : (fullReport ?? rawMarkdown))
                        ) }}
                      />
                    ) : (
                      <div className="h-full whitespace-pre-wrap rounded-lg bg-white p-4 font-mono text-xs text-gray-700">
                        {reportLanguage === 'both' && langTab === 'kr' && fullReportKr
                          ? fullReportKr
                          : (reportLanguage === 'both' && langTab === 'en' && fullReportEn
                            ? fullReportEn
                            : rawMarkdown)}
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
                  <>
                    <div className="mt-4 flex gap-2">
                      <button
                        onClick={() => setStep(2)}
                        className="flex-1 rounded-full bg-gray-900 px-6 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-gray-800 hover:shadow-lg"
                      >
                        PROCEED TO REVIEW →
                      </button>
                      <button
                        onClick={handleVerify}
                        disabled={verifying || !file}
                        className="rounded-full border border-gray-300 px-5 py-3.5 text-sm font-semibold text-gray-700 transition hover:bg-gray-50 disabled:opacity-50"
                      >
                        {verifying ? '...' : '🔍 Verify'}
                      </button>
                    </div>

                    {/* Verify Results */}
                    {verifyResult && (
                      <div className="mt-3 rounded-xl border border-gray-200 bg-white p-4">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <span className={`rounded-full px-3 py-1 text-sm font-bold ${
                              verifyResult.overall_grade === 'A' ? 'bg-emerald-100 text-emerald-700' :
                              verifyResult.overall_grade === 'B' ? 'bg-blue-100 text-blue-700' :
                              verifyResult.overall_grade === 'C' ? 'bg-amber-100 text-amber-700' :
                              'bg-red-100 text-red-700'
                            }`}>
                              Grade: {verifyResult.overall_grade}
                            </span>
                            <span className="text-xs text-gray-500">
                              {verifyResult.summary.accuracy_score}% accuracy
                            </span>
                          </div>
                          <button
                            onClick={() => setVerifyExpanded(!verifyExpanded)}
                            className="text-xs text-blue-600 hover:text-blue-700"
                          >
                            {verifyExpanded ? 'Collapse' : 'Details'}
                          </button>
                        </div>
                        <div className="flex flex-wrap gap-3 text-[11px]">
                          <span className="text-gray-600">
                            📊 {verifyResult.summary.total_repos_checked} repos checked
                          </span>
                          <span className={verifyResult.summary.repos_with_stat_issues > 0 ? 'text-red-600 font-medium' : 'text-emerald-600'}>
                            {verifyResult.summary.repos_with_stat_issues > 0
                              ? `⚠️ ${verifyResult.summary.repos_with_stat_issues} stat issues`
                              : '✓ Stats accurate'}
                          </span>
                          <span className={verifyResult.summary.phantom_features > 0 ? 'text-red-600 font-medium' : 'text-emerald-600'}>
                            {verifyResult.summary.phantom_features > 0
                              ? `👻 ${verifyResult.summary.phantom_features} phantom features`
                              : '✓ No phantoms'}
                          </span>
                        </div>

                        {verifyExpanded && verifyResult.details.length > 0 && (
                          <div className="mt-3 space-y-2 max-h-60 overflow-y-auto">
                            {verifyResult.details.map((d, i) => (
                              <details key={i} className="rounded-lg border border-gray-100 p-2">
                                <summary className="cursor-pointer text-xs font-medium text-gray-700 flex items-center justify-between">
                                  <span>{d.repo}</span>
                                  <span className="flex gap-2">
                                    {d.stat_issues.length > 0 && (
                                      <span className="text-red-500">{d.stat_issues.length} stat issue{d.stat_issues.length > 1 ? 's' : ''}</span>
                                    )}
                                    {d.phantom_bullets.length > 0 && (
                                      <span className="text-red-500">{d.phantom_bullets.length} phantom{d.phantom_bullets.length > 1 ? 's' : ''}</span>
                                    )}
                                    {d.stat_issues.length === 0 && d.phantom_bullets.length === 0 && (
                                      <span className="text-emerald-500">✓</span>
                                    )}
                                  </span>
                                </summary>
                                <div className="mt-2 space-y-1">
                                  {d.stat_issues.map((s, j) => (
                                    <div key={j} className="text-[10px] text-red-600">
                                      {s.metric}: stated {s.stated}, actual {s.actual}
                                    </div>
                                  ))}
                                  {d.phantom_bullets.map((b, j) => (
                                    <div key={j} className="text-[10px] text-orange-600">
                                      👻 {b.length > 100 ? b.slice(0, 100) + '...' : b}
                                    </div>
                                  ))}
                                </div>
                              </details>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </>
                )}
              </div>
            </section>
          </div>
        </main>
      </div>
    )
  }

  /* ================================================================ */
  /* STEP 3 — Publish (Medium Format)                                   */
  /* ================================================================ */

  if (step === 3) {
    const finalReport = improvedReport ?? fullReport ?? rawMarkdown
    const baseMediumContent = convertToMediumFormat(finalReport)
    const mediumContent = editingPublish ? editablePublishText : baseMediumContent

    // Render medium content with bold support
    const renderMediumContent = (text: string) => {
      return text.split('\n').map((line, i) => {
        // Replace **text** with bold spans
        const parts = line.split(/(\*\*[^*]+\*\*)/g)
        return (
          <div key={i} className={line.trim() === '' ? 'h-4' : ''}>
            {parts.map((part, j) => {
              if (part.startsWith('**') && part.endsWith('**')) {
                return <strong key={j} className="font-bold">{part.slice(2, -2)}</strong>
              }
              return <span key={j}>{part}</span>
            })}
          </div>
        )
      })
    }

    return (
      <div className="min-h-screen tokamak-grid text-gray-900">
        <main className="mx-auto w-full max-w-5xl px-6 pb-16 pt-8">
          {/* Header */}
          <div className="mb-6 flex items-center justify-between">
            <div>
              <button
                onClick={() => setStep(2)}
                className="mb-2 flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition"
              >
                ← Back to Review
              </button>
              <h1 className="text-3xl font-light tracking-tight text-gray-900">PUBLISH</h1>
              <p className="mt-2 text-sm text-gray-500">
                Final report formatted for Medium. Copy and paste directly into your Medium editor.
              </p>
            </div>
            {/* Step indicator */}
            <div className="flex items-center gap-3 text-xs">
              <span className="flex items-center gap-1.5 rounded-full border border-gray-300 px-4 py-1.5 text-gray-400">
                1. Generate
              </span>
              <span className="h-px w-8 bg-gray-300" />
              <span className="flex items-center gap-1.5 rounded-full border border-gray-300 px-4 py-1.5 text-gray-400">
                2. Review
              </span>
              <span className="h-px w-8 bg-gray-300" />
              <span className="flex items-center gap-1.5 rounded-full bg-gray-900 px-4 py-1.5 font-semibold text-white">
                3. Publish
              </span>
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
            {/* Left: Medium preview */}
            <div className="space-y-4">
              {/* Medium-formatted preview */}
              <div className="rounded-2xl border border-gray-200 bg-white shadow-sm">
                <div className="border-b border-gray-100 px-6 py-3 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="rounded-full bg-emerald-100 px-3 py-1 text-[10px] font-semibold text-emerald-700 uppercase">
                      Medium Ready
                    </span>
                    <span className="text-[11px] text-gray-400">
                      {mediumContent.split('\n').length} lines
                    </span>
                    {!editingPublish ? (
                      <button
                        onClick={() => {
                          setEditablePublishText(baseMediumContent)
                          setEditingPublish(true)
                        }}
                        className="rounded-full border border-gray-300 px-3 py-1 text-[10px] font-medium text-gray-600 hover:bg-gray-50 transition"
                      >
                        Edit
                      </button>
                    ) : (
                      <div className="flex items-center gap-1">
                        <button
                          onClick={() => setEditingPublish(false)}
                          className="rounded-full bg-emerald-600 px-3 py-1 text-[10px] font-semibold text-white hover:bg-emerald-700 transition"
                        >
                          Save
                        </button>
                        <button
                          onClick={() => {
                            setEditablePublishText(baseMediumContent)
                            setEditingPublish(false)
                          }}
                          className="rounded-full border border-gray-300 px-3 py-1 text-[10px] font-medium text-gray-600 hover:bg-gray-50 transition"
                        >
                          Cancel
                        </button>
                      </div>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleCopy(mediumContent, setCopiedMedium)}
                      className="rounded-full bg-gray-900 px-5 py-2 text-xs font-semibold text-white hover:bg-gray-800 transition"
                    >
                      {copiedMedium ? 'Copied!' : 'COPY FOR MEDIUM'}
                    </button>
                    <button
                      onClick={() => handleDownload(mediumContent, `medium-report-${dateRange?.start ?? 'draft'}.md`)}
                      className="rounded-full border border-gray-300 bg-white px-4 py-2 text-xs font-medium text-gray-700 hover:bg-gray-50 transition"
                    >
                      Download .md
                    </button>
                  </div>
                </div>
                <div className="max-h-[calc(100vh-280px)] overflow-y-auto p-8">
                  {editingPublish ? (
                    <textarea
                      value={editablePublishText}
                      onChange={(e) => setEditablePublishText(e.target.value)}
                      className="w-full h-[500px] text-base leading-8 text-gray-800 font-serif border border-gray-200 rounded-lg p-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <div className="prose max-w-none text-base leading-8 text-gray-800 font-serif">
                      {renderMediumContent(mediumContent)}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Right: Publishing checklist & info */}
            <div className="space-y-4">
              {/* Format info */}
              <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
                <h3 className="text-sm font-semibold text-gray-900">Publishing Guide</h3>
                <div className="mt-3 space-y-3 text-[11px] text-gray-600">
                  <div className="rounded-lg bg-blue-50 p-3">
                    <div className="font-semibold text-blue-700 mb-1">How to paste into Medium</div>
                    <ol className="space-y-1 list-decimal list-inside">
                      <li>Click &quot;Copy for Medium&quot; above</li>
                      <li>Open Medium &rarr; New Story</li>
                      <li>Paste directly into the editor</li>
                      <li>Medium will auto-format headers &amp; lists</li>
                    </ol>
                  </div>
                  <div className="rounded-lg bg-gray-50 p-3">
                    <div className="font-semibold text-gray-700 mb-1">Format</div>
                    <ul className="space-y-1">
                      <li>&#x2022; Headers converted to <strong>bold</strong></li>
                      <li>&#x2022; Bullet points use • format</li>
                      <li>&#x2022; Links shown as text (URL)</li>
                      <li>&#x2022; Clean, paste-ready formatting</li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Report summary */}
              <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
                <h3 className="text-sm font-semibold text-gray-900">Report Summary</h3>
                <div className="mt-3 space-y-2 text-[11px]">
                  {stats && (
                    <div className="rounded-lg bg-gray-50 p-3 space-y-1">
                      <div className="flex justify-between text-gray-600">
                        <span>Commits</span><span className="font-semibold">{stats.commits}</span>
                      </div>
                      <div className="flex justify-between text-gray-600">
                        <span>Repositories</span><span className="font-semibold">{stats.repos}</span>
                      </div>
                      <div className="flex justify-between text-gray-600">
                        <span>PRs</span><span className="font-semibold">{stats.prs}</span>
                      </div>
                      {dateRange?.start && dateRange?.end && (
                        <div className="flex justify-between text-gray-600">
                          <span>Period</span><span className="font-semibold">{dateRange.start} ~ {dateRange.end}</span>
                        </div>
                      )}
                    </div>
                  )}
                  {Object.keys(postScores).length > 0 && (
                    <div className="rounded-lg bg-emerald-50 p-3">
                      <div className="flex justify-between text-emerald-700">
                        <span>Final review score</span>
                        <span className="font-bold">
                          {(Object.values(postScores).reduce((s, v) => s + v, 0) / Object.values(postScores).length).toFixed(1)}/10
                        </span>
                      </div>
                    </div>
                  )}
                  <div className="rounded-lg bg-gray-50 p-3">
                    <div className="flex justify-between text-gray-600">
                      <span>Report type</span><span className="font-semibold capitalize">{reportType}</span>
                    </div>
                    <div className="flex justify-between text-gray-600 mt-1">
                      <span>Format</span><span className="font-semibold capitalize">{reportFormat}</span>
                    </div>
                    <div className="flex justify-between text-gray-600 mt-1">
                      <span>Source</span><span className="font-semibold">{improvedReport ? 'Improved' : 'Original'}</span>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </main>
      </div>
    )
  }

  /* ================================================================ */
  /* STEP 2 — Review & Improve                                         */
  /* ================================================================ */

  return (
    <div className="min-h-screen tokamak-grid text-gray-900">
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
            <div className="flex items-center gap-3">
              <h1 className="text-3xl font-light tracking-tight text-gray-900">REVIEW &amp; IMPROVE</h1>
              {matchingHistory.length > 0 && (
                <button
                  onClick={() => setShowHistory(!showHistory)}
                  className={`rounded-full px-3 py-1 text-[10px] font-semibold transition ${
                    showHistory ? 'bg-violet-600 text-white' : 'bg-violet-100 text-violet-700 hover:bg-violet-200'
                  }`}
                >
                  History ({matchingHistory.length})
                </button>
              )}
            </div>
            <p className="mt-2 text-sm text-gray-500">{metaText}</p>
          </div>
          {/* Step indicator */}
          <div className="flex items-center gap-3 text-xs">
            <span className="flex items-center gap-1.5 rounded-full border border-gray-300 px-4 py-1.5 text-gray-400">
              1. Generate
            </span>
            <span className="h-px w-8 bg-gray-300" />
            <span className="flex items-center gap-1.5 rounded-full bg-gray-900 px-4 py-1.5 font-semibold text-white">
              2. Review
            </span>
            <span className="h-px w-8 bg-gray-300" />
            <span className="flex items-center gap-1.5 rounded-full border border-gray-300 px-4 py-1.5 text-gray-400">
              3. Publish
            </span>
          </div>
        </div>

        {/* History Panel */}
        {showHistory && matchingHistory.length > 0 && (
          <div className="mb-6 rounded-2xl border border-violet-200 bg-violet-50 p-4 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-violet-900">
                Review History for {dateRange?.start} ~ {dateRange?.end}
              </h3>
              <button
                onClick={() => setShowHistory(false)}
                className="text-violet-400 hover:text-violet-600 text-xs"
              >
                Close
              </button>
            </div>
            <div className="space-y-2 max-h-[300px] overflow-y-auto">
              {matchingHistory.map((entry) => {
                const date = new Date(entry.timestamp)
                const timeStr = date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
                return (
                  <div
                    key={entry.id}
                    className="flex items-center justify-between rounded-xl bg-white border border-violet-100 p-3 hover:border-violet-300 transition"
                  >
                    <div className="flex items-center gap-4">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-semibold text-gray-800">{entry.model}</span>
                          <span className="text-[10px] text-gray-400">{timeStr}</span>
                          {entry.improvedReport && (
                            <span className="rounded bg-emerald-100 px-1.5 py-0.5 text-[9px] font-medium text-emerald-700">
                              Improved
                            </span>
                          )}
                        </div>
                        <div className="flex items-center gap-2 mt-1">
                          {entry.reviews.map((r) => {
                            const reviewer = REVIEWERS.find(rv => rv.level === r.reviewer_level)
                            return (
                              <span
                                key={r.reviewer_level}
                                className={`rounded px-1.5 py-0.5 text-[9px] font-medium ${reviewer?.badge ?? 'bg-gray-100 text-gray-600'}`}
                              >
                                {r.reviewer_ko}: {r.score}/10
                              </span>
                            )
                          })}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <div className="text-lg font-bold text-violet-700">{entry.avgScore.toFixed(1)}</div>
                        <div className="text-[9px] text-gray-400">avg score</div>
                      </div>
                      <div className="flex items-center gap-1">
                        <button
                          onClick={() => loadHistoryEntry(entry)}
                          className="rounded-lg bg-violet-600 px-3 py-1.5 text-[10px] font-semibold text-white hover:bg-violet-700 transition"
                        >
                          Load
                        </button>
                        <button
                          onClick={() => deleteHistoryEntry(entry.id)}
                          className="rounded-lg border border-gray-200 px-2 py-1.5 text-[10px] font-medium text-gray-400 hover:text-red-500 hover:border-red-200 transition"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
            <p className="mt-3 text-[10px] text-violet-600">
              Compare past reviews with different models to choose the best report.
            </p>
          </div>
        )}

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
                  {/* Visual mode for comprehensive reports */}
                  {reportFormat === 'comprehensive' && Object.keys(reportSummaries).length > 0 && (
                    <button
                      onClick={() => { setViewMode('visual'); setEditingReport(false) }}
                      className={`rounded-lg px-3 py-1 text-xs font-medium transition ${viewMode === 'visual' ? 'bg-blue-100 text-blue-700 ring-1 ring-blue-300' : 'text-gray-400 hover:text-gray-600'}`}
                    >
                      Visual
                    </button>
                  )}
                  <button
                    onClick={() => { setViewMode('original'); setEditingReport(false) }}
                    className={`rounded-lg px-3 py-1 text-xs font-medium transition ${viewMode === 'original' && !editingReport ? 'bg-gray-100 text-gray-700' : 'text-gray-400 hover:text-gray-600'}`}
                  >
                    {reportFormat === 'comprehensive' ? 'Markdown' : 'Original'}
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
                {htmlReport && (
                  <>
                    <button
                      onClick={() => {
                        const blob = new Blob([htmlReport], { type: 'text/html' })
                        const url = URL.createObjectURL(blob)
                        const link = document.createElement('a')
                        link.href = url
                        link.download = `report-${dateRange?.start ?? 'draft'}.html`
                        link.click()
                        URL.revokeObjectURL(url)
                      }}
                      className="rounded-lg bg-orange-500 px-3 py-1.5 text-xs font-semibold text-white hover:bg-orange-600 transition"
                    >
                      Download .html
                    </button>
                    <button
                      onClick={() => {
                        const blob = new Blob([htmlReport], { type: 'text/html' })
                        const url = URL.createObjectURL(blob)
                        window.open(url, '_blank')
                      }}
                      className="rounded-lg bg-blue-500 px-3 py-1.5 text-xs font-semibold text-white hover:bg-blue-600 transition"
                    >
                      Preview HTML
                    </button>
                    <button
                      onClick={() => {
                        const printWindow = window.open('', '_blank')
                        if (printWindow) {
                          printWindow.document.write(htmlReport)
                          printWindow.document.close()
                          setTimeout(() => {
                            printWindow.focus()
                            printWindow.print()
                          }, 800)
                        }
                      }}
                      className="rounded-lg bg-red-500 px-3 py-1.5 text-xs font-semibold text-white hover:bg-red-600 transition"
                    >
                      Download PDF
                    </button>
                  </>
                )}
              </div>
            </div>

            {/* Applied changes log */}
            {appliedChanges.length > 0 && viewMode === 'original' && !editingReport && (
              <div className="rounded-xl border border-blue-200 bg-blue-50/50 p-3 mb-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-[10px] font-semibold uppercase text-blue-600">
                    Applied Changes ({appliedChanges.length})
                  </div>
                  <button
                    onClick={() => { setAppliedChanges([]); setAppliedIssues(new Set()) }}
                    className="text-[10px] text-gray-400 hover:text-gray-600"
                  >
                    Clear log
                  </button>
                </div>
                <div className="space-y-1.5 max-h-40 overflow-y-auto">
                  {appliedChanges.map((c, i) => (
                    <div key={i} className="rounded-lg bg-white border border-blue-100 p-2">
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <span className="shrink-0 rounded bg-blue-100 px-1.5 py-0.5 text-[9px] font-semibold text-blue-700">
                            {c.reviewerKo}
                          </span>
                          <span className="text-[9px] text-gray-400">{c.category}</span>
                        </div>
                        <button
                          onClick={() => handleUndoChange(c)}
                          className="text-[9px] text-red-500 hover:text-red-700 font-medium transition"
                        >
                          Undo
                        </button>
                      </div>
                      <div className="text-[10px] leading-4">
                        <span className="text-red-500 line-through">{c.originalText.length > 80 ? c.originalText.slice(0, 80) + '...' : c.originalText}</span>
                        <span className="mx-1 text-gray-300">&rarr;</span>
                        <span className="text-emerald-600">{c.revisedText.length > 80 ? c.revisedText.slice(0, 80) + '...' : c.revisedText}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Report content */}
            <div className="rounded-2xl border border-gray-200 bg-white shadow-sm">
              <div ref={reportContentRef} className="max-h-[calc(100vh-220px)] overflow-y-auto p-8">
                {viewMode === 'visual' && Object.keys(reportSummaries).length > 0 && stats && dateRange ? (
                  <VisualReport
                    stats={{
                      total_commits: stats.commits,
                      total_prs: stats.prs,
                      total_repos: stats.repos,
                      total_lines_added: stats.linesAdded ?? 0,
                      total_lines_deleted: stats.linesDeleted ?? 0,
                      total_changes: stats.totalChanges ?? 0,
                      net_change: stats.netChange ?? 0,
                      total_contributors: stats.contributors ?? 0,
                    }}
                    dateRange={{
                      start: dateRange.start ?? '',
                      end: dateRange.end ?? '',
                      days: dateRange.days ?? 0,
                    }}
                    summaries={reportSummaries}
                    sections={sections}
                  />
                ) : editingReport ? (
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
                    dangerouslySetInnerHTML={{ __html: renderMarkdownWithHighlight(currentReport) }}
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
                        className={`flex items-center justify-between gap-4 px-4 py-3 cursor-pointer rounded-xl transition ${
                          result ? reviewer.bg : 'hover:bg-gray-50'
                        }`}
                        onClick={() => setExpandedReview(isExpanded ? null : reviewer.level)}
                      >
                        <div className="flex items-center gap-3 min-w-0">
                          <div className={`h-2.5 w-2.5 rounded-full shrink-0 ${result ? reviewer.dot : 'bg-gray-300'}`} />
                          <div className="min-w-0">
                            <div className="flex items-center gap-2 flex-wrap">
                              <span className="text-xs font-semibold text-gray-800">{reviewer.name_ko}</span>
                              <span className="text-[10px] text-gray-400">{reviewer.name}</span>
                              <span className={`rounded px-1.5 py-0.5 text-[9px] font-medium shrink-0 ${reviewer.badge}`}>Lv.{reviewer.level}</span>
                            </div>
                            <p className="text-[10px] text-gray-500 mt-0.5">{reviewer.description}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
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

                              {/* Warning when no structured feedback was generated */}
                              {(!result.review.issues || result.review.issues.length === 0) &&
                               (!result.review.strengths || result.review.strengths.length === 0) && (
                                <div className="rounded-lg border border-amber-200 bg-amber-50 p-3">
                                  <p className="text-[11px] text-amber-700 font-medium">
                                    구조화된 피드백이 생성되지 않았습니다. AI 응답 파싱에 실패했을 수 있습니다.
                                  </p>
                                  <button
                                    onClick={(e) => { e.stopPropagation(); handleReview(reviewer.level) }}
                                    disabled={isReviewing}
                                    className="mt-2 rounded-lg bg-amber-100 px-3 py-1.5 text-[11px] font-semibold text-amber-800 hover:bg-amber-200 transition disabled:opacity-50"
                                  >
                                    {isReviewing ? 'Reviewing...' : 'Retry Review'}
                                  </button>
                                </div>
                              )}

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
                                  <div className="flex items-center justify-between mb-1">
                                    <div className="text-[10px] font-semibold uppercase text-gray-500">
                                      Feedback ({result.review.issues.length})
                                    </div>
                                    {(() => {
                                      const toggleableKeys = result.review.issues
                                        .filter((iss) => iss.original_text && iss.revised_text && !appliedIssues.has(`${iss.original_text}::${iss.revised_text}`))
                                        .map((iss) => `${iss.original_text}::${iss.revised_text}`)
                                      if (toggleableKeys.length === 0) return null
                                      const allIncluded = toggleableKeys.every((k) => !excludedIssues.has(k))
                                      return (
                                        <button
                                          onClick={() => {
                                            setExcludedIssues((prev) => {
                                              const next = new Set(prev)
                                              if (allIncluded) {
                                                toggleableKeys.forEach((k) => next.add(k))
                                              } else {
                                                toggleableKeys.forEach((k) => next.delete(k))
                                              }
                                              return next
                                            })
                                          }}
                                          className="text-[9px] text-blue-500 hover:text-blue-700 transition"
                                        >
                                          {allIncluded ? 'Deselect all' : 'Select all'}
                                        </button>
                                      )
                                    })()}
                                  </div>
                                  <div className="space-y-2">
                                    {result.review.issues.map((issue, i) => {
                                      const issueKey = `${issue.original_text}::${issue.revised_text}`
                                      const isApplied = appliedIssues.has(issueKey)
                                      const isHighlighted = highlightedText === issue.original_text
                                      const isExcluded = excludedIssues.has(issueKey)
                                      const hasTextChange = !!(issue.original_text && issue.revised_text)

                                      return (
                                        <div
                                          key={i}
                                          className={`rounded-lg border p-2.5 cursor-pointer transition ${
                                            isHighlighted
                                              ? 'border-yellow-400 bg-yellow-50 ring-1 ring-yellow-300'
                                              : isApplied
                                              ? 'border-emerald-200 bg-emerald-50/50'
                                              : isExcluded
                                              ? 'border-gray-100 bg-gray-50/50 opacity-60'
                                              : 'border-gray-100 hover:border-gray-200'
                                          }`}
                                          onClick={() => handleHighlightIssue(issue.original_text)}
                                        >
                                          <div className="flex items-center gap-2 mb-1">
                                            {hasTextChange && !isApplied && (
                                              <input
                                                type="checkbox"
                                                checked={!isExcluded}
                                                onChange={(e) => {
                                                  e.stopPropagation()
                                                  setExcludedIssues((prev) => {
                                                    const next = new Set(prev)
                                                    if (next.has(issueKey)) next.delete(issueKey)
                                                    else next.add(issueKey)
                                                    return next
                                                  })
                                                }}
                                                onClick={(e) => e.stopPropagation()}
                                                className="h-3 w-3 rounded border-gray-300 text-blue-600 cursor-pointer shrink-0"
                                                title={isExcluded ? 'Include in AI Improvement' : 'Exclude from AI Improvement'}
                                              />
                                            )}
                                            <span className={`rounded px-1.5 py-0.5 text-[9px] font-semibold uppercase ${severityBadge(issue.severity)}`}>
                                              {issue.severity}
                                            </span>
                                            <span className="text-[10px] text-gray-400">{issue.category}</span>
                                            {isApplied && (
                                              <span className="ml-auto rounded bg-emerald-100 px-1.5 py-0.5 text-[9px] font-semibold text-emerald-700">Applied</span>
                                            )}
                                            {isExcluded && !isApplied && (
                                              <span className="ml-auto rounded bg-gray-100 px-1.5 py-0.5 text-[9px] font-semibold text-gray-500">Excluded</span>
                                            )}
                                          </div>
                                          <p className="text-[11px] text-gray-700 leading-4">{issue.description}</p>
                                          {issue.suggestion && (
                                            <p className="mt-1 text-[11px] text-blue-600 leading-4">Suggestion: {issue.suggestion}</p>
                                          )}
                                          {issue.original_text && issue.revised_text && (
                                            <div className="mt-2 space-y-1">
                                              <div className="rounded bg-red-50 px-2 py-1 text-[10px] text-red-700 line-through">{issue.original_text}</div>
                                              <div className="rounded bg-emerald-50 px-2 py-1 text-[10px] text-emerald-700">{issue.revised_text}</div>
                                              {!isApplied ? (
                                                <button
                                                  onClick={(e) => { e.stopPropagation(); handleApplyIssue(issue, result.reviewer_ko) }}
                                                  className="mt-1 rounded bg-blue-600 px-2.5 py-1 text-[10px] font-semibold text-white hover:bg-blue-700 transition"
                                                >
                                                  Apply this change
                                                </button>
                                              ) : (
                                                <button
                                                  onClick={(e) => {
                                                    e.stopPropagation()
                                                    const change = appliedChanges.find(c => c.issueKey === issueKey)
                                                    if (change) handleUndoChange(change)
                                                  }}
                                                  className="mt-1 rounded bg-gray-100 px-2.5 py-1 text-[10px] font-semibold text-red-600 hover:bg-red-50 transition"
                                                >
                                                  Undo this change
                                                </button>
                                              )}
                                            </div>
                                          )}
                                        </div>
                                      )
                                    })}
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
                Select which reviewers&apos; feedback to apply, then improve the report.
              </p>

              {reviews.length > 0 && (
                <div className="mt-3 rounded-lg bg-gray-50 p-3">
                  <div className="flex items-center justify-between text-xs text-gray-600 mb-2">
                    <span>{reviews.length} review{reviews.length > 1 ? 's' : ''} collected</span>
                    <span className="font-medium">
                      Avg score: {(reviews.reduce((sum, r) => sum + r.review.overall_score, 0) / reviews.length).toFixed(1)}/10
                    </span>
                  </div>
                  <div className="space-y-1.5">
                    {reviews.map((r) => {
                      const rv = REVIEWERS.find((rv) => rv.level === r.reviewer_level)
                      const isSelected = selectedReviewers.has(r.reviewer_level)
                      return (
                        <label
                          key={r.reviewer_level}
                          className={`flex items-center gap-2 rounded-lg px-2.5 py-1.5 cursor-pointer transition ${
                            isSelected ? 'bg-white border border-gray-200' : 'hover:bg-white/50'
                          }`}
                        >
                          <input
                            type="checkbox"
                            checked={isSelected}
                            onChange={() => {
                              setSelectedReviewers((prev) => {
                                const next = new Set(prev)
                                if (next.has(r.reviewer_level)) next.delete(r.reviewer_level)
                                else next.add(r.reviewer_level)
                                return next
                              })
                            }}
                            className="h-3.5 w-3.5 rounded border-gray-300 text-blue-600"
                          />
                          <span className={`rounded px-1.5 py-0.5 text-[10px] font-medium ${rv?.badge ?? 'bg-gray-100 text-gray-600'}`}>
                            {r.reviewer_ko}
                          </span>
                          <span className={`ml-auto text-xs font-bold ${scoreColor(r.review.overall_score)}`}>
                            {r.review.overall_score}/10
                          </span>
                        </label>
                      )
                    })}
                  </div>
                  <div className="mt-2 flex gap-2">
                    <button
                      onClick={() => setSelectedReviewers(new Set(reviews.map((r) => r.reviewer_level)))}
                      className="text-[10px] text-blue-600 hover:text-blue-700"
                    >
                      Select all
                    </button>
                    <button
                      onClick={() => setSelectedReviewers(new Set())}
                      className="text-[10px] text-gray-400 hover:text-gray-600"
                    >
                      Clear
                    </button>
                  </div>
                </div>
              )}

              {(() => {
                const activeIssueCount = reviews
                  .filter((r) => selectedReviewers.has(r.reviewer_level))
                  .reduce((sum, r) => sum + (r.review.issues ?? []).filter((iss) => {
                    if (!iss.original_text || !iss.revised_text) return true
                    const k = `${iss.original_text}::${iss.revised_text}`
                    return !appliedIssues.has(k) && !excludedIssues.has(k)
                  }).length, 0)
                return (
                  <button
                    onClick={handleImprove}
                    disabled={selectedReviewers.size === 0 || improving || activeIssueCount === 0}
                    className="mt-3 w-full rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    {improving ? (
                      <span className="flex items-center justify-center gap-2">
                        <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                        Improving...
                      </span>
                    ) : selectedReviewers.size === 0 ? (
                      'Select reviewers to apply'
                    ) : activeIssueCount === 0 ? (
                      'No actionable feedback to apply'
                    ) : (
                      `Improve with ${activeIssueCount} issue${activeIssueCount > 1 ? 's' : ''} from ${selectedReviewers.size} reviewer${selectedReviewers.size > 1 ? 's' : ''}`
                    )}
                  </button>
                )
              })()}

              {improveError && (
                <div className="mt-3 rounded-lg bg-red-50 border border-red-200 p-3">
                  <p className="text-xs font-medium text-red-700">{improveError}</p>
                </div>
              )}

              {/* Proceed button - shown when no AI improvements have been generated yet */}
              {!improvedReport && (
                <button
                  onClick={() => setStep(3)}
                  className={`mt-3 w-full rounded-full px-6 py-3 text-sm font-semibold transition ${
                    appliedChanges.length > 0
                      ? 'bg-gray-900 text-white shadow-sm hover:bg-gray-800 hover:shadow-lg'
                      : 'border border-gray-300 text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  {appliedChanges.length > 0
                    ? `PROCEED WITH ${appliedChanges.length} CHANGE${appliedChanges.length > 1 ? 'S' : ''} →`
                    : 'SKIP & PROCEED TO PUBLISH →'}
                </button>
              )}

              {improvedReport && (
                <div className="mt-3 space-y-3">
                  <div className="rounded-lg bg-emerald-50 border border-emerald-200 p-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 text-xs font-semibold text-emerald-700">
                        <span className="flex h-4 w-4 items-center justify-center rounded-full bg-emerald-200 text-[10px]">&#10003;</span>
                        Improved report generated
                      </div>
                      <button
                        onClick={() => {
                          setImprovedReport(null)
                          setViewMode('original')
                          setPostScores({})
                        }}
                        className="text-[10px] text-gray-500 hover:text-red-600 font-medium transition"
                      >
                        Revert to Original
                      </button>
                    </div>
                    <p className="mt-1 text-[11px] text-emerald-600">
                      Switch to &quot;Improved&quot; or &quot;Changes&quot; tab to view the result.
                    </p>
                  </div>

                  {/* Score comparison */}
                  <div className="rounded-lg border border-gray-200 p-3">
                    <div className="flex items-center justify-between mb-2">
                      <div className="text-[10px] font-semibold uppercase text-gray-500">Score Comparison</div>
                      <button
                        onClick={handleReReviewImproved}
                        disabled={reReviewing}
                        className="rounded bg-violet-100 px-2 py-0.5 text-[10px] font-semibold text-violet-700 hover:bg-violet-200 transition disabled:opacity-50"
                      >
                        {reReviewing ? 'Re-reviewing...' : Object.keys(postScores).length > 0 ? 'Re-review again' : 'Re-review improved'}
                      </button>
                    </div>
                    <div className="space-y-1.5">
                      {Object.entries(preScores).map(([lvl, before]) => {
                        const level = Number(lvl)
                        const after = postScores[level]
                        const rv = REVIEWERS.find((r) => r.level === level)
                        const delta = after !== undefined ? after - before : null
                        return (
                          <div key={level} className="flex items-center justify-between text-[11px]">
                            <span className="text-gray-600">{rv?.name_ko ?? `Lv.${level}`}</span>
                            <div className="flex items-center gap-2">
                              <span className={`font-medium ${scoreColor(before)}`}>{before}/10</span>
                              {after !== undefined && (
                                <>
                                  <span className="text-gray-400">→</span>
                                  <span className={`font-bold ${scoreColor(after)}`}>{after}/10</span>
                                  {delta !== null && delta !== 0 && (
                                    <span className={`text-[10px] font-semibold ${delta > 0 ? 'text-emerald-600' : 'text-red-500'}`}>
                                      {delta > 0 ? '+' : ''}{delta.toFixed(1)}
                                    </span>
                                  )}
                                </>
                              )}
                              {after === undefined && reReviewing && (
                                <span className="inline-block h-3 w-3 animate-spin rounded-full border border-gray-300 border-t-gray-600" />
                              )}
                            </div>
                          </div>
                        )
                      })}
                    </div>
                    {Object.keys(postScores).length > 0 && (
                      <div className="mt-2 pt-2 border-t border-gray-100 flex items-center justify-between text-xs">
                        <span className="font-medium text-gray-600">Average</span>
                        <div className="flex items-center gap-2">
                          <span className="text-gray-500">
                            {(Object.values(preScores).reduce((s, v) => s + v, 0) / Object.values(preScores).length).toFixed(1)}
                          </span>
                          <span className="text-gray-400">→</span>
                          <span className="font-bold text-gray-800">
                            {(Object.values(postScores).reduce((s, v) => s + v, 0) / Object.values(postScores).length).toFixed(1)}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Proceed to Publish */}
                  <button
                    onClick={() => setStep(3)}
                    className="w-full rounded-full bg-gray-900 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-gray-800 hover:shadow-lg"
                  >
                    PROCEED TO PUBLISH →
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
