import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../services/database_service.dart';

// 🛡️ Fixed: Added the missing StatefulWidget class
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

      // ⚡ SPEED BOOST: Navigation First
      setState(() => loading = false);
      if (!mounted) return;

      if (response.containsKey('error')) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(response['error'], style: const TextStyle(color: Colors.white)),
            backgroundColor: Colors.redAccent,
            behavior: SnackBarBehavior.floating,
          ),
        );
        return;
      }

      // 1. Move to results immediately
      Navigator.pushNamed(context, '/analysis', arguments: response);

      // 2. Archive to Firebase in the background (Non-blocking)
      DatabaseService.saveAnalysisResult(response);

    } catch (e) {
      setState(() => loading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Analysis failed. Please check signal strength.")),
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
            Text("ResumeAI Analyzer", style: GoogleFonts.poppins(fontSize: 48, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 50),
            GestureDetector(
              onTap: loading ? null : pickResume,
              child: Container(
                width: 500, height: 220,
                decoration: BoxDecoration(
                  color: const Color(0xFF0F172A),
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(color: const Color(0xFF6366F1).withOpacity(0.5), width: 2),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(loading ? Icons.sync : Icons.cloud_upload_outlined, color: const Color(0xFF22D3EE), size: 60),
                    const SizedBox(height: 20),
                    Text(
                      loading ? "AI is processing..." : "Upload Resume to Analyze", 
                      style: GoogleFonts.poppins(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w500)
                    ),
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