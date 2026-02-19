'use client'

import { useMemo } from 'react'

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

interface RepoSummary {
  project: string
  total_commits: number
  merged_prs: number
  lines_added: number
  lines_deleted: number
  total_changes: number
  net_change: number
  contributors: string[]
  contributor_count: number
  github_url: string | null
  top_commits: Array<{
    message: string
    additions: number
    deletions: number
  }>
  // Enhanced fields for investor reports
  purpose?: string
  biweekly_goals?: string
  accomplishment_summary?: string
}

interface ReportStats {
  total_commits: number
  total_prs: number
  total_repos: number
  total_lines_added: number
  total_lines_deleted: number
  total_changes: number
  net_change: number
  total_contributors: number
}

interface DateRange {
  start: string
  end: string
  days: number
}

interface VisualReportProps {
  stats: ReportStats
  dateRange: DateRange
  summaries: Record<string, RepoSummary>
  sections: Array<{ project: string; title: string; content: string }>
}

/* ------------------------------------------------------------------ */
/* Helper Functions                                                    */
/* ------------------------------------------------------------------ */

const formatNumber = (num: number): string => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toLocaleString()
}

const formatDate = (dateStr: string): string => {
  if (!dateStr) return ''
  // Handle format like "2026.02.05"
  const parts = dateStr.split('.')
  if (parts.length === 3) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return `${months[parseInt(parts[1]) - 1]} ${parseInt(parts[2])}, ${parts[0]}`
  }
  return dateStr
}

/* ------------------------------------------------------------------ */
/* Sub-components                                                      */
/* ------------------------------------------------------------------ */

const TOKAMAK_COLORS = {
  blue: '#2A72E5',
  blueDark: '#1E5BB8',
  blueLight: '#4A8FF0',
  green: '#10B981',
  red: '#EF4444',
  purple: '#8B5CF6',
  orange: '#F59E0B',
}

// Get period label based on days
const getPeriodLabel = (days: number): string => {
  if (days <= 10) return 'Weekly'
  if (days <= 20) return 'Biweekly'
  if (days <= 45) return 'Monthly'
  return 'Quarterly'
}

// Cover Section
function ReportCover({ dateRange, stats }: { dateRange: DateRange; stats: ReportStats }) {
  const periodLabel = getPeriodLabel(dateRange.days)

  return (
    <div className="report-cover">
      <div className="relative z-10">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
            <svg className="w-8 h-8" viewBox="0 0 100 60" fill="currentColor">
              <ellipse cx="50" cy="30" rx="45" ry="25" fill="none" stroke="currentColor" strokeWidth="4" />
              <path d="M20 30 Q50 10 80 30 Q50 50 20 30" fill="currentColor" opacity="0.3" />
            </svg>
          </div>
          <span className="text-xl font-semibold tracking-wide opacity-90">TOKAMAK NETWORK</span>
        </div>
        <h1 className="report-cover-title">
          Development<br />Progress Report
        </h1>
        <p className="report-cover-subtitle">
          {periodLabel} Engineering & Ecosystem Update
        </p>
        <div className="report-cover-date">
          {formatDate(dateRange.start)} — {formatDate(dateRange.end)}
          <span className="ml-4 opacity-60">({dateRange.days} days)</span>
        </div>
        <div className="mt-8 flex flex-wrap gap-6 text-sm">
          <div>
            <div className="text-3xl font-bold">{formatNumber(stats.total_changes)}</div>
            <div className="opacity-70">Lines Changed</div>
          </div>
          <div>
            <div className="text-3xl font-bold">{stats.total_repos}</div>
            <div className="opacity-70">Repositories</div>
          </div>
          <div>
            <div className="text-3xl font-bold">{stats.total_commits}</div>
            <div className="opacity-70">Commits</div>
          </div>
          <div>
            <div className="text-3xl font-bold">{stats.total_contributors}</div>
            <div className="opacity-70">Contributors</div>
          </div>
        </div>
      </div>
    </div>
  )
}

