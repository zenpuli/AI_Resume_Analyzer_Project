import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/auth_service.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});
  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  void _showAlert(String msg, Color color) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(msg, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        backgroundColor: color,
        behavior: SnackBarBehavior.floating,
        margin: const EdgeInsets.all(20),
        duration: const Duration(seconds: 3),
      ),
    );
  }

  Future<void> _handleLogin() async {
    final email = _emailController.text.trim();
    final pass = _passwordController.text.trim();

    if (email.isEmpty || pass.isEmpty) {
      _showAlert("Please enter all fields", Colors.redAccent);
      return;
    }

    setState(() => _isLoading = true);
    // ⚡ Speed Optimized Call
    String? result = await AuthService.login(email, pass);
    
    if (!mounted) return;
    setState(() => _isLoading = false);

    switch (result) {
      case "success":
        Navigator.pushReplacementNamed(context, '/home');
        break;
      case "invalid_format":
        _showAlert("Invalid format. Use @gmail.com", Colors.redAccent);
        break;
      case "no_user":
        _showAlert("User not found pls sign up", Colors.redAccent);
        break;
      case "wrong_password":
        _showAlert("Incorrect password. Try again.", Colors.redAccent);
        break;
      case "low_signal":
        _showAlert("Try again after some time your signal strength may be low", Colors.redAccent);
        break;
      default:
        _showAlert("Something went wrong. Try again.", Colors.redAccent);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF020617),
      body: Center(
        child: Container(
          width: 400, padding: const EdgeInsets.all(32),
          decoration: BoxDecoration(color: const Color(0xFF0F172A), borderRadius: BorderRadius.circular(24)),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.description, color: Color(0xFF22D3EE), size: 48),
              const SizedBox(height: 16),
              Text("ResumeAI", style: GoogleFonts.poppins(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white)),
              Text("Welcome Back", style: GoogleFonts.poppins(fontSize: 20, color: Colors.white70)),
              const SizedBox(height: 32),
              TextField(controller: _emailController, decoration: const InputDecoration(labelText: "Email", prefixIcon: Icon(Icons.email))),
              const SizedBox(height: 16),
              TextField(controller: _passwordController, obscureText: true, decoration: const InputDecoration(labelText: "Password", prefixIcon: Icon(Icons.lock))),
              const SizedBox(height: 32),
              SizedBox(
                width: double.infinity, height: 50,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _handleLogin,
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF6366F1), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                  child: _isLoading 
                    ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)) 
                    : const Text("Sign In"),
                ),
              ),
              const SizedBox(height: 16),
              TextButton(onPressed: () => Navigator.pushNamed(context, '/signup'), child: const Text("Don't have an account? Sign up", style: TextStyle(color: Color(0xFF22D3EE)))),
            ],
          ),
        ),
      ),
    );
  }
}