import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool loading = false;
  String? fileName;

  Future<void> pickResume() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'docx', 'jpg', 'jpeg', 'png'],
      withData: true,
    );

    if (result == null) return;

    setState(() {
      loading = true;
      fileName = result.files.single.name;
    });

    final response = await ApiService.analyzeResume(
      result.files.single.bytes!,
      result.files.single.name,
    );

    setState(() => loading = false);

    Navigator.pushNamed(context, '/analysis', arguments: response);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF050B18),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text("Unlock Your Career Potential",
                style: TextStyle(fontSize: 36, fontWeight: FontWeight.bold)),

            const SizedBox(height: 40),

            GestureDetector(
              onTap: loading ? null : pickResume,
              child: Container(
                width: 600,
                height: 180,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(24),
                  gradient: const LinearGradient(
                    colors: [Color(0xFF6366F1), Color(0xFF22D3EE)],
                  ),
                ),
                child: Center(
                  child: Text(
                    loading
                        ? "Analyzing Resume..."
                        : (fileName ?? "Click to Upload Resume"),
                    style: const TextStyle(fontSize: 20),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