// Statistics Cards
function StatCards({ stats }: { stats: ReportStats }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
      <div className="stat-card">
        <div className="stat-card-value stat-card-green">+{formatNumber(stats.total_lines_added)}</div>
        <div className="stat-card-label">Lines Added</div>
        <div className="mt-3 progress-bar">
          <div
            className="progress-bar-fill progress-bar-fill-green"
            style={{ width: `${Math.min(100, (stats.total_lines_added / stats.total_changes) * 100)}%` }}
          />
        </div>
      </div>
      <div className="stat-card">
        <div className="stat-card-value stat-card-red">-{formatNumber(stats.total_lines_deleted)}</div>
        <div className="stat-card-label">Lines Deleted</div>
        <div className="mt-3 progress-bar">
          <div
            className="progress-bar-fill progress-bar-fill-red"
            style={{ width: `${Math.min(100, (stats.total_lines_deleted / stats.total_changes) * 100)}%` }}
          />
        </div>
      </div>
      <div className="stat-card">
        <div className="stat-card-value stat-card-blue">
          {stats.net_change >= 0 ? '+' : ''}{formatNumber(stats.net_change)}
        </div>
        <div className="stat-card-label">Net Change</div>
        <div className="mt-3 progress-bar">
          <div
            className="progress-bar-fill progress-bar-fill-blue"
            style={{ width: '100%' }}
          />
        </div>
      </div>
      <div className="stat-card">
        <div className="stat-card-value stat-card-purple">{formatNumber(stats.total_changes)}</div>
        <div className="stat-card-label">Total Changes</div>
        <div className="mt-3 text-xs text-gray-500">
          {stats.total_commits} commits across {stats.total_repos} repos
        </div>
      </div>
    </div>
  )
}

// Section Header
function SectionHeader({ title, subtitle, icon }: { title: string; subtitle?: string; icon?: string }) {
  return (
    <div className="section-header">
      <h2 className="section-header-title">
        {icon && <span>{icon}</span>}
        {title}
      </h2>
      {subtitle && <p className="section-header-subtitle">{subtitle}</p>}
    </div>
  )
}

