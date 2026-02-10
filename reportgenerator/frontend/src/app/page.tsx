'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, Download, Sparkles, BarChart3, Users, Code } from 'lucide-react'

interface ReportSection {
  project: string
  title: string
  content: string
}

interface ReportData {
  success: boolean
  report_type: string
  stats: {
    total_commits: number
    total_prs: number
    total_repos: number
  }
  highlight: string
  sections: ReportSection[]
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [reportType, setReportType] = useState<'technical' | 'public'>('public')
  const [useAI, setUseAI] = useState(true)
  const [loading, setLoading] = useState(false)
  const [report, setReport] = useState<ReportData | null>(null)
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
      setError(null)
      setReport(null)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/csv': ['.csv'] },
    multiple: false,
  })

  const generateReport = async () => {
    if (!file) return

    setLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('report_type', reportType)
      formData.append('use_ai', useAI.toString())

      const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to generate report')
      }

      const data = await response.json()
      setReport(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const getFullReport = () => {
    if (!report) return ''

    let content = `### Highlight\n\n${report.highlight}\n\n`
    content += `### Development Activity\n\n`
    content += `**Total**: ${report.stats.total_commits} commits, ${report.stats.total_prs} merged PRs across ${report.stats.total_repos} repositories.\n\n`
    content += `---\n\n`

    for (const section of report.sections) {
      content += section.content + '\n'
    }

    return content
  }

  const downloadReport = (format: 'md' | 'csv' | 'tsv') => {
    if (!report) return

    let content = ''
    let filename = `report_${reportType}_${new Date().toISOString().split('T')[0]}`
    let mimeType = 'text/plain'

    if (format === 'md') {
      content = getFullReport()
      filename += '.md'
      mimeType = 'text/markdown'
    } else if (format === 'csv' || format === 'tsv') {
      const separator = format === 'csv' ? ',' : '\t'
      const rows = [['Section', 'Title', 'Content'].join(separator)]

      for (const section of report.sections) {
        const cleanContent = section.content.replace(/[\n\r]+/g, ' ').replace(/"/g, '""')
        rows.push([section.project, `"${section.title}"`, `"${cleanContent}"`].join(separator))
      }

      content = rows.join('\n')
      filename += `.${format}`
      mimeType = format === 'csv' ? 'text/csv' : 'text/tab-separated-values'
    }

    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-blue-600" />
            <span className="text-xl font-semibold text-gray-900">Biweekly Report Generator</span>
          </div>
          <span className="text-sm text-gray-500">Tokamak Network</span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Title */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <BarChart3 className="w-7 h-7 text-blue-600" />
            Custom Data Export Builder
          </h1>
          <p className="text-gray-600 mt-1">
            Upload GitHub CSV export and generate ecosystem reports
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Panel - Input */}
          <div className="space-y-6">
            {/* File Upload */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Upload className="w-5 h-5 text-gray-600" />
                Upload CSV File
              </h2>

              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
                  ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
                  ${file ? 'bg-green-50 border-green-300' : ''}`}
              >
                <input {...getInputProps()} />
                {file ? (
                  <div className="flex items-center justify-center gap-2 text-green-700">
                    <FileText className="w-6 h-6" />
                    <span className="font-medium">{file.name}</span>
                  </div>
                ) : isDragActive ? (
                  <p className="text-blue-600">Drop the CSV file here...</p>
                ) : (
                  <div>
                    <Upload className="w-10 h-10 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-600">Drag & drop a CSV file here</p>
                    <p className="text-sm text-gray-400 mt-1">or click to select</p>
                  </div>
                )}
              </div>
            </div>

            {/* Report Type */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-lg font-semibold mb-4">Report Type</h2>

              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => setReportType('public')}
                  className={`p-4 rounded-lg border-2 text-left transition-all
                    ${reportType === 'public'
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'}`}
                >
                  <Users className={`w-6 h-6 mb-2 ${reportType === 'public' ? 'text-blue-600' : 'text-gray-400'}`} />
                  <div className="font-medium">Public / Investor</div>
                  <div className="text-sm text-gray-500">Non-technical, business-focused</div>
                </button>

                <button
                  onClick={() => setReportType('technical')}
                  className={`p-4 rounded-lg border-2 text-left transition-all
                    ${reportType === 'technical'
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'}`}
                >
                  <Code className={`w-6 h-6 mb-2 ${reportType === 'technical' ? 'text-blue-600' : 'text-gray-400'}`} />
                  <div className="font-medium">Technical</div>
                  <div className="text-sm text-gray-500">Developer-focused with links</div>
                </button>
              </div>
            </div>

            {/* Options */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-lg font-semibold mb-4">Options</h2>

              <label className="flex items-center gap-3 cursor-pointer">
                <div className="relative">
                  <input
                    type="checkbox"
                    checked={useAI}
                    onChange={(e) => setUseAI(e.target.checked)}
                    className="sr-only"
                  />
                  <div className={`w-11 h-6 rounded-full transition-colors ${useAI ? 'bg-blue-500' : 'bg-gray-300'}`}>
                    <div className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition-transform ${useAI ? 'translate-x-5' : ''}`} />
                  </div>
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-blue-500" />
                    <span className="font-medium">Use AI for summaries</span>
                  </div>
                  <p className="text-sm text-gray-500">AI will generate intelligent summaries from commit messages</p>
                </div>
              </label>
            </div>

            {/* Generate Button */}
            <button
              onClick={generateReport}
              disabled={!file || loading}
              className={`w-full py-4 rounded-lg font-medium text-white flex items-center justify-center gap-2 transition-colors
                ${!file || loading
                  ? 'bg-gray-300 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'}`}
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Generate Report
                </>
              )}
            </button>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
                {error}
              </div>
            )}
          </div>

          {/* Right Panel - Preview */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <FileText className="w-5 h-5 text-gray-600" />
                Report Preview
              </h2>

              {report && (
                <div className="flex gap-2">
                  <button
                    onClick={() => downloadReport('md')}
                    className="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center gap-1"
                  >
                    <Download className="w-4 h-4" />
                    .md
                  </button>
                  <button
                    onClick={() => downloadReport('csv')}
                    className="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center gap-1"
                  >
                    <Download className="w-4 h-4" />
                    .csv
                  </button>
                  <button
                    onClick={() => downloadReport('tsv')}
                    className="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center gap-1"
                  >
                    <Download className="w-4 h-4" />
                    .tsv
                  </button>
                </div>
              )}
            </div>

            <div className="border border-gray-200 rounded-lg p-4 min-h-[500px] max-h-[700px] overflow-y-auto bg-gray-50">
              {report ? (
                <div className="markdown-preview prose prose-sm max-w-none">
                  {/* Stats */}
                  <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="bg-white rounded-lg p-3 border border-gray-200 text-center">
                      <div className="text-2xl font-bold text-blue-600">{report.stats.total_commits}</div>
                      <div className="text-sm text-gray-500">Commits</div>
                    </div>
                    <div className="bg-white rounded-lg p-3 border border-gray-200 text-center">
                      <div className="text-2xl font-bold text-green-600">{report.stats.total_prs}</div>
                      <div className="text-sm text-gray-500">Merged PRs</div>
                    </div>
                    <div className="bg-white rounded-lg p-3 border border-gray-200 text-center">
                      <div className="text-2xl font-bold text-purple-600">{report.stats.total_repos}</div>
                      <div className="text-sm text-gray-500">Repositories</div>
                    </div>
                  </div>

                  {/* Highlight */}
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                    <h3 className="font-semibold text-blue-800 mb-2">Highlight</h3>
                    <p className="text-blue-700">{report.highlight}</p>
                  </div>

                  {/* Sections */}
                  {report.sections.map((section, idx) => (
                    <div key={idx} className="mb-6">
                      <div
                        className="whitespace-pre-wrap text-sm"
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
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-gray-400">
                  <FileText className="w-12 h-12 mb-2" />
                  <p>Upload a CSV file and generate a report</p>
                  <p className="text-sm">Preview will appear here</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
