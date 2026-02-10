"""
Utility Municipalization Monitor - Single File Version
All-in-one Flask application with embedded frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Data storage directory
DATA_DIR = Path(os.environ.get('DATA_DIR', 'data'))
DATA_DIR.mkdir(exist_ok=True)
MENTIONS_FILE = DATA_DIR / 'mentions.json'
CRAWL_LOG_FILE = DATA_DIR / 'crawl_log.json'

# HTML content embedded in the app
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Utility Monitor - Municipalization Tracking</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
        }
        #root { width: 100%; min-height: 100vh; }
        .loading {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #e2e8f0;
            font-size: 1.5rem;
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        .spin { animation: spin 1s linear infinite; }
    </style>
</head>
<body>
    <div id="root"><div class="loading">Loading Utility Monitor...</div></div>
    <script type="text/babel">
        const { useState, useEffect } = React;
        const { Search, X, Filter, AlertCircle, CheckCircle, Clock, ChevronDown, ChevronUp, MapPin, Zap, RefreshCw, Loader, Server, ExternalLink } = lucide;
        const API_BASE_URL = '/api';

        const UtilityMonitorApp = () => {
          const [mentions, setMentions] = useState([]);
          const [filteredMentions, setFilteredMentions] = useState([]);
          const [view, setView] = useState('review');
          const [selectedMention, setSelectedMention] = useState(null);
          const [searchQuery, setSearchQuery] = useState('');
          const [filters, setFilters] = useState({ source: 'all', location: 'all', priority: 'all', utilityType: 'all' });
          const [showFilters, setShowFilters] = useState(false);
          const [stats, setStats] = useState({ pending: 0, approved: 0, deleted: 0, todaysCaptured: 0 });
          const [isCrawling, setIsCrawling] = useState(false);
          const [crawlStatus, setCrawlStatus] = useState('');
          const [backendConnected, setBackendConnected] = useState(false);

          useEffect(() => {
            checkBackendConnection();
            fetchMentions();
            fetchStats();
          }, []);

          const checkBackendConnection = async () => {
            try {
              const response = await fetch(`${API_BASE_URL}/health`);
              if (response.ok) setBackendConnected(true);
            } catch (error) {
              setBackendConnected(false);
              console.error('Backend connection failed:', error);
            }
          };

          const fetchMentions = async () => {
            try {
              const response = await fetch(`${API_BASE_URL}/mentions`);
              if (response.ok) {
                const data = await response.json();
                setMentions(data);
              }
            } catch (error) {
              console.error('Error fetching mentions:', error);
            }
          };

          const fetchStats = async () => {
            try {
              const response = await fetch(`${API_BASE_URL}/stats`);
              if (response.ok) {
                const data = await response.json();
                setStats({
                  pending: data.pending,
                  approved: data.approved,
                  deleted: data.deleted,
                  todaysCaptured: data.today_captured
                });
              }
            } catch (error) {
              console.error('Error fetching stats:', error);
            }
          };

          useEffect(() => {
            let filtered = mentions.filter(m => 
              view === 'review' ? m.status === 'pending' : m.status === 'approved'
            );
            if (searchQuery) {
              const query = searchQuery.toLowerCase();
              filtered = filtered.filter(m => 
                m.title.toLowerCase().includes(query) ||
                m.snippet.toLowerCase().includes(query) ||
                m.location.toLowerCase().includes(query) ||
                m.utility.toLowerCase().includes(query)
              );
            }
            if (filters.source !== 'all') filtered = filtered.filter(m => m.source === filters.source);
            if (filters.location !== 'all') filtered = filtered.filter(m => m.location === filters.location);
            if (filters.priority !== 'all') filtered = filtered.filter(m => m.priority === filters.priority);
            if (filters.utilityType !== 'all') filtered = filtered.filter(m => m.utilityType === filters.utilityType);
            setFilteredMentions(filtered);
          }, [mentions, view, searchQuery, filters]);

          const handleAction = async (mentionId, action) => {
            try {
              const response = await fetch(`${API_BASE_URL}/mentions/${mentionId}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: action })
              });
              if (response.ok) {
                await fetchMentions();
                await fetchStats();
                setSelectedMention(null);
              }
            } catch (error) {
              console.error('Error updating mention:', error);
            }
          };

          const getUniqueValues = (key) => ['all', ...new Set(mentions.map(m => m[key]))];

          const performCrawl = async () => {
            setIsCrawling(true);
            setCrawlStatus('Starting crawl...');
            try {
              const response = await fetch(`${API_BASE_URL}/crawl`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  queries: ['utility municipalization news', 'public power initiative', 'municipal utility ballot', 'franchise agreement utility'],
                  max_results_per_query: 10
                })
              });
              const data = await response.json();
              if (data.success) {
                setCrawlStatus(`✓ Crawl complete! Found ${data.new_mentions} new mentions (${data.duplicates} duplicates filtered)`);
                await fetchMentions();
                await fetchStats();
              } else {
                setCrawlStatus(`✗ Crawl failed: ${data.error}`);
              }
            } catch (error) {
              setCrawlStatus(`✗ Error: ${error.message}`);
            } finally {
              setIsCrawling(false);
              setTimeout(() => setCrawlStatus(''), 5000);
            }
          };

          return (
            <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)', color: '#e2e8f0', padding: '2rem' }}>
              <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                  <h1 style={{ fontSize: '2.5rem', fontWeight: '700', marginBottom: '0.5rem' }}>⚡ Utility Monitor</h1>
                  <p style={{ color: '#94a3b8' }}>Municipalization Intelligence Platform</p>
                  <div style={{ marginTop: '1rem', padding: '0.5rem 1rem', background: backendConnected ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)', borderRadius: '8px', display: 'inline-block', color: backendConnected ? '#6ee7b7' : '#fca5a5' }}>
                    {backendConnected ? '✓ Connected' : '✗ Disconnected'}
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
                  <div style={{ background: 'rgba(251, 191, 36, 0.1)', padding: '1.5rem', borderRadius: '12px', textAlign: 'center' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#fbbf24' }}>{stats.todaysCaptured}</div>
                    <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Today</div>
                  </div>
                  <div style={{ background: 'rgba(245, 158, 11, 0.1)', padding: '1.5rem', borderRadius: '12px', textAlign: 'center' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#f59e0b' }}>{stats.pending}</div>
                    <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Pending</div>
                  </div>
                  <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '1.5rem', borderRadius: '12px', textAlign: 'center' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#10b981' }}>{stats.approved}</div>
                    <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Approved</div>
                  </div>
                  <div style={{ background: 'rgba(99, 102, 241, 0.1)', padding: '1.5rem', borderRadius: '12px', textAlign: 'center' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#6366f1' }}>{stats.deleted}</div>
                    <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Deleted</div>
                  </div>
                </div>

                <div style={{ marginBottom: '2rem' }}>
                  <button onClick={performCrawl} disabled={isCrawling || !backendConnected} style={{ width: '100%', padding: '1rem', background: isCrawling ? 'rgba(100, 116, 139, 0.5)' : 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)', border: 'none', borderRadius: '12px', color: 'white', cursor: isCrawling ? 'not-allowed' : 'pointer', fontSize: '1rem', fontWeight: '600' }}>
                    {isCrawling ? '⏳ Crawling...' : '🔄 Run Crawl Now'}
                  </button>
                  {crawlStatus && <div style={{ marginTop: '1rem', padding: '1rem', background: crawlStatus.startsWith('✓') ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', textAlign: 'center', color: crawlStatus.startsWith('✓') ? '#6ee7b7' : '#fca5a5' }}>{crawlStatus}</div>}
                </div>

                <div style={{ marginBottom: '2rem' }}>
                  <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
                    <button onClick={() => setView('review')} style={{ flex: 1, padding: '0.75rem', background: view === 'review' ? 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)' : 'rgba(51, 65, 85, 0.5)', border: 'none', borderRadius: '8px', color: 'white', cursor: 'pointer', fontWeight: '600' }}>Review Queue</button>
                    <button onClick={() => setView('approved')} style={{ flex: 1, padding: '0.75rem', background: view === 'approved' ? 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)' : 'rgba(51, 65, 85, 0.5)', border: 'none', borderRadius: '8px', color: 'white', cursor: 'pointer', fontWeight: '600' }}>Approved Items</button>
                  </div>
                </div>

                {filteredMentions.length === 0 ? (
                  <div style={{ padding: '4rem 2rem', textAlign: 'center', background: 'rgba(51, 65, 85, 0.3)', borderRadius: '16px' }}>
                    <h3 style={{ color: '#94a3b8', fontSize: '1.25rem', marginBottom: '0.5rem' }}>No items found</h3>
                    <p style={{ color: '#64748b', fontSize: '0.875rem' }}>{view === 'review' ? 'Run a crawl to collect mentions' : 'No approved items yet'}</p>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {filteredMentions.map(mention => (
                      <div key={mention.id} style={{ background: 'rgba(51, 65, 85, 0.3)', border: '1px solid rgba(148, 163, 184, 0.1)', borderRadius: '16px', padding: '1.5rem' }}>
                        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem', flexWrap: 'wrap' }}>
                          {mention.priority === 'high' && <span style={{ background: 'rgba(239, 68, 68, 0.2)', color: '#fca5a5', padding: '0.25rem 0.75rem', borderRadius: '6px', fontSize: '0.75rem', fontWeight: '600' }}>HIGH PRIORITY</span>}
                          <span style={{ background: 'rgba(139, 92, 246, 0.2)', color: '#c4b5fd', padding: '0.25rem 0.75rem', borderRadius: '6px', fontSize: '0.75rem', fontWeight: '600' }}>{mention.source}</span>
                          <span style={{ background: 'rgba(59, 130, 246, 0.2)', color: '#93c5fd', padding: '0.25rem 0.75rem', borderRadius: '6px', fontSize: '0.75rem', fontWeight: '600' }}>{mention.stage}</span>
                        </div>
                        <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.5rem', color: '#e2e8f0' }}>{mention.title}</h3>
                        <p style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.75rem' }}>{mention.snippet}</p>
                        <div style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '1rem' }}>
                          📍 {mention.location} | ⚡ {mention.utility} | 🕒 {new Date(mention.capturedAt).toLocaleDateString()}
                        </div>
                        {view === 'review' && (
                          <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button onClick={() => handleAction(mention.id, 'approved')} style={{ flex: 1, padding: '0.5rem', background: 'rgba(16, 185, 129, 0.2)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '8px', color: '#6ee7b7', cursor: 'pointer', fontWeight: '600' }}>✓ Approve</button>
                            <button onClick={() => handleAction(mention.id, 'deleted')} style={{ flex: 1, padding: '0.5rem', background: 'rgba(239, 68, 68, 0.2)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#fca5a5', cursor: 'pointer', fontWeight: '600' }}>✗ Delete</button>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<UtilityMonitorApp />);
    </script>
</body>
</html>"""

