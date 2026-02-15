"""
Utility Municipalization Monitor - With PostgreSQL Database
Persistent storage that survives restarts and refreshes
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
import logging
import psycopg
from psycopg.rows import dict_row
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """Get database connection"""
    if not DATABASE_URL:
        logger.error("DATABASE_URL not set!")
        return None
    
    # Parse database URL (Render provides postgres:// but psycopg2 needs postgresql://)
    url = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    try:
conn = psycopg.connect(url, row_factory=dict_row)
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize database tables"""
    conn = get_db_connection()
    if not conn:
        logger.warning("No database connection - using fallback mode")
        return False
    
    try:
        cur = conn.cursor()
        
        # Create mentions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mentions (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                snippet TEXT,
                source TEXT,
                location TEXT,
                utility TEXT,
                utility_type TEXT,
                stage TEXT,
                priority TEXT,
                captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                tags TEXT[],
                notes TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index on status for faster queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_mentions_status 
            ON mentions(status)
        """)
        
        # Create index on URL for duplicate checking
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_mentions_url 
            ON mentions(url)
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        
        logger.info("Database initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        if conn:
            conn.close()
        return False

# Initialize database on startup
init_database()

# HTML content (embedded frontend)
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
              console.log('Updating mention:', mentionId, 'to status:', action);
              const response = await fetch(`${API_BASE_URL}/mentions/${mentionId}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: action })
              });
              
              console.log('Response status:', response.status);
              
              if (response.ok) {
                const data = await response.json();
                console.log('Update successful:', data);
                await fetchMentions();
                await fetchStats();
                setSelectedMention(null);
              } else {
                const errorData = await response.json();
                console.error('Update failed:', errorData);
                alert(`Failed to update: ${errorData.error || 'Unknown error'}`);
              }
            } catch (error) {
              console.error('Error updating mention:', error);
              alert(`Error: ${error.message}`);
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
                  queries: [
                    'utility municipalization',
                    'public power initiative',
                    'municipal utility formation',
                    'community choice energy',
                    'franchise agreement utility expiration',
                    'eminent domain electric utility',
                    'ballot measure municipal utility',
                    'public utility district',
                    'city takeover electric utility',
                    'municipal utility feasibility study',
                    'public ownership utility',
                    'community choice aggregation',
                    'municipal electric utility referendum',
                    'utility rate increase municipalization'
                  ],
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
                        <div style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '0.5rem' }}>
                          📍 {mention.location} | ⚡ {mention.utility} | 🕒 {new Date(mention.captured_at).toLocaleDateString()}
                        </div>
                        <a 
                          href={mention.url} 
                          target="_blank" 
                          rel="noopener noreferrer" 
                          style={{ 
                            display: 'inline-flex', 
                            alignItems: 'center', 
                            gap: '0.5rem',
                            fontSize: '0.875rem', 
                            color: '#60a5fa', 
                            textDecoration: 'none',
                            marginBottom: '1rem',
                            padding: '0.5rem 0.75rem',
                            background: 'rgba(59, 130, 246, 0.1)',
                            borderRadius: '6px',
                            border: '1px solid rgba(59, 130, 246, 0.2)',
                            transition: 'all 0.2s'
                          }}
                          onMouseOver={(e) => {
                            e.currentTarget.style.background = 'rgba(59, 130, 246, 0.2)';
                            e.currentTarget.style.color = '#93c5fd';
                          }}
                          onMouseOut={(e) => {
                            e.currentTarget.style.background = 'rgba(59, 130, 246, 0.1)';
                            e.currentTarget.style.color = '#60a5fa';
                          }}
                        >
                          🔗 Read Full Article
                        </a>
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

# Serve frontend
@app.route('/')
def index():
    """Serve the main frontend page"""
    return HTML_CONTENT

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    conn = get_db_connection()
    db_status = 'connected' if conn else 'disconnected'
    if conn:
        conn.close()
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'database': db_status
    })

@app.route('/api/mentions', methods=['GET'])
def get_mentions():
    """Get all mentions with optional filtering"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database not available'}), 500
    
    try:
        cur = conn.cursor()
        
        status = request.args.get('status')
        location = request.args.get('location')
        priority = request.args.get('priority')
        
        query = "SELECT * FROM mentions WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = %s"
            params.append(status)
        if location and location != 'all':
            query += " AND location = %s"
            params.append(location)
        if priority and priority != 'all':
            query += " AND priority = %s"
            params.append(priority)
        
        query += " ORDER BY captured_at DESC"
        
        cur.execute(query, params)
        mentions = cur.fetchall()
        
        # Convert to list of dicts and fix field names
        result = []
        for m in mentions:
            mention_dict = dict(m)
            # Map database fields to frontend expected fields
            mention_dict['utilityType'] = mention_dict.pop('utility_type', None)
            mention_dict['capturedAt'] = mention_dict.pop('captured_at', None)
            if mention_dict['capturedAt']:
                mention_dict['capturedAt'] = mention_dict['capturedAt'].isoformat()
            result.append(mention_dict)
        
        cur.close()
        conn.close()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting mentions: {e}")
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/mentions/<mention_id>', methods=['PATCH'])
def update_mention(mention_id):
    """Update a mention"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database not available'}), 500
    
    try:
        data = request.json
        cur = conn.cursor()
        
        # Build update query
        update_fields = []
        params = []
        
        if 'status' in data:
            update_fields.append("status = %s")
            params.append(data['status'])
        if 'tags' in data:
            update_fields.append("tags = %s")
            params.append(data['tags'])
        if 'notes' in data:
            update_fields.append("notes = %s")
            params.append(data['notes'])
        if 'priority' in data:
            update_fields.append("priority = %s")
            params.append(data['priority'])
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        params.append(mention_id)
        
        query = f"UPDATE mentions SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
        
        cur.execute(query, params)
        updated_mention = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
        
        if updated_mention:
            result = dict(updated_mention)
            result['utilityType'] = result.pop('utility_type', None)
            result['capturedAt'] = result.pop('captured_at', None)
            if result['capturedAt']:
                result['capturedAt'] = result['capturedAt'].isoformat()
            return jsonify(result)
        
        return jsonify({'error': 'Mention not found'}), 404
        
    except Exception as e:
        logger.error(f"Error updating mention: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/crawl', methods=['POST'])
def trigger_crawl():
    """Trigger a web crawl"""
    try:
        from crawler import run_crawl
        
        data = request.json or {}
        queries = data.get('queries', ['utility municipalization', 'public power initiative'])
        max_results_per_query = data.get('max_results_per_query', 10)
        
        logger.info(f"Starting crawl with {len(queries)} queries")
        new_mentions = run_crawl(queries, max_results_per_query)
        
        # Save to database
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database not available'}), 500
        
        cur = conn.cursor()
        
        # Get existing URLs to check for duplicates
        cur.execute("SELECT url FROM mentions")
        existing_urls = {row['url'] for row in cur.fetchall()}
        
        unique_new_mentions = []
        for mention in new_mentions:
            if mention.get('url') not in existing_urls:
                try:
                    cur.execute("""
                        INSERT INTO mentions 
                        (id, title, url, snippet, source, location, utility, utility_type, stage, priority, status, tags)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (url) DO NOTHING
                    """, (
                        mention['id'],
                        mention['title'],
                        mention['url'],
                        mention['snippet'],
                        mention['source'],
                        mention['location'],
                        mention['utility'],
                        mention['utilityType'],
                        mention['stage'],
                        mention['priority'],
                        mention['status'],
                        mention.get('tags', [])
                    ))
                    unique_new_mentions.append(mention)
                    existing_urls.add(mention['url'])
                except Exception as e:
                    logger.error(f"Error inserting mention: {e}")
                    continue
        
        conn.commit()
        cur.close()
        conn.close()
        
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
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database not available'}), 500
    
    try:
        cur = conn.cursor()
        
        # Get counts by status
        cur.execute("SELECT status, COUNT(*) as count FROM mentions GROUP BY status")
        status_counts = {row['status']: row['count'] for row in cur.fetchall()}
        
        # Get today's count
        cur.execute("""
            SELECT COUNT(*) as count FROM mentions 
            WHERE DATE(captured_at) = CURRENT_DATE
        """)
        today_count = cur.fetchone()['count']
        
        cur.close()
        conn.close()
        
        return jsonify({
            'total': sum(status_counts.values()),
            'pending': status_counts.get('pending', 0),
            'approved': status_counts.get('approved', 0),
            'deleted': status_counts.get('deleted', 0),
            'today_captured': today_count
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Utility Monitor on port {port}")
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true', host='0.0.0.0', port=port)
