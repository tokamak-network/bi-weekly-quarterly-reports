'use client'

import { useMemo } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'

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

const PIE_COLORS = [TOKAMAK_COLORS.blue, TOKAMAK_COLORS.green, TOKAMAK_COLORS.purple, TOKAMAK_COLORS.orange, '#6366F1', '#EC4899']

// Cover Section
function ReportCover({ dateRange, stats }: { dateRange: DateRange; stats: ReportStats }) {
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
          Biweekly Engineering & Ecosystem Update
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

// Activity Chart
function ActivityChart({ summaries }: { summaries: Record<string, RepoSummary> }) {
  const chartData = useMemo(() => {
    return Object.entries(summaries)
      .sort((a, b) => b[1].total_changes - a[1].total_changes)
      .slice(0, 10)
      .map(([name, data]) => ({
        name: name.length > 15 ? name.substring(0, 15) + '...' : name,
        fullName: name,
        added: data.lines_added,
        deleted: data.lines_deleted,
        commits: data.total_commits,
      }))
  }, [summaries])

  return (
    <div className="chart-container mt-8">
      <h3 className="chart-title">Top 10 Repositories by Code Changes</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} layout="vertical" margin={{ left: 20, right: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis type="number" tickFormatter={formatNumber} />
          <YAxis type="category" dataKey="name" width={120} tick={{ fontSize: 12 }} />
          <Tooltip
            formatter={(value: number, name: string) => [formatNumber(value), name === 'added' ? 'Lines Added' : 'Lines Deleted']}
            labelFormatter={(label) => chartData.find(d => d.name === label)?.fullName || label}
          />
          <Bar dataKey="added" name="added" fill={TOKAMAK_COLORS.green} radius={[0, 4, 4, 0]} />
          <Bar dataKey="deleted" name="deleted" fill={TOKAMAK_COLORS.red} radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// Contribution Pie Chart
function ContributionChart({ summaries }: { summaries: Record<string, RepoSummary> }) {
  const pieData = useMemo(() => {
    return Object.entries(summaries)
      .sort((a, b) => b[1].total_changes - a[1].total_changes)
      .slice(0, 6)
      .map(([name, data]) => ({
        name: name.length > 20 ? name.substring(0, 20) + '...' : name,
        value: data.total_changes,
      }))
  }, [summaries])

  return (
    <div className="chart-container mt-8">
      <h3 className="chart-title">Code Changes Distribution</h3>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={pieData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={2}
            dataKey="value"
            label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
            labelLine={false}
          >
            {pieData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value: number) => formatNumber(value)} />
        </PieChart>
      </ResponsiveContainer>
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

// Repository Card
function RepoCard({ name, data }: { name: string; data: RepoSummary }) {
  const topAccomplishments = useMemo(() => {
    return data.top_commits?.slice(0, 5).map(c => ({
      title: c.message.split('\n')[0].substring(0, 80),
      changes: c.additions + c.deletions,
    })) || []
  }, [data.top_commits])

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

      {/* Progress visualization */}
      <div className="mt-4 mb-4">
        <div className="flex items-center gap-2 text-xs text-gray-500 mb-1">
          <span>Code Balance</span>
          <span className="ml-auto">Net: {data.net_change >= 0 ? '+' : ''}{formatNumber(data.net_change)}</span>
        </div>
        <div className="flex h-2 rounded-full overflow-hidden bg-gray-100">
          <div
            className="bg-green-500"
            style={{ width: `${(data.lines_added / (data.lines_added + data.lines_deleted)) * 100}%` }}
          />
          <div
            className="bg-red-400"
            style={{ width: `${(data.lines_deleted / (data.lines_added + data.lines_deleted)) * 100}%` }}
          />
        </div>
      </div>

      {/* Key accomplishments */}
      {topAccomplishments.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Key Changes</div>
          <ul className="accomplishment-list">
            {topAccomplishments.map((item, idx) => (
              <li key={idx} className="accomplishment-item py-2">
                <div className="accomplishment-icon text-xs">
                  {idx + 1}
                </div>
                <div className="accomplishment-content">
                  <div className="text-sm text-gray-700">{item.title}</div>
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

/* ------------------------------------------------------------------ */
/* Main Component                                                      */
/* ------------------------------------------------------------------ */

export default function VisualReport({ stats, dateRange, summaries, sections }: VisualReportProps) {
  const sortedRepos = useMemo(() => {
    return Object.entries(summaries)
      .sort((a, b) => b[1].total_changes - a[1].total_changes)
  }, [summaries])

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

      {/* Charts */}
      <div className="grid md:grid-cols-2 gap-6">
        <ActivityChart summaries={summaries} />
        <ContributionChart summaries={summaries} />
      </div>

      {/* All Repositories */}
      <SectionHeader
        title="Repository Details"
        subtitle={`Detailed breakdown of all ${Object.keys(summaries).length} active repositories`}
        icon="📁"
      />

      <div className="space-y-4">
        {sortedRepos.map(([name, data]) => (
          <RepoCard key={name} name={name} data={data} />
        ))}
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
