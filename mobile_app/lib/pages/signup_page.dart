import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import '../widgets/input_field.dart';

class SignupPage extends StatefulWidget {
  const SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {
  final nameController = TextEditingController();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  bool isLoading = false;

  void register() async {
    setState(() => isLoading = true);

    final success = await AuthService.register(
      nameController.text,
      emailController.text,
      passwordController.text,
    );

    setState(() => isLoading = false);

    if (success) {
      Navigator.pushReplacementNamed(context, '/login');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF050B18),
      body: Center(
        child: Container(
          width: 420,
          padding: const EdgeInsets.all(32),
          decoration: BoxDecoration(
            color: const Color(0xFF0A1226),
            borderRadius: BorderRadius.circular(24),
            boxShadow: const [
              BoxShadow(color: Colors.black54, blurRadius: 40),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.description, size: 48, color: Colors.cyan),
              const SizedBox(height: 10),
              const Text("ResumeAI",
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              const SizedBox(height: 20),

              const Text("Create Account",
                  style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
              const SizedBox(height: 6),
              const Text("Sign up to analyze your resume",
                  style: TextStyle(color: Colors.white54)),
              const SizedBox(height: 30),

              InputField(
                  hint: "Full Name",
                  icon: Icons.person,
                  controller: nameController),
              const SizedBox(height: 16),

              InputField(
                  hint: "Email",
                  icon: Icons.email,
                  controller: emailController),
              const SizedBox(height: 16),

              InputField(
                  hint: "Password",
                  icon: Icons.lock,
                  isPassword: true,
                  controller: passwordController),
              const SizedBox(height: 24),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: register,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(14)),
                    backgroundColor: const Color(0xFF6366F1),
                  ),
                  child: isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text("Create Account"),
                ),
              ),

              const SizedBox(height: 14),
              GestureDetector(
                onTap: () => Navigator.pop(context),
                child: const Text(
                  "Already have an account? Sign in",
                  style: TextStyle(color: Color(0xFF22D3EE)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
