import 'package:flutter/material.dart';

class JobCard extends StatelessWidget {
  final String title;
  final int match;

  const JobCard({super.key, required this.title, required this.match});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 260,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.cyan),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontSize: 18)),
          const SizedBox(height: 10),
          Text("$match% Match", style: const TextStyle(color: Colors.green)),
          const SizedBox(height: 10),
          LinearProgressIndicator(value: match / 100),
        ],
      ),
    );
  }
}
