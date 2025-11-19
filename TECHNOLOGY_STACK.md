# IP Risk Radar - Technology Stack

## 🎯 Main Technologies, Frameworks & Tools

---

## **Backend Technologies**

### **Core Framework**
- **Flask 3.x** - Python web framework for REST API
- **Python 3.8+** - Primary programming language

### **Threat Intelligence APIs**
- **AbuseIPDB API** - IP reputation and abuse reports
- **VirusTotal API** - Malware and URL scanning
- **Shodan API** - Internet-connected device search
- **AlienVault OTX API** - Open Threat Exchange intelligence
- **IPQualityScore API** - Fraud detection and proxy detection
- **ThreatFox API** - Malware IOC database
- **IP-API** - Free IP geolocation service

### **MITRE ATT&CK Integration**
- **Custom MITRE Scraper** - Web scraping for threat group data
- **BeautifulSoup4** - HTML parsing for MITRE website
- **Requests** - HTTP library for API calls

### **PDF Generation**
- **ReportLab** - Professional PDF report generation
- **reportlab.platypus** - High-level document building

### **Data Processing**
- **JSON** - Data serialization and mock database
- **datetime** - Timestamp handling
- **concurrent.futures** - Parallel API calls (ThreadPoolExecutor)

### **Utilities**
- **Custom Caching System** - File-based caching (disabled for fresh data)
- **Custom Scoring Engine** - Multi-source threat scoring algorithm
- **Data Normalizer** - API response standardization

---

## **Frontend Technologies**

### **Core Framework**
- **React 18.3.1** - UI library
- **TypeScript 5.x** - Type-safe JavaScript
- **Vite 5.4.19** - Fast build tool and dev server

### **UI Components & Styling**
- **shadcn/ui** - Component library (Radix UI based)
- **Tailwind CSS 3.x** - Utility-first CSS framework
- **Radix UI** - Accessible component primitives
- **Lucide React** - Icon library

### **State Management & Routing**
- **React Router DOM** - Client-side routing
- **React Hooks** - useState, useEffect for state management
- **TanStack Query (React Query)** - Server state management (optional)

### **Maps Integration**
- **@vis.gl/react-google-maps** - Google Maps React wrapper
- **Google Maps JavaScript API** - Interactive map visualization

### **Charts & Visualization**
- **Recharts** - Chart library for data visualization
- **Custom components** - Threat level indicators, risk meters

### **Form Handling**
- **React Hook Form** - Form validation and handling
- **Zod** - Schema validation

---

## **Development Tools**

### **Build Tools**
- **Vite** - Frontend build tool (faster than Webpack)
- **PostCSS** - CSS processing
- **Autoprefixer** - CSS vendor prefixing

### **Code Quality**
- **ESLint** - JavaScript/TypeScript linting
- **TypeScript Compiler** - Type checking
- **Prettier** (implicit) - Code formatting

### **Package Managers**
- **npm** - Node package manager (frontend)
- **pip** - Python package manager (backend)

---

## **Database & Storage**

### **Mock Database**
- **JSON File Storage** - `mock_threat_database.json`
- **Custom Python Module** - `utils/mock_threat_db.py`

### **Caching**
- **File-based Cache** - JSON files in `cache/` directory
- **Note:** Currently disabled for real-time data

---

## **Security & Authentication**

### **API Key Management**
- **Environment Variables** - `.env` file for API keys
- **config.py** - Centralized configuration
- **CORS Handling** - Flask-CORS for cross-origin requests

---

## **Testing Tools**

### **Test Scripts**
- **Custom Python Scripts** - `test_mock_database.py`, `test_integration.py`
- **pytest** (optional) - Unit testing framework

---

## **Deployment & DevOps**

### **Version Control**
- **Git** - Version control system
- **GitHub** - Code repository hosting

### **Development Server**
- **Flask Development Server** - Backend (port 5000)
- **Vite Dev Server** - Frontend (port 8080)

### **Scripts**
- **PowerShell Scripts** - `start-all.ps1`, `setup.ps1`
- **Python Scripts** - Test and utility scripts

---

## **Documentation Tools**

### **Markdown**
- **README.md** - Project documentation
- **Multiple .md files** - Feature guides and implementation summaries

---

## **Key Libraries (Python)**

```python
flask==3.0.0
requests==2.31.0
reportlab==4.0.7
beautifulsoup4==4.12.2
python-dotenv==1.0.0
flask-cors==4.0.0
```

---

## **Key Libraries (Node/TypeScript)**

```json
{
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "react-router-dom": "^6.26.2",
  "typescript": "~5.6.2",
  "@vis.gl/react-google-maps": "^1.3.4",
  "tailwindcss": "^3.4.1",
  "vite": "^5.4.19",
  "recharts": "^2.15.0",
  "lucide-react": "^0.469.0"
}
```

---

## **Architecture Pattern**

### **Backend**
- **MVC-like Pattern**
  - Models: `models/threat_profile.py`
  - Controllers: `app.py` (Flask routes)
  - Services: `core/correlator.py`, `core/scorer.py`

### **Frontend**
- **Component-based Architecture**
  - Pages: `src/pages/`
  - Components: `src/components/`
  - Utilities: `src/lib/`

### **API Communication**
- **REST API** - JSON over HTTP
- **CORS Enabled** - Cross-origin requests allowed

---

## **Design Patterns Used**

1. **Singleton Pattern** - Configuration management
2. **Factory Pattern** - API client creation
3. **Strategy Pattern** - Multiple scoring algorithms
4. **Observer Pattern** - React state updates
5. **Module Pattern** - Code organization

---

## **External Services**

1. **AbuseIPDB** - Threat intelligence
2. **VirusTotal** - Malware scanning
3. **Shodan** - Network intelligence
4. **AlienVault OTX** - Community threat data
5. **IPQualityScore** - Fraud detection
6. **Google Maps API** - Geolocation visualization
7. **MITRE ATT&CK** - Threat actor database (scraped)

---

## **Performance Optimizations**

- **Concurrent API Calls** - ThreadPoolExecutor
- **Vite HMR** - Hot Module Replacement
- **React Memo** - Component memoization
- **Lazy Loading** - Code splitting
- **Caching** - File-based (optional)

---

## **Browser Compatibility**

- **Chrome/Edge** - Recommended
- **Firefox** - Supported
- **Safari** - Supported
- **Modern browsers** - ES6+ support required

---

## **System Requirements**

### **Backend**
- Python 3.8+
- 2GB RAM minimum
- Internet connection for APIs

### **Frontend**
- Node.js 18+
- npm 9+
- Modern web browser

---

## **Summary**

| Category | Technologies |
|----------|-------------|
| **Backend** | Flask, Python 3.8+ |
| **Frontend** | React 18, TypeScript, Vite |
| **UI** | shadcn/ui, Tailwind CSS, Radix UI |
| **APIs** | AbuseIPDB, VirusTotal, Shodan, OTX, IPQualityScore |
| **Maps** | Google Maps JavaScript API, @vis.gl/react-google-maps |
| **PDF** | ReportLab |
| **Intelligence** | MITRE ATT&CK (custom scraper) |
| **Charts** | Recharts |
| **Database** | JSON (Mock Database) |
| **Version Control** | Git, GitHub |
| **Development** | Vite, Flask Dev Server, PowerShell |

---

**Total Technologies:** 30+  
**Programming Languages:** Python, TypeScript/JavaScript, HTML, CSS  
**Framework Count:** 5+ major frameworks  
**API Integrations:** 7 external services  

---

*Last Updated: November 7, 2025*
