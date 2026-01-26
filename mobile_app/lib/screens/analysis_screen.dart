import 'package:flutter/material.dart';
import '../services/auth_service.dart';

class AnalysisScreen extends StatelessWidget {
  const AnalysisScreen({super.key});

  @override
  Widget build(BuildContext context) {
    if (!AuthService.isLoggedIn()) {
      Future.microtask(() =>
          Navigator.pushReplacementNamed(context, '/login'));
      return const SizedBox();
    }

    final data =
        ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Resume Analysis"),
        actions: [
          TextButton.icon(
            onPressed: () {
              AuthService.logout();
              Navigator.pushReplacementNamed(context, '/login');
            },
            icon: const Icon(Icons.logout, color: Colors.white),
            label: const Text("Sign Out",
                style: TextStyle(color: Colors.white)),
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 👤 USER PROFILE CARD
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF0A1226),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                  const CircleAvatar(
                    radius: 28,
                    child: Icon(Icons.person, size: 32),
                  ),
                  const SizedBox(width: 16),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        AuthService.userName,
                        style: const TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                      Text(
                        AuthService.email,
                        style: const TextStyle(color: Colors.white54),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 30),

            // ⚠ Backend Error Message
            if (data.containsKey("error"))
              Text(
                data["error"],
                style: const TextStyle(color: Colors.redAccent),
              ),

            const SizedBox(height: 20),

            Text("Score: ${data['score']}%"),
            const SizedBox(height: 20),

            const Text("Detected Skills"),
            Wrap(
              children: (data['skills'] as List)
                  .map((e) => Chip(label: Text(e)))
                  .toList(),
            ),

            const SizedBox(height: 20),
            const Text("Missing Skills"),
            Wrap(
              children: (data['missing_skills'] as List)
                  .map((e) => Chip(label: Text(e)))
                  .toList(),
            ),

            const SizedBox(height: 20),
            const Text("Top Jobs"),
            ...List.from(data['top_jobs']).map((e) => Text("• $e")),
          ],
        ),
      ),
    );
  }
}
