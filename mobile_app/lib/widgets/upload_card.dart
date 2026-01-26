import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../services/api_service.dart';

class UploadCard extends StatefulWidget {
  const UploadCard({super.key});

  @override
  State<UploadCard> createState() => _UploadCardState();
}

class _UploadCardState extends State<UploadCard> {
  bool loading = false;

  Future<void> pickResume(BuildContext context) async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'docx', 'jpg', 'jpeg', 'png'],
      withData: true, // required for Flutter Web
    );

    if (result == null || result.files.single.bytes == null) return;

    setState(() => loading = true);

    try {
      final response = await ApiService.analyzeResume(
        result.files.single.bytes!,
        result.files.single.name,
      );

      if (!mounted) return;
      setState(() => loading = false);

      Navigator.pushNamed(context, '/analysis', arguments: response);
    } catch (e) {
      setState(() => loading = false);

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Failed to analyze resume")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: loading ? null : () => pickResume(context),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(40),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(24),
          gradient: const LinearGradient(
            colors: [Color(0xFF6366F1), Color(0xFF22D3EE)],
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.blueAccent.withOpacity(0.3),
              blurRadius: 40,
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.upload_file, size: 64, color: Colors.white),
            const SizedBox(height: 20),
            Text(
              loading ? "Analyzing Resume..." : "Upload Resume",
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              "PDF, DOCX, JPG, PNG supported",
              style: TextStyle(color: Colors.white70),
            ),
          ],
        ),
      ),
    );
  }
}
