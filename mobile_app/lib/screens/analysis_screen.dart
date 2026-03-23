import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/auth_service.dart';

class AnalysisScreen extends StatelessWidget {
  const AnalysisScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // 🛡️ Web-safe Data Casting
    final dynamic rawArgs = ModalRoute.of(context)!.settings.arguments;
    final Map<String, dynamic> data = (rawArgs is Map) ? Map<String, dynamic>.from(rawArgs) : {};

    // --- DYNAMIC DATA EXTRACTION ---
    final scores = Map<String, dynamic>.from(data['scores'] ?? {});
    final roles = List.from(data['top_3_roles'] ?? []);
    final resumeSkills = List.from(data['resume_skills'] ?? []);
    
    // This now pulls dynamically from the flattened backend key
    final missingSkills = List.from(data['missing_skills'] ?? []);
    
    final recommendations = List.from(data['recommendations'] ?? []);

    return Scaffold(
      backgroundColor: const Color(0xFF020617), // Premium Dark Slate
      appBar: _buildAppBar(context),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 30),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. Dynamic Gauges
            _buildScoreGrid(scores),
            const SizedBox(height: 50),

            // 2. Job Role Cards
            Text("Predicted Job Roles", style: GoogleFonts.poppins(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 20),
            _buildRoleCards(roles),
            const SizedBox(height: 50),

            // 3. Responsive Skills Analysis
            Text("Skills Gap Analysis", style: GoogleFonts.poppins(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 20),
            _buildSkillsLayout(missingSkills, resumeSkills), // Now using dynamic lists
            const SizedBox(height: 50),

            // 4. Actionable Roadmap
            Text("Improvement Recommendations", style: GoogleFonts.poppins(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 20),
            _buildRecommendationGrid(recommendations),
          ],
        ),
      ),
    );
  }

  // --- Header, Gauges, and UI Methods (Remaining Identical) ---
  PreferredSizeWidget _buildAppBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      title: Text("Resume Analysis Results", style: GoogleFonts.poppins(fontWeight: FontWeight.w600)),
      actions: [
        Center(child: Text(AuthService.email, style: const TextStyle(color: Colors.white54, fontSize: 13))),
        const SizedBox(width: 15),
        IconButton(
          icon: const Icon(Icons.logout_rounded, color: Color(0xFFF87171)),
          onPressed: () {
            AuthService.logout();
            Navigator.pushReplacementNamed(context, '/login');
          },
        ),
        const SizedBox(width: 20),
      ],
    );
  }

  Widget _buildScoreGrid(Map scores) {
    return Wrap(
      spacing: 40, runSpacing: 30,
      alignment: WrapAlignment.center,
      children: [
        _gauge(scores['overall'] ?? 0, "Overall Score", 160, const Color(0xFF22D3EE)),
        _gauge(scores['skills'] ?? 0, "Skills Match", 110, const Color(0xFF818CF8)),
        _gauge(scores['education'] ?? 0, "Education", 110, const Color(0xFF34D399)),
        _gauge(scores['formatting'] ?? 0, "Formatting", 110, const Color(0xFFFBBF24)),
      ],
    );
  }

  Widget _gauge(int val, String label, double size, Color color) {
    return Column(
      children: [
        Stack(alignment: Alignment.center, children: [
          SizedBox(height: size, width: size, child: CircularProgressIndicator(value: val / 100, color: color, strokeWidth: 10, backgroundColor: Colors.white10)),
          Text("$val%", style: GoogleFonts.poppins(fontSize: size * 0.22, fontWeight: FontWeight.bold, color: Colors.white)),
        ]),
        const SizedBox(height: 12),
        Text(label, style: const TextStyle(color: Colors.white70, fontSize: 14)),
      ],
    );
  }

  Widget _buildRoleCards(List roles) {
    return Wrap(
      spacing: 20, runSpacing: 20,
      children: roles.map((r) => Container(
        width: 320, padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(color: const Color(0xFF1E293B), borderRadius: BorderRadius.circular(16), border: Border.all(color: Colors.white10)),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
            Expanded(child: Text(r['role'].toString().toUpperCase(), style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white))),
            _demandBadge(r['confidence']),
          ]),
          const SizedBox(height: 15),
          LinearProgressIndicator(value: (r['confidence'] as num) / 100, color: const Color(0xFF6366F1), backgroundColor: Colors.white10, minHeight: 6),
          const SizedBox(height: 10),
          Text("${r['confidence']}% Match Confidence", style: const TextStyle(color: Colors.white54, fontSize: 12)),
        ]),
      )).toList(),
    );
  }

  Widget _demandBadge(dynamic confidence) {
    bool isHigh = (confidence as num) > 30;
    Color c = isHigh ? const Color(0xFF34D399) : const Color(0xFFFBBF24);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(color: c.withOpacity(0.1), borderRadius: BorderRadius.circular(6)),
      child: Text(isHigh ? "High Demand" : "Medium Demand", style: TextStyle(color: c, fontSize: 10, fontWeight: FontWeight.bold)),
    );
  }

  Widget _buildSkillsLayout(List missingSkills, List resumeSkills) {
    return LayoutBuilder(builder: (context, constraints) {
      return Wrap(
        spacing: 20, runSpacing: 20,
        children: [
          _skillBox("Detected Skills", resumeSkills, const Color(0xFF34D399), constraints.maxWidth > 800 ? 0.45 : 1),
          _skillBox("Missing Skills", missingSkills, const Color(0xFFF87171), constraints.maxWidth > 800 ? 0.45 : 1),
        ],
      );
    });
  }

  Widget _skillBox(String title, List skills, Color color, double widthFactor) {
    return Builder(builder: (context) {
      return Container(
        width: MediaQuery.of(context).size.width * widthFactor,
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(color: const Color(0xFF0F172A), borderRadius: BorderRadius.circular(20)),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(title, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 18)),
          const SizedBox(height: 20),
          Wrap(spacing: 8, runSpacing: 8, children: skills.map((s) => Chip(
            label: Text(s.toString(), style: const TextStyle(color: Colors.white, fontSize: 12)),
            backgroundColor: color.withOpacity(0.1),
            side: BorderSide(color: color.withOpacity(0.2)),
          )).toList()),
        ]),
      );
    });
  }

  Widget _buildRecommendationGrid(List recs) {
    return Wrap(
      spacing: 20, runSpacing: 20,
      children: recs.map((r) {
        Color sevColor = _getSevColor(r['severity']);
        return Container(
          width: 380, padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(color: const Color(0xFF1E293B), borderRadius: BorderRadius.circular(20), border: Border.all(color: sevColor.withOpacity(0.2))),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
              Expanded(child: Text(r['title'], style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.white))),
              _severityTag(r['severity'], sevColor),
            ]),
            const SizedBox(height: 12),
            Text(r['reason'], style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.5)),
          ]),
        );
      }).toList(),
    );
  }

  Widget _severityTag(String sev, Color c) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(color: c.withOpacity(0.1), borderRadius: BorderRadius.circular(8), border: Border.all(color: c)),
      child: Text(sev.toUpperCase(), style: TextStyle(color: c, fontSize: 10, fontWeight: FontWeight.bold)),
    );
  }

  Color _getSevColor(String? s) {
    if (s?.toLowerCase() == 'high') return const Color(0xFFF87171);
    if (s?.toLowerCase() == 'medium') return const Color(0xFFFBBF24);
    return const Color(0xFF60A5FA);
  }
}