def load_mentions():
    """Load mentions from JSON file"""
    if MENTIONS_FILE.exists():
        try:
            with open(MENTIONS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Error loading mentions file, returning empty list")
            return []
    return []

def save_mentions(mentions):
    """Save mentions to JSON file"""
    try:
        with open(MENTIONS_FILE, 'w') as f:
            json.dump(mentions, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving mentions: {e}")

def load_crawl_log():
    """Load crawl history"""
    if CRAWL_LOG_FILE.exists():
        try:
            with open(CRAWL_LOG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_crawl_log(log_entry):
    """Append to crawl log"""
    logs = load_crawl_log()
    logs.append(log_entry)
    logs = logs[-100:]
    try:
        with open(CRAWL_LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving crawl log: {e}")

# Serve frontend
@app.route('/')
def index():
    """Serve the main frontend page"""
    return HTML_CONTENT

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/mentions', methods=['GET'])
def get_mentions():
    """Get all mentions with optional filtering"""
    try:
        mentions = load_mentions()
        status = request.args.get('status')
        location = request.args.get('location')
        priority = request.args.get('priority')
        
        if status:
            mentions = [m for m in mentions if m.get('status') == status]
        if location and location != 'all':
            mentions = [m for m in mentions if m.get('location') == location]
        if priority and priority != 'all':
            mentions = [m for m in mentions if m.get('priority') == priority]
        
        return jsonify(mentions)
    except Exception as e:
        logger.error(f"Error getting mentions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mentions/<mention_id>', methods=['PATCH'])
def update_mention(mention_id):
    """Update a mention"""
    try:
        mentions = load_mentions()
        data = request.json
        
        mention_index = next((i for i, m in enumerate(mentions) if str(m.get('id')) == mention_id), None)
        
        if mention_index is not None:
            allowed_fields = ['status', 'tags', 'notes', 'priority']
            for field in allowed_fields:
                if field in data:
                    mentions[mention_index][field] = data[field]
            
            mentions[mention_index]['updated_at'] = datetime.now().isoformat()
            save_mentions(mentions)
            return jsonify(mentions[mention_index])
        
        return jsonify({'error': 'Mention not found'}), 404
    except Exception as e:
        logger.error(f"Error updating mention: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/crawl', methods=['POST'])
def trigger_crawl():
    """Trigger a web crawl"""
    try:
        try:
            from crawler import run_crawl
        except ImportError as ie:
            logger.error(f"Crawler import error: {ie}")
            return jsonify({
                'success': False,
                'error': 'Crawler module not found',
                'details': str(ie)
            }), 500
        
        data = request.json or {}
        queries = data.get('queries', ['utility municipalization', 'public power initiative'])
        max_results_per_query = data.get('max_results_per_query', 10)
        
        logger.info(f"Starting crawl with {len(queries)} queries")
        new_mentions = run_crawl(queries, max_results_per_query)
        
        existing_mentions = load_mentions()
        existing_urls = {m.get('url') for m in existing_mentions}
        
        unique_new_mentions = [m for m in new_mentions if m.get('url') not in existing_urls]
        
        all_mentions = existing_mentions + unique_new_mentions
        save_mentions(all_mentions)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'queries': queries,
            'total_found': len(new_mentions),
            'new_unique': len(unique_new_mentions),
            'duplicates': len(new_mentions) - len(unique_new_mentions)
        }
        save_crawl_log(log_entry)
        
        return jsonify({
            'success': True,
            'new_mentions': len(unique_new_mentions),
            'total_found': len(new_mentions),
            'duplicates': len(new_mentions) - len(unique_new_mentions)
        })
        
    except Exception as e:
        logger.error(f"Crawl error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    try:
        mentions = load_mentions()
        total = len(mentions)
        pending = len([m for m in mentions if m.get('status') == 'pending'])
        approved = len([m for m in mentions if m.get('status') == 'approved'])
        deleted = len([m for m in mentions if m.get('status') == 'deleted'])
        
        today = datetime.now().date()
        today_captures = 0
        for m in mentions:
            try:
                capture_date = datetime.fromisoformat(m.get('capturedAt', '2000-01-01')).date()
                if capture_date == today:
                    today_captures += 1
            except:
                pass
        
        return jsonify({
            'total': total,
            'pending': pending,
            'approved': approved,
            'deleted': deleted,
            'today_captured': today_captures
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    DATA_DIR.mkdir(exist_ok=True)
    if not MENTIONS_FILE.exists():
        save_mentions([])
    
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Utility Monitor on port {port}")
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true', host='0.0.0.0', port=port)
