import 'package:flutter/material.dart';

class RecommendationCard extends StatelessWidget {
  final String title;
  final String level;

  const RecommendationCard(
      {super.key, required this.title, required this.level});

  @override
  Widget build(BuildContext context) {
    Color color =
        level == "High" ? Colors.red : level == "Medium" ? Colors.orange : Colors.green;

    return Card(
      child: ListTile(
        leading: Icon(Icons.trending_up, color: color),
        title: Text(title),
        trailing: Chip(label: Text(level)),
      ),
    );
  }
}
