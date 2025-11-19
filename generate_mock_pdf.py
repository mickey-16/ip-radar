"""
Generate PDF Report for Mock Threat IP
Test end-to-end PDF generation with MITRE intelligence
"""

from config import config
from core.correlator import ThreatCorrelator
from reports.pdf_generator import PDFReportGenerator

def generate_mock_pdf(ip_address):
    """Generate PDF report for a mock threat IP"""
    
    print(f"Generating PDF report for {ip_address}...")
    print("=" * 80)
    
    # Analyze IP
    correlator = ThreatCorrelator(config)
    profile = correlator.analyze_ip(ip_address, use_cache=False)
    
    # Display summary
    print(f"\n✅ Analysis Complete:")
    print(f"   Threat Actor: {profile.threat_actor}")
    print(f"   Threat Score: {profile.threat_score}/100")
    print(f"   Risk Level: {profile.risk_level.upper()}")
    
    # Generate PDF
    print(f"\n📄 Generating PDF...")
    generator = PDFReportGenerator()
    pdf_data = generator.generate_report(profile.to_dict())
    
    # Save PDF
    filename = f"mock_threat_report_{ip_address.replace('.', '_')}.pdf"
    with open(filename, 'wb') as f:
        f.write(pdf_data)
    
    print(f"✅ PDF Generated: {filename}")
    print(f"   File Size: {len(pdf_data) / 1024:.2f} KB")
    print("\n" + "=" * 80)
    print("PDF GENERATION COMPLETE!")
    print("=" * 80)
    print(f"\nOpen the file: {filename}")
    print("\nExpected contents:")
    print("  ✅ Threat Actor identification")
    print("  ✅ MITRE ATT&CK tactics and techniques")
    print("  ✅ Campaign information")
    print("  ✅ Malware families")
    print("  ✅ Target sectors and regions")
    print("  ✅ CRITICAL confidence level")
    

if __name__ == "__main__":
    # Test with APT41 (China)
    generate_mock_pdf("1.222.92.35")
