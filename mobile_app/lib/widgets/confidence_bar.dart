import 'package:flutter/material.dart';

class ConfidenceBar extends StatelessWidget {
  final int value;
  final String label;
  final bool large;

  const ConfidenceBar({
    super.key,
    required this.value,
    required this.label,
    this.large = false,
  });

  @override
  Widget build(BuildContext context) {
    final size = large ? 140.0 : 100.0;
    final fontSize = large ? 28.0 : 20.0;

    return Column(
      children: [
        SizedBox(
          width: size,
          height: size,
          child: Stack(
            alignment: Alignment.center,
            children: [
              CircularProgressIndicator(
                value: value / 100,
                strokeWidth: 10,
                backgroundColor: Colors.white12,
                valueColor: const AlwaysStoppedAnimation(Colors.cyan),
              ),
              Text(
                "$value%",
                style: TextStyle(
                  fontSize: fontSize,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 10),
        Text(
          label,
          style: const TextStyle(color: Colors.grey),
        ),
      ],
    );
  }
}
