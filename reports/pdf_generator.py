"""
PDF Report Generator for TICE
Creates professional threat intelligence reports in PDF format
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime


class PDFReportGenerator:
    """Generate professional PDF reports for threat intelligence analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=6,
            spaceBefore=6,
            fontName='Helvetica-Bold'
        ))
        
        # Info style
        self.styles.add(ParagraphStyle(
            name='InfoText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            spaceAfter=6
        ))
        
        # Risk level styles
        for level, color in [
            ('Critical', '#dc3545'),
            ('High', '#fd7e14'),
            ('Medium', '#ffc107'),
            ('Low', '#28a745'),
            ('Benign', '#20c997')
        ]:
            self.styles.add(ParagraphStyle(
                name=f'Risk{level}',
                parent=self.styles['Normal'],
                fontSize=14,
                textColor=colors.HexColor(color),
                fontName='Helvetica-Bold',
                alignment=TA_CENTER
            ))
    
    def _get_risk_color(self, risk_level):
        """Get color based on risk level"""
        colors_map = {
            'critical': colors.HexColor('#dc3545'),
            'high': colors.HexColor('#fd7e14'),
            'medium': colors.HexColor('#ffc107'),
            'low': colors.HexColor('#28a745'),
            'benign': colors.HexColor('#20c997')
        }
        return colors_map.get(risk_level.lower(), colors.grey)
    
    def generate_report(self, profile_data):
        """
        Generate PDF report from threat profile data
        
        Args:
            profile_data: Dictionary containing threat intelligence data
        
        Returns:
            BytesIO object containing the PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=72)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Add title
        elements.append(Paragraph("TICE Threat Intelligence Report", self.styles['CustomTitle']))
        elements.append(Spacer(1, 12))
        
        # Add metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(Paragraph(f"<b>Generated:</b> {timestamp}", self.styles['InfoText']))
        elements.append(Paragraph(f"<b>IP Address:</b> {profile_data.get('ip_address', 'N/A')}", self.styles['InfoText']))
        elements.append(Spacer(1, 20))
        
        # Executive Summary
        elements.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        
        threat_score = profile_data.get('threat_score', 0)
        risk_level = profile_data.get('risk_level', 'Unknown').title()
        is_malicious = profile_data.get('is_malicious', False)
        confidence = profile_data.get('confidence', 0)
        
        # Summary table
        summary_data = [
            ['Metric', 'Value'],
            ['Threat Score', f"{threat_score}/100"],
            ['Risk Level', risk_level],
            ['Classification', 'MALICIOUS' if is_malicious else 'BENIGN'],
            ['Confidence', f"{confidence}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (1, 3), (1, 3), 
             colors.HexColor('#dc3545') if is_malicious else colors.HexColor('#28a745')),
            ('TEXTCOLOR', (1, 3), (1, 3), colors.whitesmoke),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Geolocation Information
        geolocation = profile_data.get('geolocation', {})
        if geolocation:
            elements.append(Paragraph("Geographic Information", self.styles['CustomHeading']))
            
            geo_data = [
                ['Field', 'Value'],
                ['Country', geolocation.get('country', 'Unknown')],
                ['Region', geolocation.get('region', 'Unknown')],
                ['City', geolocation.get('city', 'Unknown')],
                ['ISP', geolocation.get('isp', 'Unknown')],
                ['Organization', geolocation.get('org', 'Unknown')],
            ]
            
            geo_table = Table(geo_data, colWidths=[2*inch, 4*inch])
            geo_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ]))
            
            elements.append(geo_table)
            elements.append(Spacer(1, 20))
        
        # Network Information
        network_info = profile_data.get('network_info', {})
        if network_info:
            elements.append(Paragraph("Network Indicators", self.styles['CustomHeading']))
            
            indicators = []
            if network_info.get('is_vpn'):
                indicators.append('VPN Detected')
            if network_info.get('is_proxy'):
                indicators.append('Proxy Detected')
            if network_info.get('is_tor'):
                indicators.append('Tor Network')
            if network_info.get('is_hosting'):
                indicators.append('Hosting Provider')
            if network_info.get('is_bot'):
                indicators.append('Bot Activity')
            
            if indicators:
                elements.append(Paragraph(
                    f"<b>Detected:</b> {', '.join(indicators)}", 
                    self.styles['InfoText']
                ))
            else:
                elements.append(Paragraph(
                    "<b>Status:</b> No suspicious network indicators detected", 
                    self.styles['InfoText']
                ))
            
            elements.append(Spacer(1, 20))
        
        # Threat Categories
        categories = profile_data.get('categories', [])
        if categories:
            elements.append(Paragraph("Threat Categories", self.styles['CustomHeading']))
            
            cat_data = [['Category', 'Severity']]
            for cat in categories[:10]:  # Limit to top 10
                # Handle both string and dict formats
                if isinstance(cat, dict):
                    cat_name = cat.get('name', 'Unknown')
                    cat_severity = cat.get('severity', 'Unknown').upper()
                else:
                    cat_name = str(cat)
                    cat_severity = 'MEDIUM'
                
                cat_data.append([cat_name, cat_severity])
            
            cat_table = Table(cat_data, colWidths=[4*inch, 2*inch])
            cat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffe6e6')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(cat_table)
            elements.append(Spacer(1, 20))
        
        # Data Sources
        sources = profile_data.get('sources', {})
        source_scores = profile_data.get('source_scores', {})
        
        if sources:
            elements.append(Paragraph("Intelligence Sources", self.styles['CustomHeading']))
            
            source_data = [['Source', 'Status', 'Data Received']]
            
            # Handle both dict and list formats
            if isinstance(sources, dict):
                for source_name, source_info in sources.items():
                    status = '✓ Active' if source_info else '✗ No Data'
                    # Check if we got actual data or just a marker
                    has_data = 'Yes' if (isinstance(source_info, dict) and source_info) else 'No'
                    source_data.append([
                        source_name.upper(),
                        status,
                        has_data
                    ])
            else:
                # List format (legacy)
                for source in sources:
                    source_data.append([
                        source.get('name', 'Unknown').upper(),
                        '✓ Active' if source.get('queried') else '✗ Inactive',
                        'Yes' if source.get('queried') else 'No'
                    ])
            
            source_table = Table(source_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
            source_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d6eaf8')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(source_table)
            elements.append(Spacer(1, 20))
        
        # Open Ports (if available)
        ports = profile_data.get('ports', [])
        if ports:
            elements.append(Paragraph("Open Ports & Services", self.styles['CustomHeading']))
            
            port_data = [['Port', 'Service', 'Product']]
            for port_info in ports[:15]:  # Limit to 15 ports
                # Handle both int (just port number) and dict (port with details)
                if isinstance(port_info, int):
                    port_data.append([
                        str(port_info),
                        'Unknown',
                        'N/A'
                    ])
                elif isinstance(port_info, dict):
                    port_data.append([
                        str(port_info.get('port', 'N/A')),
                        port_info.get('service', 'Unknown'),
                        port_info.get('product', 'N/A')
                    ])
                else:
                    # Handle string or other types
                    port_data.append([
                        str(port_info),
                        'Unknown',
                        'N/A'
                    ])
            
            port_table = Table(port_data, colWidths=[1.5*inch, 2.5*inch, 2*inch])
            port_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ebdef0')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(port_table)
            elements.append(Spacer(1, 20))
        
        # Vulnerabilities (if available)
        vulnerabilities = profile_data.get('vulnerabilities', [])
        if vulnerabilities:
            elements.append(Paragraph("Known Vulnerabilities", self.styles['CustomHeading']))
            
            vuln_data = [['CVE ID', 'Summary']]
            for vuln in vulnerabilities[:10]:  # Limit to 10 vulnerabilities
                cve = vuln if isinstance(vuln, str) else vuln.get('cve', 'Unknown')
                summary = vuln.get('summary', 'No details available')[:80] if isinstance(vuln, dict) else 'CVE detected'
                vuln_data.append([cve, summary])
            
            vuln_table = Table(vuln_data, colWidths=[2*inch, 4*inch])
            vuln_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            elements.append(vuln_table)
            elements.append(Spacer(1, 20))
        
        # ML Prediction (if available)
        ml_prediction = profile_data.get('ml_prediction', {})
        if ml_prediction.get('available'):
            elements.append(Paragraph("Machine Learning Analysis", self.styles['CustomHeading']))
            
            ml_data = [
                ['Metric', 'Value'],
                ['ML Threat Score', f"{ml_prediction.get('predicted_threat_score', 0)}/100"],
                ['ML Classification', 'MALICIOUS' if ml_prediction.get('is_malicious') else 'BENIGN'],
                ['Model Confidence', f"{ml_prediction.get('confidence', 0)}%"],
                ['Agreement with APIs', 'YES' if ml_prediction.get('is_malicious') == is_malicious else 'NO']
            ]
            
            ml_table = Table(ml_data, colWidths=[3*inch, 3*inch])
            ml_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d5f4e6')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ]))
            
            elements.append(ml_table)
            elements.append(Spacer(1, 20))
        
        # MITRE ATT&CK Threat Intelligence (Law Enforcement Context)
        # Support both mock database format and real OTX format
        mitre_intel = profile_data.get('mitre_intelligence', {})
        
        # Check if this is from mock database (has apt_groups instead of threat_actors)
        apt_groups = mitre_intel.get('apt_groups', [])
        threat_actors_list = mitre_intel.get('threat_actors', [])
        
        has_real_threats = (
            len(apt_groups) > 0 or  # Mock database APT groups
            len(threat_actors_list) > 0 or  # OTX threat actors
            mitre_intel.get('is_c2_server', False) or  # Is C2 server
            mitre_intel.get('is_botnet', False) or  # Is botnet
            len(mitre_intel.get('malware_families', [])) > 0 or  # Has malware
            profile_data.get('threat_actor') is not None  # Has threat actor from mock DB
        )
        
        if mitre_intel.get('found') and has_real_threats:
            elements.append(PageBreak())  # New page for threat intelligence
            elements.append(Paragraph("■ MITRE ATT&CK Threat Intelligence", self.styles['CustomHeading']))
            elements.append(Paragraph(
                "<i>Historical attack context for law enforcement investigations</i>",
                ParagraphStyle(
                    name='ThreatIntelSubtitle',
                    parent=self.styles['Normal'],
                    fontSize=9,
                    textColor=colors.grey,
                    spaceAfter=12
                )
            ))
            
            # Confidence level banner - based on APT attribution and evidence
            # Determine confidence based on actual threat evidence
            apt_groups = mitre_intel.get('apt_groups', [])
            threat_actors_list = mitre_intel.get('threat_actors', [])
            total_actors = len(apt_groups) + len(threat_actors_list)
            
            if total_actors > 0 or profile_data.get('threat_actor'):
                # Has APT groups - CRITICAL confidence for mock DB
                if apt_groups or profile_data.get('threat_actor'):
                    confidence_level = 'CRITICAL'  # Mock database = high confidence
                elif total_actors >= 2 or mitre_intel.get('is_c2_server'):
                    confidence_level = 'CRITICAL'
                else:
                    confidence_level = 'HIGH'
            elif mitre_intel.get('is_c2_server') or mitre_intel.get('is_botnet'):
                # C2/Botnet without APT - HIGH confidence
                confidence_level = 'HIGH'
            elif len(mitre_intel.get('malware_families', [])) > 5:
                # Multiple malware families - MEDIUM confidence
                confidence_level = 'MEDIUM'
            else:
                # Fallback to correlator's confidence
                confidence_level = mitre_intel.get('confidence', 'LOW')
            
            confidence_color = {
                'CRITICAL': colors.HexColor('#dc3545'),
                'HIGH': colors.HexColor('#fd7e14'),
                'MEDIUM': colors.HexColor('#ffc107'),
                'LOW': colors.HexColor('#28a745'),
                'NONE': colors.grey
            }.get(confidence_level, colors.grey)
            
            # Professional two-column banner with dark header
            conf_data = [['Intelligence Confidence Level', confidence_level]]
            conf_table = Table(conf_data, colWidths=[3.5*inch, 2.5*inch])
            conf_table.setStyle(TableStyle([
                # Dark header background for label
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.whitesmoke),
                # Colored background for confidence level
                ('BACKGROUND', (1, 0), (1, 0), confidence_color),
                ('TEXTCOLOR', (1, 0), (1, 0), colors.whitesmoke),
                # Styling
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, 0), 12),
                ('FONTSIZE', (1, 0), (1, 0), 16),
                ('PADDING', (0, 0), (-1, -1), 12),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#2c3e50')),
            ]))
            elements.append(conf_table)
            elements.append(Spacer(1, 15))
            
            # Threat Actors (APT Groups)
            # Handle both mock database format (apt_groups) and OTX format (threat_actors)
            apt_groups = mitre_intel.get('apt_groups', [])
            threat_actors_list = mitre_intel.get('threat_actors', [])
            
            # Get threat actor from profile if available (mock database)
            primary_threat_actor = profile_data.get('threat_actor')
            threat_country = mitre_intel.get('country', profile_data.get('geolocation', {}).get('country'))
            
            if apt_groups or threat_actors_list or primary_threat_actor:
                elements.append(Paragraph("▸ Identified Threat Actors", self.styles['CustomSubHeading']))
                
                # Display primary threat actor from mock database
                if primary_threat_actor:
                    actor_header = f"<b>{primary_threat_actor}</b>"
                    if threat_country:
                        actor_header += f" - <font color='red'>ATTRIBUTION: {threat_country}</font>"
                    
                    elements.append(Paragraph(actor_header, self.styles['InfoText']))
                    
                    # Display APT group aliases
                    if apt_groups:
                        aliases = ', '.join(apt_groups)
                        elements.append(Paragraph(f"<i>Also known as: {aliases}</i>", self.styles['InfoText']))
                    
                    # Display campaign information
                    campaign = mitre_intel.get('campaign', profile_data.get('campaign'))
                    if campaign:
                        elements.append(Paragraph(f"<b>Campaign:</b> {campaign}", self.styles['InfoText']))
                    
                    # Display target sectors
                    target_sectors = mitre_intel.get('target_sectors', [])
                    if target_sectors:
                        sectors_text = ', '.join(target_sectors)
                        elements.append(Paragraph(f"<b>Target Sectors:</b> {sectors_text}", self.styles['InfoText']))
                    
                    # Display target regions
                    target_regions = mitre_intel.get('target_regions', [])
                    if target_regions:
                        regions_text = ', '.join(target_regions)
                        elements.append(Paragraph(f"<b>Target Regions:</b> {regions_text}", self.styles['InfoText']))
                    
                    elements.append(Spacer(1, 10))
                
                # Also display OTX threat actors if available
                for actor in threat_actors_list:
                    actor_name = actor.get('name', 'Unknown')
                    mitre_id = actor.get('mitre_id', '')
                    attribution = actor.get('attribution', 'Unknown')
                    aliases = ', '.join(actor.get('aliases', []))
                    description = actor.get('description', 'No description available.')
                    
                    # Actor header
                    actor_header = f"<b>{actor_name}</b> ({mitre_id})"
                    if attribution:
                        actor_header += f" - <font color='red'>ATTRIBUTION: {attribution}</font>"
                    
                    elements.append(Paragraph(actor_header, self.styles['InfoText']))
                    
                    if aliases:
                        elements.append(Paragraph(f"<i>Also known as: {aliases}</i>", self.styles['InfoText']))
                    
                    elements.append(Paragraph(description[:300], self.styles['InfoText']))
                    elements.append(Spacer(1, 10))
            
            # Attack Timeline
            timeline = mitre_intel.get('timeline', {})
            if timeline.get('first_seen') or timeline.get('last_seen'):
                elements.append(Paragraph("▸ Attack Timeline", self.styles['CustomSubHeading']))
                
                timeline_data = [
                    ['Event', 'Date'],
                    ['First Detected', timeline.get('first_seen', 'Unknown')],
                    ['Last Detected', timeline.get('last_seen', 'Unknown')],
                    ['Activity Span', f"{timeline.get('activity_span_days', 0)} days"]
                ]
                
                timeline_table = Table(timeline_data, colWidths=[2*inch, 4*inch])
                timeline_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c0392b')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ]))
                
                elements.append(timeline_table)
                elements.append(Spacer(1, 15))
            
            # Past Campaigns
            campaigns = mitre_intel.get('campaigns', [])
            if campaigns:
                elements.append(Paragraph("▸ Associated Campaigns", self.styles['CustomSubHeading']))
                
                camp_data = [['Campaign Name', 'Date', 'Source']]
                for camp in campaigns[:10]:  # Limit to 10
                    camp_data.append([
                        camp.get('name', 'Unknown'),
                        camp.get('date', 'Unknown')[:10],  # Just date
                        camp.get('source', 'Unknown')
                    ])
                
                camp_table = Table(camp_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
                camp_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e44ad')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ebdef0')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                
                elements.append(camp_table)
                elements.append(Spacer(1, 15))
            
            # Malware Families
            malware = mitre_intel.get('malware_families', [])
            # Also get from profile if available (mock database)
            profile_malware = profile_data.get('malware_families', [])
            all_malware = list(set(malware + profile_malware))  # Combine and deduplicate
            
            if all_malware:
                elements.append(Paragraph("▸ Identified Malware", self.styles['CustomSubHeading']))
                malware_text = ', '.join(all_malware[:15])  # Limit to 15
                elements.append(Paragraph(malware_text, self.styles['InfoText']))
                elements.append(Spacer(1, 15))
            
            # Attack Techniques (MITRE ATT&CK)
            techniques = mitre_intel.get('techniques', [])
            tactics = mitre_intel.get('tactics', [])
            
            if techniques:
                elements.append(Paragraph("▸ Attack Techniques (MITRE ATT&CK)", self.styles['CustomSubHeading']))
                
                # Show tactics first if available
                if tactics:
                    tactics_text = ', '.join(tactics)
                    elements.append(Paragraph(f"<b>Tactics:</b> {tactics_text}", self.styles['InfoText']))
                    elements.append(Spacer(1, 8))
                
                tech_data = [['Technique ID', 'Technique Name', 'Description']]
                for tech in techniques[:10]:  # Limit to 10
                    tech_id = tech.get('id', 'Unknown')
                    tech_name = tech.get('name', 'Unknown')
                    tech_desc = tech.get('description', '')[:100]  # Limit description
                    
                    tech_data.append([
                        tech_id,
                        tech_name,
                        tech_desc
                    ])
                
                tech_table = Table(tech_data, colWidths=[1*inch, 2*inch, 3*inch])
                tech_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2980b9')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d6eaf8')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                
                elements.append(tech_table)
                elements.append(Spacer(1, 15))
            
            # Evidence Summary
            elements.append(Paragraph("📊 Intelligence Sources", self.styles['CustomSubHeading']))
            evidence_data = [
                ['Source', 'Findings'],
                ['AlienVault OTX', f"{mitre_intel.get('otx_pulse_count', 0)} threat pulses"],
                ['ThreatFox IOC', f"{mitre_intel.get('threatfox_ioc_count', 0)} malware indicators"],
                ['MITRE ATT&CK', f"{mitre_intel.get('mitre_group_count', 0)} threat group profiles"],
                ['C2 Server', 'YES' if mitre_intel.get('is_c2_server') else 'NO'],
                ['Botnet', 'YES' if mitre_intel.get('is_botnet') else 'NO'],
            ]
            
            evidence_table = Table(evidence_data, colWidths=[2*inch, 4*inch])
            evidence_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d5f4e6')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ]))
            
            elements.append(evidence_table)
            elements.append(Spacer(1, 20))
        
        # Dark Web Intelligence
        darkweb_intel = profile_data.get('darkweb_intelligence', {})
        if darkweb_intel and darkweb_intel.get('found_in_darkweb'):
            elements.append(PageBreak())  # New page for dark web intelligence
            elements.append(Paragraph("■ Dark Web Intelligence", self.styles['CustomHeading']))
            elements.append(Paragraph(
                "<i>Underground activity detection from public dark web databases</i>",
                ParagraphStyle(
                    name='DarkWebSubtitle',
                    parent=self.styles['Normal'],
                    fontSize=9,
                    textColor=colors.grey,
                    spaceAfter=12
                )
            ))
            
            # Threat Level Banner
            threat_level = darkweb_intel.get('threat_level', 'low').upper()
            threat_color = {
                'CRITICAL': colors.HexColor('#8B0000'),
                'HIGH': colors.HexColor('#dc3545'),
                'MEDIUM': colors.HexColor('#fd7e14'),
                'LOW': colors.HexColor('#ffc107')
            }.get(threat_level, colors.grey)
            
            banner_data = [['DARK WEB ACTIVITY DETECTED', f'{threat_level} RISK']]
            banner_table = Table(banner_data, colWidths=[3.5*inch, 2.5*inch])
            banner_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), threat_color),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, 0), 12),
                ('FONTSIZE', (1, 0), (1, 0), 16),
                ('PADDING', (0, 0), (-1, -1), 12),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ]))
            elements.append(banner_table)
            elements.append(Spacer(1, 15))
            
            # Indicators
            indicators = darkweb_intel.get('indicators', [])
            if indicators:
                elements.append(Paragraph("▸ Detected Indicators", self.styles['CustomSubHeading']))
                for indicator in indicators:
                    elements.append(Paragraph(
                        f"• {indicator}",
                        ParagraphStyle(
                            name='DarkWebIndicator',
                            parent=self.styles['Normal'],
                            fontSize=10,
                            textColor=colors.HexColor('#8B0000'),
                            leftIndent=20,
                            spaceAfter=4
                        )
                    ))
                elements.append(Spacer(1, 10))
            
            # Tor Exit Node
            if darkweb_intel.get('tor_exit_node'):
                elements.append(Paragraph("▸ Tor Network Activity", self.styles['CustomSubHeading']))
                elements.append(Paragraph(
                    "🧅 <b>This IP is a Tor exit node</b>",
                    self.styles['InfoText']
                ))
                elements.append(Paragraph(
                    "Traffic from this IP may originate from anonymous Tor users. "
                    "This could include legitimate privacy-conscious users or malicious actors hiding their identity.",
                    self.styles['InfoText']
                ))
                elements.append(Spacer(1, 10))
            
            # Malware URLs
            malware_urls = darkweb_intel.get('malware_urls', {})
            if malware_urls.get('found'):
                elements.append(Paragraph("▸ Malware Distribution", self.styles['CustomSubHeading']))
                url_count = malware_urls.get('url_count', 0)
                elements.append(Paragraph(
                    f"⚠️ <b>{url_count} malicious URL(s) detected in URLhaus database</b>",
                    ParagraphStyle(
                        name='MalwareWarning',
                        parent=self.styles['Normal'],
                        fontSize=11,
                        textColor=colors.HexColor('#dc3545'),
                        fontName='Helvetica-Bold',
                        spaceAfter=8
                    )
                ))
                
                # Malware URLs table
                urls = malware_urls.get('urls', [])[:5]  # Limit to 5 URLs
                if urls:
                    url_data = [['URL', 'Threat Type', 'Status', 'Date Added']]
                    for url in urls:
                        url_str = url.get('url', 'N/A')[:50] + '...' if len(url.get('url', '')) > 50 else url.get('url', 'N/A')
                        threat = url.get('threat', 'Unknown')
                        status = url.get('status', 'Unknown')
                        date_added = url.get('date_added', 'Unknown')
                        if isinstance(date_added, str) and len(date_added) > 10:
                            date_added = date_added[:10]
                        
                        url_data.append([url_str, threat, status, date_added])
                    
                    url_table = Table(url_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1*inch])
                    url_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 9),
                        ('FONTSIZE', (0, 1), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffe6e6')),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('WORDWRAP', (0, 0), (-1, -1), True),
                    ]))
                    
                    elements.append(url_table)
                    
                    if url_count > 5:
                        elements.append(Spacer(1, 5))
                        elements.append(Paragraph(
                            f"<i>... and {url_count - 5} more malicious URLs</i>",
                            ParagraphStyle(
                                name='MoreURLs',
                                parent=self.styles['Normal'],
                                fontSize=8,
                                textColor=colors.grey,
                                alignment=TA_CENTER
                            )
                        ))
                    elements.append(Spacer(1, 10))
            
            # Breach Activity
            breach_activity = darkweb_intel.get('breach_activity', {})
            if breach_activity.get('found'):
                elements.append(Paragraph("▸ Data Breach Activity", self.styles['CustomSubHeading']))
                breach_count = breach_activity.get('breach_count', 0)
                elements.append(Paragraph(
                    f"💾 <b>{breach_count} data breach(es) associated with this IP</b>",
                    ParagraphStyle(
                        name='BreachWarning',
                        parent=self.styles['Normal'],
                        fontSize=11,
                        textColor=colors.HexColor('#fd7e14'),
                        fontName='Helvetica-Bold',
                        spaceAfter=8
                    )
                ))
                elements.append(Spacer(1, 10))
            
            # Data Sources
            elements.append(Paragraph("📊 Data Sources", self.styles['CustomSubHeading']))
            source_data = [
                ['Source', 'Description'],
                ['Tor Project', 'Official Tor exit node list'],
                ['URLhaus (abuse.ch)', 'Malware URL repository'],
                ['Public Threat Intel', 'Aggregated dark web intelligence'],
            ]
            
            source_table = Table(source_data, colWidths=[2*inch, 4*inch])
            source_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6c3483')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ebdef0')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ]))
            
            elements.append(source_table)
            elements.append(Spacer(1, 20))
        
        # Footer
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            "─" * 80,
            self.styles['Normal']
        ))
        elements.append(Paragraph(
            "<i>This report was automatically generated by TICE (Threat Intelligence Correlation Engine)</i>",
            ParagraphStyle(
                name='Footer',
                parent=self.styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        ))
        elements.append(Paragraph(
            f"<i>Report ID: {profile_data.get('ip_address', 'unknown').replace('.', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}</i>",
            ParagraphStyle(
                name='Footer2',
                parent=self.styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        ))
        
        # Build PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        return pdf