// Enhanced Repository Card
function RepoCard({ name, data, sectionContent }: { name: string; data: RepoSummary; sectionContent?: string }) {
  const topAccomplishments = useMemo(() => {
    return data.top_commits?.slice(0, 5).map(c => ({
      title: c.message.split('\n')[0].substring(0, 100),
      changes: c.additions + c.deletions,
      type: detectCommitType(c.message),
    })) || []
  }, [data.top_commits])

  // Extract structured info from section content if available
  const extractedInfo = useMemo(() => {
    if (!sectionContent) return null

    // Extract Overview section (between ### Overview and next ###)
    const overviewMatch = sectionContent.match(/###\s*Overview\s*\n([\s\S]*?)(?=###|$)/i)
    const overviewText = overviewMatch?.[1]?.trim().replace(/\*\*/g, '').replace(/\n+/g, ' ').trim()

    // Extract Period Goals section
    const goalsMatch = sectionContent.match(/###\s*Period Goals?\s*\n([\s\S]*?)(?=###|$)/i)
    const goalsText = goalsMatch?.[1]?.trim().replace(/\*\*/g, '').replace(/\n+/g, ' ').trim()

    // Extract Key Accomplishments section - get the first 3 bullets as summary
    const accomplishmentsMatch = sectionContent.match(/###\s*Key Accomplishments?\s*\n([\s\S]*?)(?=###|$)/i)
    let accomplishmentsText = null
    if (accomplishmentsMatch) {
      const bullets = accomplishmentsMatch[1].match(/\*\s+\*\*[^*]+\*\*[^*\n]*/g)
      if (bullets && bullets.length > 0) {
        // Take first 2 accomplishments and clean them up
        accomplishmentsText = bullets.slice(0, 2)
          .map(b => b.replace(/^\*\s+/, '').replace(/\*\*/g, '').trim())
          .join('; ')
      }
    }

    return {
      purpose: overviewText || null,
      goals: goalsText || null,
      summary: accomplishmentsText || null,
    }
  }, [sectionContent])

  return (
    <div className="repo-card">
      <div className="repo-card-header">
        <div>
          <h3 className="repo-card-title">{name}</h3>
          {data.github_url && (
            <a
              href={data.github_url}
              target="_blank"
              rel="noopener noreferrer"
              className="github-badge mt-2"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              View on GitHub
            </a>
          )}
        </div>
        <div className="repo-card-stats">
          <div className="repo-stat">
            <div className="repo-stat-value text-gray-800">{data.total_commits}</div>
            <div className="repo-stat-label">Commits</div>
          </div>
          <div className="repo-stat">
            <div className="repo-stat-value" style={{ color: TOKAMAK_COLORS.green }}>+{formatNumber(data.lines_added)}</div>
            <div className="repo-stat-label">Added</div>
          </div>
          <div className="repo-stat">
            <div className="repo-stat-value" style={{ color: TOKAMAK_COLORS.red }}>-{formatNumber(data.lines_deleted)}</div>
            <div className="repo-stat-label">Deleted</div>
          </div>
          <div className="repo-stat">
            <div className="repo-stat-value text-gray-600">{data.contributor_count}</div>
            <div className="repo-stat-label">Contributors</div>
          </div>
        </div>
      </div>

      {/* Repository Purpose & Context */}
      {(data.purpose || extractedInfo?.purpose) && (
        <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
          <div className="text-xs font-semibold text-blue-700 uppercase tracking-wide mb-1">Repository Purpose</div>
          <p className="text-sm text-gray-700">{data.purpose || extractedInfo?.purpose}</p>
        </div>
      )}

      {/* Biweekly Goals */}
      {(data.biweekly_goals || extractedInfo?.goals) && (
        <div className="mt-3 p-3 bg-purple-50 rounded-lg border border-purple-100">
          <div className="text-xs font-semibold text-purple-700 uppercase tracking-wide mb-1">This Period&apos;s Focus</div>
          <p className="text-sm text-gray-700">{data.biweekly_goals || extractedInfo?.goals}</p>
        </div>
      )}

      {/* Accomplishment Summary */}
      {(data.accomplishment_summary || extractedInfo?.summary) && (
        <div className="mt-3 p-3 bg-green-50 rounded-lg border border-green-100">
          <div className="text-xs font-semibold text-green-700 uppercase tracking-wide mb-1">Key Accomplishments</div>
          <p className="text-sm text-gray-700">{data.accomplishment_summary || extractedInfo?.summary}</p>
        </div>
      )}

      {/* Progress visualization */}
      <div className="mt-4 mb-4">
        <div className="flex items-center gap-2 text-xs text-gray-500 mb-1">
          <span>Code Balance</span>
          <span className="ml-auto">Net: {data.net_change >= 0 ? '+' : ''}{formatNumber(data.net_change)}</span>
        </div>
        <div className="flex h-2 rounded-full overflow-hidden bg-gray-100">
          <div
            className="bg-green-500"
            style={{ width: `${(data.lines_added / Math.max(1, data.lines_added + data.lines_deleted)) * 100}%` }}
          />
          <div
            className="bg-red-400"
            style={{ width: `${(data.lines_deleted / Math.max(1, data.lines_added + data.lines_deleted)) * 100}%` }}
          />
        </div>
      </div>

      {/* Key Changes with context */}
      {topAccomplishments.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Key Changes</div>
          <ul className="accomplishment-list">
            {topAccomplishments.map((item, idx) => (
              <li key={idx} className="accomplishment-item py-2">
                <div className="accomplishment-icon text-xs" style={{ backgroundColor: getTypeColor(item.type) + '20', color: getTypeColor(item.type) }}>
                  {getTypeIcon(item.type)}
                </div>
                <div className="accomplishment-content">
                  <div className="flex items-center gap-2">
                    <span className="text-xs px-1.5 py-0.5 rounded-full font-medium" style={{ backgroundColor: getTypeColor(item.type) + '20', color: getTypeColor(item.type) }}>
                      {item.type}
                    </span>
                  </div>
                  <div className="text-sm text-gray-700 mt-1">{item.title}</div>
                  <div className="text-xs text-gray-400 mt-0.5">{formatNumber(item.changes)} lines changed</div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

// Others Card for small repos
function OthersCard({ repos }: { repos: Array<[string, RepoSummary]> }) {
  const totalStats = useMemo(() => {
    return repos.reduce((acc, [, data]) => ({
      commits: acc.commits + data.total_commits,
      added: acc.added + data.lines_added,
      deleted: acc.deleted + data.lines_deleted,
    }), { commits: 0, added: 0, deleted: 0 })
  }, [repos])

  return (
    <div className="repo-card bg-gray-50">
      <div className="repo-card-header">
        <div>
          <h3 className="repo-card-title text-gray-600">Other Repositories</h3>
          <p className="text-sm text-gray-500 mt-1">{repos.length} repositories with minor changes (&lt; 10 lines each)</p>
        </div>
        <div className="repo-card-stats">
          <div className="repo-stat bg-white">
            <div className="repo-stat-value text-gray-800">{totalStats.commits}</div>
            <div className="repo-stat-label">Commits</div>
          </div>
          <div className="repo-stat bg-white">
            <div className="repo-stat-value" style={{ color: TOKAMAK_COLORS.green }}>+{formatNumber(totalStats.added)}</div>
            <div className="repo-stat-label">Added</div>
          </div>
          <div className="repo-stat bg-white">
            <div className="repo-stat-value" style={{ color: TOKAMAK_COLORS.red }}>-{formatNumber(totalStats.deleted)}</div>
            <div className="repo-stat-label">Deleted</div>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Changes Summary</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {repos.map(([name, data]) => (
            <div key={name} className="flex items-center justify-between p-2 bg-white rounded border border-gray-100">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-700 truncate max-w-[200px]">{name}</span>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <span className="text-gray-500">{data.total_commits} commit{data.total_commits !== 1 ? 's' : ''}</span>
                {data.top_commits?.[0] && (
                  <span className="text-gray-400 truncate max-w-[150px]" title={data.top_commits[0].message}>
                    {data.top_commits[0].message.slice(0, 30)}...
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// Helper functions for commit type detection
function detectCommitType(message: string): string {
  const lower = message.toLowerCase()
  if (lower.startsWith('feat') || lower.includes('add ') || lower.includes('implement')) return 'feature'
  if (lower.startsWith('fix') || lower.includes('bug') || lower.includes('resolve')) return 'fix'
  if (lower.startsWith('refactor') || lower.includes('refactor')) return 'refactor'
  if (lower.startsWith('docs') || lower.includes('readme') || lower.includes('documentation')) return 'docs'
  if (lower.startsWith('test') || lower.includes('test')) return 'test'
  if (lower.startsWith('chore') || lower.includes('update') || lower.includes('bump')) return 'chore'
  if (lower.startsWith('ci') || lower.includes('workflow') || lower.includes('deploy')) return 'ci'
  return 'update'
}

function getTypeColor(type: string): string {
  const colors: Record<string, string> = {
    feature: TOKAMAK_COLORS.green,
    fix: TOKAMAK_COLORS.red,
    refactor: TOKAMAK_COLORS.purple,
    docs: TOKAMAK_COLORS.blue,
    test: TOKAMAK_COLORS.orange,
    chore: '#6B7280',
    ci: '#EC4899',
    update: '#6B7280',
  }
  return colors[type] || '#6B7280'
}

function getTypeIcon(type: string): string {
  const icons: Record<string, string> = {
    feature: '+',
    fix: '!',
    refactor: '~',
    docs: 'D',
    test: 'T',
    chore: 'C',
    ci: 'CI',
    update: 'U',
  }
  return icons[type] || 'U'
}

/* ------------------------------------------------------------------ */
/* Main Component                                                      */
/* ------------------------------------------------------------------ */

export default function VisualReport({ stats, dateRange, summaries, sections }: VisualReportProps) {
  const { mainRepos, otherRepos } = useMemo(() => {
    const sorted = Object.entries(summaries)
      .sort((a, b) => b[1].total_changes - a[1].total_changes)

    // Split into main repos (>= 10 line changes) and others (< 10 line changes)
    const main: Array<[string, RepoSummary]> = []
    const others: Array<[string, RepoSummary]> = []

    for (const entry of sorted) {
      if (entry[1].total_changes >= 10) {
        main.push(entry)
      } else {
        others.push(entry)
      }
    }

    return { mainRepos: main, otherRepos: others }
  }, [summaries])

  // Map sections to repo names for content lookup
  const sectionContentMap = useMemo(() => {
    const map: Record<string, string> = {}
    for (const section of sections) {
      map[section.project] = section.content
    }
    return map
  }, [sections])

  return (
    <div className="visual-report space-y-8 pb-16">
      {/* Cover */}
      <ReportCover dateRange={dateRange} stats={stats} />

      {/* Executive Summary */}
      <SectionHeader
        title="Executive Summary"
        subtitle="Key metrics and highlights from this reporting period"
        icon="📊"
      />
      <StatCards stats={stats} />

      {/* All Repositories */}
      <SectionHeader
        title="Repository Details"
        subtitle={`Detailed breakdown of all ${Object.keys(summaries).length} active repositories`}
        icon="📁"
      />

      <div className="space-y-4">
        {mainRepos.map(([name, data]) => (
          <RepoCard
            key={name}
            name={name}
            data={data}
            sectionContent={sectionContentMap[name]}
          />
        ))}

        {/* Others section for small repos */}
        {otherRepos.length > 0 && (
          <OthersCard repos={otherRepos} />
        )}
      </div>

      {/* Footer */}
      <div className="mt-12 pt-8 border-t border-gray-200 text-center text-sm text-gray-500">
        <div className="flex items-center justify-center gap-2 mb-2">
          <svg className="w-5 h-5" viewBox="0 0 100 60" fill="currentColor" style={{ color: TOKAMAK_COLORS.blue }}>
            <ellipse cx="50" cy="30" rx="45" ry="25" fill="none" stroke="currentColor" strokeWidth="4" />
          </svg>
          <span className="font-semibold" style={{ color: TOKAMAK_COLORS.blue }}>Tokamak Network</span>
        </div>
        <p>Generated on {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
      </div>
    </div>
  )
}
