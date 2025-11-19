import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Progress } from "@/components/ui/progress";
import { Download, Search, Globe, Shield, Activity, Database, CheckCircle2, XCircle, AlertTriangle, Loader2, Sun, Moon, ExternalLink } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { analyzeIP, downloadReport, transformToIntelligenceRecords, type IntelligenceRecord, type ThreatAnalysisResponse } from "@/lib/api";
import ThreatMap from "@/components/ThreatMap";
import { DarkWebIntelligence } from "@/components/DarkWebIntelligence";

const Index = () => {
  const [ipAddress, setIpAddress] = useState("");
  const [threatScore, setThreatScore] = useState(0);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [hasAnalyzed, setHasAnalyzed] = useState(false);
  const { toast } = useToast();
  const [theme, setTheme] = useState<"light" | "dark">(() => {
    try {
      const saved = localStorage.getItem("theme");
      return (saved === "dark" ? "dark" : "light");
    } catch (e) {
      return "light";
    }
  });

  useEffect(() => {
    try {
      if (theme === "dark") {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
      localStorage.setItem("theme", theme);
    } catch (e) {
      // ignore (e.g., SSR)
    }
  }, [theme]);
  
  const [apiSources, setApiSources] = useState([
    { name: "AbuseIPDB", status: "active" },
    { name: "VirusTotal", status: "active" },
    { name: "Shodan", status: "active" },
    { name: "AlienVault OTX", status: "active" },
    { name: "IPQualityScore", status: "active" },
  ]);

  const [threatCategories, setThreatCategories] = useState([
    { name: "Botnet", active: false },
    { name: "C2 Server", active: false },
    { name: "Phishing", active: false },
    { name: "Spam", active: false },
    { name: "Proxy", active: false },
  ]);

  // flexible intelligence data shape so backend can provide additional/different fields
  const [intelligenceData, setIntelligenceData] = useState<IntelligenceRecord[]>([]);
  const [analysisResult, setAnalysisResult] = useState<ThreatAnalysisResponse | null>(null);

  const [trendData, setTrendData] = useState([0, 0, 0, 0, 0, 0, 0]);
  const [activeSourcesCount, setActiveSourcesCount] = useState(5);
  const [confidenceLevel, setConfidenceLevel] = useState(0);
  const [isDownloading, setIsDownloading] = useState(false);
  const [geolocation, setGeolocation] = useState<{
    country?: string;
    city?: string;
    latitude?: number;
    longitude?: number;
  } | null>(null);

  // Simulate API status updates
  useEffect(() => {
    const interval = setInterval(() => {
      setApiSources(prev => prev.map(api => {
        if (Math.random() > 0.95) {
          const statuses = ['active', 'error', 'inactive'];
          return { ...api, status: statuses[Math.floor(Math.random() * statuses.length)] };
        }
        return api;
      }));
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Update active sources count
  useEffect(() => {
    const active = apiSources.filter(api => api.status === 'active').length;
    setActiveSourcesCount(active);
  }, [apiSources]);

  const handleAnalyze = async () => {
    if (!ipAddress.trim()) {
      toast({
        title: "Error",
        description: "Please enter an IP address",
        variant: "destructive",
      });
      return;
    }

    setIsAnalyzing(true);
    setHasAnalyzed(false);
    setThreatScore(0);
    setIntelligenceData([]);
    setGeolocation(null);
    
    try {
      // Call the real backend API (without cache)
      const result = await analyzeIP(ipAddress, false);
      
      // Store full analysis result for dark web component
      setAnalysisResult(result);
      
      // Animate threat score increase
      const targetScore = result.threat_score;
      let currentScore = 0;
      const scoreInterval = setInterval(() => {
        currentScore += Math.ceil((targetScore - currentScore) / 10);
        setThreatScore(currentScore);
        if (currentScore >= targetScore) {
          clearInterval(scoreInterval);
          setIsAnalyzing(false);
          setHasAnalyzed(true);
        }
      }, 50);

      // Update threat categories from backend
      const categories = result.categories || [];
      const mitre = result.mitre_intelligence;
      setThreatCategories([
        { name: "Botnet", active: Boolean(mitre?.is_botnet) || categories.includes("Botnet") },
        { name: "C2 Server", active: Boolean(mitre?.is_c2_server) || categories.includes("C2 Server") },
        { name: "Phishing", active: categories.includes("Phishing") || categories.includes("phishing") },
        { name: "Spam", active: categories.includes("Spam") || categories.includes("Web Spam") },
        { name: "Proxy", active: categories.includes("Proxy") },
      ]);

      // Transform API results to intelligence records
      const records = transformToIntelligenceRecords(result.sources || result.api_results || {});
      setIntelligenceData(records);

      // Store geolocation data
      setGeolocation(result.geolocation || null);

      // Update confidence level (backend returns confidence as a number 0-100)
      const confidenceValue = typeof result.confidence === 'number' 
        ? Math.round(result.confidence) 
        : 75;
      setConfidenceLevel(confidenceValue);

      // Update trend data
      setTrendData(prev => [...prev.slice(1), targetScore]);

      toast({
        title: "Analysis Complete",
        description: `IP ${ipAddress} analyzed successfully - Risk: ${result.risk_level}`,
      });
    } catch (error) {
      setIsAnalyzing(false);
      toast({
        title: "Analysis Failed",
        description: error instanceof Error ? error.message : "Failed to analyze IP address",
        variant: "destructive",
      });
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "active":
        return <CheckCircle2 className="h-4 w-4 text-green-600" />;
      case "error":
        return <XCircle className="h-4 w-4 text-red-600" />;
      case "inactive":
        return <AlertTriangle className="h-4 w-4 text-amber-600" />;
      default:
        return null;
    }
  };

  // Return label and hex color so we can apply a consistent palette (from your design tokens)
  const getRiskLevel = (score: number) => {
    if (score >= 70) return { label: "Malicious", color: "#DC3545" }; // Red
    if (score >= 40) return { label: "Suspicious", color: "#FD7E14" }; // Orange
    return { label: "Benign", color: "#28A745" }; // Green
  };

  const handleDownloadPDF = async () => {
    if (!hasAnalyzed || !ipAddress.trim()) {
      toast({
        title: "Error",
        description: "Please analyze an IP address first",
        variant: "destructive",
      });
      return;
    }

    setIsDownloading(true);
    try {
      const blob = await downloadReport(ipAddress);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `TICE-Report-${ipAddress.replace(/\./g, '-')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      toast({
        title: "Download Complete",
        description: `PDF report for ${ipAddress} downloaded successfully`,
      });
    } catch (error) {
      toast({
        title: "Download Failed",
        description: error instanceof Error ? error.message : "Failed to download PDF report",
        variant: "destructive",
      });
    } finally {
      setIsDownloading(false);
    }
  };

  const riskLevel = getRiskLevel(threatScore);

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-foreground flex items-center gap-3">
            <Shield className="h-10 w-10 text-primary" />
            IP Risk Radar
          </h1>
          <p className="text-sm text-muted-foreground mt-1">Advanced IP threat intelligence and risk assessment platform.</p>
        </div>
        <div className="flex items-center gap-2">
          <Button className="gap-2" onClick={handleDownloadPDF} disabled={!hasAnalyzed || isDownloading}>
            {isDownloading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Downloading...
              </>
            ) : (
              <>
                <Download className="h-4 w-4" />
                Download PDF
              </>
            )}
          </Button>
          <Button
            variant="ghost"
            aria-label="Toggle theme"
            onClick={() => setTheme(prev => (prev === "dark" ? "light" : "dark"))}
            title="Toggle dark / light"
          >
            {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>
        </div>
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Input & Score */}
        <div className="space-y-6">
          {/* IP Input */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Search className="h-5 w-5 text-primary" />
                IP Address Analysis
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-2">
                <Input
                  placeholder="Enter IP address (e.g., 192.168.1.1)"
                  value={ipAddress}
                  onChange={(e) => setIpAddress(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
                  className="flex-1"
                  disabled={isAnalyzing}
                />
                <Button onClick={handleAnalyze} disabled={isAnalyzing}>
                  {isAnalyzing ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin mr-2" />
                      Analyzing
                    </>
                  ) : (
                    'Analyze'
                  )}
                </Button>
                {/* demo button removed */}
              </div>
            </CardContent>
          </Card>

          {/* (Threat Score moved to right column) */}

          {/* API Status */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Database className="h-5 w-5 text-primary" />
                API Sources Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {apiSources.map((api) => (
                  <div
                    key={api.name}
                    className="flex items-center justify-between p-2 rounded-md bg-secondary/50 hover:bg-secondary transition-all duration-200 cursor-pointer"
                  >
                    <span className="text-sm font-medium text-foreground">{api.name}</span>
                    <div className="transition-transform duration-200 hover:scale-110">
                      {getStatusIcon(api.status)}
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4 pt-4 border-t space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Active Sources:</span>
                  <span className="font-medium text-foreground transition-all duration-300">{activeSourcesCount} / 5</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Confidence Level:</span>
                  <span className="font-medium text-foreground transition-all duration-300">{confidenceLevel}%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Last Updated:</span>
                  <span className="font-medium text-foreground">Just now</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column - Charts & Data */}
        <div className="lg:col-span-2 space-y-6">
          {/* Threat Score (moved here from left column) */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Activity className="h-5 w-5 text-primary" />
                Threat Score
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-col items-center justify-center py-6">
                <div className="relative w-40 h-40 flex items-center justify-center">
                  <svg className="w-40 h-40 transform -rotate-90">
                    <circle
                      cx="80"
                      cy="80"
                      r="70"
                      stroke="currentColor"
                      strokeWidth="10"
                      fill="none"
                      className="text-muted"
                    />
                    <circle
                      cx="80"
                      cy="80"
                      r="70"
                      stroke={riskLevel.color}
                      strokeWidth="10"
                      fill="none"
                      strokeDasharray={`${2 * Math.PI * 70}`}
                      strokeDashoffset={`${2 * Math.PI * 70 * (1 - threatScore / 100)}`}
                      className={`transition-all duration-500`}
                      strokeLinecap="round"
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-4xl font-bold text-foreground transition-all duration-300">{threatScore}</span>
                    <span className="text-xs text-muted-foreground">/ 100</span>
                  </div>
                </div>
                {hasAnalyzed && (
                  <Badge style={{ backgroundColor: riskLevel.color, color: "#ffffff" }} className={`mt-4 animate-in fade-in slide-in-from-bottom-2 duration-300`}>
                    {riskLevel.label}
                  </Badge>
                )}
              </div>

              <div className="space-y-2">
                <div className="text-sm font-medium text-foreground">Threat Categories</div>
                <div className="flex flex-wrap gap-2">
                  {threatCategories.map((cat, idx) => (
                    <Badge
                      key={cat.name}
                      variant={cat.active ? "default" : "outline"}
                      className={`transition-all duration-300 animate-in fade-in slide-in-from-left ${
                        cat.active 
                          ? "bg-red-500 hover:bg-red-600 text-white border-red-500 shadow-md shadow-red-500/20" 
                          : "bg-transparent text-muted-foreground border-border/50 opacity-50"
                      }`}
                      style={{ animationDelay: `${idx * 100}ms` }}
                    >
                      {cat.name}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Google Maps Geolocation */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Globe className="h-5 w-5 text-primary" />
                Global IP Geolocation
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="relative w-full rounded-lg overflow-hidden" style={{ height: '420px' }}>
                {hasAnalyzed && geolocation && geolocation.latitude && geolocation.longitude ? (
                  <ThreatMap
                    latitude={geolocation.latitude}
                    longitude={geolocation.longitude}
                    threatScore={threatScore}
                    city={geolocation.city}
                    country={geolocation.country}
                    ipAddress={ipAddress}
                  />
                ) : (
                  /* Empty State */
                  <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-slate-900/40 to-slate-800/40 dark:from-slate-950/60 dark:to-slate-900/60">
                    <div className="text-center space-y-3">
                      <div className="relative">
                        <Globe className="h-20 w-20 text-primary/30 mx-auto" />
                        <div className="absolute inset-0 flex items-center justify-center">
                          <div className="h-16 w-16 border-2 border-primary/20 border-t-primary/40 rounded-full animate-spin"></div>
                        </div>
                      </div>
                      <div className="space-y-1.5">
                        <div className="text-sm font-medium text-foreground/70">
                          {hasAnalyzed ? "Location data not available" : "Ready to Map Threats"}
                        </div>
                        {!hasAnalyzed && (
                          <div className="text-xs text-muted-foreground">
                            Analyze an IP to see its global location on Google Maps
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Dark Web Intelligence */}
          {hasAnalyzed && analysisResult?.darkweb_intelligence && (
            <DarkWebIntelligence data={analysisResult.darkweb_intelligence} />
          )}

          {/* Intelligence Table */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Database className="h-5 w-5 text-primary" />
                Consolidated Intelligence
              </CardTitle>
            </CardHeader>
            <CardContent>
              {intelligenceData.length > 0 ? (
                <div className="rounded-lg border border-border overflow-hidden">
                  <Table>
                    <TableHeader>
                      <TableRow className="bg-muted/50 hover:bg-muted/50">
                        <TableHead className="font-semibold">Source</TableHead>
                        <TableHead className="font-semibold">Category</TableHead>
                        <TableHead className="font-semibold">Evidence</TableHead>
                        <TableHead className="font-semibold text-center">Confidence</TableHead>
                        <TableHead className="font-semibold">Date</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {intelligenceData.map((intel, idx) => {
                        const category = intel.category?.toLowerCase() || '';
                        const getCategoryColor = () => {
                          if (category.includes('malicious')) return 'bg-red-500/15 text-red-600 dark:text-red-400 border-red-500/30';
                          if (category.includes('c2') || category.includes('server')) return 'bg-orange-500/15 text-orange-600 dark:text-orange-400 border-orange-500/30';
                          if (category.includes('botnet')) return 'bg-red-500/15 text-red-600 dark:text-red-400 border-red-500/30';
                          if (category.includes('suspicious')) return 'bg-yellow-500/15 text-yellow-600 dark:text-yellow-400 border-yellow-500/30';
                          if (category.includes('open ports')) return 'bg-blue-500/15 text-blue-600 dark:text-blue-400 border-blue-500/30';
                          if (category.includes('spam')) return 'bg-purple-500/15 text-purple-600 dark:text-purple-400 border-purple-500/30';
                          if (category.includes('fraud')) return 'bg-orange-500/15 text-orange-600 dark:text-orange-400 border-orange-500/30';
                          if (category.includes('malware')) return 'bg-red-500/15 text-red-600 dark:text-red-400 border-red-500/30';
                          if (category.includes('clean')) return 'bg-green-500/15 text-green-600 dark:text-green-400 border-green-500/30';
                          return 'bg-gray-500/15 text-gray-600 dark:text-gray-400 border-gray-500/30';
                        };

                        const confidence = parseInt((intel.confidence ?? "0").toString().replace('%', ''));
                        const getConfidenceColor = () => {
                          if (confidence >= 90) return 'text-red-500';
                          if (confidence >= 75) return 'text-orange-500';
                          if (confidence >= 50) return 'text-yellow-500';
                          return 'text-muted-foreground';
                        };

                        return (
                          <TableRow
                            key={idx}
                            className="animate-in fade-in slide-in-from-bottom duration-300 hover:bg-muted/30 transition-colors border-b border-border/50"
                            style={{ animationDelay: `${idx * 50}ms` }}
                          >
                            {/* Source with external link */}
                            <TableCell className="font-medium">
                              <div className="flex items-center gap-2">
                                <span>{intel.source ?? "-"}</span>
                                <ExternalLink className="h-3 w-3 text-muted-foreground opacity-50 hover:opacity-100 transition-opacity cursor-pointer" />
                              </div>
                            </TableCell>

                            {/* Category Badge */}
                            <TableCell>
                              <Badge 
                                variant="outline" 
                                className={`${getCategoryColor()} font-medium border`}
                              >
                                {intel.category ?? "-"}
                              </Badge>
                            </TableCell>

                            {/* Evidence */}
                            <TableCell className="text-sm text-muted-foreground max-w-md">
                              {intel.evidence ?? "-"}
                            </TableCell>

                            {/* Confidence with progress bar */}
                            <TableCell>
                              <div className="flex flex-col items-center gap-1.5">
                                <span className={`text-sm font-bold ${getConfidenceColor()}`}>
                                  {intel.confidence ?? "-"}
                                </span>
                                {confidence > 0 && (
                                  <Progress 
                                    value={confidence} 
                                    className="w-16 h-1.5" 
                                  />
                                )}
                              </div>
                            </TableCell>

                            {/* Date */}
                            <TableCell className="text-sm text-muted-foreground whitespace-nowrap">
                              {intel.date ?? "-"}
                            </TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </div>
              ) : (
                <div className="h-48 flex items-center justify-center text-muted-foreground">
                  <div className="text-center space-y-2">
                    <Database className="h-12 w-12 mx-auto opacity-30" />
                    <p className="text-sm">No intelligence data yet. Analyze an IP to see results.</p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Index;
