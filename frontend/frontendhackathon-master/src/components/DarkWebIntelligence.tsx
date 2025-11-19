import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Shield, Activity, AlertTriangle, ExternalLink } from "lucide-react";

interface DarkWebIntelProps {
  data: {
    found_in_darkweb: boolean;
    tor_exit_node: boolean;
    breach_activity: {
      found: boolean;
      breach_count: number;
      breaches: any[];
    };
    malware_urls: {
      found: boolean;
      url_count: number;
      urls: any[];
    };
    threat_level: string;
    indicators: string[];
  } | undefined;
}

export function DarkWebIntelligence({ data }: DarkWebIntelProps) {
  if (!data) {
    return null;
  }

  const getThreatLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'critical': return 'destructive';
      case 'high': return 'destructive';
      case 'medium': return 'default';
      case 'low': return 'secondary';
      default: return 'outline';
    }
  };

  const getThreatLevelIcon = (level: string) => {
    switch (level.toLowerCase()) {
      case 'critical':
      case 'high':
        return <AlertTriangle className="h-5 w-5 text-red-500" />;
      case 'medium':
        return <Activity className="h-5 w-5 text-orange-500" />;
      default:
        return <Shield className="h-5 w-5 text-green-500" />;
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl">
          🕵️ Dark Web Intelligence
          <Badge variant={data.found_in_darkweb ? "destructive" : "outline"} className="ml-2">
            {data.found_in_darkweb ? "ACTIVITY DETECTED" : "NO ACTIVITY"}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {!data.found_in_darkweb ? (
          <Alert className="border-green-500/50 bg-green-50 dark:bg-green-950/20">
            <Shield className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-700 dark:text-green-400">
              ✅ No dark web activity detected for this IP address. 
              This is a good sign indicating the IP is not associated with underground marketplaces, 
              Tor exit nodes, or malware distribution.
            </AlertDescription>
          </Alert>
        ) : (
          <>
            {/* Threat Level */}
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-red-50 to-orange-50 dark:from-red-950/20 dark:to-orange-950/20 rounded-lg border border-red-200 dark:border-red-800">
              <div className="flex items-center gap-3">
                {getThreatLevelIcon(data.threat_level)}
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Dark Web Threat Level</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white capitalize">
                    {data.threat_level}
                  </p>
                </div>
              </div>
              <Badge variant={getThreatLevelColor(data.threat_level)} className="text-lg px-4 py-2">
                {data.indicators.length} Indicators
              </Badge>
            </div>

            {/* Indicators */}
            {data.indicators.length > 0 && (
              <div className="space-y-2">
                <h3 className="font-semibold text-lg flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-orange-500" />
                  Detected Indicators
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {data.indicators.map((indicator, idx) => (
                    <div key={idx} className="flex items-center gap-2 p-3 bg-orange-50 dark:bg-orange-950/20 rounded border border-orange-200 dark:border-orange-800">
                      <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{indicator}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Tor Exit Node */}
            {data.tor_exit_node && (
              <Alert className="border-purple-500/50 bg-purple-50 dark:bg-purple-950/20">
                <Activity className="h-4 w-4 text-purple-600" />
                <AlertDescription>
                  <div>
                    <p className="font-semibold text-purple-900 dark:text-purple-200 mb-1">
                      🧅 Tor Exit Node Detected
                    </p>
                    <p className="text-purple-700 dark:text-purple-300 text-sm">
                      This IP is listed as a Tor network exit node. Traffic from this IP may originate from 
                      users seeking anonymity, which could include legitimate privacy-conscious users or 
                      malicious actors hiding their identity.
                    </p>
                  </div>
                </AlertDescription>
              </Alert>
            )}

            {/* Malware URLs */}
            {data.malware_urls.found && (
              <div className="space-y-3">
                <h3 className="font-semibold text-lg flex items-center gap-2 text-red-600 dark:text-red-400">
                  <AlertTriangle className="h-5 w-5" />
                  Malware Distribution ({data.malware_urls.url_count} URLs)
                </h3>
                <Alert className="border-red-500/50 bg-red-50 dark:bg-red-950/20">
                  <AlertDescription className="text-red-700 dark:text-red-300">
                    ⚠️ This IP has been identified hosting malware URLs in the URLhaus database. 
                    This is a critical indicator of malicious infrastructure.
                  </AlertDescription>
                </Alert>
                
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {data.malware_urls.urls.slice(0, 5).map((url, idx) => (
                    <div key={idx} className="p-3 bg-white dark:bg-gray-900 border border-red-200 dark:border-red-800 rounded-lg">
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1 min-w-0">
                          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">URL</p>
                          <p className="text-sm font-mono break-all text-gray-900 dark:text-gray-100 mb-2">
                            {url.url}
                          </p>
                          <div className="flex flex-wrap gap-2">
                            <Badge variant="destructive" className="text-xs">
                              {url.threat || 'Unknown Threat'}
                            </Badge>
                            <Badge variant="outline" className="text-xs">
                              {url.status || 'Unknown'}
                            </Badge>
                            {url.date_added && (
                              <Badge variant="secondary" className="text-xs">
                                Added: {new Date(url.date_added).toLocaleDateString()}
                              </Badge>
                            )}
                          </div>
                          {url.tags && url.tags.length > 0 && (
                            <div className="flex flex-wrap gap-1 mt-2">
                              {url.tags.map((tag: string, tagIdx: number) => (
                                <span key={tagIdx} className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded">
                                  {tag}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                        <ExternalLink className="h-4 w-4 text-gray-400 flex-shrink-0" />
                      </div>
                    </div>
                  ))}
                </div>
                
                {data.malware_urls.url_count > 5 && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
                    ... and {data.malware_urls.url_count - 5} more malicious URLs
                  </p>
                )}
              </div>
            )}

            {/* Breach Activity */}
            {data.breach_activity.found && (
              <Alert className="border-orange-500/50 bg-orange-50 dark:bg-orange-950/20">
                <AlertTriangle className="h-4 w-4 text-orange-600" />
                <AlertDescription>
                  <div>
                    <p className="font-semibold text-orange-900 dark:text-orange-200 mb-1">
                      💾 Data Breach Activity ({data.breach_activity.breach_count} breaches)
                    </p>
                    <p className="text-orange-700 dark:text-orange-300 text-sm">
                      This IP has been associated with data breach activity.
                    </p>
                  </div>
                </AlertDescription>
              </Alert>
            )}

            {/* Source Attribution */}
            <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
              <p className="text-xs text-gray-500 dark:text-gray-400">
                <strong>Data Sources:</strong> Tor Project Exit Node List, URLhaus (abuse.ch), Public Threat Intelligence
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                <strong>Real-time Data:</strong> All checks performed against live public databases
              </p>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
