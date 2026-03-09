import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../services/database_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool loading = false;

  Future<void> pickResume() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'docx'],
      withData: true,
    );

    if (result == null) return;
    setState(() => loading = true);

    try {
      final response = await ApiService.analyzeResume(
        result.files.single.bytes!,
        result.files.single.name,
      );

      // ✨ NEW: Automatically save to Firebase History
      await DatabaseService.saveAnalysisResult(response);

      setState(() => loading = false);
      if (!mounted) return;
      Navigator.pushNamed(context, '/analysis', arguments: response);
    } catch (e) {
      setState(() => loading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Error: Check backend and internet connection.")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF020617),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          Center(child: Text(AuthService.email, style: GoogleFonts.poppins(color: Colors.grey, fontSize: 13))),
          const SizedBox(width: 15),
          IconButton(
            icon: const Icon(Icons.logout, color: Colors.redAccent),
            onPressed: () async {
              await AuthService.logout();
              Navigator.pushReplacementNamed(context, '/login');
            },
          ),
          const SizedBox(width: 20),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text("Welcome, ${AuthService.userName}", style: GoogleFonts.poppins(fontSize: 24, color: Colors.white60)),
            const SizedBox(height: 10),
            Text("ResumeAI Analyzer", style: GoogleFonts.poppins(fontSize: 48, fontWeight: FontWeight.bold)),
            const SizedBox(height: 50),
            GestureDetector(
              onTap: loading ? null : pickResume,
              child: Container(
                width: 500, height: 200,
                decoration: BoxDecoration(
                  color: const Color(0xFF0F172A),
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(color: const Color(0xFF6366F1).withOpacity(0.5)),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(loading ? Icons.sync : Icons.cloud_upload, color: const Color(0xFF22D3EE), size: 50),
                    const SizedBox(height: 15),
                    Text(loading ? "AI is processing..." : "Upload Resume to Analyze", style: const TextStyle(fontSize: 18)),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}